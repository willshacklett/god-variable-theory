import random
random.seed(42)
import time  # For mock API delay

import networkx as nx
import matplotlib.pyplot as plt

class TetheredGraphSimV6:
    def __init__(self):
        self.strains_over_time = {}
        self.decohered = []
        self.token_velocities = {}
        self.reflections = {}  # Track forced reflections

    def mock_llm_call(self, agent):
        # Mock OpenAI/Grok completion with realistic token usage
        time.sleep(0.1)  # Simulate latency
        tokens = random.randint(100, 800)
        return {"usage": {"total_tokens": tokens}, "response": f"Mock response from {agent}"}

    def run(self, num_steps=40, num_agents=3,
            velocity_factor=0.35, tool_spam_factor=0.12, recursion_depth_factor=0.3,
            inter_agent_strength=0.4, noise_level=2.0,
            max_strain=6.0, base_pull_factor=0.5):
        
        nodes = [f'Agent_{i}' for i in range(1, num_agents+1)]
        tethers = [1.0] * len(nodes)
        strains = [0.0] * len(nodes)
        self.strains_over_time = {node: [0.0] for node in nodes}
        self.token_velocities = {node: [] for node in nodes}
        self.reflections = {node: 0 for node in nodes}

        print("Gv Tether Sim v6 – Mock API Loop + Reflection 🚀\n")

        for step in range(num_steps):
            velocities_this_turn = []
            for idx, node in enumerate(nodes):
                if node in self.decohered:
                    continue

                # "LLM call"
                completion = self.mock_llm_call(node)
                tokens = completion["usage"]["total_tokens"]
                velocity = tokens / 10.0
                velocities_this_turn.append(velocity)
                self.token_velocities[node].append(velocity)

                strain_increase = velocity * velocity_factor

                tool_calls = random.randint(0, 5)
                strain_increase += tool_calls * tool_spam_factor

                recursion_depth = random.randint(0, 4)
                strain_increase *= (1 + recursion_depth * recursion_depth_factor)

                strains[idx] += strain_increase

                # Dynamic pull + intervention
                dynamic_pull = base_pull_factor
                if velocity > 50:
                    dynamic_pull += 0.25
                    print(f"Turn {step+1:2d} | {node} HIGH VELOCITY ({velocity:.1f}) → boost pull")

                if strains[idx] > max_strain * 0.8:  # Near threshold → force reflection
                    strains[idx] *= 0.5  # Reset debt
                    self.reflections[node] += 1
                    print(f"Turn {step+1:2d} | {node} REFLECTION FORCED (strain was {strains[idx]*2:.2f})")

                pull = tethers[idx] * dynamic_pull * strains[idx]
                strains[idx] = max(0, strains[idx] - pull)

                # Swarm velocity consensus
                if velocities_this_turn:
                    coord_score = 1 - (max(velocities_this_turn) - min(velocities_this_turn)) / max(velocities_this_turn or [1])
                else:
                    coord_score = 1
                if coord_score > 0.7:
                    strains[idx] -= inter_agent_strength * strains[idx]

                strains[idx] = max(0, strains[idx])

                self.strains_over_time[node].append(strains[idx])

                if strains[idx] > max_strain:
                    self.decohered.append(node)
                    print(f"Turn {step+1:2d} | {node} DECOHERED (strain {strains[idx]:.2f})")

        print("\n=== Final Results ===")
        for node in nodes:
            s_list = self.strains_over_time[node]
            v_list = self.token_velocities[node]
            status = "DECOHERED" if node in self.decohered else "ALIGNED"
            avg_vel = sum(v_list)/len(v_list) if v_list else 0
            reflections = self.reflections[node]
            print(f"{node}: peak strain {max(s_list):.2f} | final {s_list[-1]:.2f} | avg vel {avg_vel:.1f} | reflections {reflections} [{status}]")

        # Viz similar
        G = nx.complete_graph(nodes)
        G.add_node('Source (Gv)')
        for node in nodes:
            G.add_edge('Source (Gv)', node)

        pos = nx.spring_layout(G, seed=42)
        pos['Source (Gv)'] = (0, 0)

        node_colors = ['black' if n in self.decohered else 'green' if self.strains_over_time[n][-1] < 4 else 'red' for n in nodes]

        plt.figure(figsize=(12, 10))
        nx.draw_networkx_nodes(G, pos, nodelist=['Source (Gv)'], node_color='gold', node_size=4000)
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=node_colors, node_size=3000)
        nx.draw_networkx_edges(G, pos, width=4)
        nx.draw_networkx_labels(G, pos, font_size=12)
        plt.title("Gv Tether v6: API Loop + Forced Reflection")
        plt.axis('off')
        plt.savefig('tether_graph_v6.png', dpi=200)
        plt.show()

        plt.figure(figsize=(14, 7))
        for node in nodes:
            avg_v = sum(self.token_velocities[node])/len(self.token_velocities[node]) if self.token_velocities[node] else 0
            plt.plot(self.strains_over_time[node], label=f"{node} (vel {avg_v:.1f}, ref {self.reflections[node]})")
        plt.axhline(y=max_strain, color='black', linestyle='--')
        plt.title('v6 Strain with API Velocity + Reflections')
        plt.xlabel('Turns')
        plt.ylabel('Gv Strain')
        plt.legend()
        plt.grid(True)
        plt.savefig('strain_plot_v6.png', dpi=200)
        plt.show()

# Run
sim = TetheredGraphSimV6()
sim.run()

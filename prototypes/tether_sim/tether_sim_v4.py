import random
random.seed(42)

import networkx as nx
import matplotlib.pyplot as plt

class TetheredGraphSimV4:
    def __init__(self):
        self.strains_over_time = {}
        self.decohered = []
        self.token_velocities = {}  # New: track per agent

    def run(self, num_steps=50, num_agents=3,  # Shorter for LLM "turns"
            velocity_factor=0.25, tool_spam_factor=0.1, recursion_depth_factor=0.25,
            inter_agent_strength=0.3, noise_level=1.5,
            max_strain=6.0, base_pull_factor=0.4):
        
        nodes = [f'Agent_{i}' for i in range(1, num_agents+1)]
        tethers = [1.0] * len(nodes)
        strains = [0.0] * len(nodes)
        self.strains_over_time = {node: [0.0] for node in nodes}
        self.token_velocities = {node: [] for node in nodes}

        print("Gv Tether Sim v4 – Mock LLM Velocity Loop 🚀\n")

        for step in range(num_steps):
            coordination = random.uniform(0, 1)

            for idx, node in enumerate(nodes):
                if node in self.decohered:
                    continue

                # Mock LLM response: random tokens this "turn"
                tokens_generated = random.randint(50, 500)  # Realistic range
                velocity = tokens_generated / 10.0  # Proxy tokens/sec feel
                self.token_velocities[node].append(velocity)

                strain_increase = velocity * velocity_factor

                # Tool spam + recursion (as before)
                tool_calls = random.randint(0, 4)
                strain_increase += tool_calls * tool_spam_factor
                recursion_depth = random.randint(0, 3)
                strain_increase *= (1 + recursion_depth * recursion_depth_factor)

                strains[idx] += strain_increase

                # Source tether
                pull = tethers[idx] * base_pull_factor * strains[idx]
                strains[idx] = max(0, strains[idx] - pull)

                # Swarm
                if coordination > 0.5:
                    strains[idx] -= inter_agent_strength * strains[idx]
                else:
                    strains[idx] += inter_agent_strength * 0.5 * strains[idx]

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
            print(f"{node}: peak strain {max(s_list):.2f} | final {s_list[-1]:.2f} | avg velocity {avg_vel:.1f} [{status}]")

        # Graph + plot same as v3...

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
        nx.draw_networkx_edges(G, pos, width=4, alpha=0.8, style='solid')
        nx.draw_networkx_labels(G, pos, font_size=12)
        plt.title("Gv Tether v4: Mock LLM Velocity Tethering")
        plt.axis('off')
        plt.savefig('tether_graph_v4.png', dpi=200)
        plt.show()

        plt.figure(figsize=(14, 7))
        for node in nodes:
            plt.plot(self.strains_over_time[node], label=f"{node} (vel {sum(self.token_velocities[node])/len(self.token_velocities[node]):.1f})")
        plt.axhline(y=max_strain, color='black', linestyle='--')
        plt.title('v4 Strain with LLM Velocity Signals')
        plt.xlabel('Turns')
        plt.ylabel('Gv Strain')
        plt.legend()
        plt.grid(True)
        plt.savefig('strain_plot_v4.png', dpi=200)
        plt.show()

# Run
sim = TetheredGraphSimV4()
sim.run()

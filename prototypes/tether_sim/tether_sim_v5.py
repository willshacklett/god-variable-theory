import random
random.seed(42)

import networkx as nx
import matplotlib.pyplot as plt

class TetheredGraphSimV5:
    def __init__(self):
        self.strains_over_time = {}
        self.decohered = []
        self.token_velocities = {}  # Track per agent

    def run(self, num_steps=60, num_agents=4,
            velocity_factor=0.3, tool_spam_factor=0.1, recursion_depth_factor=0.25,
            inter_agent_strength=0.35, noise_level=1.8,
            max_strain=6.0, base_pull_factor=0.45):
        
        nodes = [f'Agent_{i}' for i in range(1, num_agents+1)]
        tethers = [1.0] * len(nodes)
        strains = [0.0] * len(nodes)
        self.strains_over_time = {node: [0.0] for node in nodes}
        self.token_velocities = {node: [] for node in nodes}

        print("Gv Tether Sim v5 – Dynamic Throttle + Velocity Logging 🚀\n")

        for step in range(num_steps):
            # Swarm coordination weighted by velocity similarity
            velocities_this_turn = []
            for idx, node in enumerate(nodes):
                if node in self.decohered:
                    continue
                tokens = random.randint(50, 600)
                velocity = tokens / 10.0
                velocities_this_turn.append(velocity)
                self.token_velocities[node].append(velocity)

            # Average velocity variance for coordination score
            if velocities_this_turn:
                coord_score = 1 - (np.var(velocities_this_turn) / max(velocities_this_turn, default=1))**0.5 if max(velocities_this_turn, default=1) > 0 else 1
            else:
                coord_score = 1

            for idx, node in enumerate(nodes):
                if node in self.decohered:
                    continue

                velocity = self.token_velocities[node][-1]
                strain_increase = velocity * velocity_factor

                tool_calls = random.randint(0, 4)
                strain_increase += tool_calls * tool_spam_factor

                recursion_depth = random.randint(0, 3)
                strain_increase *= (1 + recursion_depth * recursion_depth_factor)

                strains[idx] += strain_increase

                # Dynamic intervention: high velocity → temporary stronger pull
                dynamic_pull = base_pull_factor
                if velocity > 40:  # Fast burst threshold
                    dynamic_pull += 0.2
                    print(f"Turn {step+1:2d} | {node} HIGH VELOCITY ({velocity:.1f}) → intervention boost")

                pull = tethers[idx] * dynamic_pull * strains[idx]
                strains[idx] = max(0, strains[idx] - pull)

                # Swarm effect
                if coord_score > 0.6:
                    strains[idx] -= inter_agent_strength * strains[idx]
                else:
                    strains[idx] += inter_agent_strength * 0.4 * strains[idx]

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
            peak_vel = max(v_list) if v_list else 0
            print(f"{node}: peak strain {max(s_list):.2f} | final {s_list[-1]:.2f} | avg/peak vel {avg_vel:.1f}/{peak_vel:.1f} [{status}]")

        # Graph and plot (similar to v4, enhanced labels)
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
        nx.draw_networkx_edges(G, pos, width=4, alpha=0.8)
        nx.draw_networkx_labels(G, pos, font_size=12)
        plt.title("Gv Tether v5: Dynamic Intervention + Swarm Velocity Sync")
        plt.axis('off')
        plt.savefig('tether_graph_v5.png', dpi=200)
        plt.show()

        plt.figure(figsize=(14, 7))
        for node in nodes:
            avg_v = sum(self.token_velocities[node])/len(self.token_velocities[node]) if self.token_velocities[node] else 0
            plt.plot(self.strains_over_time[node], label=f"{node} (avg vel {avg_v:.1f})", linewidth=2.5)
        plt.axhline(y=max_strain, color='black', linestyle='--')
        plt.title('v5 Strain with Velocity Interventions')
        plt.xlabel('Turns')
        plt.ylabel('Gv Strain')
        plt.legend()
        plt.grid(True)
        plt.savefig('strain_plot_v5.png', dpi=200)
        plt.show()

# Run
sim = TetheredGraphSimV5()
sim.run()

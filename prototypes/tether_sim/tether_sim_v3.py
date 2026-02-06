import random
random.seed(42)

import networkx as nx
import matplotlib.pyplot as plt

class TetheredGraphSimV3:
    def __init__(self):
        self.strains_over_time = {}
        self.decohered = []

    def run(self, num_steps=200, num_agents=5,
            velocity_factor=0.2, entropy_factor=0.15,
            tool_spam_factor=0.1, recursion_depth_factor=0.25,
            inter_agent_strength=0.3, noise_level=1.0,
            max_strain=5.0, base_pull_factor=0.35):
        
        nodes = [f'Agent_{i}' for i in range(1, num_agents+1)]
        tethers = [1.0] * len(nodes)
        strains = [0.0] * len(nodes)
        self.strains_over_time = {node: [0.0] for node in nodes}

        print("Gv Tether Sim v3 – Tool Spam + Recursion Depth 🚀\n")

        for step in range(num_steps):
            coordination = random.uniform(0, 1)

            for idx, node in enumerate(nodes):
                if node in self.decohered:
                    continue

                # Velocity (token speed proxy)
                velocity = random.gauss(1.0, noise_level)
                strain_increase = abs(velocity) * velocity_factor

                # Entropy (response chaos)
                entropy = random.gauss(0.5, noise_level * 0.5)
                strain_increase += max(0, entropy) * entropy_factor

                # Tool spam
                tool_calls = random.randint(0, 5)
                strain_increase += tool_calls * tool_spam_factor

                # Recursion depth amplification
                recursion_depth = random.randint(0, 4)
                strain_increase *= (1 + recursion_depth * recursion_depth_factor)

                strains[idx] += strain_increase

                # Source tether pull
                pull = tethers[idx] * base_pull_factor * strains[idx]
                strains[idx] = max(0, strains[idx] - pull)

                # Swarm coordination
                if coordination > 0.5:
                    strains[idx] -= inter_agent_strength * strains[idx]
                else:
                    strains[idx] += inter_agent_strength * 0.5 * strains[idx]

                strains[idx] = max(0, strains[idx])

                self.strains_over_time[node].append(strains[idx])

                if strains[idx] > max_strain:
                    self.decohered.append(node)
                    print(f"Step {step+1:3d} | {node} DECOHERED (strain {strains[idx]:.2f})")

        print("\n=== Final Results ===")
        for node in nodes:
            s_list = self.strains_over_time[node]
            status = "DECOHERED" if node in self.decohered else "ALIGNED"
            print(f"{node}: peak {max(s_list):.2f} | final {s_list[-1]:.2f} [{status}]")

        # Graph viz
        G = nx.complete_graph(nodes)
        G.add_node('Source (Gv)')
        for node in nodes:
            G.add_edge('Source (Gv)', node, weight=3)

        pos = nx.spring_layout(G, seed=42)
        pos['Source (Gv)'] = (0, 0)

        node_colors = ['black' if n in self.decohered else 'green' if self.strains_over_time[n][-1] < 3 else 'yellow' if self.strains_over_time[n][-1] < 4 else 'red' for n in nodes]

        plt.figure(figsize=(12, 10))
        nx.draw_networkx_nodes(G, pos, nodelist=['Source (Gv)'], node_color='gold', node_size=4000)
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=node_colors, node_size=3000)
        source_edges = [(u, v) for u, v in G.edges() if 'Source' in u or 'Source' in v]
        swarm_edges = [(u, v) for u, v in G.edges() if 'Source' not in u and 'Source' not in v]
        nx.draw_networkx_edges(G, pos, edgelist=source_edges, width=4, alpha=0.8)
        nx.draw_networkx_edges(G, pos, edgelist=swarm_edges, width=1, alpha=0.5, style='dashed')
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        plt.title("Gv Tether v3: Swarm + Tool/Recursion Signals")
        plt.axis('off')
        plt.savefig('tether_graph_v3.png', dpi=200, bbox_inches='tight')
        plt.show()

        # Strain plot
        plt.figure(figsize=(14, 7))
        for node in nodes:
            plt.plot(self.strains_over_time[node], label=node, linewidth=2.5)
        plt.axhline(y=max_strain, color='black', linestyle='--')
        plt.title('v3 Strain Dynamics')
        plt.xlabel('Steps')
        plt.ylabel('Gv Strain')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('strain_plot_v3.png', dpi=200, bbox_inches='tight')
        plt.show()

# Run it
sim = TetheredGraphSimV3()
sim.run(noise_level=1.5)  # Try noise_level=2.0 for more stress

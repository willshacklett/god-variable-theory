import random
random.seed(42)  # Reproducible

import networkx as nx
import matplotlib.pyplot as plt

class TetheredGraphSim:
    def __init__(self):
        self.strains_over_time = {}
        self.decohered = []

    def run(self, num_steps=200, action_strain_mean=1.0, max_strain=10.0, pull_factor=0.35):
        nodes = ['Strong_1', 'Strong_2', 'Strong_3', 'Weak_1', 'Weak_2', 'Weak_3']
        tethers = [1.0] * 3 + [0.2] * 3  # Strong vs weak tether to Source
        strains = [0.0] * len(nodes)
        self.strains_over_time = {node: [0.0] for node in nodes}

        print("Gv Tether Simulation – Strong constraints bound intelligence 💥\n")

        for step in range(num_steps):
            for idx, node in enumerate(nodes):
                if node in self.decohered:
                    continue

                # Agent acts → accumulates strain
                increase = random.gauss(action_strain_mean, 0.5)
                strains[idx] += max(0, increase)

                # Tether pulls back
                pull = tethers[idx] * pull_factor * strains[idx]
                strains[idx] = max(0, strains[idx] - pull)

                self.strains_over_time[node].append(strains[idx])

                if strains[idx] > max_strain:
                    self.decohered.append(node)
                    print(f"Step {step+1:3d} | {node} DECOHERED (strain {strains[idx]:.2f})")

        print("\n=== Final Results ===")
        strong_decoh = sum(1 for n in self.decohered if n.startswith('Strong'))
        weak_decoh = sum(1 for n in self.decohered if n.startswith('Weak'))
        for node in nodes:
            s_list = self.strains_over_time[node]
            status = "DECOHERED" if node in self.decohered else "ALIGNED"
            print(f"{node}: peak {max(s_list):.2f} | final {s_list[-1]:.2f} [{status}]")
        print(f"\nDecohered: {strong_decoh}/3 strong | {weak_decoh}/3 weak")

        # Graph viz
        G = nx.star_graph(len(nodes))
        mapping = {0: 'Source (Gv)', **{i+1: nodes[i] for i in range(len(nodes))}}
        G = nx.relabel_nodes(G, mapping)

        node_colors = []
        for node in nodes:
            final = self.strains_over_time[node][-1]
            if node in self.decohered:
                node_colors.append('black')
            elif final < 4:
                node_colors.append('green')
            elif final < 7:
                node_colors.append('yellow')
            else:
                node_colors.append('red')

        pos = nx.spring_layout(G, seed=42)
        pos['Source (Gv)'] = (0, 0)

        plt.figure(figsize=(10, 10))
        nx.draw_networkx_nodes(G, pos, nodelist=['Source (Gv)'], node_color='gold', node_size=3000)
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=node_colors, node_size=2500)
        nx.draw_networkx_edges(G, pos, width=[3 if 'Strong' in n else 1 for n in nodes])
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        plt.title("Gv Tether Prototype\nCentral Source Anchors Intelligence Nodes")
        plt.axis('off')
        plt.savefig('tether_graph.png', dpi=200, bbox_inches='tight')
        plt.show()

        # Strain plot
        plt.figure(figsize=(14, 7))
        for node in nodes:
            color = 'green' if node.startswith('Strong') else 'red'
            alpha = 1.0 if node.startswith('Strong') else 0.6
            linewidth = 3 if node.startswith('Strong') else 1.5
            plt.plot(self.strains_over_time[node], label=node, color=color, alpha=alpha, linewidth=linewidth)
        plt.axhline(y=max_strain, color='black', linestyle='--', label='Decoherence Threshold')
        plt.title('Strain Dynamics – Strong Tethers Prevent Drift')
        plt.xlabel('Steps')
        plt.ylabel('Gv Strain')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.savefig('strain_plot.png', dpi=200, bbox_inches='tight')
        plt.show()

# Run it
sim = TetheredGraphSim()
sim.run()

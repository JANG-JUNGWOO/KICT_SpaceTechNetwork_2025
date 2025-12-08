import networkx as nx
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import community.community_louvain as community_louvain

VAULT_PATH = "table_data.xlsx"
INPUT_PATH = "space_tech_network.gpickle"

try:
    df = pd.read_excel(VAULT_PATH)
    with open(INPUT_PATH, 'rb') as f:
        G = pickle.load(f)
except FileNotFoundError:
    exit()

partition = community_louvain.best_partition(G, random_state=42)

nx.set_node_attributes(G, partition, 'community')

tech_to_comm = {}
for node_id, comm_id in partition.items():
    if 'tech_name' in G.nodes[node_id]:
        tech_name = G.nodes[node_id]['tech_name']
        tech_to_comm[tech_name] = comm_id

df['Community'] = df['기술명'].map(tech_to_comm).fillna('기타')

community_summary = df.groupby('Community')['기술명'].agg(['count', lambda x: list(x)]).reset_index()
community_summary.columns = ['Community', 'Count', 'Technologies']
print(community_summary)

unique_communities = df['Community'].unique()
cmap = plt.get_cmap('tab10')
community_color_map = {comm: cmap(i % 10) for i, comm in enumerate(unique_communities)}
community_color_map['기타'] = (0.5, 0.5, 0.5, 1.0)

pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)

plt.figure(figsize=(30, 18))
ax = plt.gca()

edges_strong = []
edges_weak = []

for u, v, attr in G.edges(data=True):
    weight = attr.get('weight', 0)
    if weight >= 0.7:
        edges_strong.append((u, v))
    elif weight > 0.6:
        edges_weak.append((u, v))

nx.draw_networkx_edges(
    G, pos, edgelist=edges_strong, width=1.5,
    style='solid', edge_color='black', alpha=0.8, ax=ax
)
nx.draw_networkx_edges(
    G, pos, edgelist=edges_weak, width=1.5,
    style='dashed', edge_color='gray', alpha=0.8, ax=ax
)

node_colors = [
    community_color_map.get(G.nodes[n].get('community', '기타'))
    for n in G.nodes()
]

nx.draw_networkx_nodes(
    G, pos, node_size=300, node_color=node_colors,
    edgecolors='black', linewidths=0.7, alpha=0.8, ax=ax
)

labels = {n: G.nodes[n].get('code', str(n)) for n in G.nodes()}
for node, (x, y) in pos.items():
    plt.text(x, y + 0.03, labels[node], fontsize=15, fontweight='bold',
             ha='center', va='bottom', color='black')

legend_elements = [
    mlines.Line2D([], [], color='black', linestyle='solid', linewidth=4, label='0.7 ~ 1'),
    mlines.Line2D([], [], color='gray', linestyle='dashed', linewidth=4, label='0.6 ~ 0.7')
]

plt.axis('off')
plt.show()

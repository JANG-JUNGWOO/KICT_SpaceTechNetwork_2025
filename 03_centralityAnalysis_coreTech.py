import networkx as nx
import pandas as pd
import pickle
from IPython.display import display

VAULT_PATH = "table_data.xlsx"
INPUT_PATH = "space_tech_network.gpickle"

try:
    df_meta = pd.read_excel(VAULT_PATH)
    with open(INPUT_PATH, 'rb') as f:
        G = pickle.load(f)
except FileNotFoundError:
    exit()

metrics = {
    'Degree': nx.degree_centrality,
    'Betweenness': nx.betweenness_centrality,
    'Closeness': nx.closeness_centrality
}

node_info = []
for node in G.nodes():
    tech_name = G.nodes[node].get('tech_name', node)
    node_info.append({'Node_ID': node, '기술명': tech_name})

cent_df = pd.DataFrame(node_info)

for name, func in metrics.items():
    scores = func(G)
    cent_df[name] = cent_df['Node_ID'].map(scores)

metric_cols = list(metrics.keys())
for col in metric_cols:
    min_val = cent_df[col].min()
    max_val = cent_df[col].max()
    if max_val - min_val != 0:
        cent_df[col] = (cent_df[col] - min_val) / (max_val - min_val)
    else:
        cent_df[col] = 0.0

final_df = pd.merge(cent_df, df_meta, on='기술명', how='left')

cols = ['Node_ID'] + metric_cols
final_df = final_df[cols]

styled_df = final_df.style.background_gradient(cmap='coolwarm', subset=['Degree', 'Betweenness', 'Closeness'])
display(styled_df, final_df.describe())

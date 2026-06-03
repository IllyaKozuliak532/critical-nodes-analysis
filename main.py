import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.title("Виявлення критичних вузлів мережі")

# 1. Вбудовані дані (замість CSV)
data = {
    "source": ["Server-1", "Server-1", "Router-1", "Router-1", "PC-2", "PC-3"],
    "target": ["PC-1", "PC-2", "PC-3", "Server-2", "Server-2", "PC-1"]
}
df = pd.DataFrame(data)

st.write("### 📋 Аналізована топологія мережі:")
st.table(df)

# 2. Побудова графа
G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["source"], row["target"])

# 3. Розрахунок центральності
degree = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)

# 4. Формування таблиці результатів
result = pd.DataFrame({
    "Вузол": list(G.nodes()),
    "Degree": [degree[n] for n in G.nodes()],
    "Betweenness": [betweenness[n] for n in G.nodes()],
    "Closeness": [closeness[n] for n in G.nodes()]
})

st.write("### 📊 Показники центральності:")
st.dataframe(result)

# 5. Визначення та виведення критичних вузлів
top_nodes = result.sort_values(by="Betweenness", ascending=False).head(3)

st.write("### ⚠️ Найбільш критичні вузли (за Betweenness):")
st.table(top_nodes)

# 6. Візуалізація
st.write("### 🗺 Візуальна схема мережі:")
fig, ax = plt.subplots()
nx.draw(G, with_labels=True, node_color='lightgreen', node_size=1500, font_weight='bold', ax=ax)
st.pyplot(fig)


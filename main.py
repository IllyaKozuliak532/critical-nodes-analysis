import streamlit as st
import pandas as pd
import networkx as nx

st.title("Виявлення критичних вузлів мережі")

uploaded_file = st.file_uploader("Завантажте CSV файл", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if df.shape[1] < 2:
            st.error("CSV-файл повинен містити щонайменше два стовпці.")
            st.stop()

        df = df.iloc[:, :2]
        df.columns = ["source", "target"]

    except Exception as e:
        st.error(f"Помилка зчитування файлу: {e}")
        st.stop()

    st.write("Вхідні дані:")
    st.write(df)

    G = nx.Graph()

    for _, row in df.iterrows():
        G.add_edge(row["source"], row["target"])

    st.write(f"Кількість вузлів: {G.number_of_nodes()}")
    st.write(f"Кількість ребер: {G.number_of_edges()}")

    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)

    result = pd.DataFrame({
        "Вузол": list(G.nodes()),
        "Degree": [degree[n] for n in G.nodes()],
        "Betweenness": [betweenness[n] for n in G.nodes()],
        "Closeness": [closeness[n] for n in G.nodes()]
    })

    st.write("Показники центральності:")
    st.write(result)

    top_nodes = result.sort_values(by="Betweenness", ascending=False).head(3)

    st.write("Найбільш критичні вузли:")
    st.write(top_nodes)


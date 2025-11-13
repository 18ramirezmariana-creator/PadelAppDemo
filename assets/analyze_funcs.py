import itertools
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def get_unique_players(fixture):
    """Devuelve lista ordenada de jugadores únicos del fixture."""
    return sorted({p for r in fixture for m in r["partidos"] for p in (m["pareja1"] + m["pareja2"])})


def build_matrices(fixture, players):
    """Construye matrices de parejas y enfrentamientos."""
    matrix_parejas = pd.DataFrame(0, index=players, columns=players)
    matrix_enfrentamientos = pd.DataFrame(0, index=players, columns=players)

    for ronda in fixture:
        for partido in ronda["partidos"]:
            p1, p2 = partido["pareja1"], partido["pareja2"]

            # compañeros
            for a, b in itertools.combinations(p1, 2):
                matrix_parejas.loc[a, b] += 1
                matrix_parejas.loc[b, a] += 1
            for a, b in itertools.combinations(p2, 2):
                matrix_parejas.loc[a, b] += 1
                matrix_parejas.loc[b, a] += 1

            # enfrentamientos
            for a in p1:
                for b in p2:
                    matrix_enfrentamientos.loc[a, b] += 1
                    matrix_enfrentamientos.loc[b, a] += 1

    return matrix_parejas, matrix_enfrentamientos


def plot_heatmap(matrix, title, cmap, cbar_label):
    """Genera y muestra un mapa de calor triangular superior."""
    mask = np.tril(np.ones_like(matrix, dtype=bool))
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(matrix, mask=mask, annot=True, fmt="d", cmap=cmap, ax=ax,
                cbar_kws={"label": cbar_label})
    plt.title(title)
    st.pyplot(fig)


def analyze_descansos(fixture, players):
    """Analiza descansos consecutivos y genera mapa de calor."""
    descanso_data = []
    for p in players:
        pattern = [1 if p in r["descansan"] else 0 for r in fixture]
        descanso_data.append(pattern)

    df_desc = pd.DataFrame(descanso_data, index=players)
    df_desc["consec_descansos"] = df_desc.apply(
        lambda x: max((sum(1 for _ in g) for k, g in itertools.groupby(x) if k == 1), default=0), axis=1
    )

    st.dataframe(df_desc[["consec_descansos"]].rename(columns={"consec_descansos": "Descansos consecutivos"}))

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(pd.DataFrame(descanso_data, index=players), cmap="YlOrRd", cbar=False, ax=ax)
    plt.title("Mapa de descansos por ronda (1 = descanso)")
    plt.xlabel("Ronda")
    plt.ylabel("Jugador")
    st.pyplot(fig)


def analyze_algorithm_results(fixture):
    """Ejecuta todo el análisis visual y estadístico del algoritmo."""
    st.markdown("## 🔍 Análisis de Resultados del Algoritmo")

    players = get_unique_players(fixture)
    matrix_parejas, matrix_enfrentamientos = build_matrices(fixture, players)

    st.markdown("#### 🤝 Mapa de calor: quién jugó con quién (parejas)")
    plot_heatmap(matrix_parejas, "Frecuencia de jugadores que compartieron pareja", "PuBuGn", "Veces como pareja")

    st.markdown("#### ⚔️ Mapa de calor: quién jugó contra quién")
    plot_heatmap(matrix_enfrentamientos, "Frecuencia de jugadores que se enfrentaron", "OrRd", "Veces como oponentes")

    st.markdown("#### 💤 Análisis de descansos consecutivos")
    analyze_descansos(fixture, players)

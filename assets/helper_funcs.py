import streamlit as st
import itertools,random
import pandas as pd
from typing import List, Dict, Tuple

#Streamlit Functions
def initialize_vars(defaults:dict):
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
        else:
            pass

#Tournament Logic Functions
def generar_fixture_parejas(parejas, num_canchas):
    """Genera las rondas con máximo num_canchas partidos por ronda.Parejas fijas previamente establecidas"""
    enfrentamientos = list(itertools.combinations(parejas, 2))
    random.shuffle(enfrentamientos)
    rondas = []
    pendientes = enfrentamientos.copy()

    while pendientes:
        ronda = []
        disponibles = set(parejas)
        for _ in range(num_canchas):
            for match in pendientes:
                p1, p2 = match
                if p1 in disponibles and p2 in disponibles:
                    ronda.append(match)
                    disponibles.remove(p1)
                    disponibles.remove(p2)
                    pendientes.remove(match)
                    break
        rondas.append(ronda)
    return rondas

def calcular_ranking_parejas(parejas: List[str], resultados: Dict[Tuple[str,str], Tuple[int,int]]) -> pd.DataFrame:
    """Calcula el ranking acumulado según los resultados ingresados."""
    
    # 1. Uniformizar los nombres de las parejas al formato usado en el fixture (' & ')
    # Si las parejas vienen como ['serg-mari', ...], se convierten a ['serg & mari', ...]
    nombres_uniformes = [
        p.replace("-", " & ") if "-" in p else p
        for p in parejas
    ]
    
    # 2. Inicializar el diccionario de puntajes con los nombres uniformes
    puntajes = {p: 0 for p in nombres_uniformes}
    
    # 3. Calcular los puntajes (ahora las claves p1 y p2 coincidirán)
    for (p1, p2), (r1, r2) in resultados.items():
        # Aquí, p1 y p2 ya están en el formato 'serg & mari', y la clave existe.
        puntajes[p1] += r1
        puntajes[p2] += r2
        
    # 4. Generar el ranking
    ranking = pd.DataFrame(
        sorted(puntajes.items(), key=lambda x: x[1], reverse=True),
        columns=["Jugador", "Puntos"]
    )
    return ranking

def calcular_ranking_individual(resultados: Dict[Tuple[str, str], Tuple[int, int]], 
                                fixture: List[Dict] = None) -> pd.DataFrame:
    """
    Calcula el ranking individual acumulado según los resultados ingresados.
    Cada jugador recibe los puntos que su pareja obtuvo en cada partido.
    Los ayudantes NO suman puntos (verificado con valido_para).
    """
    puntajes = {}
    
    # Construir mapa de válidos si tenemos fixture
    validos_map = {}
    if fixture:
        for ronda_data in fixture:
            for partido in ronda_data["partidos"]:
                pareja1_str = " & ".join(partido["pareja1"])
                pareja2_str = " & ".join(partido["pareja2"])
                validos_map[(pareja1_str, pareja2_str)] = partido.get("valido_para", 
                                                                       partido["pareja1"] + partido["pareja2"])

    for (p1, p2), (r1, r2) in resultados.items():
        # Separar los nombres de cada jugador en la pareja
        jugadores_p1 = p1.split(" & ")
        jugadores_p2 = p2.split(" & ")
        
        # Obtener lista de jugadores válidos para este partido
        validos = validos_map.get((p1, p2), jugadores_p1 + jugadores_p2)
        
        # Sumar puntos SOLO a jugadores válidos (no ayudantes)
        for j in jugadores_p1:
            if j in validos:
                puntajes[j] = puntajes.get(j, 0) + r1
        for j in jugadores_p2:
            if j in validos:
                puntajes[j] = puntajes.get(j, 0) + r2

    # Ordenar ranking
    ranking = pd.DataFrame(
        sorted(puntajes.items(), key=lambda x: x[1], reverse=True),
        columns=["Jugador", "Puntos"]
    )
    return ranking

def render_nombre(jugador, ayudantes):
    if jugador in ayudantes:
        return f"{jugador} 🛟"     # Salvavidas
    return jugador


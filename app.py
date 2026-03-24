import streamlit as st
import random
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SEASON 212 - Official App", layout="wide")

# --- 1. DICCIONARIO MAESTRO DE POSICIONES Y TIERS ---
# (Aquí la app consulta quién es cada uno)
TIERS_POWER = {"Goat": 5.0, "Casi goat": 3.5, "Buenísimos": 2.5, "Muy buenos": 2.0, "Bueno": 1.5, "Base": 1.0}

if 'info_jugadores' not in st.session_state:
    st.session_state.info_jugadores = {
        # Ajax
        "Ferrodada": ("Bueno", "DF Central"), "Forretress": ("Base", "DF Central"), "Klingklang": ("Base", "Lat. Izquierdo"), "Archeops": ("Bueno", "Lat. Derecho"),
        "Duraludon": ("Bueno", "Pivote"), "Empoleon": ("Bueno", "Mediocentro"), "Kingambit": ("Muy buenos", "Mediapunta"),
        "Chien pao": ("Casi goat", "Ext. Izquierdo"), "Kilowatrel": ("Muy buenos", "Ext. Derecho"), "Sandslash alola": ("Bueno", "Delantero Centro"),
        # Real Madrid
        "Metagross": ("Bueno", "DF Central"), "Golbat": ("Base", "Lateral"), "Croagunk": ("Base", "Lateral"), "Inteleon": ("Buenísimos", "Mediocentro"),
        "Liligant": ("Bueno", "MC Lateral"), "Wyglituff": ("Base", "MC Lateral"), "Cinderace": ("Goat", "Mediapunta"),
        "Zeraora": ("Goat", "Ext. Izquierdo"), "Keldeo": ("Buenísimos", "Ext. Derecho"), "Swampert": ("Casi goat", "Delantero Centro"),
        # Sporting Lisboa
        "Ferrothorn": ("Bueno", "DF Central"), "Carbink": ("Base", "Lateral"), "Palossand": ("Base", "Lateral"), "Aromatise": ("Base", "Pivote"),
        "Rotom horno": ("Bueno", "Mediocentro"), "Mismagius": ("Bueno", "MC Lateral"), "Minior": ("Base", "MC Lateral"),
        "Sandslash": ("Base", "Ext. Izquierdo"), "Dugtrio alola": ("Base", "Ext. Derecho"), "Emboar": ("Bueno", "Delantero Centro"),
        # Man City
        "Toxapex": ("Base", "DF Central"), "Electrode": ("Base", "Lateral"), "Durant": ("Bueno", "Lateral"), "Tentacruel": ("Base", "Pivote"),
        "Mr. Mime": ("Base", "Mediocentro"), "Kingdra": ("Muy buenos", "Mediocentro"), "Armarouge": ("Casi goat", "Mediapunta"),
        "Aerodactyl": ("Buenísimos", "Ext. Izquierdo"), "Chien pao": ("Casi goat", "Ext. Derecho"), "Flygon": ("Casi goat", "Delantero Centro"),
        # PORTEROS
        "Onana": ("Goat", "Portero"), "Courtois": ("Goat", "Portero"), "Adan": ("Bueno", "Portero"), "Ederson": ("Goat", "Portero"), "Ter Stegen": ("Goat", "Portero")
    }

# --- 2. DEFINICIÓN DE EQUIPOS (ORDENADOS POR POSICIÓN) ---
if 'equipos' not in st.session_state:
    st.session_state.equipos = {
        "Ajax de Amsterdam": ["Ferrodada", "Forretress", "Klingklang", "Archeops", "Duraludon", "Empoleon", "Kingambit", "Chien pao", "Kilowatrel", "Sandslash alola", "Onana"],
        "Real Madrid": ["Metagross", "Golbat", "Croagunk", "Inteleon", "Liligant", "Wyglituff", "Cinderace", "Zeraora", "Keldeo", "Swampert", "Courtois"],
        "Sporting Lisboa": ["Ferrothorn", "Carbink", "Palossand", "Aromatise", "Rotom horno", "Mismagius", "Minior", "Sandslash", "Dugtrio alola", "Emboar", "Adan"],
        "Man City": ["Toxapex", "Electrode", "Durant", "Tentacruel", "Mr. Mime", "Kingdra", "Armarouge", "Aerodactyl", "Chien pao", "Flygon", "Ederson"]
    }

# --- 3. INICIALIZACIÓN DE DATOS ---
if 'data' not in st.session_state:
    comps = ["Superliga Europea", "Champions", "Supercopa Enter", "Supercopa Exit", "Copa Elite", "FinalCup"]
    st.session_state.data = {c: {"Goles": {}, "Asis": {}, "MVP": {}, "Historial": []} for c in comps}

# --- 4. MOTOR DE SIMULACIÓN ---
def simular_partido(local, visitante, comp):
    p_l = st.session_state.equipos.get(local, [])
    p_v = st.session_state.equipos.get(visitante, [])
    
    def get_prob(j, tipo):
        info = st.session_state.info_jugadores.get(j, ("Base", "Mediocentro"))
        tier, pos = info[0], info[1]
        poder = TIERS_POWER.get(tier, 1.0)
        if tipo == "gol":
            mult = 9.0 if "Delantero" in pos or "Ext." in pos else 3.0 if "Mediapunta" in pos else 0.5
        else:
            mult = 7.0 if "Mediocentro" in pos or "Mediapunta" in pos else 2.0
        return poder * mult

    g_l, g_v = random.randint(0, 5), random.randint(0, 5)
    eventos = []
    for g, eq, plantilla in [(g_l, local, p_l), (g_v, visitante, p_v)]:
        for _ in range(g):
            autor = random.choices(plantilla, weights=[get_prob(j, "gol") for j in plantilla])[0]
            asist = random.choices(plantilla, weights=[get_prob(j, "asis") for j in plantilla])[0]
            eventos.append({"min": random.randint(1, 90), "autor": autor, "asist": asist, "eq": eq})
            st.session_state.data[comp]["Goles"][autor] = st.session_state.data[comp]["Goles"].get(autor, 0) + 1
            st.session_state.data[comp]["Asis"][asist] = st.session_state.data[comp]["Asis"].get(asist, 0) + 1
    
    ganador = local if g_l > g_v else visitante if g_v > g_l else random.choice([local, visitante])
    mvp = random.choice(st.session_state.equipos[ganador])
    st.session_state.data[comp]["MVP"][mvp] = st.session_state.data[comp]["MVP"].get(mvp, 0) + 1
    return {"l": local, "v": visitante, "gl": g_l, "gv": g_v, "evs": sorted(eventos, key=lambda x: x['min']), "mvp": mvp}

# --- 5. INTERFAZ ---
st.sidebar.title("⭐ SEASON 212")
seccion = st.sidebar.radio("MENÚ", ["🏆 Competiciones", "📋 Plantillas", "👤 Buscador", "🌍 Ranking Global"])

if seccion == "🏆 Competiciones":
    comp_activa = st.selectbox("Torneo", list(st.session_state.data.keys()))
    t1, t2 = st.tabs(["🎮 Simulador", "📊 Stats"])
    with t1:
        c1, c2 = st.columns([1, 2])
        with c1:
            txt = st.text_area("Partidos (Local - Visitante)")
            if st.button("Simular"):
                partidos = [l.strip() for l in txt.split("\n") if "-" in l]
                st.session_state.data[comp_activa]["Historial"] = [simular_partido(p.split("-")[0].strip(), p.split("-")[1].strip(), comp_activa) for p in partidos]
        with c2:
            for r in st.session_state.data[comp_activa]["Historial"]:
                st.write(f"### {r['l']} {r['gl']} - {r['gv']} {r['v']}")
                st.caption(f"🌟 MVP: {r['mvp']}")

elif seccion == "📋 Plantillas":
    st.header("📋 Alineaciones Oficiales")
    for eq, jugadores in st.session_state.equipos.items():
        with st.expander(f"Ver plantilla de {eq}"):
            for j in jugadores:
                pos = st.session_state.info_jugadores.get(j, ("?", "Desconocida"))[1]
                st.write(f"**{j}** - <span style='color:#ff4b4b'>{pos}</span>", unsafe_allow_html=True)

elif seccion == "👤 Buscador":
    todos = sorted(list(set([j for e in st.session_state.equipos.values() for j in e])))
    nombre = st.selectbox("Jugador", todos)
    if nombre:
        tier, pos = st.session_state.info_jugadores.get(nombre, ("Base", "MC"))
        st.markdown(f"<div style='background:#262730;padding:20px;border-radius:10px;border-left:5px solid red'><h2>{nombre}</h2><p>{pos} | {tier}</p></div>", unsafe_allow_html=True)
        
        st.write("### Stats por Torneo")
        tabs = st.tabs(list(st.session_state.data.keys()) + ["TOTAL"])
        total_g, total_a, total_m = 0, 0, 0
        for i, c in enumerate(st.session_state.data.keys()):
            g, a, m = st.session_state.data[c]["Goles"].get(nombre, 0), st.session_state.data[c]["Asis"].get(nombre, 0), st.session_state.data[c]["MVP"].get(nombre, 0)
            tabs[i].metric("Goles", g); tabs[i].metric("Asist", a); tabs[i].metric("MVP", m)
            total_g += g; total_a += a; total_m += m
        tabs[-1].success(f"Global: {total_g} G | {total_a} A | {total_m} M")

elif seccion == "🌍 Ranking Global":
    st.header("🌍 Top 30 Global")
    # (Lógica de ranking similar a la anterior...)
    

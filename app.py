import streamlit as st
import random
import pandas as pd

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="SEASON 212 - Official App", layout="wide")

# --- 1. BASE DE DATOS: TIER LIST Y POSICIONES ---
# (Aquí es donde la app "sabe" quién es bueno y dónde juega)
TIERS_POWER = {"Goat": 5.0, "Casi goat": 3.5, "Buenísimos": 2.5, "Muy buenos": 2.0, "Bueno": 1.5, "Base": 1.0}

if 'info_jugadores' not in st.session_state:
    st.session_state.info_jugadores = {
        # DELANTEROS (DC) - Los que más marcan
        "Cinderace": ("Goat", "DC"), "Zeraora": ("Goat", "DC"), "Blaziken": ("Goat", "DC"), 
        "Marshadow": ("Goat", "DC"), "Lucario": ("Buenísimos", "DC"), "Inteleon": ("Buenísimos", "DC"),
        # MEDIOCENTROS (MC) - Los que más asisten
        "Armarouge": ("Casi goat", "MC"), "Gholdengo": ("Casi goat", "MC"), "Zoroark": ("Casi goat", "MC"),
        "Meowscarada": ("Casi goat", "MC"), "Serperior": ("Buenísimos", "MC"),
        # DEFENSAS (DF) - Los que protegen el área
        "Garchomp": ("Casi goat", "DF"), "Flygon": ("Casi goat", "DF"), "Hydreigon": ("Casi goat", "DF"),
        "Toxapex": ("Base", "DF"), "Metagross": ("Bueno", "DF"), "Skarmory": ("Base", "DF"),
        # PORTEROS (POR) - Los reales (0% goles, 100% seguridad)
        "Courtois": ("Goat", "POR"), "Ter Stegen": ("Goat", "POR"), "Ederson": ("Goat", "POR"), 
        "Neuer": ("Goat", "POR"), "Alisson": ("Goat", "POR")
    }

# --- 2. ALINEACIONES OFICIALES ---
if 'equipos' not in st.session_state:
    st.session_state.equipos = {
        "Real Madrid": ["Metagross", "Inteleon", "Lilligant", "Swampert", "Mewtwo", "Keldeo", "Zeraora", "Cinderace", "Courtois"],
        "Manchester City": ["Toxapex", "Electrode", "Durant", "Tentacruel", "Flygon", "Gholdengo", "Armarouge", "Chien pao", "Ederson"],
        "Barcelona": ["Skarmory", "Flareon", "Cloyster", "Vaporeon", "Serperior", "Zoroark", "Marshadow", "Pidgeot", "Ter Stegen"],
        "Liverpool": ["Stonjourner", "Gourgeist", "Skuntank", "Clawitzer", "Ninetales", "Magmortar", "Toxtricity", "Blaziken", "Alisson"],
        "Bayern Munich": ["Kommo-o", "Darmanitan Galar", "Escavalier", "Primarina", "Klefki", "Hydreigon", "Haxorus", "Garchomp", "Neuer"]
    }

# --- 3. INICIALIZAR ESTADÍSTICAS Y COMPETICIONES ---
if 'data' not in st.session_state:
    comps = ["Superliga Europea", "Champions", "Supercopa Enter", "Supercopa Exit", "Copa Elite", "FinalCup"]
    st.session_state.data = {c: {"Goles": {}, "Asis": {}, "MVP": {}, "Historial": []} for c in comps}
    # Para los hitos de los jugadores
    st.session_state.hazañas = {"Zeraora": "Marcó el gol de la victoria en el último minuto.", "Cinderace": "Pichichi histórico."}

# --- 4. MOTOR DE SIMULACIÓN PROFESIONAL ---
def simular_partido(local, visitante, comp):
    p_l = st.session_state.equipos.get(local, [])
    p_v = st.session_state.equipos.get(visitante, [])
    
    def get_prob(j, tipo):
        tier, pos = st.session_state.info_jugadores.get(j, ("Base", "MC"))
        poder = TIERS_POWER.get(tier, 1.0)
        if tipo == "gol":
            mult = 6.0 if pos == "DC" else 2.0 if pos == "MC" else 0.4 if pos == "DF" else 0.0
        else:
            mult = 5.0 if pos == "MC" else 2.5 if pos == "DC" else 1.0 if pos == "DF" else 0.1
        return poder * mult

    # Goles totales (influenciado por el Tier promedio del equipo)
    g_l = max(0, int(random.gauss(2, 1.2)))
    g_v = max(0, int(random.gauss(1.8, 1.2)))
    
    eventos = []
    for g, eq, plantilla in [(g_l, local, p_l), (g_v, visitante, p_v)]:
        for _ in range(g):
            pesos_g = [get_prob(j, "gol") for j in plantilla]
            autor = random.choices(plantilla, weights=pesos_g)[0]
            pesos_a = [get_prob(j, "asis") for j in plantilla]
            asist = random.choices(plantilla, weights=pesos_a)[0]
            if asist == autor: asist = random.choice(plantilla)
            
            minuto = random.randint(1, 90)
            eventos.append({"min": minuto, "autor": autor, "asist": asist, "equipo": eq})
            
            # Guardar stats en la competición actual
            st.session_state.data[comp]["Goles"][autor] = st.session_state.data[comp]["Goles"].get(autor, 0) + 1
            st.session_state.data[comp]["Asis"][asist] = st.session_state.data[comp]["Asis"].get(asist, 0) + 1

    mvp = random.choice(p_l if g_l >= g_v else p_v)
    st.session_state.data[comp]["MVP"][mvp] = st.session_state.data[comp]["MVP"].get(mvp, 0) + 1
    
    return {"l": local, "v": visitante, "gl": g_l, "gv": g_v, "evs": sorted(eventos, key=lambda x: x['min']), "mvp": mvp}

# --- 5. INTERFAZ: MENÚ PRINCIPAL ---
st.sidebar.title("⭐ SEASON 212")
seccion = st.sidebar.selectbox("Ir a:", ["🏆 Competiciones", "👤 Jugadores", "🌍 Ranking Global"])

if seccion == "🏆 Competiciones":
    comp_activa = st.selectbox("Selecciona Torneo", list(st.session_state.data.keys()))
    t1, t2 = st.tabs(["🎮 Simulador", "📊 Estadísticas Torneo"])
    
    with t1:
        col_izq, col_der = st.columns([1, 2])
        with col_izq:
            st.subheader("Chat de Simulación")
            prompt = st.text_area("Pega los partidos (Ej: Real Madrid - Barcelona)", height=200)
            if st.button("🚀 Simular Jornada"):
                lineas = [l.strip() for l in prompt.split("\n") if "-" in l]
                st.session_state.data[comp_activa]["Historial"] = [simular_partido(l.split("-")[0].strip(), l.split("-")[1].strip(), comp_activa) for l in lineas]

        with col_der:
            st.subheader("Resultados")
            for r in st.session_state.data[comp_activa]["Historial"]:
                st.markdown(f"**{r['l']} {r['gl']} - {r['gv']} {r['v']}**")
                st.caption(f"🌟 MVP: {r['mvp']}")
                with st.expander("Ver detalle de goles"):
                    for e in r['evs']: st.write(f"{e['min']}' ⚽ {e['autor']} (Asist: {e['asist']})")
                    st.info(f"Resumen: Un partido vibrante de {comp_activa}.")

    with t2:
        st.header(f"Rankings {comp_activa}")
        c1, c2, c3 = st.columns(3)
        for col, tipo, tit in zip([c1, c2, c3], ["Goles", "Asis", "MVP"], ["Top Goleadores", "Top Asistentes", "Top MVPs"]):
            df = pd.DataFrame.from_dict(st.session_state.data[comp_activa][tipo], orient='index', columns=['Cant.']).sort_values('Cant.', ascending=False).head(30)
            col.table(df)

elif seccion == "👤 Jugadores":
    st.header("👤 Buscador de Jugadores")
    todos = sorted(list(set([j for e in st.session_state.equipos.values() for j in e])))
    nombre = st.selectbox("Busca un Pokémon", todos)
    
    if nombre:
        tier, pos = st.session_state.info_jugadores.get(nombre, ("Base", "MC"))
        club = next((k for k, v in st.session_state.equipos.items() if nombre in v), "Agente Libre")
        st.subheader(f"{nombre} ({pos})")
        st.write(f"**Club:** {club} | **Tier:** {tier}")
        st.write(f"**Azañas:** {st.session_state.hazañas.get(nombre, 'Sin registros importantes aún.')}")
        
        st.write("---")
        st.subheader("Estadísticas Detalladas")
        tabs_c = st.tabs(list(st.session_state.data.keys()) + ["TOTAL GLOBAL"])
        g_t, a_t, m_t = 0, 0, 0
        for i, c in enumerate(st.session_state.data.keys()):
            g = st.session_state.data[c]["Goles"].get(nombre, 0)
            a = st.session_state.data[c]["Asis"].get(nombre, 0)
            m = st.session_state.data[c]["MVP"].get(nombre, 0)
            tabs_c[i].metric("Goles", g); tabs_c[i].metric("Asist", a); tabs_c[i].metric("MVP", m)
            g_t += g; a_t += a; m_t += m
        tabs_c[-1].success(f"Goles: {g_t} | Asistencias: {a_t} | MVPs: {m_t}")

elif seccion == "🌍 Ranking Global":
    st.header("🌍 Rankings Globales (Todas las Competiciones)")
    g_g, a_g, m_g = {}, {}, {}
    for c in st.session_state.data:
        for j, v in st.session_state.data[c]["Goles"].items(): g_g[j] = g_g.get(j, 0) + v
        for j, v in st.session_state.data[c]["Asis"].items(): a_g[j] = a_g.get(j, 0) + v
        for j, v in st.session_state.data[c]["MVP"].items(): m_g[j] = m_g.get(j, 0) + v
    
    c1, c2, c3 = st.columns(3)
    c1.subheader("Bota de Oro"); c1.table(pd.Series(g_g).sort_values(ascending=False).head(30))
    c2.subheader("Asistidores"); c2.table(pd.Series(a_g).sort_values(ascending=False).head(30))
    c3.subheader("Líderes MVP"); c3.table(pd.Series(m_g).sort_values(ascending=False).head(30))

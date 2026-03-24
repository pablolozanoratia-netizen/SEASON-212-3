import streamlit as st
import random
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="SEASON 212 - Official App", layout="wide")

# --- 1. BASE DE DATOS MAESTRA (TIERS Y POSICIONES) ---
# He mapeado los jugadores según el texto que me pasaste
TIERS_POWER = {"Goat": 5.0, "Casi goat": 3.5, "Buenísimos": 2.5, "Muy buenos": 2.0, "Bueno": 1.5, "Base": 1.0}

if 'info_jugadores' not in st.session_state:
    st.session_state.info_jugadores = {
        # AJAX
        "Ferrodada": ("Bueno", "Central"), "Forretress": ("Base", "Central"), "Klingklang": ("Base", "Lat. Izquierdo"), "Archeops": ("Bueno", "Lat. Derecho"),
        "Duraludon": ("Bueno", "Pivote"), "Empoleon": ("Bueno", "Mediocentro"), "Kingambit 2": ("Muy buenos", "Mediapunta"),
        "Chien pao 2": ("Casi goat", "Ext. Izquierdo"), "Kilowatrel": ("Muy buenos", "Ext. Derecho"), "Sandslash alola": ("Bueno", "Delantero Centro"),
        # REAL MADRID
        "Metagross": ("Bueno", "Central"), "Golbat": ("Base", "Lateral"), "Croagunk": ("Base", "Lateral"), "Inteleon": ("Buenísimos", "Mediocentro"),
        "Liligant": ("Bueno", "MC Lateral"), "Wyglituff": ("Base", "MC Lateral"), "Cinderace": ("Goat", "Mediapunta"),
        "Zeraora": ("Goat", "Ext. Izquierdo"), "Keldeo": ("Buenísimos", "Ext. Derecho"), "Swampert": ("Casi goat", "Delantero Centro"),
        # SPORTING LISBOA
        "Ferrothorn": ("Bueno", "Central"), "Carbink": ("Base", "Lateral"), "Palossand": ("Base", "Lateral"), "Aromatise": ("Base", "Pivote"),
        "Rotom horno": ("Bueno", "Mediocentro"), "Mismagius": ("Bueno", "MC Lateral"), "Minior": ("Base", "MC Lateral"), "Sandslash": ("Base", "Ext. Izquierdo"), "Dugtrio alola": ("Base", "Ext. Derecho"), "Emboar": ("Bueno", "Delantero Centro"),
        # BENFICA
        "Scolipede": ("Bueno", "Central"), "Apletun": ("Base", "Central"), "Jumpluff": ("Base", "Lateral"), "Electrode galar": ("Bueno", "Lateral"), "Fearow": ("Base", "Pivote"), "Omastar": ("Base", "Mediocentro"), "Kingdra": ("Muy buenos", "Mediapunta"), "Hitmonlee": ("Bueno", "Ext. Izquierdo"), "Wyedeer": ("Bueno", "Ext. Derecho"), "Persian": ("Base", "Delantero Centro"),
        # MAN CITY
        "Toxapex": ("Base", "Central"), "Electrode": ("Base", "Lateral"), "Durant": ("Bueno", "Lateral"), "Tentacruel": ("Base", "Pivote"), "Mr. Mime": ("Base", "Mediocentro"), "Kingdra": ("Muy buenos", "Mediocentro"), "Armarouge": ("Casi goat", "Mediapunta"), "Aerodactyl": ("Buenísimos", "Ext. Izquierdo"), "Chien pao": ("Casi goat", "Ext. Derecho"), "Flygon": ("Casi goat", "Delantero Centro"),
        # BARCELONA
        "Skarmory": ("Base", "Central"), "Flareon": ("Base", "Lateral"), "Cloyster": ("Bueno", "Lateral"), "Slowking": ("Bueno", "Pivote"), "Vaporeon": ("Bueno", "Mediocentro"), "Vespiquen": ("Base", "Mediocentro"), "Serperior": ("Buenísimos", "Mediapunta"), "Zoroark": ("Casi goat", "Ext. Izquierdo"), "Marshadow": ("Goat", "Ext. Derecho"), "Pidgeot": ("Muy buenos", "Delantero Centro"),
        # PORTEROS
        "Courtois": ("Goat", "Portero"), "Ter Stegen": ("Goat", "Portero"), "Ederson": ("Goat", "Portero"), "Onana": ("Goat", "Portero"), "Alisson": ("Goat", "Portero"), "Raya": ("Muy buenos", "Portero"), "Neuer": ("Goat", "Portero")
    }

# --- 2. ALINEACIONES (SQUAD LISTS) ---
if 'equipos' not in st.session_state:
    st.session_state.equipos = {
        "Ajax de Amsterdam": ["Ferrodada", "Forretress", "Klingklang", "Archeops", "Duraludon", "Empoleon", "Kingambit 2", "Chien pao 2", "Kilowatrel", "Sandslash alola", "Onana"],
        "Real Madrid": ["Metagross", "Golbat", "Croagunk", "Inteleon", "Liligant", "Wyglituff", "Cinderace", "Zeraora", "Keldeo", "Swampert", "Courtois"],
        "Sporting Lisboa": ["Ferrothorn", "Carbink", "Palossand", "Aromatise", "Rotom horno", "Mismagius", "Minior", "Sandslash", "Dugtrio alola", "Emboar", "Adan"],
        "Benfica": ["Scolipede", "Apletun", "Jumpluff", "Electrode galar", "Fearow", "Omastar", "Kingdra", "Hitmonlee", "Wyedeer", "Persian", "Trubin"],
        "Man City": ["Toxapex", "Electrode", "Durant", "Tentacruel", "Mr. Mime", "Kingdra", "Armarouge", "Aerodactyl", "Chien pao", "Flygon", "Ederson"],
        "Barcelona": ["Skarmory", "Flareon", "Cloyster", "Slowking", "Vaporeon", "Vespiquen", "Serperior", "Zoroark", "Marshadow", "Pidgeot", "Ter Stegen"]
    }

# --- 3. PERSISTENCIA DE DATOS ---
if 'data' not in st.session_state:
    comps = ["Superliga Europea", "Champions", "Supercopa Enter", "Supercopa Exit", "Copa Elite", "FinalCup"]
    st.session_state.data = {c: {"Goles": {}, "Asis": {}, "MVP": {}, "Historial": []} for c in comps}

# --- 4. MOTOR DE SIMULACIÓN LÓGICO ---
def simular_partido(local, visitante, comp):
    plantilla_l = st.session_state.equipos.get(local, [])
    plantilla_v = st.session_state.equipos.get(visitante, [])
    
    def calcular_peso(jugador, tipo):
        tier, pos = st.session_state.info_jugadores.get(jugador, ("Base", "Mediocentro"))
        puntos = TIERS_POWER.get(tier, 1.0)
        if tipo == "gol":
            mult = 12.0 if "Delantero" in pos or "Ext." in pos else 4.0 if "Mediapunta" in pos else 0.5
        else:
            mult = 9.0 if "Mediocentro" in pos or "Mediapunta" in pos else 1.5
        return puntos * mult

    g_l, g_v = random.randint(0, 4), random.randint(0, 4)
    resumen_goles = []
    
    for goles, equipo, plantilla in [(g_l, local, plantilla_l), (g_v, visitante, plantilla_v)]:
        for _ in range(goles):
            autor = random.choices(plantilla, weights=[calcular_peso(j, "gol") for j in plantilla])[0]
            asist = random.choices(plantilla, weights=[calcular_peso(j, "asis") for j in plantilla])[0]
            minuto = random.randint(1, 90)
            resumen_goles.append({"min": minuto, "autor": autor, "asist": asist, "equipo": equipo})
            st.session_state.data[comp]["Goles"][autor] = st.session_state.data[comp]["Goles"].get(autor, 0) + 1
            st.session_state.data[comp]["Asis"][asist] = st.session_state.data[comp]["Asis"].get(asist, 0) + 1

    mvp = random.choice(plantilla_l if g_l >= g_v else plantilla_v)
    st.session_state.data[comp]["MVP"][mvp] = st.session_state.data[comp]["MVP"].get(mvp, 0) + 1
    return {"l": local, "v": visitante, "gl": g_l, "gv": g_v, "evs": sorted(resumen_goles, key=lambda x: x['min']), "mvp": mvp}

# --- 5. INTERFAZ DE USUARIO (EL MENÚ) ---
menu = st.sidebar.radio("NAVEGACIÓN", ["🏆 Competiciones", "📋 Ver Plantillas", "👤 Buscador de Jugadores", "🌍 Ranking Global"])

if menu == "🏆 Competiciones":
    comp_activa = st.selectbox("Selecciona Torneo", list(st.session_state.data.keys()))
    tab_sim, tab_stats = st.tabs(["🎮 Simulador", "📊 Estadísticas"])
    
    with tab_sim:
        chat = st.text_area("Pega los partidos aquí (Ej: Real Madrid - Barcelona)", height=150)
        if st.button("🚀 Simular Partidos"):
            lineas = [l.strip() for l in chat.split("\n") if "-" in l]
            st.session_state.data[comp_activa]["Historial"] = [simular_partido(l.split("-")[0].strip(), l.split("-")[1].strip(), comp_activa) for l in lineas]
        
        for r in st.session_state.data[comp_activa]["Historial"]:
            st.markdown(f"### {r['l']} {r['gl']} - {r['gv']} {r['v']}")
            st.write(f"🌟 **MVP:** {r['mvp']}")
            with st.expander("Ver Goles"):
                for e in r['evs']: st.write(f"{e['min']}' ⚽ {e['autor']} (Asist: {e['asist']})")

    with tab_stats:
        c1, c2, c3 = st.columns(3)
        for col, t, tit in zip([c1, c2, c3], ["Goles", "Asis", "MVP"], ["GOLEADORES", "ASISTENTES", "MVPs"]):
            col.subheader(tit)
            df = pd.DataFrame.from_dict(st.session_state.data[comp_activa][t], orient='index', columns=['Total']).sort_values('Total', ascending=False).head(30)
            col.table(df)

elif menu == "📋 Ver Plantillas":
    st.header("📋 Alineaciones con Posiciones")
    for eq, jugs in st.session_state.equipos.items():
        with st.expander(f"Plantilla de {eq}"):
            for j in jugs:
                pos = st.session_state.info_jugadores.get(j, ("?", "Desconocida"))[1]
                st.markdown(f"**{j}** - <span style='color:red; font-weight:bold'>{pos}</span>", unsafe_allow_html=True)

elif menu == "👤 Buscador de Jugadores":
    st.header("👤 Perfil del Jugador")
    nombre = st.selectbox("Selecciona un Pokémon", sorted(list(st.session_state.info_jugadores.keys())))
    if nombre:
        tier, pos = st.session_state.info_jugadores.get(nombre)
        club = next((k for k, v in st.session_state.equipos.items() if nombre in v), "Agente Libre")
        st.markdown(f"""
        <div style="background-color:#1e1e1e; padding:25px; border-radius:15px; border-left: 8px solid #ff4b4b;">
            <h1 style="margin:0; color:white;">{nombre}</h1>
            <p style="font-size:20px; color:#ff4b4b;">{pos} | {tier} | {club}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### 📊 Rendimiento por Competición")
        tabs = st.tabs(list(st.session_state.data.keys()) + ["TOTAL GLOBAL"])
        tg, ta, tm = 0, 0, 0
        for i, c in enumerate(st.session_state.data.keys()):
            g, a, m = st.session_state.data[c]["Goles"].get(nombre, 0), st.session_state.data[c]["Asis"].get(nombre, 0), st.session_state.data[c]["MVP"].get(nombre, 0)
            tabs[i].metric("Goles", g); tabs[i].metric("Asistencias", a); tabs[i].metric("MVPs", m)
            tg += g; ta += a; tm += m
        tabs[-1].success(f"Estadísticas Totales: {tg} Goles | {ta} Asistencias | {tm} MVPs")

elif menu == "🌍 Ranking Global":
    st.header("🌍 Ranking Top 30 Temporada 212")
    g_global = {}
    for c in st.session_state.data:
        for j, v in st.session_state.data[c]["Goles"].items(): g_global[j] = g_global.get(j, 0) + v
    st.table(pd.DataFrame.from_dict(g_global, orient='index', columns=['Goles Totales']).sort_values('Goles Totales', ascending=False).head(30))
 

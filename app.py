import streamlit as st
import random
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Pokémon Football Engine S212", layout="wide")

# --- DATA ACTUALIZADA SEGÚN TU TIER LIST ---
TIERS = {"Goat": 5.0, "Casi goat": 4.0, "Buenísimos": 3.0, "Muy buenos": 2.0, "Bueno": 1.5, "Base": 1.0}

STARS = {
    "Cinderace": "Goat", "Blaziken": "Goat", "Zeraora": "Goat", "Marshadow": "Goat",
    "Weavile": "Casi goat", "Garchomp": "Casi goat", "Flygon": "Casi goat", "Hydreigon": "Casi goat",
    "Armarouge": "Casi goat", "Infernape": "Casi goat", "Zoroark": "Casi goat", "Dragapult": "Casi goat",
    "Meowscarada": "Casi goat", "Chien pao": "Casi goat", "Gholdengo": "Casi goat", "Noivern": "Casi goat"
}

# --- BASE DE DATOS EQUIPOS (Añade los que necesites aquí) ---
if 'equipos' not in st.session_state:
    st.session_state.equipos = {
        "Manchester city": ["Toxapex", "Electrode", "Durant", "Tentacruel", "Mr. Mime", "Kingdra", "Armarouge", "Aerodactyl", "Chien pao", "Flygon", "Gholdengo"],
        "Bayern Munich": ["Kommo-o", "Darmanitan Galar", "Escavalier", "Primarina", "Klefki", "Hydreigon", "Tapu fini", "Haxorus", "Raichu", "Garchomp", "Glaceon"],
        "Real Madrid": ["Metagross", "Golbat", "Croagunk", "Inteleon", "Lilligant", "Wigglytuff", "Cinderace", "Zeraora", "Keldeo", "Swampert", "Mewtwo"],
        "Barcelona": ["Skarmory", "Flareon", "Cloyster", "Slowking", "Vaporeon", "Vespiquen", "Serperior", "Zoroark", "Marshadow", "Pidgeot", "Gardevoir"],
        "Liverpool": ["Stonjourner", "Gourgeist", "Skuntank", "Clawitzer", "Ninetales", "Magmortar", "Toxtricity", "Blaziken", "Boltund", "Rampardos", "Lucario"]
    }
    # Inicializar estadísticas
    for c in ["Superliga", "Champions", "Copa Elite", "Global"]:
        if f'stats_{c}' not in st.session_state:
            st.session_state[f'stats_{c}'] = {"Goles": {}, "Asis": {}, "MVP": {}}

# --- MOTOR DE SIMULACIÓN ---
def simular(local, visitante, torneo):
    def get_p(p): return TIERS.get(STARS.get(p, "Base"), 1.0)
    p_l = sum([get_p(x) for x in st.session_state.equipos[local]]) / 10
    p_v = sum([get_p(x) for x in st.session_state.equipos[visitante]]) / 10
    
    g_l = max(0, int(random.gauss(p_l, 1.2)))
    g_v = max(0, int(random.gauss(p_v, 1.2)))
    
    eventos = []
    for g, eq in [(g_l, local), (g_v, visitante)]:
        for _ in range(g):
            m = random.randint(1, 90)
            aut = random.choice(st.session_state.equipos[eq][-4:])
            asi = random.choice(st.session_state.equipos[eq])
            eventos.append(f"{m}' ⚽ {aut} (Asist: {asi}) - {eq}")
            for c in [torneo, "Global"]:
                st.session_state[f'stats_{c}']["Goles"][aut] = st.session_state[f'stats_{c}']["Goles"].get(aut, 0) + 1
                st.session_state[f'stats_{c}']["Asis"][asi] = st.session_state[f'stats_{c}']["Asis"].get(asi, 0) + 1

    mvp = random.choice(st.session_state.equipos[local if g_l >= g_v else visitante])
    st.session_state[f'stats_{torneo}']["MVP"][mvp] = st.session_state[f'stats_{torneo}']["MVP"].get(mvp, 0) + 1
    st.session_state['stats_Global']["MVP"][mvp] = st.session_state['stats_Global']["MVP"].get(mvp, 0) + 1
    return g_l, g_v, sorted(eventos), mvp

# --- INTERFAZ ---
st.title("🏆 Pokémon Football Simulator - Season 212")
t1, t2, t3 = st.tabs(["🎮 Simular", "📊 Rankings Torneo", "🌍 Ranking Global"])

with t1:
    torneo = st.selectbox("Torneo", ["Superliga", "Champions", "Copa Elite"])
    partidos = st.text_area("Partidos (Ejemplo: Manchester city - Real Madrid)")
    if st.button("Simular Jornada"):
        for p in partidos.split("\n"):
            if "-" in p:
                l, v = [x.strip() for x in p.split("-")]
                if l in st.session_state.equipos and v in st.session_state.equipos:
                    gl, gv, evs, mvp = simular(l, v, torneo)
                    with st.expander(f"🏁 {l} {gl} - {gv} {v}", expanded=True):
                        for e in evs: st.write(e)
                        st.success(f"MVP: {mvp}")
                else: st.error(f"Nombre de equipo mal escrito: {l} o {v}")

with t2:
    st.subheader(f"Top 10 - {torneo}")
    c1, c2 = st.columns(2)
    c1.write("⚽ Goles"); c1.table(pd.Series(st.session_state[f'stats_{torneo}']["Goles"]).sort_values(ascending=False).head(10))
    c2.write("🌟 MVPs"); c2.table(pd.Series(st.session_state[f'stats_{torneo}']["MVP"]).sort_values(ascending=False).head(10))

with t3:
    st.header("🌍 Bota de Oro Global")
    st.table(pd.Series(st.session_state['stats_Global']["Goles"]).sort_values(ascending=False).head(15))
                      

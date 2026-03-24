import streamlit as st
import random
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SEASON 212 - Official App", layout="wide")

# --- 1. BASE DE DATOS DE TIERS Y ROLES (POSICIONES REALES SEGÚN TU TEXTO) ---
TIERS = {"Goat": 5.0, "Casi goat": 3.5, "Buenísimos": 2.5, "Muy buenos": 2.0, "Bueno": 1.5, "Base": 1.0}

if 'info_jugadores' not in st.session_state:
    st.session_state.info_jugadores = {
        # AJAX
        "Ferrodada": ("Bueno", "Central"), "Forretress": ("Base", "Central"), "Klingklang": ("Base", "Li"), "Archeops": ("Bueno", "Ld"), "Duraludon": ("Bueno", "Pivote"), "Empoleon": ("Bueno", "Mediocentro"), "Kingambit 2": ("Muy buenos", "MEDIAPUNTA"), "Chien pao 2": ("Casi goat", "Ex izq"), "Kilowatrel": ("Muy buenos", "Ex der"), "Sandslash alola": ("Bueno", "Del centro"),
        # REAL MADRID
        "Metagross": ("Bueno", "Defensa central"), "Golbat": ("Base", "Lateral"), "Croagunk": ("Base", "Lateral"), "Inteleon": ("Buenísimos", "Mediocentro"), "Liligant": ("Bueno", "Mediocentro lateral"), "Wyglituff": ("Base", "Mediocentro lateral"), "Cinderace": ("Goat", "Media punta"), "zeraora": ("Goat", "Extremo izq"), "keldeo": ("Buenísimos", "Extremo derecho"), "Swampert": ("Casi goat", "Delantero centro"),
        # SPORTING LISBOA
        "ferrothorn": ("Bueno", "Defensa central"), "carbink": ("Base", "Lateral"), "palossand": ("Base", "Lateral"), "aromatise": ("Base", "Medio centro defensifo"), "rotom horno": ("Bueno", "Mediocentro"), "mismagius": ("Bueno", "Mediocentros lateral"), "minior": ("Base", "Mediocentros lateral"), "sandslash": ("Base", "Extremo izq"), "dugtrio alola": ("Base", "Extremo derecho"), "emboar": ("Bueno", "Delantero centro"),
        # JUVENTUS
        "steelix": ("Bueno", "Defensa central"), "DUBWOl": ("Base", "Lateral"), "armaldo": ("Base", "Lateral"), "reuniclus": ("Bueno", "Mediocentro"), "magmar": ("Bueno", "Mediocentro"), "alakazam": ("Goat", "Media punta"), "absol": ("Muy buenos", "Media punta orbitante"), "tapu koko": ("Goat", "Extremo izq"), "medicham": ("Buenísimos", "Extremo derecho"), "urshifu": ("Goat", "Delantero centro"),
        # BAYERN
        "kommo": ("Buenísimos", "Defensa central"), "darmanitan galar": ("Bueno", "Lateral"), "escavalier": ("Bueno", "Lateral"), "Primarina": ("Bueno", "Mediocentro"), "klefki": ("Base", "Mediocentro"), "hydreigon": ("Casi goat", "Media punta"), "tapu fini": ("Goat", "Media punta orbitante"), "haxorus": ("Buenísimos", "Extremo izq"), "raichu": ("Bueno", "Extremo derecho"), "garchomp": ("Casi goat", "Delantero centro"),
        # ARSENAL
        "weezing": ("Bueno", "Defensa central"), "toucanon": ("Base", "Lateral"), "klinklang": ("Base", "Lateral"), "Blastoise": ("Buenísimos", "Medio centro defensifo"), "Porygon 2": ("Bueno", "Mediocentro"), "indedee": ("Base", "Mediocentro"), "melenaleteo": ("Goat", "Media punta"), "DRAGAPULT": ("Casi goat", "Extremo izq"), "ceruledge": ("Buenísimos", "Extremo derecho"), "hawlucha": ("Buenísimos", "Delantero centro")
    }

# --- 2. ALINEACIONES (LOS 30 EQUIPOS) ---
if 'equipos' not in st.session_state:
    st.session_state.equipos = {
        "Man City": ["toxapex", "electrode", "Durant", "tentacruel", "me mime", "kingdra", "armarouge", "aerodactyl", "chien pao", "flygon", "Ederson"],
        "Bayern Munich": ["kommo", "darmanitan galar", "escavalier", "Primarina", "klefki", "hydreigon", "tapu fini", "haxorus", "raichu", "garchomp", "Neuer"],
        "Juventus": ["steelix", "DUBWOl", "armaldo", "reuniclus", "magmar", "alakazam", "absol", "tapu koko", "medicham", "urshifu", "Di Gregorio"],
        "PSG": ["darmanitan", "drednaw", "goodra", "delphox", "talonflame", "noiverm", "kingambit", "zarude", "swellow", "Pawmot", "Donnarumma"],
        "Arsenal": ["weezing", "toucanon", "klinklang", "Blastoise", "Porygon 2", "indedee", "melenaleteo", "DRAGAPULT", "ceruledge", "hawlucha", "Raya"],
        "Real Madrid": ["Metagross", "Golbat", "Croagunk", "Inteleon", "Liligant", "Wyglituff", "Cinderace", "zeraora", "keldeo", "Swampert", "Courtois"],
        "Barcelona": ["skarmory", "flareon", "cloyster", "slowking", "vaporeon", "vespiquen", "serperior", "zoroark", "marshadow", "pidgeot", "Ter Stegen"],
        "Ajax": ["Ferrodada", "Forretress", "Klingklang", "Archeops", "Duraludon", "Empoleon", "Kingambit 2", "Chien pao 2", "Kilowatrel", "Sandslash alola", "Onana"],
        "Sp Lisboa": ["ferrothorn", "carbink", "palossand", "aromatise", "rotom horno", "mismagius", "minior", "sandslash", "dugtrio alola", "emboar", "Adan"],
        # ... (Resto de los 30 equipos se añaden aquí siguiendo el mismo formato)
    }

# --- 3. INICIALIZACIÓN DE DATOS ---
if 'data' not in st.session_state:
    comps = ["Superliga Europea", "Champions", "Supercopa Enter", "Supercopa Exit", "Copa Elite", "FinalCup"]
    st.session_state.data = {c: {"Goles": {}, "Asis": {}, "MVP": {}, "Historial": []} for c in comps}

# --- 4. MOTOR DE SIMULACIÓN ---
def simular_partido(local, visitante, comp, modo_prueba=False):
    p_l = st.session_state.equipos.get(local, ["?"]*11)
    p_v = st.session_state.equipos.get(visitante, ["?"]*11)
    
    def get_peso(j, tipo):
        info = st.session_state.info_jugadores.get(j, ("Base", "Mediocentro"))
        puntos = TIERS.get(info[0], 1.0)
        pos = info[1].lower()
        if tipo == "gol":
            mult = 20.0 if any(x in pos for x in ["del", "ext", "ex ", "punta"]) else 0.5
        else:
            mult = 15.0 if any(x in pos for x in ["medio", "punta", "pivote", "defensifo"]) else 2.0
        return puntos * mult

    gl, gv = random.randint(0, 5), random.randint(0, 5)
    evs = []
    for g, eq, plant in [(gl, local, p_l), (gv, visitante, p_v)]:
        for _ in range(g):
            autor = random.choices(plant, weights=[get_peso(j, "gol") for j in plant])[0]
            asist = random.choices(plant, weights=[get_peso(j, "asis") for j in plant])[0]
            evs.append({"min": random.randint(1, 90), "autor": autor, "asist": asist, "eq": eq})
            if not modo_prueba:
                st.session_state.data[comp]["Goles"][autor] = st.session_state.data[comp]["Goles"].get(autor, 0) + 1
                st.session_state.data[comp]["Asis"][asist] = st.session_state.data[comp]["Asis"].get(asist, 0) + 1
    
    mvp = random.choice(p_l if gl >= gv else p_v)
    if not modo_prueba:
        st.session_state.data[comp]["MVP"][mvp] = st.session_state.data[comp]["MVP"].get(mvp, 0) + 1
    return {"l": local, "v": visitante, "gl": gl, "gv": gv, "evs": sorted(evs, key=lambda x: x['min']), "mvp": mvp}

# --- 5. INTERFAZ ---
st.sidebar.title("⭐ SEASON 212")
menu = st.sidebar.radio("MENÚ", ["🏆 Competiciones", "📋 Plantillas", "👤 Buscador"])

if menu == "🏆 Competiciones":
    comp_activa = st.selectbox("Torneo", list(st.session_state.data.keys()))
    t1, t2 = st.tabs(["🎮 Simulador", "📊 Estadísticas"])
    with t1:
        modo_prueba = st.toggle("🧪 Modo Prueba (No suma estadísticas)")
        txt = st.text_area("Pega aquí (Ej: Real Madrid - Barcelona)", height=150)
        
        if st.button("🚀 Simular Partido(s)"):
            if txt:
                lineas = [l.strip() for l in txt.split("\n") if "-" in l]
                for p in lineas:
                    nombres = p.split("-")
                    loc, vis = nombres[0].strip(), nombres[1].strip()
                    
                    if loc in st.session_state.equipos and vis in st.session_state.equipos:
                        res = simular_partido(loc, vis, comp_activa, modo_prueba)
                        if not modo_prueba:
                            st.session_state.data[comp_activa]["Historial"].append(res)
                        
                        # Mostrar resultado
                        st.subheader(f"{res['l']} {res['gl']} - {res['gv']} {res['v']}")
                        st.write(f"🌟 MVP: **{res['mvp']}**")
                        with st.expander("Ver detalle de goles"):
                            for e in res['evs']:
                                st.write(f"{e['min']}' ⚽ **{e['autor']}** (Asist: {e['asist']})")
                    else:
                        st.error(f"Error: Asegúrate de que '{loc}' y '{vis}' estén bien escritos.")
            else:
                st.warning("Escribe al menos un partido.")

elif menu == "📋 Plantillas":
    for eq, jugs in st.session_state.equipos.items():
        with st.expander(f"Ver {eq}"):
            for j in jugs:
                pos = st.session_state.info_jugadores.get(j, ("Base", "Posición por definir"))[1]
                st.markdown(f"**{j}** - <span style='color:#FF4B4B; font-weight:bold;'>{pos}</span>", unsafe_allow_html=True)

elif menu == "👤 Buscador":
    nombre = st.selectbox("Selecciona Jugador", sorted(list(set([j for e in st.session_state.equipos.values() for j in e]))))
    if nombre:
        tier, pos = st.session_state.info_jugadores.get(nombre, ("Base", "Mediocentro"))
        st.markdown(f"<div style='background:#1e1e1e;padding:20px;border-left:8px solid #FF4B4B; border-radius:10px;'><h1>{nombre}</h1><p style='color:#FF4B4B; font-size:20px;'>{pos} | {tier}</p></div>", unsafe_allow_html=True)
        # Stats por competición (6 pestañas)
        tabs = st.tabs(list(st.session_state.data.keys()) + ["TOTAL GLOBAL"])
        tg, ta, tm = 0, 0, 0
        for i, c in enumerate(st.session_state.data.keys()):
            g = st.session_state.data[c]["Goles"].get(nombre, 0)
            a = st.session_state.data[c]["Asis"].get(nombre, 0)
            m = st.session_state.data[c]["MVP"].get(nombre, 0)
            tabs[i].metric("Goles", g); tabs[i].metric("Asistencias", a); tabs[i].metric("MVPs", m)
            tg += g; ta += a; tm += m
        tabs[-1].success(f"Estadísticas Globales: {tg} Goles | {ta} Asistencias | {tm} MVPs")

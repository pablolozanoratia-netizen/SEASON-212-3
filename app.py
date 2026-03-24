import streamlit as st
import random
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SEASON 212 - Official App", layout="wide")

# --- 1. BASE DE DATOS DE TIERS Y ROLES ---
TIERS = {"Goat": 5.0, "Casi goat": 3.5, "Buenísimos": 2.5, "Muy buenos": 2.0, "Bueno": 1.5, "Base": 1.0}

if 'info_jugadores' not in st.session_state:
    st.session_state.info_jugadores = {
        # Ajax
        "Ferrodada": ("Bueno", "Central"), "Forretress": ("Base", "Central"), "Klingklang": ("Base", "Li"), "Archeops": ("Bueno", "Ld"), "Duraludon": ("Bueno", "Pivote"), "Empoleon": ("Bueno", "Mediocentro"), "Kingambit 2": ("Muy buenos", "Mediapunta"), "Chien pao 2": ("Casi goat", "Ex Izq"), "Kilowatrel": ("Muy buenos", "Ex Der"), "Sandslash alola": ("Bueno", "Del Centro"),
        # Madrid
        "Metagross": ("Bueno", "Defensa Central"), "Golbat": ("Base", "Lateral"), "Croagunk": ("Base", "Lateral"), "Inteleon": ("Buenísimos", "Mediocentro"), "Liligant": ("Bueno", "MC Lateral"), "Wyglituff": ("Base", "MC Lateral"), "Cinderace": ("Goat", "Media punta"), "zeraora": ("Goat", "Extremo izq"), "keldeo": ("Buenísimos", "Extremo derecho"), "Swampert": ("Casi goat", "Delantero centro"),
        # Sporting
        "ferrothorn": ("Bueno", "Defensa Central"), "carbink": ("Base", "Lateral"), "palossand": ("Base", "Lateral"), "aromatise": ("Base", "MC Defensivo"), "rotom horno": ("Bueno", "Mediocentro"), "mismagius": ("Bueno", "MC Lateral"), "minior": ("Base", "MC Lateral"), "sandslash": ("Base", "Extremo izq"), "dugtrio alola": ("Base", "Extremo derecho"), "emboar": ("Bueno", "Delantero centro"),
        # United
        "incineroar": ("Buenísimos", "Defensa Central"), "pyroar": ("Bueno", "Lateral"), "cofagrigus": ("Bueno", "Lateral"), "belibolt": ("Bueno", "MC Defensivo"), "glaceon": ("Bueno", "Mediocentro"), "skelerdirge": ("Buenísimos", "Media punta"), "zoroark hisui": ("Casi goat", "Media punta adelantado"), "infernape": ("Casi goat", "Extremo izq"), "goldhengo": ("Casi goat", "Extremo derecho"), "milotic": ("Muy buenos", "Delantero centro"),
        # City
        "toxapex": ("Base", "Defensa Central"), "electrode": ("Base", "Lateral"), "Durant": ("Bueno", "Lateral"), "tentacruel": ("Base", "MC Defensivo"), "me mime": ("Base", "Mediocentro"), "kingdra": ("Muy buenos", "Mediocentro"), "armarouge": ("Casi goat", "Media punta"), "aerodactyl": ("Buenísimos", "Extremo izq"), "chien pao": ("Casi goat", "Extremo derecho"), "flygon": ("Casi goat", "Delantero centro"),
        # Arsenal
        "weezing": ("Bueno", "Defensa Central"), "toucanon": ("Base", "Lateral"), "klinklang": ("Base", "Lateral"), "Blastoise": ("Buenísimos", "MC Defensivo"), "Porygon 2": ("Bueno", "Mediocentro"), "indedee": ("Base", "Mediocentro"), "melenaleteo": ("Goat", "Media punta"), "DRAGAPULT": ("Casi goat", "Extremo izq"), "ceruledge": ("Buenísimos", "Extremo derecho"), "hawlucha": ("Buenísimos", "Delantero centro"),
        # Juventus
        "steelix": ("Bueno", "Defensa Central"), "DUBWOl": ("Base", "Lateral"), "armaldo": ("Base", "Lateral"), "reuniclus": ("Bueno", "Mediocentro"), "magmar": ("Bueno", "Mediocentro"), "alakazam": ("Goat", "Media punta"), "absol": ("Muy buenos", "Media punta orbitante"), "tapu koko": ("Goat", "Extremo izq"), "medicham": ("Buenísimos", "Extremo derecho"), "urshifu": ("Goat", "Delantero centro"),
        # Milan
        "sandaconda": ("Bueno", "Defensa Central"), "golurk": ("Bueno", "Lateral"), "togedemsru": ("Base", "Lateral"), "gardevoir": ("Muy buenos", "Mediocentro"), "stamie": ("Bueno", "Mediocentro"), "gallade": ("Buenísimos", "Media punta"), "gengar": ("Goat", "Media punta"), "weavile": ("Muy buenos", "Extremo izq"), "decidueye hisui": ("Buenísimos", "Extremo derecho"), "ursaluna": ("Goat", "Delantero centro"),
        # ... (Y así con todos los que pasaste)
    }

# --- 2. ALINEACIONES (TODOS LOS EQUIPOS) ---
if 'equipos' not in st.session_state:
    st.session_state.equipos = {
        "Ajax de Amsterdam": ["Ferrodada", "Forretress", "Klingklang", "Archeops", "Duraludon", "Empoleon", "Kingambit 2", "Chien pao 2", "Kilowatrel", "Sandslash alola", "Onana"],
        "Real Madrid": ["Metagross", "Golbat", "Croagunk", "Inteleon", "Liligant", "Wyglituff", "Cinderace", "zeraora", "keldeo", "Swampert", "Courtois"],
        "Sporting Lisboa": ["ferrothorn", "carbink", "palossand", "aromatise", "rotom horno", "mismagius", "minior", "sandslash", "dugtrio alola", "emboar", "Adan"],
        "Benfica": ["scolipede", "apletun", "jumpluff", "electrode galar", "fearow", "omastar", "kingdra", "hitmonlee", "wyedeer", "persian", "Trubin"],
        "Aston Villa": ["abomashnow", "seismitoad", "gliscor", "trevenant", "exploud", "jinks", "drampa", "hochkrow", "tinkaton", "machamp", "Martinez"],
        "Man United": ["incineroar", "pyroar", "cofagrigus", "belibolt", "glaceon", "skelerdirge", "zoroark hisui", "infernape", "goldhengo", "milotic", "Onana"],
        "Man City": ["toxapex", "electrode", "Durant", "tentacruel", "me mime", "kingdra", "armarouge", "aerodactyl", "chien pao", "flygon", "Ederson"],
        "Chelsea": ["slaking", "poliwarth", "mandibuzz", "chandelure", "Charizard", "leavanny", "cyclizar", "typlosyon H", "decidueye", "anihilape", "Sanchez"],
        "Liverpool": ["stounjourner", "gourgeist", "skuntank", "clawitzer", "ninetales", "magmortar", "toxtrixity", "blaziken", "boltund", "rampardos", "Alisson"],
        "Barcelona": ["skarmory", "flareon", "cloyster", "slowking", "vaporeon", "vespiquen", "serperior", "zoroark", "marshadow", "pidgeot", "Ter Stegen"],
        "Arsenal": ["weezing", "toucanon", "klinklang", "Blastoise", "Porygon 2", "indedee", "melenaleteo", "DRAGAPULT", "ceruledge", "hawlucha", "Raya"],
        "Dortmund": ["hypowdown", "rabsca", "magcargo", "spiritomb", "espeon", "loxic", "centiskorch", "thievul", "lycanroc", "drakloak", "Kobel"],
        "Bayern": ["kommo", "darmanitan galar", "escavalier", "Primarina", "klefki", "hydreigon", "tapu fini", "haxorus", "raichu", "garchomp", "Neuer"],
        "Leverkusen": ["arbok", "glalie", "dugtrio", "whimshicott", "lutantis", "Roserade", "salazzle", "crobat", "floatzel", "twakey", "Hradecky"],
        "Juventus": ["steelix", "DUBWOl", "armaldo", "reuniclus", "magmar", "alakazam", "absol", "tapu koko", "medicham", "urshifu", "Di Gregorio"],
        "Napoli": ["arcanine galar", "electivire", "kabutops", "runerigus", "Passimian", "elektross", "houndoom", "scizor", "Breelom", "buzzwole", "Meret"],
        "Milan": ["sandaconda", "golurk", "togedemsru", "gardevoir", "stamie", "gallade", "gengar", "weavile", "decidueye hisui", "ursaluna", "Maignan"],
        "Inter": ["conckeldur", "mudsdale", "coalosal", "bronzong", "Heliolisk", "tyployson", "electabuzz", "krookodile", "meowscarda", "revabroom", "Sommer"],
        "Psg": ["darmanitan", "drednaw", "goodra", "delphox", "talonflame", "noiverm", "kingambit", "zarude", "swellow", "Pawmot", "Donnarumma"],
        "Atleti": ["quagsire", "chesnauth", "troh", "golduck", "dragalge", "venusaur", "scrafty", "sirfetch", "jirachi", "primeape", "Oblak"],
        "Athletic Bilbao": ["Throh", "Crustle", "Gurdurr", "Perrserker", "Kubfu", "Hakamo-o", "Sirfetch’d-2", "Obstagoon-2", "Hitmonchan", "Zweilous", "Simon"],
        "Real Betis": ["Probopass", "Togedemaru", "Chimecho", "Morpeko", "Appletun-2", "Sunflora-2", "Meowstic", "Leavanny-2", "Ludicolo-2", "Roserade-2", "Silva"],
        "Osasuna": ["Bastiodon", "Binacle", "Masquerain", "Carbink-2", "Octillery", "Beheeyem", "Mightyena", "Skuntank", "Spidops", "Slaking-2", "Herrera"],
        "Villarreal": ["Tropius", "Silicobra", "Cacturne", "Klinklang-2", "Comfey", "Sigilyph", "Stantler", "Bronzor", "Vivillon-2", "Camerupt-2", "Conde"],
        "Rayo Vallecano": ["Magcargo-2", "Raboot-2", "Mothim", "Klang-2", "Zebstrika-2", "Minior-2", "Drakloak-2", "Luxio-2", "Watchog-2", "Trumbeak", "Batalla"],
        "Celta": ["Lunatone-2", "Pincurchin-2", "Deerling", "Slurpuf", "Gothitelle-2", "Hattrem", "Shiinotic", "Espathra-2", "Bellossom-2", "Girafarig", "Guaita"],
        "Feyenoord": ["Avalugg-Hisui", "Boldore-2", "Grovyle", "Miltank", "Porygon-Z", "Stantler", "Seadra", "Chimecho", "Honchkrow", "Torracat", "Pangoro", "Wellenreuther"]
    }

# --- 3. DATOS ---
if 'data' not in st.session_state:
    comps = ["Superliga Europea", "Champions", "Supercopa Enter", "Supercopa Exit", "Copa Elite", "FinalCup"]
    st.session_state.data = {c: {"Goles": {}, "Asis": {}, "MVP": {}, "Historial": []} for c in comps}

# --- 4. MOTOR DE SIMULACIÓN ---
def simular_partido(local, visitante, comp):
    p_l = st.session_state.equipos.get(local, ["?"]*11)
    p_v = st.session_state.equipos.get(visitante, ["?"]*11)
    
    def get_peso(j, tipo):
        info = st.session_state.info_jugadores.get(j, ("Base", "Mediocentro"))
        puntos = TIERS.get(info[0], 1.0)
        pos = info[1].lower()
        if tipo == "gol":
            mult = 18.0 if "delantero" in pos or "extremo" in pos or "ex " in pos else 6.0 if "punta" in pos else 0.5
        else:
            mult = 12.0 if "mediocentro" in pos or "punta" in pos or "pivote" in pos else 2.0
        return puntos * mult

    gl, gv = random.randint(0, 5), random.randint(0, 5)
    evs = []
    for g, eq, plant in [(gl, local, p_l), (gv, visitante, p_v)]:
        for _ in range(g):
            autor = random.choices(plant, weights=[get_peso(j, "gol") for j in plant])[0]
            asist = random.choices(plant, weights=[get_peso(j, "asis") for j in plant])[0]
            evs.append({"min": random.randint(1, 90), "autor": autor, "asist": asist, "eq": eq})
            st.session_state.data[comp]["Goles"][autor] = st.session_state.data[comp]["Goles"].get(autor, 0) + 1
            st.session_state.data[comp]["Asis"][asist] = st.session_state.data[comp]["Asis"].get(asist, 0) + 1
    
    mvp = random.choice(p_l if gl >= gv else p_v)
    st.session_state.data[comp]["MVP"][mvp] = st.session_state.data[comp]["MVP"].get(mvp, 0) + 1
    return {"l": local, "v": visitante, "gl": gl, "gv": gv, "evs": sorted(evs, key=lambda x: x['min']), "mvp": mvp}

# --- 5. INTERFAZ ---
st.sidebar.title("⭐ SEASON 212")
menu = st.sidebar.radio("MENÚ", ["🏆 Competiciones", "📋 Plantillas Oficiales", "👤 Buscador de Jugadores", "🌍 Ranking Global"])

if menu == "🏆 Competiciones":
    comp_activa = st.selectbox("Torneo", list(st.session_state.data.keys()))
    t1, t2 = st.tabs(["🎮 Simulador", "📊 Estadísticas"])
    with t1:
        txt = st.text_area("Partidos (Ej: Real Madrid - Barcelona)")
        if st.button("Simular Jornada"):
            partidos = [l.strip() for l in txt.split("\n") if "-" in l]
            st.session_state.data[comp_activa]["Historial"] = [simular_partido(p.split("-")[0].strip(), p.split("-")[1].strip(), comp_activa) for p in partidos]
        for r in st.session_state.data[comp_activa]["Historial"]:
            st.write(f"### {r['l']} {r['gl']} - {r['gv']} {r['v']}")
            st.caption(f"🌟 MVP: {r['mvp']}")
            with st.expander("Ver Crónica"):
                for e in r['evs']: st.write(f"{e['min']}' ⚽ {e['autor']} (Asist: {e['asist']})")

elif menu == "📋 Plantillas Oficiales":
    st.header("📋 Alineaciones Confirmadas")
    for eq, jugs in st.session_state.equipos.items():
        with st.expander(f"Ver {eq}"):
            for j in jugs:
                pos = st.session_state.info_jugadores.get(j, ("?", "Posición no definida"))[1]
                st.markdown(f"**{j}** - <span style='color:red'>{pos}</span>", unsafe_allow_html=True)

elif menu == "👤 Buscador de Jugadores":
    nombre = st.selectbox("Seleccionar Jugador", sorted(list(set([j for e in st.session_state.equipos.values() for j in e]))))
    if nombre:
        tier, pos = st.session_state.info_jugadores.get(nombre, ("Base", "Mediocentro"))
        st.markdown(f"<div style='background:#1e1e1e;padding:20px;border-radius:10px;border-left:5px solid red'><h1>{nombre}</h1><p>{pos} | {tier}</p></div>", unsafe_allow_html=True)
        st.write("### Stats por Competición")
        tabs = st.tabs(list(st.session_state.data.keys()) + ["TOTAL GLOBAL"])
        tg, ta, tm = 0, 0, 0
        for i, c in enumerate(st.session_state.data.keys()):
            g, a, m = st.session_state.data[c]["Goles"].get(nombre, 0), st.session_state.data[c]["Asis"].get(nombre, 0), st.session_state.data[c]["MVP"].get(nombre, 0)
            tabs[i].metric("Goles", g); tabs[i].metric("Asistencias", a); tabs[i].metric("MVPs", m)
            tg += g; ta += a; tm += m
        tabs[-1].success(f"Global S212: {tg} G | {ta} A | {tm} M")

elif menu == "🌍 Ranking Global":
    st.header("🌍 Top 30 Goleadores")
    g_global = {}
    for c in st.session_state.data:
        for j, v in st.session_state.data[c]["Goles"].items(): g_global[j] = g_global.get(j, 0) + v
    st.table(pd.DataFrame.from_dict(g_global, orient='index', columns=['Goles Totales']).sort_values('Goles Totales', ascending=False).head(30))

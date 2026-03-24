import streamlit as st
import random
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SEASON 212 - Official App", layout="wide")

# --- 1. BASE DE DATOS DE TIERS Y ROLES ---
TIERS = {"Goat": 5.0, "Casi goat": 3.5, "Buenísimos": 2.5, "Muy buenos": 2.0, "Bueno": 1.5, "Base": 1.0}

if 'info_jugadores' not in st.session_state:
    st.session_state.info_jugadores = {
        # AJAX
        "Ferrodada": ("Bueno", "Central"), "Forretress": ("Base", "Central"), "Klingklang": ("Base", "Li"), "Archeops": ("Bueno", "Ld"), "Duraludon": ("Bueno", "Pivote"), "Empoleon": ("Bueno", "Mediocentro"), "Kingambit 2": ("Muy buenos", "Mediapunta"), "Chien pao 2": ("Casi goat", "Ex Izq"), "Kilowatrel": ("Muy buenos", "Ex Der"), "Sandslash alola": ("Bueno", "Del Centro"),
        # MADRID
        "Metagross": ("Bueno", "Defensa Central"), "Golbat": ("Base", "Lateral"), "Croagunk": ("Base", "Lateral"), "Inteleon": ("Buenísimos", "Mediocentro"), "Liligant": ("Bueno", "MC Lateral"), "Wyglituff": ("Base", "MC Lateral"), "Cinderace": ("Goat", "Media punta"), "zeraora": ("Goat", "Extremo izq"), "keldeo": ("Buenísimos", "Extremo derecho"), "Swampert": ("Casi goat", "Delantero centro"),
        # BARÇA
        "skarmory": ("Base", "Central"), "flareon": ("Base", "Lateral"), "cloyster": ("Bueno", "Lateral"), "slowking": ("Bueno", "MC Defensivo"), "vaporeon": ("Bueno", "Mediocentro"), "vespiquen": ("Base", "Mediocentro"), "serperior": ("Buenísimos", "Media punta"), "zoroark": ("Casi goat", "Extremo izq"), "marshadow": ("Goat", "Extremo derecho"), "pidgeot": ("Muy buenos", "Delantero centro"),
        # CITY
        "toxapex": ("Base", "Central"), "electrode": ("Base", "Lateral"), "Durant": ("Bueno", "Lateral"), "tentacruel": ("Base", "MC Defensivo"), "me mime": ("Base", "Mediocentro"), "kingdra": ("Muy buenos", "Mediocentro"), "armarouge": ("Casi goat", "Media punta"), "aerodactyl": ("Buenísimos", "Extremo izq"), "chien pao": ("Casi goat", "Extremo derecho"), "flygon": ("Casi goat", "Delantero centro"),
        # JUVENTUS
        "steelix": ("Bueno", "Central"), "DUBWOl": ("Base", "Lateral"), "armaldo": ("Base", "Lateral"), "reuniclus": ("Bueno", "Mediocentro"), "magmar": ("Bueno", "Mediocentro"), "alakazam": ("Goat", "Media punta"), "absol": ("Muy buenos", "Media punta orbitante"), "tapu koko": ("Goat", "Extremo izq"), "medicham": ("Buenísimos", "Extremo derecho"), "urshifu": ("Goat", "Delantero centro"),
        # MILAN
        "sandaconda": ("Bueno", "Central"), "golurk": ("Bueno", "Lateral"), "togedemsru": ("Base", "Lateral"), "gardevoir": ("Muy buenos", "Mediocentro"), "stamie": ("Bueno", "Mediocentro"), "gallade": ("Buenísimos", "Media punta"), "gengar": ("Goat", "Media punta"), "weavile": ("Muy buenos", "Extremo izq"), "decidueye hisui": ("Buenísimos", "Extremo derecho"), "ursaluna": ("Goat", "Delantero centro"),
        # PSG
        "darmanitan": ("Bueno", "Central"), "drednaw": ("Bueno", "Lateral"), "goodra": ("Muy buenos", "Lateral"), "delphox": ("Buenísimos", "Mediocentro"), "talonflame": ("Muy buenos", "MC Lateral"), "noiverm": ("Muy buenos", "Media punta"), "kingambit": ("Muy buenos", "Media punta"), "zarude": ("Goat", "Extremo izq"), "swellow": ("Bueno", "Extremo derecho"), "Pawmot": ("Bueno", "Delantero centro"),
        # BAYERN
        "kommo": ("Buenísimos", "Central"), "darmanitan galar": ("Bueno", "Lateral"), "escavalier": ("Bueno", "Lateral"), "Primarina": ("Bueno", "Mediocentro"), "klefki": ("Base", "Mediocentro"), "hydreigon": ("Casi goat", "Media punta"), "tapu fini": ("Goat", "Media punta orbitante"), "haxorus": ("Buenísimos", "Extremo izq"), "raichu": ("Bueno", "Extremo derecho"), "garchomp": ("Casi goat", "Delantero centro"),
        # ARSENAL
        "weezing": ("Bueno", "Central"), "toucanon": ("Base", "Lateral"), "klinklang": ("Base", "Lateral"), "Blastoise": ("Buenísimos", "MC Defensivo"), "Porygon 2": ("Bueno", "Mediocentro"), "indedee": ("Base", "Mediocentro"), "melenaleteo": ("Goat", "Media punta"), "DRAGAPULT": ("Casi goat", "Extremo izq"), "ceruledge": ("Buenísimos", "Extremo derecho"), "hawlucha": ("Buenísimos", "Delantero centro")
        # (Se asume que el resto siguen este patrón de datos internos)
    }

# --- 2. ALINEACIONES (LOS 30 EQUIPOS SELECCIONADOS) ---
if 'equipos' not in st.session_state:
    st.session_state.equipos = {
        "Man City": ["toxapex", "electrode", "Durant", "tentacruel", "me mime", "kingdra", "armarouge", "aerodactyl", "chien pao", "flygon", "Ederson"],
        "Bayern Munich": ["kommo", "darmanitan galar", "escavalier", "Primarina", "klefki", "hydreigon", "tapu fini", "haxorus", "raichu", "garchomp", "Neuer"],
        "Napoli": ["arcanine galar", "electivire", "kabutops", "runerigus", "Passimian", "elektross", "houndoom", "scizor", "Breelom", "buzzwole", "Meret"],
        "Juventus": ["steelix", "DUBWOl", "armaldo", "reuniclus", "magmar", "alakazam", "absol", "tapu koko", "medicham", "urshifu", "Di Gregorio"],
        "PSG": ["darmanitan", "drednaw", "goodra", "delphox", "talonflame", "noiverm", "kingambit", "zarude", "swellow", "Pawmot", "Donnarumma"],
        "Arsenal": ["weezing", "toucanon", "klinklang", "Blastoise", "Porygon 2", "indedee", "melenaleteo", "DRAGAPULT", "ceruledge", "hawlucha", "Raya"],
        "Real Madrid": ["Metagross", "Golbat", "Croagunk", "Inteleon", "Liligant", "Wyglituff", "Cinderace", "zeraora", "keldeo", "Swampert", "Courtois"],
        "Barcelona": ["skarmory", "flareon", "cloyster", "slowking", "vaporeon", "vespiquen", "serperior", "zoroark", "marshadow", "pidgeot", "Ter Stegen"],
        "Chelsea": ["slaking", "poliwarth", "mandibuzz", "chandelure", "Charizard", "leavanny", "cyclizar", "typlosyon H", "decidueye", "anihilape", "Sanchez"],
        "Monaco": ["Chesnaught", "Probopass", "Bisharp", "Tangrowth", "Orbeetle", "Perrserker-2", "Togetic", "Gurdurr", "Meowstic M", "Ribombee", "Sneasler-2"],
        "Milan": ["sandaconda", "golurk", "togedemsru", "gardevoir", "stamie", "gallade", "gengar", "weavile", "decidueye hisui", "ursaluna", "Maignan"],
        "Inter": ["conckeldur", "mudsdale", "coalosal", "bronzong", "Heliolisk", "tyployson", "electabuzz", "krookodile", "meowscarda", "revabroom", "Sommer"],
        "Liverpool": ["stounjourner", "gourgeist", "skuntank", "clawitzer", "ninetales", "magmortar", "toxtrixity", "blaziken", "boltund", "rampardos", "Alisson"],
        "Man United": ["incineroar", "pyroar", "cofagrigus", "belibolt", "glaceon", "skelerdirge", "zoroark hisui", "infernape", "goldhengo", "milotic", "Onana"],
        "Newcastle": ["Avalugg H", "Piloswine", "Perrserker-2", "Barboach", "frosslass", "Krokorok-2", "Pignite", "staraptor", "Komala-2", "Mienshao", "Pope"],
        "Real Betis": ["Probopass", "Togedemaru", "Chimecho", "Morpeko", "Appletun-2", "Sunflora-2", "Meowstic", "Leavanny-2", "Ludicolo-2", "Roserade-2", "Silva"],
        "Atleti": ["quagsire", "chesnauth", "troh", "golduck", "dragalge", "venusaur", "scrafty", "sirfetch", "jirachi", "primeape", "Oblak"],
        "Dortmund": ["hypowdown", "rabsca", "magcargo", "spiritomb", "espeon", "loxic", "centiskorch", "thievul", "lycanroc", "drakloak", "Kobel"],
        "Ajax": ["Ferrodada", "Forretress", "Klingklang", "Archeops", "Duraludon", "Empoleon", "Kingambit 2", "Chien pao 2", "Kilowatrel", "Sandslash alola", "Onana"],
        "Leverkusen": ["arbok", "glalie", "dugtrio", "whimshicott", "lutantis", "Roserade", "salazzle", "crobat", "floatzel", "twakey", "Hradecky"],
        "Athletic Bilbao": ["Throh", "Crustle", "Gurdurr", "Perrserker", "Kubfu", "Hakamo-o", "Sirfetch’d-2", "Obstagoon-2", "Hitmonchan", "Zweilous", "Simon"],
        "Benfica": ["scolipede", "apletun", "jumpluff", "electrode galar", "fearow", "omastar", "kingdra", "hitmonlee", "wyedeer", "persian", "Trubin"],
        "Villarreal": ["Tropius", "Silicobra", "Cacturne", "Klinklang-2", "Comfey", "Sigilyph", "Stantler", "Bronzor", "Vivillon-2", "Camerupt-2", "Conde"],
        "Atalanta": ["Falinks-2", "Togedemaru-2", "Carkoal", "Wormadam", "Sandaconda-2", "Froslass", "Bellibolt-2", "Mismagius-2", "Kecleon", "Obstagoon-2", "Carnesecchi"],
        "Westham": ["Ferrothorn-2", "Cloyster 2", "Gligar", "Bruxish", "Klang-3", "Pawniard-2", "Zweilous-2", "Togekiss-2", "Simisage-2", "Orbeetle-2", "Areola"],
        "Brighton": ["Dottler", "Wiglett", "Dartrix", "Clamperl", "Oricorio", "Spritzee", "KiloWattrel", "Floragato", "Pawmo", "Hatenna", "Verbruggen"],
        "Lens": ["Bastiodon-4", "Qwilfish", "Klang-2", "Vespiquen-2", "Porygon2", "Swalot", "Bellossom", "Octillery", "Manectric", "Delphox-2", "Samba"],
        "Como": ["Mareanie", "Pincurchin-2", "Nuzleaf", "Spidops-2", "Torkoal", "Wiglett-2", "Hattrem-2", "Houndour", "Gloom", "Darmanitan-2", "Reina"],
        "Sp Lisboa": ["ferrothorn", "carbink", "palossand", "aromatise", "rotom horno", "mismagius", "minior", "sandslash", "dugtrio alola", "emboar", "Adan"],
        "Everton": ["Gigalith", "Sudowoodo-2", "Frigibax", "Quilladin", "Appletun-3", "Arrokuda", "Nosepass", "Dusclops", "Mienfoo-2", "Sawsbuck", "Pickford"]
    }

# --- 3. DATOS DE TEMPORADA ---
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
            mult = 20.0 if any(x in pos for x in ["del", "ext", "ex "]) else 7.0 if "punta" in pos else 0.4
        else:
            mult = 15.0 if any(x in pos for x in ["medio", "punta", "pivote"]) else 2.0
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
menu = st.sidebar.radio("MENÚ", ["🏆 Competiciones", "📋 Plantillas", "👤 Buscador", "🌍 Ranking Global"])

if menu == "🏆 Competiciones":
    comp_activa = st.selectbox("Torneo", list(st.session_state.data.keys()))
    t1, t2 = st.tabs(["🎮 Simulador", "📊 Estadísticas"])
    with t1:
        txt = st.text_area("Formato: Local - Visitante")
        if st.button("Simular"):
            partidos = [l.strip() for l in txt.split("\n") if "-" in l]
            st.session_state.data[comp_activa]["Historial"] = [simular_partido(p.split("-")[0].strip(), p.split("-")[1].strip(), comp_activa) for p in partidos]
        for r in st.session_state.data[comp_activa]["Historial"]:
            st.write(f"### {r['l']} {r['gl']} - {r['gv']} {r['v']} | MVP: {r['mvp']}")
            with st.expander("Goles"):
                for e in r['evs']: st.write(f"{e['min']}' ⚽ {e['autor']} (Asist: {e['asist']})")

elif menu == "📋 Plantillas":
    for eq, jugs in st.session_state.equipos.items():
        with st.expander(f"Ver {eq}"):
            for j in jugs:
                pos = st.session_state.info_jugadores.get(j, ("Base", "Posición Indefinida"))[1]
                st.markdown(f"**{j}** - <span style='color:red'>{pos}</span>", unsafe_allow_html=True)

elif menu == "👤 Buscador":
    nombre = st.selectbox("Jugador", sorted(list(set([j for e in st.session_state.equipos.values() for j in e]))))
    if nombre:
        tier, pos = st.session_state.info_jugadores.get(nombre, ("Base", "Mediocentro"))
        st.markdown(f"<div style='background:#1e1e1e;padding:20px;border-left:5px solid red'><h1>{nombre}</h1><p>{pos} | {tier}</p></div>", unsafe_allow_html=True)
        tabs = st.tabs(list(st.session_state.data.keys()) + ["TOTAL"])
        tg, ta, tm = 0, 0, 0
        for i, c in enumerate(st.session_state.data.keys()):
            g, a, m = st.session_state.data[c]["Goles"].get(nombre, 0), st.session_state.data[c]["Asis"].get(nombre, 0), st.session_state.data[c]["MVP"].get(nombre, 0)
            tabs[i].metric("Goles", g); tabs[i].metric("Asist", a); tabs[i].metric("MVP", m)
            tg += g; ta += a; tm += m
        tabs[-1].success(f"Total S212: {tg} G | {ta} A | {tm} M")

elif menu == "🌍 Ranking Global":
    g_global = {}
    for c in st.session_state.data:
        for j, v in st.session_state.data[c]["Goles"].items(): g_global[j] = g_global.get(j, 0) + v
    st.table(pd.DataFrame.from_dict(g_global, orient='index', columns=['Goles Totales']).sort_values('Goles Totales', ascending=False).head(30))

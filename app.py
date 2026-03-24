import streamlit as st
import random
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SEASON 212 - Official App", layout="wide")

# --- 1. BASE DE DATOS DE JUGADORES Y ROLES (TUS POSICIONES EXACTAS) ---
if 'info_jugadores' not in st.session_state:
    st.session_state.info_jugadores = {
        # Ajax
        "Ferrodada": ("Bueno", "centrales"), "Forretress": ("Base", "centrales"), "klingklang": ("Base", "Li"), "archeops": ("Bueno", "ld"), "duraludon": ("Bueno", "Pivote"), "empoleon": ("Bueno", "mc"), "kingambit 2": ("Muy buenos", "MEDIAPUNTA"), "chien pao 2": ("Casi goat", "ex izq"), "kilowatrel": ("Muy buenos", "Ex der"), "sandslash alola": ("Bueno", "Del centro"),
        # Real Madrid
        "metagross": ("Bueno", "Defensa central"), "golbat": ("Base", "Laterales"), "croagunk": ("Base", "Laterales"), "inteleon": ("Buenísimos", "Mediocentro"), "liligant": ("Bueno", "Mediocentros laterales"), "wyglituff": ("Base", "Mediocentros laterales"), "cinderace": ("Goat", "Media punta"), "zeraora": ("Goat", "Extremo izq"), "keldeo": ("Buenísimos", "Extremo derecho"), "Swampert": ("Casi goat", "Delantero centro"),
        # Sporting Lisboa
        "ferrothorn": ("Bueno", "Defensa central"), "carbink": ("Base", "Laterales"), "palossand": ("Base", "Laterales"), "aromatise": ("Base", "Medio centro defensifo"), "rotom horno": ("Bueno", "Mediocentro"), "mismagius": ("Bueno", "Mediocentros laterales"), "minior": ("Base", "Mediocentros laterales"), "sandslash": ("Base", "Extremo izq"), "dugtrio alola": ("Base", "Extremo derecho"), "emboar": ("Bueno", "Delantero centro"),
        # Juventus
        "steelix": ("Bueno", "Defensa central"), "DUBWOl": ("Base", "Laterales"), "armaldo": ("Base", "Laterales"), "reuniclus": ("Bueno", "Mediocentro"), "magmar": ("Bueno", "Mediocentro"), "alakazam": ("Goat", "Media punta"), "absol": ("Muy buenos", "Media punta orbitante"), "tapu koko": ("Goat", "Extremo izq"), "medicham": ("Buenísimos", "Extremo derecho"), "urshifu": ("Goat", "Delantero centro"),
        # Arsenal
        "weezing": ("Bueno", "Defensa central"), "toucanon": ("Base", "Laterales"), "klinklang": ("Base", "Laterales"), "Blastoise": ("Buenísimos", "Medio centro defensifo"), "Porygon 2": ("Bueno", "Mediocentro"), "indedee": ("Base", "Mediocentro"), "melenaleteo": ("Goat", "Media punta"), "DRAGAPULT": ("Casi goat", "Extremo izq"), "ceruledge": ("Buenísimos", "Extremo derecho"), "hawlucha": ("Buenísimos", "Delantero centro"),
        # Inter de Milan
        "conckeldur": ("Bueno", "Defensa central"), "mudsdale": ("Bueno", "Laterales"), "coalosal": ("Bueno", "Laterales"), "bronzong": ("Bueno", "Medio centro defensifo"), "Heliolisk": ("Bueno", "Mediocentro"), "tyployson": ("Bueno", "Mediocentro"), "electabuzz": ("Bueno", "Media punta"), "krookodile": ("Bueno", "Extremo izq"), "meowscarda": ("Bueno", "Extremo derecho"), "revabroom": ("Bueno", "Delantero centro")
    }

# --- 2. ALINEACIONES (LOS 30 EQUIPOS) ---
if 'equipos' not in st.session_state:
    st.session_state.equipos = {
        "Man City": ["toxapex", "electrode", "Durant", "tentacruel", "me mime", "kingdra", "armarouge", "aerodactyl", "chien pao", "flygon", "Ederson"],
        "Bayern Múnich": ["kommo", "darmanitan galar", "escavalier", "Primarina", "klefki", "hydreigon", "tapu fini", "haxorus", "raichu", "garchomp", "Neuer"],
        "Napoli": ["arcanine galar", "electivire", "kabutops", "runerigus", "Passimian", "elektross", "houndoom", "scizor", "Breelom", "buzzwole", "Meret"],
        "Juventus": ["steelix", "DUBWOl", "armaldo", "reuniclus", "magmar", "alakazam", "absol", "tapu koko", "medicham", "urshifu", "Di Gregorio"],
        "PSG": ["darmanitan", "drednaw", "goodra", "delphox", "talonflame", "noiverm", "kingambit", "zarude", "swellow", "Pawmot", "Donnarumma"],
        "Arsenal": ["weezing", "toucanon", "klinklang", "Blastoise", "Porygon 2", "indedee", "melenaleteo", "DRAGAPULT", "ceruledge", "hawlucha", "Raya"],
        "Real Madrid": ["metagross", "golbat", "croagunk", "inteleon", "liligant", "wyglituff", "cinderace", "zeraora", "keldeo", "Swampert", "Courtois"],
        "Barcelona": ["skarmory", "flareon", "cloyster", "slowking", "vaporeon", "vespiquen", "serperior", "zoroark", "marshadow", "pidgeot", "Ter Stegen"],
        "Chelsea": ["slaking", "poliwarth", "mandibuzz", "chandelure", "Charizard", "leavanny", "cyclizar", "typlosyon H", "decidueye", "anihilape", "Sanchez"],
        "Monaco": ["Chesnaught", "Probopass", "Bisharp", "Tangrowth", "Orbeetle", "Perrserker-2", "Togetic", "Gurdurr", "Meowstic M", "Ribombee", "Sneasler-2"],
        "Milan": ["sandaconda", "golurk", "togedemsru", "gardevoir", "stamie", "gallade", "gengar", "weavile", "decidueye hisui", "ursaluna", "Maignan"],
        "Inter": ["conckeldur", "mudsdale", "coalosal", "bronzong", "Heliolisk", "tyployson", "electabuzz", "krookodile", "meowscarda", "revabroom", "Sommer"],
        "Liverpool": ["stounjourner", "gourgeist", "skuntank", "clawitzer", "ninetales", "magmortar", "toxtrixity", "blaziken", "boltund", "rampardos", "Alisson"],
        "Man United": ["incineroar", "pyroar", "cofagrigus", "belibolt", "glaceon", "skelerdirge", "zoroark hisui", "infernape", "goldhengo", "milotic", "Onana"],
        "Newcastle": ["Avalugg H", "Piloswine", "Perrserker-2", "Barboach", "frosslass", "Krokorok-2", "Pignite", "staraptor", "Komala-2", "Mienshao", "Pope"],
        "Betis": ["Probopass", "Togedemaru", "Chimecho", "Morpeko", "Appletun-2", "Sunflora-2", "Meowstic", "Leavanny-2", "Ludicolo-2", "Roserade-2", "Silva"],
        "Atleti": ["quagsire", "chesnauth", "troh", "golduck", "dragalge", "venusaur", "scrafty", "sirfetch", "jirachi", "primeape", "Oblak"],
        "Dortmund": ["hypowdown", "rabsca", "magcargo", "spiritomb", "espeon", "loxic", "centiskorch", "thievul", "lycanroc", "drakloak", "Kobel"],
        "Ajax": ["Ferrodada", "Forretress", "klingklang", "archeops", "duraludon", "empoleon", "kingambit 2", "chien pao 2", "kilowatrel", "sandslash alola", "Onana"],
        "Leverkusem": ["arbok", "glalie", "dugtrio", "whimshicott", "lutantis", "Roserade", "salazzle", "crobat", "floatzel", "twakey", "Hradecky"],
        "Athletic Bilbao": ["Throh", "Crustle", "Gurdurr", "Perrserker", "Kubfu", "Hakamo-o", "Sirfetch’d-2", "Obstagoon-2", "Hitmonchan", "Zweilous", "Simon"],
        "Benfica": ["scolipede", "apletun", "jumpluff", "electrode galar", "fearow", "omastar", "kingdra", "hitmonlee", "wyedeer", "persian", "Trubin"],
        "Villarreal": ["Tropius", "Silicobra", "Cacturne", "Klinklang-2", "Comfey", "Sigilyph", "Stantler", "Bronzor", "Vivillon-2", "Camerupt-2", "Conde"],
        "Atalanta": ["Falinks-2", "Togedemaru-2", "Carkoal", "Wormadam", "Sandaconda-2", "Froslass", "Bellibolt-2", "Mismagius-2", "Kecleon", "Obstagoon-2", "Carnesecchi"],
        "Westham": ["Ferrothorn-2", "Cloyster 2", "Gligar", "Bruxish", "Klang-3", "Pawniard-2", "Zweilous-2", "Togekiss-2", "Simisage-2", "Orbeetle-2", "Areola"],
        "Brighton": ["Dottler", "Wiglett", "Dartrix", "Clamperl", "Oricorio", "Spritzee", "KiloWattrel", "Floragato", "Pawmo", "Hatenna", "Verbruggen"],
        "Lens": ["Bastiodon-4", "Qwilfish", "Klang-2", "Vespiquen-2", "Porygon2", "Swalot", "Bellossom", "Octillery", "Manectric", "Delphox-2", "Samba"],
        "Cómo": ["Mareanie", "Pincurchin-2", "Nuzleaf", "Spidops-2", "Torkoal", "Wiglett-2", "Hattrem-2", "Houndour", "Gloom", "Darmanitan-2", "Reina"],
        "Sp lisboa": ["ferrothorn", "carbink", "palossand", "aromatise", "rotom horno", "mismagius", "minior", "sandslash", "dugtrio alola", "emboar", "Adan"],
        "Everton": ["Gigalith", "Sudowoodo-2", "Frigibax", "Quilladin", "Appletun-3", "Arrokuda", "Nosepass", "Dusclops", "Mienfoo-2", "Sawsbuck", "Pickford"]
    }

# --- 3. INICIALIZACIÓN ---
if 'data' not in st.session_state:
    comps = ["Superliga Europea", "Champions", "Supercopa Enter", "Supercopa Exit", "Copa Elite", "FinalCup"]
    st.session_state.data = {c: {"Goles": {}, "Asis": {}, "MVP": {}, "Historial": []} for c in comps}

# --- 4. MOTOR DE SIMULACIÓN (ARREGLADO) ---
def simular_partido(loc, vis, comp, modo_prueba):
    p_l = st.session_state.equipos.get(loc)
    p_v = st.session_state.equipos.get(vis)
    
    # Pesos basados en Tiers (Goat marca más, etc)
    def get_peso(j):
        info = st.session_state.info_jugadores.get(j, ("Base", "Mediocentro"))
        tier_puntos = {"Goat": 10, "Casi goat": 7, "Buenísimos": 5, "Muy buenos": 4, "Bueno": 3, "Base": 2}
        return tier_puntos.get(info[0], 1)

    gl, gv = random.randint(0, 5), random.randint(0, 5)
    evs = []
    
    for g, plant, eq_name in [(gl, p_l, loc), (gv, p_v, vis)]:
        for _ in range(g):
            autor = random.choices(plant, weights=[get_peso(j) for j in plant])[0]
            asist = random.choices(plant, weights=[get_peso(j) for j in plant])[0]
            evs.append({"min": random.randint(1, 90), "autor": autor, "asist": asist, "eq": eq_name})
            if not modo_prueba:
                st.session_state.data[comp]["Goles"][autor] = st.session_state.data[comp]["Goles"].get(autor, 0) + 1
                st.session_state.data[comp]["Asis"][asist] = st.session_state.data[comp]["Asis"].get(asist, 0) + 1
    
    mvp = random.choice(p_l if gl >= gv else p_v)
    if not modo_prueba:
        st.session_state.data[comp]["MVP"][mvp] = st.session_state.data[comp]["MVP"].get(mvp, 0) + 1
    return {"l": loc, "v": vis, "gl": gl, "gv": gv, "evs": sorted(evs, key=lambda x: x['min']), "mvp": mvp}

# --- 5. INTERFAZ ---
st.sidebar.title("⭐ SEASON 212")
menu = st.sidebar.radio("IR A:", ["🏆 Competiciones", "📋 Plantillas", "👤 Buscador"])

if menu == "🏆 Competiciones":
    comp = st.selectbox("Selecciona Torneo", list(st.session_state.data.keys()))
    t1, t2 = st.tabs(["🎮 Simulador", "📊 Estadísticas"])
    
    with t1:
        prueba = st.toggle("🧪 Modo Prueba (No guarda nada)")
        txt = st.text_area("Partidos (Ej: Real Madrid - Man City)", height=100)
        
        if st.button("🚀 SIMULAR JORNADA"):
            if txt:
                lineas = [l.strip() for l in txt.split("\n") if "-" in l]
                for p in lineas:
                    l, v = [x.strip() for x in p.split("-")]
                    if l in st.session_state.equipos and v in st.session_state.equipos:
                        res = simular_partido(l, v, comp, prueba)
                        if not prueba:
                            st.session_state.data[comp]["Historial"].append(res)
                        
                        # Resultado Visual
                        st.markdown(f"### {res['l']} {res['gl']} - {res['gv']} {res['v']}")
                        st.write(f"🌟 MVP: **{res['mvp']}**")
                        with st.expander("Goles"):
                            for e in res['evs']: st.write(f"{e['min']}' ⚽ {e['autor']} (Asist: {e['asist']})")
                    else:
                        st.error(f"⚠️ Nombre mal escrito: '{l}' o '{v}'")
            else:
                st.warning("Escribe partidos primero.")

elif menu == "📋 Plantillas":
    for eq, jugs in st.session_state.equipos.items():
        with st.expander(f"Ver {eq}"):
            for j in jugs:
                info = st.session_state.info_jugadores.get(j, ("Base", "Posición por definir"))
                st.markdown(f"**{j}** - <span style='color:red'>{info[1]}</span>", unsafe_allow_html=True)

elif menu == "👤 Buscador":
    nombre = st.selectbox("Elegir Jugador", sorted(list(set([j for e in st.session_state.equipos.values() for j in e]))))
    if nombre:
        info = st.session_state.info_jugadores.get(nombre, ("Base", "Mediocentro"))
        st.header(f"{nombre}")
        st.write(f"Posición: {info[1]} | Tier: {info[0]}")
        tabs = st.tabs(list(st.session_state.data.keys()) + ["TOTAL"])
        tg = 0
        for i, c in enumerate(st.session_state.data.keys()):
            g = st.session_state.data[c]["Goles"].get(nombre, 0)
            tabs[i].metric("Goles", g)
            tg += g
        tabs[-1].metric("Goles Totales", tg)

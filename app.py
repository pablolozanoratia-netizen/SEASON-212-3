import streamlit as st
import random
import pandas as pd

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="SEASON 212 - Official App", layout="wide")

# --- 1. BASE DE DATOS DE POSICIONES Y TIERS ---
TIERS_POWER = {"Goat": 5.0, "Casi goat": 3.5, "Buenísimos": 2.5, "Muy buenos": 2.0, "Bueno": 1.5, "Base": 1.0}

if 'info_jugadores' not in st.session_state:
    st.session_state.info_jugadores = {
        # --- DELANTEROS (DC) / EXTREMOS ---
        "Sandslash alola": ("Bueno", "DC"), "Swampert": ("Casi goat", "DC"), "Emboar": ("Bueno", "DC"),
        "Persian": ("Base", "DC"), "Machamp": ("Bueno", "DC"), "Milotic": ("Muy buenos", "DC"),
        "Flygon": ("Casi goat", "DC"), "Rampardos": ("Buenísimos", "DC"), "Pidgeot": ("Muy buenos", "DC"),
        "Hawlucha": ("Buenísimos", "DC"), "Drakloak": ("Base", "DC"), "Garchomp": ("Casi goat", "DC"),
        "Urshifu": ("Goat", "DC"), "Buzzwole": ("Buenísimos", "DC"), "Ursaluna": ("Goat", "DC"),
        "Revabroom": ("Bueno", "DC"), "Pawmot": ("Bueno", "DC"), "Primeape": ("Bueno", "DC"),
        "Zeraora": ("Goat", "DC"), "Keldeo": ("Buenísimos", "DC"), "Blaziken": ("Goat", "DC"),
        "Marshadow": ("Goat", "DC"), "Dragapult": ("Casi goat", "DC"), "Ceruledge": ("Buenísimos", "DC"),
        "Zarude": ("Goat", "DC"), "Jirachi": ("Goat", "DC"), "Zweilous": ("Base", "DC"),
        "Slaking-2": ("Bueno", "DC"), "Camerupt-2": ("Base", "DC"), "Pangoro": ("Bueno", "DC"),

        # --- MEDIOCENTROS (MC) ---
        "Kingambit": ("Muy buenos", "MC"), "Cinderace": ("Goat", "MC"), "Inteleon": ("Buenísimos", "MC"),
        "Armarouge": ("Casi goat", "MC"), "Gholdengo": ("Casi goat", "MC"), "Melenaleteo": ("Goat", "MC"),
        "Tapu fini": ("Goat", "MC"), "Hydreigon": ("Casi goat", "MC"), "Alakazam": ("Goat", "MC"),
        "Gengar": ("Goat", "MC"), "Serperior": ("Buenísimos", "MC"), "Zoroark": ("Casi goat", "MC"),
        "Toxtrixity": ("Muy buenos", "MC"), "Magmortar": ("Muy buenos", "MC"),

        # --- DEFENSAS (DF) ---
        "Ferrodada": ("Bueno", "DF"), "Metagross": ("Bueno", "DF"), "Ferrothorn": ("Bueno", "DF"),
        "Scolipede": ("Bueno", "DF"), "Gliscor": ("Muy buenos", "DF"), "Incineroar": ("Buenísimos", "DF"),
        "Toxapex": ("Base", "DF"), "Slaking": ("Muy buenos", "DF"), "Skarmory": ("Base", "DF"),
        "Weezing": ("Bueno", "DF"), "Kommo": ("Buenísimos", "DF"), "Steelix": ("Bueno", "DF"),
        "Arcanine galar": ("Buenísimos", "DF"), "Sandaconda": ("Bueno", "DF"), "Conckeldur": ("Bueno", "DF"),
        
        # --- PORTEROS (POR) ---
        "Courtois": ("Goat", "POR"), "Ter Stegen": ("Goat", "POR"), "Ederson": ("Goat", "POR"), 
        "Neuer": ("Goat", "POR"), "Alisson": ("Goat", "POR"), "Oblak": ("Goat", "POR"),
        "Onana": ("Goat", "POR"), "Maignan": ("Goat", "POR"), "Sommer": ("Goat", "POR"),
        "Raya": ("Muy buenos", "POR"), "Kobel": ("Muy buenos", "POR"), "Martinez": ("Goat", "POR")
    }

# --- 2. ALINEACIONES OFICIALES ---
if 'equipos' not in st.session_state:
    st.session_state.equipos = {
        "Ajax de Amsterdam": ["Ferrodada", "Forretress", "Klingklang", "Archeops", "Duraludon", "Empoleon", "Kingambit", "Chien pao", "Kilowatrel", "Sandslash alola", "Onana"],
        "Real Madrid": ["Metagross", "Golbat", "Croagunk", "Inteleon", "Liligant", "Wyglituff", "Cinderace", "Zeraora", "Keldeo", "Swampert", "Courtois"],
        "Sporting Lisboa": ["Ferrothorn", "Carbink", "Palossand", "Aromatise", "Rotom horno", "Mismagius", "Minior", "Sandslash", "Dugtrio alola", "Emboar", "Adan"],
        "Benfica": ["Scolipede", "Apletun", "Jumpluff", "Electrode galar", "Fearow", "Omastar", "Kingdra", "Hitmonlee", "Wyedeer", "Persian", "Trubin"],
        "Aston Villa": ["Abomashnow", "Seismitoad", "Gliscor", "Trevenant", "Exploud", "Jinks", "Drampa", "Hochkrow", "Tinkaton", "Machamp", "Martinez"],
        "Man United": ["Incineroar", "Pyroar", "Cofagrigus", "Belibolt", "Glaceon", "Skelerdirge", "Zoroark hisui", "Infernape", "Goldhengo", "Milotic", "Onana"],
        "Man City": ["Toxapex", "Electrode", "Durant", "Tentacruel", "Mr. Mime", "Kingdra", "Armarouge", "Aerodactyl", "Chien pao", "Flygon", "Ederson"],
        "Chelsea": ["Slaking", "Poliwarth", "Mandibuzz", "Chandelure", "Charizard", "Leavanny", "Cyclizar", "Typlosyon h", "Decidueye", "Anihilape", "Sanchez"],
        "Liverpool": ["Stounjourner", "Gourgeist", "Skuntank", "Clawitzer", "Ninetales", "Magmortar", "Toxtrixity", "Blaziken", "Boltund", "Rampardos", "Alisson"],
        "Barcelona": ["Skarmory", "Flareon", "Cloyster", "Slowking", "Vaporeon", "Vespiquen", "Serperior", "Zoroark", "Marshadow", "Pidgeot", "Ter Stegen"],
        "Arsenal": ["Weezing", "Toucanon", "Klinklang", "Blastoise", "Porygon 2", "Indedee", "Melenaleteo", "Dragapult", "Ceruledge", "Hawlucha", "Raya"],
        "Bayern": ["Kommo", "Darmanitan galar", "Escavalier", "Primarina", "Klefki", "Hydreigon", "Tapu fini", "Haxorus", "Raichu", "Garchomp", "Neuer"],
        "Juventus": ["Steelix", "Dubwol", "Armaldo", "Reuniclus", "Magmar", "Alakazam", "Absol", "Tapu koko", "Medicham", "Urshifu", "Di Gregorio"],
        "Athletic Bilbao": ["Throh", "Crustle", "Gurdurr", "Perrserker", "Kubfu", "Hakamo-o", "Sirfetch’d-2", "Obstagoon-2", "Hitmonchan", "Zweilous", "Unai Simon"],
        "Real Betis": ["Probopass", "Togedemaru", "Chimecho", "Morpeko", "Appletun-2", "Sunflora-2", "Meowstic", "Leavanny-2", "Ludicolo-2", "Roserade-2", "Rui Silva"],
        "Osasuna": ["Bastiodon", "Binacle", "Masquerain", "Carbink-2", "Octillery", "Beheeyem", "Mightyena", "Skuntank", "Spidops", "Slaking-2", "Herrera"],
        "Villarreal": ["Tropius", "Silicobra", "Cacturne", "Klinklang-2", "Comfey", "Sigilyph", "Stantler", "Bronzor", "Vivillon-2", "Camerupt-2", "Conde"],
        "PSG": ["Darmanitan", "Drednaw", "Goodra", "Delphox", "Talonflame", "Noiverm", "Kingambit", "Zarude", "Swellow", "Pawmot", "Donnarumma"]
    }

# --- 3. INICIALIZAR ESTADÍSTICAS ---
if 'data' not in st.session_state:
    comps = ["Superliga Europea", "Champions", "Supercopa Enter", "Supercopa Exit", "Copa Elite", "FinalCup"]
    st.session_state.data = {c: {"Goles": {}, "Asis": {}, "MVP": {}, "Historial": []} for c in comps}

# --- 4. MOTOR DE SIMULACIÓN ---
def simular_partido(local, visitante, comp):
    p_l = st.session_state.equipos.get(local, ["?"]*11)
    p_v = st.session_state.equipos.get(visitante, ["?"]*11)
    
    def get_prob(j, tipo):
        tier, pos = st.session_state.info_jugadores.get(j, ("Base", "MC"))
        poder = TIERS_POWER.get(tier, 1.0)
        if tipo == "gol":
            mult = 7.0 if pos == "DC" else 2.0 if pos == "MC" else 0.3 if pos == "DF" else 0.0
        else:
            mult = 5.0 if pos == "MC" else 2.5 if pos == "DC" else 1.0 if pos == "DF" else 0.1
        return poder * mult

    g_l = max(0, int(random.gauss(2.1, 1.1)))
    g_v = max(0, int(random.gauss(1.9, 1.1)))
    
    eventos = []
    for g, eq, plantilla in [(g_l, local, p_l), (g_v, visitante, p_v)]:
        for _ in range(g):
            pesos_g = [get_prob(j, "gol") for j in plantilla]
            autor = random.choices(plantilla, weights=pesos_g)[0]
            pesos_a = [get_prob(j, "asis") for j in plantilla]
            asist = random.choices(plantilla, weights=pesos_a)[0]
            minuto = random.randint(1, 90)
            eventos.append({"min": minuto, "autor": autor, "asist": asist, "equipo": eq})
            st.session_state.data[comp]["Goles"][autor] = st.session_state.data[comp]["Goles"].get(autor, 0) + 1
            st.session_state.data[comp]["Asis"][asist] = st.session_state.data[comp]["Asis"].get(asist, 0) + 1

    mvp = random.choice(p_l if g_l >= g_v else p_v)
    st.session_state.data[comp]["MVP"][mvp] = st.session_state.data[comp]["MVP"].get(mvp, 0) + 1
    return {"l": local, "v": visitante, "gl": g_l, "gv": g_v, "evs": sorted(eventos, key=lambda x: x['min']), "mvp": mvp}

# --- 5. INTERFAZ ---
st.sidebar.title("⭐ SEASON 212")
seccion = st.sidebar.selectbox("Ir a:", ["🏆 Competiciones", "👤 Jugadores", "🌍 Ranking Global"])

if seccion == "🏆 Competiciones":
    comp_activa = st.selectbox("Selecciona Torneo", list(st.session_state.data.keys()))
    t1, t2 = st.tabs(["🎮 Simulador", "📊 Estadísticas Torneo"])
    with t1:
        col_izq, col_der = st.columns([1, 2])
        with col_izq:
            prompt = st.text_area("Chat de Simulación (Local - Visitante)", height=200)
            if st.button("🚀 Simular"):
                lineas = [l.strip() for l in prompt.split("\n") if "-" in l]
                st.session_state.data[comp_activa]["Historial"] = [simular_partido(l.split("-")[0].strip(), l.split("-")[1].strip(), comp_activa) for l in lineas]
        with col_der:
            for r in st.session_state.data[comp_activa]["Historial"]:
                st.markdown(f"**{r['l']} {r['gl']} - {r['gv']} {r['v']}**")
                with st.expander("Goles y MVP"):
                    st.write(f"🌟 MVP: {r['mvp']}")
                    for e in r['evs']: st.write(f"{e['min']}' ⚽ {e['autor']} (Asist: {e['asist']})")

    with t2:
        st.header(f"Rankings {comp_activa}")
        c1, c2, c3 = st.columns(3)
        for col, tipo, tit in zip([c1, c2, c3], ["Goles", "Asis", "MVP"], ["Goleadores", "Asistentes", "MVPs"]):
            df = pd.DataFrame.from_dict(st.session_state.data[comp_activa][tipo], orient='index', columns=['Total']).sort_values('Total', ascending=False).head(30)
            col.table(df)

elif seccion == "👤 Jugadores":
    todos = sorted(list(set([j for e in st.session_state.equipos.values() for j in e])))
    nombre = st.selectbox("Busca un Pokémon", todos)
    if nombre:
        tier, pos = st.session_state.info_jugadores.get(nombre, ("Base", "MC"))
        st.subheader(f"{nombre} ({pos}) - Tier: {tier}")
        g_t = sum([st.session_state.data[c]["Goles"].get(nombre, 0) for c in st.session_state.data])
        st.metric("Goles Totales S212", g_t)

elif seccion == "🌍 Ranking Global":
    st.header("🌍 Rankings Globales")
    g_g = {}
    for c in st.session_state.data:
        for j, v in st.session_state.data[c]["Goles"].items(): g_g[j] = g_g.get(j, 0) + v
    st.table(pd.Series(g_g).sort_values(ascending=False).head(30))
        

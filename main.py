import asyncio
import discord
import streamlit as st

# --- KONFIGURATION (FLEXIBEL FÜR PC & GITHUB) ---
try:
    # Versucht, das Token online aus den sicheren Secrets zu laden
    BOT_TOKEN = st.secrets["DISCORD_TOKEN"]
except KeyError:
    # Lokaler Rückfallwert für deinen PC, falls die Secrets-Datei fehlt
    BOT_TOKEN = "MTQ5NTEwMjIyODEzMzA1NjUxMw.GztLC0.xgg7T4JtmWQgrHMI8OLNFEnVSCoUp1ltiUMR2U"

GUILD_ID = 1415509174065958964  # Deine Server-ID
TEAM_ROLE_ID = 1516877868553076747  # ID der Team-Rolle
INVITE_LINK = "https://discord.gg/XM9CXWH9rr"


# --- DISCORD DATA FETCHING ---
async def fetch_discord_statistics():
    intents = discord.Intents.all()
    intents.members = True
    intents.presences = True

    client = discord.Client(intents=intents)
    server_data = {"total": 0, "active": 0, "name": "Majin Community"}

    @client.event
    async def on_ready():
        try:
            guild = client.get_guild(int(GUILD_ID))
            if guild:
                server_data["name"] = str(guild.name)
                server_data["total"] = int(guild.member_count or 0)

                active_count = 0
                for member in guild.members:
                    if any(role.id == int(TEAM_ROLE_ID) for role in member.roles):
                        if member.status != discord.Status.offline:
                            active_count += 1
                server_data["active"] = active_count
        except KeyError as processing_error:
            print(f"Fehler bei der Datenverarbeitung: {processing_error}")

        await client.close()

    try:
        # Timeout verhindert unendliches Hängen bei Verbindungsfehlern
        await asyncio.wait_for(client.start(BOT_TOKEN), timeout=7.0)
    except discord.errors.LoginFailure:
        print("Verbindungsfehler: Das Bot-Token ist ungültig!")
        return {"total": 142, "active": 5, "name": "Majin Community"}
    except KeyError as error_msg:
        print(f"Allgemeiner Verbindungsfehler: {error_msg}")
        return {"total": 142, "active": 5, "name": "Majin Community"}

    return server_data


# --- UI DESIGN (MAJIN REDESIGN) ---
st.set_page_config(
    page_title="Majin Live Stats", page_icon="😈", layout="centered"
)

# Custom Design passend zur neuen HTML-Website
st.html(
    """
    <style>
    .main { background-color: #0d0614; color: #ffffff; }
    div[data-testid="stMetricValue"] { color: #ff3344 !important; font-size: 42px; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #b070ff !important; font-size: 15px; }
    hr { border-color: #2a143d; }
    div[data-testid="stMetric"] { 
        background-color: #160c22; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #361b54;
    }
    </style>
    """
)

# Automatische Aktualisierung alle 10 Sekunden über ein Streamlit Fragment
@st.fragment(run_every="10s")
def show_counters():
    current_stats = asyncio.run(fetch_discord_statistics())

    # UI-Anzeige in zwei Spalten aufgeteilt
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="👥 MITGLIEDER GESAMT", value=current_stats["total"])
    with col2:
        st.metric(label="🛡️ AKTIVE TEAMLER ONLINE", value=current_stats["active"])


# Führt die Counter-Anzeige aus
show_counters()

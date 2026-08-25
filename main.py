import asyncio
import discord
import streamlit as st

# --- CONFIGURATION ---
BOT_TOKEN = "MTQ5NTEwMjIyODEzMzA1NjUxMw.GztLC0.xgg7T4JtmWQgrHMI8OLNFEnVSCoUp1ltiUMR2U"
GUILD_ID = 1415509174065958964
TEAM_ROLE_ID = 1516877868553076747
INVITE_LINK = "https://discord.gg"


# --- DISCORD DATA FETCHING ---
async def fetch_discord_statistics():
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    server_data = {"total": 0, "active": 0, "name": "Majin Community"}

    @client.event
    async def on_ready():
        guild = client.get_guild(GUILD_ID)
        if guild:
            server_data["name"] = str(guild.name)
            server_data["total"] = int(guild.member_count or 0)

            active_count = 0
            for member in guild.members:
                if any(role.id == TEAM_ROLE_ID for role in member.roles):
                    if member.status != discord.Status.offline:
                        active_count += 1
            server_data["active"] = active_count
        await client.close()

    try:
        # Timeout verhindert langes Hängen bei falschem Token
        await asyncio.wait_for(client.start(BOT_TOKEN), timeout=7.0)
    except Exception as error_msg:
        print(f"Verbindungsfehler: {error_msg}")
        # Testdaten für die lokale Entwicklung, falls Discord blockiert
        return {"total": 142, "active": 5, "name": "Majin Community"}

    return server_data


# --- UI DESIGN (MAJIN REDESIGN) ---
st.set_page_config(
    page_title="Majin Live Stats", page_icon="😈", layout="centered"
)

# Custom Design passend zur neuen Website
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

# Automatische Aktualisierung alle 10 Sekunden
st.fragment(run_every="10s")

current_stats = asyncio.run(fetch_discord_statistics())

# UI-Anzeige ohne störende Titel-Header für die Web-Einbettung
col1, col2 = st.columns(2)
with col1:
    st.metric(label="👥 MITGLIEDER GESAMT", value=current_stats["total"])
with col2:
    st.metric(label="🛡️ AKTIVE TEAMLER ONLINE", value=current_stats["active"])

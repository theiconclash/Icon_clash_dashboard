import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ========= PAGE CONFIG ========= #
st.set_page_config(
    page_title="The Icon Clash Arena",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed",  # Hide sidebar
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': 'Icon Clash Arena - Battle Statistics Dashboard'
    }
)

# ========= CUSTOM CSS ========= #
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    /* Hide sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem !important;
            padding: 0.3rem 0 !important;
            margin-bottom: 0.5rem !important;
        }
        
        .section-header {
            font-size: 1.2rem !important;
            margin: 1rem 0 0.5rem 0 !important;
        }
        
        .stats-card {
            padding: 15px !important;
            margin-bottom: 10px !important;
        }
        
        .winner-banner {
            padding: 1rem !important;
            font-size: 1.1rem !important;
            margin: 0.5rem 0 !important;
        }
        
        .player-card {
            padding: 12px !important;
            margin-bottom: 8px !important;
        }
        
        .date-button {
            padding: 10px 16px !important;
            font-size: 0.9rem !important;
            margin: 3px !important;
        }
        
        .quick-stat {
            padding: 12px !important;
            margin-bottom: 8px !important;
        }
        
        /* Mobile navigation buttons */
        .mobile-nav-button {
            padding: 12px 16px !important;
            font-size: 0.9rem !important;
            margin: 2px !important;
            min-width: 80px !important;
        }
        
        /* Mobile table adjustments */
        .mobile-table {
            font-size: 0.8rem !important;
        }
        
        /* Mobile metric adjustments */
        div[data-testid="metric-container"] {
            padding: 10px !important;
            margin-bottom: 8px !important;
        }
        
        /* Mobile highlight cards */
        .mobile-highlight-card {
            padding: 12px !important;
            margin-bottom: 8px !important;
            font-size: 0.9rem !important;
        }
        
        /* Mobile column adjustments */
        .mobile-stack {
            flex-direction: column !important;
        }
        
        /* Touch-friendly buttons */
        button {
            min-height: 44px !important;
            min-width: 44px !important;
        }
        
        /* Mobile-friendly selectboxes */
        .stSelectbox {
            min-height: 44px !important;
        }
        
        /* Mobile radio buttons */
        .stRadio > div {
            gap: 8px !important;
        }
        
        .stRadio > div > label {
            padding: 8px 12px !important;
            min-height: 44px !important;
            display: flex !important;
            align-items: center !important;
        }
    }
    
    /* Tablet adjustments */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-header {
            font-size: 2rem !important;
        }
        
        .section-header {
            font-size: 1.3rem !important;
        }
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF006E, #00FFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
    }
    
    /* Date selector buttons */
    .date-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        margin: 5px;
        display: inline-block;
    }
    
    .date-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    .date-button.active {
        background: linear-gradient(135deg, #FF006E, #8B00FF);
        box-shadow: 0 5px 20px rgba(255,0,110,0.4);
    }
    
    /* Stats card */
    .stats-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Winner announcement */
    .winner-banner {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    /* Player card */
    .player-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 12px;
        color: white;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .player-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    
    /* Leaderboard row */
    .leaderboard-row {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        transition: all 0.3s;
    }
    
    .leaderboard-row:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateX(5px);
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00FFFF;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(0, 255, 255, 0.3);
    }
    
    /* Quick stats */
    .quick-stat {
        background: linear-gradient(135deg, rgba(255,0,110,0.2), rgba(0,255,255,0.2));
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Custom selectbox styling */
    .stSelectbox > div > div > div > div {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Placeholder styling */
    .stSelectbox [data-baseweb="select"] [data-baseweb="base-input"] {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Mobile-friendly highlight cards */
    .mobile-highlight-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        text-align: center;
    }
    
    /* Mobile table wrapper */
    .mobile-table-wrapper {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    
    /* Mobile-friendly buttons */
    .mobile-button {
        min-height: 44px;
        min-width: 44px;
        padding: 12px 16px;
        font-size: 1rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

DB_PATH = os.path.join(os.path.dirname(__file__), "data/daily_stats.db")

# ========= DB HELPERS (keeping all your original functions) ========= #
def get_conn():
    return sqlite3.connect(DB_PATH)

@st.cache_data(ttl=300)
def get_available_dates():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT date FROM daily_summary ORDER BY date DESC")
    dates = [r[0] for r in cursor.fetchall()]
    conn.close()
    return dates

@st.cache_data(ttl=300)
def get_daily_summary(date_str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT num_players, winner FROM daily_summary WHERE date = ?", (date_str,))
    row = cursor.fetchone()
    conn.close()
    return {"num_players": row[0], "winner": row[1]} if row else None

@st.cache_data(ttl=300)
def get_players(date_str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT player FROM player_stats WHERE date = ? ORDER BY player ASC", (date_str,))
    players = [r[0] for r in cursor.fetchall()]
    conn.close()
    return players

@st.cache_data(ttl=300)
def get_top_players(date_str, stat="kills", limit=10):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT player, {stat}
        FROM player_stats
        WHERE date = ?
        ORDER BY {stat} DESC
        LIMIT ?
    """, (date_str, limit))
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=["Player", stat.capitalize()])

@st.cache_data(ttl=300)
def get_player_stats(date_str, player):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kills, deaths, damage_dealt, damage_received, nemesis, victim
        FROM player_stats
        WHERE date = ? AND player = ?
    """, (date_str, player))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "kills": row[0],
            "deaths": row[1],
            "damage_dealt": row[2],
            "damage_received": row[3],
            "nemesis": row[4],
            "victim": row[5],
        }
    return None

@st.cache_data(ttl=300)
def get_player_rank(date_str, player):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rank FROM ranking WHERE date = ? AND player = ?
    """, (date_str, player))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

@st.cache_data(ttl=300)
def get_normalized_rank(date_str, player):
    """Get the normalized rank (1,2,3,4...) for a player, accounting for gaps in database ranks"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rank FROM ranking WHERE date = ? AND player = ?
    """, (date_str, player))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return None
    
    db_rank = row[0]
    
    # Normalize rank: convert 0 to 1, 1 to 2, etc.
    if db_rank == 0:
        return 1
    else:
        return db_rank + 1

@st.cache_data(ttl=300)
def get_all_time_stats():
    conn = get_conn()
    cursor = conn.cursor()
    
    # Get total battles
    cursor.execute("SELECT COUNT(*) FROM daily_summary")
    total_battles = cursor.fetchone()[0]
    
    # Get total unique players
    cursor.execute("SELECT COUNT(DISTINCT player) FROM player_stats")
    total_players = cursor.fetchone()[0]
    
    # Get date range
    cursor.execute("SELECT MIN(date), MAX(date) FROM daily_summary")
    date_range = cursor.fetchone()
    first_battle = date_range[0] if date_range[0] else "N/A"
    last_battle = date_range[1] if date_range[1] else "N/A"
    
    # Get top winner (by battle wins)
    cursor.execute("""
        SELECT winner, COUNT(*) as wins 
        FROM daily_summary 
        GROUP BY winner 
        ORDER BY wins DESC 
        LIMIT 1
    """)
    top_winner = cursor.fetchone()
    
    # Get total kills across all battles
    cursor.execute("SELECT SUM(kills) FROM player_stats")
    total_kills = cursor.fetchone()[0] or 0
    
    # Get total damage across all battles  
    cursor.execute("SELECT SUM(damage_dealt) FROM player_stats")
    total_damage = cursor.fetchone()[0] or 0
    
    # Get player with most cumulative kills
    cursor.execute("""
        SELECT player, SUM(kills) as total_kills
        FROM player_stats 
        GROUP BY player 
        ORDER BY total_kills DESC 
        LIMIT 1
    """)
    top_killer = cursor.fetchone()
    
    # Get player with most cumulative damage
    cursor.execute("""
        SELECT player, SUM(damage_dealt) as total_damage
        FROM player_stats 
        GROUP BY player 
        ORDER BY total_damage DESC 
        LIMIT 1
    """)
    top_damage_dealer = cursor.fetchone()
    
    # Get player with best kill efficiency (kills/deaths ratio)
    cursor.execute("""
        SELECT player, 
               SUM(kills) as total_kills,
               SUM(deaths) as total_deaths,
               CASE WHEN SUM(deaths) > 0 THEN CAST(SUM(kills) AS FLOAT) / SUM(deaths) ELSE SUM(kills) END as kdr
        FROM player_stats 
        GROUP BY player 
        HAVING SUM(kills) > 0
        ORDER BY kdr DESC 
        LIMIT 1
    """)
    top_kdr = cursor.fetchone()
    
    # Get player with most battles participated
    cursor.execute("""
        SELECT player, COUNT(*) as battles_participated
        FROM player_stats 
        GROUP BY player 
        ORDER BY battles_participated DESC 
        LIMIT 1
    """)
    most_active = cursor.fetchone()
    
    # Get highest single battle kills
    cursor.execute("""
        SELECT player, kills, date
        FROM player_stats 
        ORDER BY kills DESC 
        LIMIT 1
    """)
    highest_kills = cursor.fetchone()
    
    # Get highest single battle damage
    cursor.execute("""
        SELECT player, damage_dealt, date
        FROM player_stats 
        ORDER BY damage_dealt DESC 
        LIMIT 1
    """)
    highest_damage = cursor.fetchone()
    
    # Get most active battle day
    cursor.execute("""
        SELECT date, COUNT(*) as battles_that_day
        FROM daily_summary 
        GROUP BY date 
        ORDER BY battles_that_day DESC 
        LIMIT 1
    """)
    most_active_day = cursor.fetchone()
    
    conn.close()
    
    return {
        "total_battles": total_battles,
        "total_players": total_players,
        "first_battle": first_battle,
        "last_battle": last_battle,
        "top_winner": top_winner[0] if top_winner else None,
        "top_wins": top_winner[1] if top_winner else 0,
        "total_kills": total_kills,
        "total_damage": total_damage,
        "top_killer": top_killer[0] if top_killer else None,
        "top_killer_kills": top_killer[1] if top_killer else 0,
        "top_damage_dealer": top_damage_dealer[0] if top_damage_dealer else None,
        "top_damage_dealt": top_damage_dealer[1] if top_damage_dealer else 0,
        "top_kdr_player": top_kdr[0] if top_kdr else None,
        "top_kdr_ratio": round(top_kdr[2], 2) if top_kdr else 0,
        "top_kdr_kills": top_kdr[1] if top_kdr else 0,
        "most_active_player": most_active[0] if most_active else None,
        "most_active_battles": most_active[1] if most_active else 0,
        "highest_kills_player": highest_kills[0] if highest_kills else None,
        "highest_kills_count": highest_kills[1] if highest_kills else 0,
        "highest_kills_date": highest_kills[2] if highest_kills else None,
        "highest_damage_player": highest_damage[0] if highest_damage else None,
        "highest_damage_amount": highest_damage[1] if highest_damage else 0,
        "highest_damage_date": highest_damage[2] if highest_damage else None,
        "most_active_day": most_active_day[0] if most_active_day else None,
        "most_active_day_battles": most_active_day[1] if most_active_day else 0
    }

@st.cache_data(ttl=300)
def get_all_daily_winners():
    """Get all daily winners with their dates"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, winner, 
               (SELECT COUNT(*) FROM player_stats WHERE date = ds.date) as participants
        FROM daily_summary ds
        WHERE date IS NOT NULL AND winner IS NOT NULL
        ORDER BY date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    # Filter out any rows with None or empty values
    valid_rows = [(date, winner, participants) for date, winner, participants in rows 
                  if date is not None and winner is not None and participants is not None]
    
    return pd.DataFrame(valid_rows, columns=["Date", "Winner", "Participants"])

# ========= HELPER FUNCTIONS ========= #
def get_rank_emoji(rank):
    if rank == 0: return "👑"
    elif rank == 1: return "🥇"
    elif rank == 2: return "🥈"
    elif rank == 3: return "🥉"
    elif rank and rank <= 10: return "⭐"
    else: return "⚔️"

def create_mini_damage_chart(damage_dealt, damage_received):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Dealt', 'Received'],
        y=[damage_dealt, damage_received],
        marker_color=['#00FFFF', '#FF006E'],
        text=[f"{damage_dealt:.0f}", f"{damage_received:.0f}"],
        textposition='outside'
    ))
    
    fig.update_layout(
        showlegend=False,
        height=200,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=10),
        yaxis=dict(showgrid=False, showticklabels=False),
        xaxis=dict(showgrid=False)
    )
    
    return fig

# ========= MAIN APP ========= #

# Header
st.markdown('<h1 class="main-header">⚔️ THE ICON CLASH ARENA ⚔️</h1>', unsafe_allow_html=True)

# Get available dates
available_dates = get_available_dates()
if not available_dates:
    st.error("🚫 No data available in database.")
    st.stop()

# ========= MAIN NAVIGATION ========= #
st.markdown('<div class="section-header">🎮 SELECT SECTION</div>', unsafe_allow_html=True)

# Initialize navigation state
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Daily Battles"

# Create three main navigation buttons - Mobile responsive
nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])

with nav_col1:
    if st.button("⚔️ DAILY BATTLES", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_section == "Daily Battles" else "secondary",
                 key="nav_daily"):
        st.session_state.current_section = "Daily Battles"
        st.rerun()

with nav_col2:
    if st.button("🌍 ALL TIME STATS", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_section == "All Time Stats" else "secondary",
                 key="nav_alltime"):
        st.session_state.current_section = "All Time Stats"
        st.rerun()

with nav_col3:
    if st.button("🔍 FIGHTER ANALYSIS", 
                 use_container_width=True, 
                 type="primary" if st.session_state.current_section == "Fighter Analysis" else "secondary",
                 key="nav_analysis"):
        st.session_state.current_section = "Fighter Analysis"
        st.rerun()

# ========= DAILY BATTLES SECTION ========= #
if st.session_state.current_section == "Daily Battles":
    # ========= DATE SELECTION SECTION ========= #
    st.markdown('<div class="section-header">📅 SELECT BATTLE DATE</div>', unsafe_allow_html=True)

    # Initialize selected date in session state
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = available_dates[0]

    # Mobile-friendly date selection
    # Show last 3 dates as buttons
    recent_dates = available_dates[:3] if len(available_dates) >= 3 else available_dates
    
    # Create responsive button layout
    if len(recent_dates) == 1:
        button_cols = st.columns(1)
    elif len(recent_dates) == 2:
        button_cols = st.columns(2)
    else:
        button_cols = st.columns(3)
    
    # Recent date buttons
    for idx, (col, date) in enumerate(zip(button_cols, recent_dates)):
        with col:
            is_selected = st.session_state.selected_date == date
            button_type = "primary" if is_selected else "secondary"
            
            if st.button(
                f"⚔️ {date}",
                key=f"date_{date}",
                use_container_width=True,
                type=button_type
            ):
                st.session_state.selected_date = date
                st.rerun()
    
    # "More" button for older dates - Mobile friendly
    if len(available_dates) > 3:
        older_dates = available_dates[3:]
        selected_older = st.selectbox(
            "📆 Older Battles",
            ["Select..."] + older_dates,
            key="older_dates",
            label_visibility="collapsed"
        )
        if selected_older != "Select..." and selected_older != st.session_state.selected_date:
            st.session_state.selected_date = selected_older
            st.rerun()

    selected_date = st.session_state.selected_date

    # ========= BATTLE HIGHLIGHTS ========= #
    st.markdown('<div class="section-header">🔥 BATTLE HIGHLIGHTS</div>', unsafe_allow_html=True)

    # Create a container with consistent styling - Mobile responsive
    highlight_container = st.container()
    with highlight_container:
        # Mobile-friendly highlight cards layout
        highlight_cols = st.columns(4)

    # Champion
    with highlight_cols[0]:
        summary = get_daily_summary(selected_date)
        if summary:
            st.markdown("### 👑 Champion")
            with st.container():
                st.markdown(f"""
                <div class="mobile-highlight-card" style="background: rgba(0,255,0,0.1); border: 1px solid rgba(0,255,0,0.3); border-radius: 10px; padding: 15px; text-align: center;">
                    <strong>@{summary['winner']}</strong><br>
                    Defeated {summary['num_players']-1} fighters
                </div>
                """, unsafe_allow_html=True)

    # Most Kills
    with highlight_cols[1]:
        top_killer = get_top_players(selected_date, "kills", 1)
        if not top_killer.empty:
            st.markdown("### 💀 Most Lethal")
            with st.container():
                st.markdown(f"""
                <div class="mobile-highlight-card" style="background: rgba(0,123,255,0.1); border: 1px solid rgba(0,123,255,0.3); border-radius: 10px; padding: 15px; text-align: center;">
                    <strong>@{top_killer.iloc[0]['Player']}</strong><br>
                    {top_killer.iloc[0]['Kills']} kills
                </div>
                """, unsafe_allow_html=True)

    # Most Damage
    with highlight_cols[2]:
        top_damage = get_top_players(selected_date, "damage_dealt", 1)
        if not top_damage.empty:
            st.markdown("### 💥 Damage King")
            with st.container():
                st.markdown(f"""
                <div class="mobile-highlight-card" style="background: rgba(0,123,255,0.1); border: 1px solid rgba(0,123,255,0.3); border-radius: 10px; padding: 15px; text-align: center;">
                    <strong>@{top_damage.iloc[0]['Player']}</strong><br>
                    {top_damage.iloc[0]['Damage_dealt']:,.0f} dmg
                </div>
                """, unsafe_allow_html=True)

    # Total participants
    with highlight_cols[3]:
        st.markdown("### 👥 Warriors")
        total_players = len(get_players(selected_date)) if get_players(selected_date) else 0
        with st.container():
            st.markdown(f"""
            <div class="mobile-highlight-card" style="background: rgba(0,123,255,0.1); border: 1px solid rgba(0,123,255,0.3); border-radius: 10px; padding: 15px; text-align: center;">
                <strong>{total_players}</strong><br>
                fighters
            </div>
            """, unsafe_allow_html=True)

    # ========= MAIN CONTENT AREA ========= #
    # Mobile responsive columns
    main_col1, main_col2 = st.columns([2, 3])

    with main_col1:
        # ========= LEADERBOARD ========= #
        st.markdown('<div class="section-header">🏆 LEADERBOARD</div>', unsafe_allow_html=True)
        
        # Leaderboard type selector
        leaderboard_type = st.radio(
            "Rank by",
            ["Rank", "Kills", "Damage"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        stat_map = {
            "Rank": "rank",
            "Kills": "kills",
            "Damage": "damage_dealt"
        }
        
        # Get top players based on selected type
        if leaderboard_type == "Rank":
            # Special handling for rank - get from ranking table
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.player, r.rank
                FROM ranking r
                WHERE r.date = ?
                ORDER BY r.rank ASC
                LIMIT 10
            """, (selected_date,))
            rows = cursor.fetchall()
            conn.close()
            
            if rows:
                df = pd.DataFrame(rows, columns=["Player", "Rank"])
                # Normalize ranks: convert 0 to 1, 1 to 2, etc.
                df['Rank'] = df['Rank'].apply(lambda x: x + 1 if x == 0 else x)
                # Add position column for display
                df.insert(0, "Position", range(1, len(df) + 1))
                # Format the rank column
                df['Rank'] = df['Rank'].apply(lambda x: f"#{x}")
                # Format the player column
                df['Player'] = df['Player'].apply(lambda x: f"@{x}")
                
                # Display as table with mobile wrapper
                with st.container():
                    st.markdown('<div class="mobile-table-wrapper">', unsafe_allow_html=True)
                    st.table(df.set_index('Position'))
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No ranking data available for this date.")
        else:
            # Get top players by kills or damage
            df = get_top_players(selected_date, stat_map[leaderboard_type], 10)
            
            if not df.empty:
                # Add position column for display
                df.insert(0, "Position", range(1, len(df) + 1))
                # Format the player column
                df['Player'] = df['Player'].apply(lambda x: f"@{x}")
                # Format the numeric column
                if leaderboard_type == "Kills":
                    df[leaderboard_type.capitalize()] = df[leaderboard_type.capitalize()].astype(int).apply(lambda x: f"{x:,}")
                else:
                    df['Damage_dealt'] = df['Damage_dealt'].astype(float).apply(lambda x: f"{x:,.0f}")
                
                # Display as table with mobile wrapper
                with st.container():
                    st.markdown('<div class="mobile-table-wrapper">', unsafe_allow_html=True)
                    st.table(df.set_index('Position'))
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info(f"No {leaderboard_type.lower()} data available for this date.")

    with main_col2:
        # ========= FIGHTER ANALYSIS ========= #
        st.markdown('<div class="section-header">🔍 FIGHTER ANALYSIS</div>', unsafe_allow_html=True)
        
        players = get_players(selected_date)
        
        if players:
            st.markdown(f"**Select a fighter to analyze:** (Found {len(players)} players)")
            
            # Simple dropdown with all players and built-in search
            selected_player = st.selectbox(
                "Select a player",
                ["Type your username:"] + players,
                format_func=lambda x: x if x == "Type your username:" else f"@{x}",
                label_visibility="collapsed",
                key="player_select",
                index=0
            )
            
            if selected_player == "Type your username:":
                selected_player = None
            else:
                st.caption(f"Showing all {len(players)} players. You can type in the dropdown to search.")
            
            if selected_player:
                # Get player stats
                stats = get_player_stats(selected_date, selected_player)
                rank = get_normalized_rank(selected_date, selected_player)
                
                if stats:
                    # Player info header
                    st.markdown(f"### @{selected_player} - Battle Stats")
                    
                    # Quick stats row
                    stat_cols = st.columns(5)
                    
                    with stat_cols[0]:
                        # Normalize rank: convert 0 to 1, 1 to 2, etc.
                        normalized_rank = rank + 1 if rank == 0 else rank
                        rank_display = f"#{normalized_rank}"
                        st.metric("Rank", rank_display)
                    
                    with stat_cols[1]:
                        st.metric("Kills", stats['kills'])
                    
                    with stat_cols[2]:
                        st.metric("Deaths", stats['deaths'])
                    
                    with stat_cols[3]:
                        kd = stats['kills'] / max(stats['deaths'], 1)
                        st.metric("K/D", f"{kd:.2f}")
                    
                    with stat_cols[4]:
                        efficiency = stats['damage_dealt'] / max(stats['damage_received'], 1)
                        st.metric("Efficiency", f"{efficiency:.2f}x")
                    
                    # Damage stats in text format
                    damage_col1, damage_col2 = st.columns(2)
                    
                    with damage_col1:
                        st.markdown(f"""
                        <div style="background: rgba(0,255,255,0.1); border: 1px solid rgba(0,255,255,0.3); border-radius: 10px; padding: 15px; text-align: center;">
                            <strong style="color: #00FFFF;">Damage Dealt</strong><br>
                            <span style="font-size: 1.5rem; font-weight: bold;">{stats['damage_dealt']:,.0f}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with damage_col2:
                        st.markdown(f"""
                        <div style="background: rgba(255,0,110,0.1); border: 1px solid rgba(255,0,110,0.3); border-radius: 10px; padding: 15px; text-align: center;">
                            <strong style="color: #FF006E;">Damage Received</strong><br>
                            <span style="font-size: 1.5rem; font-weight: bold;">{stats['damage_received']:,.0f}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Nemesis and Victim
                    rival_col1, rival_col2 = st.columns(2)
                    
                    with rival_col1:
                        if stats['nemesis']:
                            st.error(f"😈 **Killed by:** [@{stats['nemesis']}](https://instagram.com/{stats['nemesis']})")
                        else:
                            st.success("🛡️ **Survived the battle!**")
                    
                    with rival_col2:
                        if stats['victim']:
                            st.info(f"🎯 **Best victim:** [@{stats['victim']}](https://instagram.com/{stats['victim']})")
                        else:
                            st.info("☮️ **No eliminations**")
                else:
                    st.error(f"❌ **No stats found for @{selected_player}**")
                    st.write("This player may not have participated in this battle, or there might be a data issue.")
        else:
            st.info("⚔️ **No battle data available for the selected date.**")
            st.write("Please select a different date or check if the data has been processed correctly.")

# ========= ALL TIME STATS SECTION ========= #
elif st.session_state.current_section == "All Time Stats":
    all_time_stats = get_all_time_stats()
    
    # ========= ALL-TIME HIGHLIGHTS ========= #
    st.markdown('<div class="section-header">🔥 ALL-TIME HIGHLIGHTS</div>', unsafe_allow_html=True)

    # Create a container with consistent styling - Mobile responsive
    highlight_container = st.container()
    with highlight_container:
        # Mobile-friendly highlight cards layout
        highlight_cols = st.columns(4)

    # Hall of Fame - Most Kills
    with highlight_cols[0]:
        st.markdown("### 🏆 Hall of Fame")
        st.markdown(f"""
        <div class="mobile-highlight-card" style="background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; padding: 15px; text-align: center;">
            <strong>@{all_time_stats['top_killer']}</strong><br>
            {all_time_stats['top_killer_kills']:,} total kills
        </div>
        """, unsafe_allow_html=True)

    # Record Breakers - Highest Single Battle Kills
    with highlight_cols[1]:
        st.markdown("### 💀 Record Breakers")
        st.markdown(f"""
        <div class="mobile-highlight-card" style="background: rgba(255,0,0,0.1); border: 1px solid rgba(255,0,0,0.3); border-radius: 10px; padding: 15px; text-align: center;">
            <strong>@{all_time_stats['highest_kills_player']}</strong><br>
            {all_time_stats['highest_kills_count']} kills in one battle
        </div>
        """, unsafe_allow_html=True)

    # Most Damage Dealt
    with highlight_cols[2]:
        st.markdown("### 💥 Damage King")
        st.markdown(f"""
        <div class="mobile-highlight-card" style="background: rgba(0,123,255,0.1); border: 1px solid rgba(0,123,255,0.3); border-radius: 10px; padding: 15px; text-align: center;">
            <strong>@{all_time_stats['top_damage_dealer']}</strong><br>
            {all_time_stats['top_damage_dealt']:,.0f} total damage
        </div>
        """, unsafe_allow_html=True)

    # Highest Single Battle Damage
    with highlight_cols[3]:
        st.markdown("### 🎯 Damage Record")
        st.markdown(f"""
        <div class="mobile-highlight-card" style="background: rgba(128,0,128,0.1); border: 1px solid rgba(128,0,128,0.3); border-radius: 10px; padding: 15px; text-align: center;">
            <strong>@{all_time_stats['highest_damage_player']}</strong><br>
            {all_time_stats['highest_damage_amount']:,.0f} damage in one battle
        </div>
        """, unsafe_allow_html=True)

    # ========= MAIN CONTENT AREA ========= #
    # Mobile responsive columns
    main_col1, main_col2 = st.columns([2, 3])

    with main_col1:
        # ========= ALL-TIME LEADERBOARD ========= #
        st.markdown('<div class="section-header">🏆 ALL-TIME LEADERBOARD</div>', unsafe_allow_html=True)
        
        # All-time leaderboard type selector
        all_time_leaderboard_type = st.radio(
            "Rank by",
            ["Kills", "Damage"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Get all-time leaderboard data based on selected type
        conn = get_conn()
        cursor = conn.cursor()
        
        if all_time_leaderboard_type == "Kills":
            cursor.execute("""
                SELECT player, 
                       SUM(kills) as total_kills,
                       SUM(damage_dealt) as total_damage,
                       COUNT(DISTINCT date) as battles_fought
                FROM player_stats 
                GROUP BY player 
                ORDER BY total_kills DESC 
                LIMIT 10
            """)
        else:  # Damage
            cursor.execute("""
                SELECT player, 
                       SUM(kills) as total_kills,
                       SUM(damage_dealt) as total_damage,
                       COUNT(DISTINCT date) as battles_fought
                FROM player_stats 
                GROUP BY player 
                ORDER BY total_damage DESC 
                LIMIT 10
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            df = pd.DataFrame(rows, columns=["Player", "Total Kills", "Total Damage", "Battles"])
            # Insert rank column
            df.insert(0, "Rank", range(1, len(df) + 1))
            
            # Format the data
            df['Player'] = df['Player'].apply(lambda x: f"@{x}")
            df['Total Kills'] = df['Total Kills'].apply(lambda x: f"{x:,}")
            df['Total Damage'] = df['Total Damage'].apply(lambda x: f"{x:,.0f}")
            
            # Display as table with mobile wrapper
            with st.container():
                st.markdown('<div class="mobile-table-wrapper">', unsafe_allow_html=True)
                st.table(df.set_index('Rank'))
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No all-time data available.")

    with main_col2:
        # ========= ALL DAILY WINNERS ========= #
        st.markdown('<div class="section-header">🏆 ALL DAILY WINNERS</div>', unsafe_allow_html=True)
        
        winners_df = get_all_daily_winners()
        
        if not winners_df.empty:
            # Format the dataframe for display
            display_winners = winners_df.copy()
            display_winners['Winner'] = display_winners['Winner'].apply(lambda x: f"@{x}")
            
            # Fix date formatting - handle different date formats
            def format_date(date_str):
                if pd.isna(date_str) or date_str is None:
                    return "N/A"
                try:
                    # If it's already in YYYY-MM-DD format
                    if len(str(date_str)) == 10 and str(date_str).count('-') == 2:
                        return str(date_str)
                    # If it's in YYYYMMDD format
                    elif len(str(date_str)) == 8:
                        date_str = str(date_str)
                        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                    else:
                        return str(date_str)
                except:
                    return str(date_str)
            
            display_winners['Date'] = display_winners['Date'].apply(format_date)
            
            # Add battle number column (reverse order - latest battle is #1)
            display_winners.insert(0, 'Battle #', range(len(display_winners), 0, -1))
            
            # Only show rows with actual data
            display_winners = display_winners.dropna(subset=['Winner', 'Date'])
            
            if not display_winners.empty:
                st.dataframe(
                    display_winners.set_index('Battle #'),
                    use_container_width=True,
                    height=400
                )
            else:
                st.info("No valid battle data available.")
        else:
            st.info("No battle data available yet.")

# ========= FIGHTER ANALYSIS SECTION ========= #
elif st.session_state.current_section == "Fighter Analysis":
    st.markdown('<div class="section-header">🔍 ALL-TIME FIGHTER ANALYSIS</div>', unsafe_allow_html=True)
    
    # Get all unique players from all battles
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT player FROM player_stats ORDER BY player ASC")
    all_players = [r[0] for r in cursor.fetchall()]
    conn.close()
    
    if all_players:
        st.markdown(f"**Select a fighter for all-time analysis:** (Found {len(all_players)} total fighters)")
        
        # Player selection
        selected_player = st.selectbox(
            "Select a player",
            ["Type your username:"] + all_players,
            format_func=lambda x: x if x == "Type your username:" else f"@{x}",
            label_visibility="collapsed",
            key="all_time_player_select",
            index=0
        )
        
        if selected_player == "Type your username:":
            selected_player = None
        else:
            st.caption(f"Showing all {len(all_players)} fighters. You can type in the dropdown to search.")
        
        if selected_player:
            # Get all-time stats for the player
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT date) as battles_fought,
                    SUM(kills) as total_kills,
                    SUM(deaths) as total_deaths,
                    SUM(damage_dealt) as total_damage_dealt,
                    SUM(damage_received) as total_damage_received,
                    AVG(kills) as avg_kills,
                    AVG(deaths) as avg_deaths,
                    AVG(damage_dealt) as avg_damage_dealt,
                    AVG(damage_received) as avg_damage_received,
                    MAX(kills) as best_kills,
                    MAX(damage_dealt) as best_damage
                FROM player_stats 
                WHERE player = ?
            """, (selected_player,))
            row = cursor.fetchone()
            conn.close()
            
            if row and row[0] > 0:
                battles_fought, total_kills, total_deaths, total_damage_dealt, total_damage_received, \
                avg_kills, avg_deaths, avg_damage_dealt, avg_damage_received, \
                best_kills, best_damage = row
                
                # Get best rank (lowest rank number from ranking table)
                conn2 = get_conn()
                cursor2 = conn2.cursor()
                cursor2.execute("""
                    SELECT MIN(rank) FROM ranking 
                    WHERE player = ?
                """, (selected_player,))
                best_rank_row = cursor2.fetchone()
                best_rank = best_rank_row[0] if best_rank_row and best_rank_row[0] else None
                conn2.close()
                
                # Player info header
                st.markdown(f"### @{selected_player} - All-Time Stats")
                
                # Quick stats row
                stat_cols = st.columns(4)
                
                with stat_cols[0]:
                    st.metric("Battles", battles_fought)
                
                with stat_cols[1]:
                    total_kd = total_kills / max(total_deaths, 1)
                    st.metric("Total K/D", f"{total_kd:.2f}")
                
                with stat_cols[2]:
                    avg_kd = avg_kills / max(avg_deaths, 1)
                    st.metric("Avg K/D", f"{avg_kd:.2f}")
                
                with stat_cols[3]:
                    efficiency = total_damage_dealt / max(total_damage_received, 1)
                    st.metric("Efficiency", f"{efficiency:.2f}x")
                
                # Detailed stats
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown("#### 💀 Kill Statistics")
                    st.markdown(f"**Total Kills:** {total_kills:,}")
                    st.markdown(f"**Average Kills/Battle:** {avg_kills:.1f}")
                    st.markdown(f"**Best Single Battle:** {best_kills}")
                    st.markdown(f"**Total Deaths:** {total_deaths:,}")
                    st.markdown(f"**Average Deaths/Battle:** {avg_deaths:.1f}")
                
                with detail_col2:
                    st.markdown("#### 💥 Damage Statistics")
                    st.markdown(f"**Total Damage Dealt:** {total_damage_dealt:,.0f}")
                    st.markdown(f"**Average Damage/Battle:** {avg_damage_dealt:,.0f}")
                    st.markdown(f"**Best Single Battle:** {best_damage:,.0f}")
                    st.markdown(f"**Total Damage Received:** {total_damage_received:,.0f}")
                    st.markdown(f"**Average Damage Received/Battle:** {avg_damage_received:,.0f}")
                
                # Performance metrics
                perf_col1, perf_col2 = st.columns(2)
                
                with perf_col1:
                    # Normalize best rank: convert 0 to 1, 1 to 2, etc.
                    if best_rank is not None:
                        normalized_best_rank = best_rank + 1 if best_rank == 0 else best_rank + 1
                        rank_display = f"#{normalized_best_rank}"
                    else:
                        rank_display = "N/A"
                    st.markdown(f"""
                    <div style="background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.3); border-radius: 10px; padding: 15px; text-align: center;">
                        <strong style="color: #FFD700;">Best Rank</strong><br>
                        <span style="font-size: 1.5rem; font-weight: bold;">{rank_display}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with perf_col2:
                    st.markdown(f"""
                    <div style="background: rgba(0,255,255,0.1); border: 1px solid rgba(0,255,255,0.3); border-radius: 10px; padding: 15px; text-align: center;">
                        <strong style="color: #00FFFF;">Damage Efficiency</strong><br>
                        <span style="font-size: 1.5rem; font-weight: bold;">{efficiency:.2f}x</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Battle history
                st.markdown("#### 📊 Battle History")
                conn3 = get_conn()
                cursor3 = conn3.cursor()
                cursor3.execute("""
                    SELECT ps.date, r.rank, ps.kills, ps.deaths, ps.damage_dealt, ps.damage_received
                    FROM player_stats ps
                    LEFT JOIN ranking r ON ps.date = r.date AND ps.player = r.player
                    WHERE ps.player = ?
                    ORDER BY ps.date DESC
                """, (selected_player,))
                history_rows = cursor3.fetchall()
                conn3.close()
                
                if history_rows:
                    history_df = pd.DataFrame(history_rows, columns=["Date", "Rank", "Kills", "Deaths", "Damage Dealt", "Damage Received"])
                    history_df['K/D'] = history_df['Kills'] / history_df['Deaths'].replace(0, 1)
                    history_df['Efficiency'] = history_df['Damage Dealt'] / history_df['Damage Received'].replace(0, 1)
                    
                    # Format the dataframe
                    history_df['Date'] = history_df['Date'].apply(lambda x: str(x))
                    # Normalize ranks: convert 0 to 1, 1 to 2, etc., handle None values
                    history_df['Rank'] = history_df['Rank'].apply(lambda x: f"#{x + 1}" if x is not None and x == 0 else f"#{x + 1}" if x is not None else "N/A")
                    history_df['K/D'] = history_df['K/D'].apply(lambda x: f"{x:.2f}")
                    history_df['Efficiency'] = history_df['Efficiency'].apply(lambda x: f"{x:.2f}x")
                    
                    st.dataframe(
                        history_df,
                        use_container_width=True,
                        height=300
                    )
                else:
                    st.info("No battle history available.")
            else:
                st.error(f"❌ **No all-time stats found for @{selected_player}**")
                st.write("This player may not have participated in any battles, or there might be a data issue.")
    else:
        st.info("⚔️ **No player data available.**")
        st.write("Please check if the database has been populated with battle data.")

# ========= END OF SECTIONS ========= #

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666;">⚔️ The Icon Clash Arena | Follow @theiconclash | New battles daily at 6PM IST</p>',
    unsafe_allow_html=True
)


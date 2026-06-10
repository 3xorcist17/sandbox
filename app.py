import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Formula 1 Racing", page_icon="🏎️", layout="wide")
st.title("Formula 1 Racing 🏎️🏁🚥🏆")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Race & Results",
    "Drivers' Championship",
    "Constructors' Championship",
    "Team & Driver Stats",
    "Driver Upgrades",
    "Season Summary"
])

def calculate_driver_rating(driver):
    points = st.session_state.total_driver_points[driver]
    wins = st.session_state.driver_wins[driver]
    podiums = st.session_state.driver_podiums[driver]
    races = st.session_state.races_completed
    if races == 0:
        return 5.0
    max_possible_points = races * 25
    points_ratio = min(points / max_possible_points, 1.0) if max_possible_points > 0 else 0
    win_ratio = wins / races if races > 0 else 0
    podium_ratio = podiums / races if races > 0 else 0
    rating = (points_ratio * 5.0) + (win_ratio * 3.0) + (podium_ratio * 2.0)
    return min(max(rating, 0.0), 10.0)


def get_current_leaderboard():
    finished_drivers = []
    racing_drivers = []
    dnf_drivers = []

    for driver_info in st.session_state.finish_order:
        finished_drivers.append({
            'driver': driver_info['driver'],
            'team': driver_info['team'],
            'progress': 100,
            'finished': True,
            'dnf': False
        })

    if 'current_race_dnfs' in st.session_state:
        for driver_info in st.session_state.current_race_dnfs:
            dnf_drivers.append({
                'driver': driver_info['driver'],
                'team': driver_info['team'],
                'progress': driver_info.get('dnf_progress', 0),
                'finished': True,
                'dnf': True
            })

    finished_driver_names = [d['driver'] for d in st.session_state.finish_order]
    dnf_driver_names = [d['driver'] for d in st.session_state.get('current_race_dnfs', [])]

    for i, driver_info in enumerate(drivers):
        if driver_info['driver'] not in finished_driver_names and driver_info['driver'] not in dnf_driver_names:
            racing_drivers.append({
                'driver': driver_info['driver'],
                'team': driver_info['team'],
                'progress': st.session_state.progress_values[i],
                'finished': False,
                'dnf': False,
                'index': i
            })

    racing_drivers.sort(key=lambda x: x['progress'], reverse=True)
    return finished_drivers + racing_drivers + dnf_drivers


def simulate_championship(n_simulations=1000):
    """Monte Carlo simulation for championship probability."""
    races_done = st.session_state.races_completed
    TOTAL_RACES = 24
    races_left = max(0, TOTAL_RACES - races_done)

    if races_left == 0:
        # Season over — winner is whoever leads
        sorted_standings = sorted(st.session_state.total_driver_points.items(), key=lambda x: x[1], reverse=True)
        results = {d: 0.0 for d, _ in sorted_standings}
        results[sorted_standings[0][0]] = 100.0
        return results, races_left

    points_system = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
    max_remaining = sum(points_system.values()) + 1  # +1 for fastest lap if added later
    driver_list = [d['driver'] for d in drivers]

    # Filter: only drivers who can mathematically still win
    leader_points = max(st.session_state.total_driver_points.values()) if st.session_state.total_driver_points else 0
    max_possible = races_left * 26  # 25 + potential fastest lap point

    win_counts = {d: 0 for d in driver_list}

    for _ in range(n_simulations):
        sim_points = dict(st.session_state.total_driver_points)

        for _race in range(races_left):
            shuffled = driver_list.copy()
            random.shuffle(shuffled)
            for pos, drv in enumerate(shuffled, 1):
                sim_points[drv] = sim_points.get(drv, 0) + points_system.get(pos, 0)

        champion = max(sim_points, key=lambda d: sim_points[d])
        win_counts[champion] += 1

    probabilities = {d: (win_counts[d] / n_simulations) * 100 for d in driver_list}
    return probabilities, races_left


st.markdown("""
    <style>
    div[data-testid="stTable"] { width: 100% !important; }
    .leaderboard {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        max-height: 600px;
        overflow-y: auto;
    }
    .leaderboard-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 12px;
        margin: 4px 0;
        background-color: white;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
        font-family: monospace;
        font-size: 14px;
        color: #000000;
    }
    .position-1 { border-left-color: #FFD700; }
    .position-2 { border-left-color: #C0C0C0; }
    .position-3 { border-left-color: #CD7F32; }
    .race-container {
        background: linear-gradient(135deg, #e74c3c 0%, #000000 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        color: #000000;
    }
    .rating-card {
        background: linear-gradient(135deg, #e74c3c 0%, #000000 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: #000000;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    .rating-card-gold { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #000000; }
    .rating-card-silver { background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%); color: #000000; }
    .rating-card-bronze { background: linear-gradient(135deg, #CD7F32 0%, #B8860B 100%); color: #000000; }
    .rating-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
    .rating-score { font-size: 2.5em; font-weight: bold; text-align: right; color: #000000; }
    .rating-details { display: flex; justify-content: space-between; font-size: 0.9em; opacity: 0.9; color: #000000; }
    .driver-name { font-size: 1.3em; font-weight: bold; color: #000000; }
    .team-name { font-size: 1em; opacity: 0.8; color: #000000; }
    .driver-row {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border-left: 5px solid var(--driver-color);
    }
    .driver-row:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15); }
    .driver-info { min-width: 150px; display: flex; flex-direction: column; }
    .progress-container { flex: 1; margin: 0 20px; position: relative; }
    .custom-progress-bar {
        width: 100%; height: 25px;
        background: linear-gradient(90deg, #ecf0f1 0%, #bdc3c7 100%);
        border-radius: 15px; overflow: hidden; position: relative;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--driver-color) 0%, var(--driver-color-light) 100%);
        border-radius: 15px; position: relative;
        transition: width 0.5s ease-out;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .progress-fill::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 50%;
        background: linear-gradient(90deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.3) 100%);
        border-radius: 15px 15px 0 0;
    }
    .progress-text {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        font-weight: bold; font-size: 12px; color: #000000;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3); z-index: 10;
    }
    .progress-status { min-width: 100px; text-align: right; display: flex; flex-direction: column; align-items: flex-end; }
    .status-text { font-weight: bold; font-size: 14px; color: #000000; }
    .status-subtext { font-size: 11px; color: #000000; margin-top: 2px; }
    .finished-row { background: rgba(255, 255, 255, 0.95); color: #000000; }
    .dnf-row {
        background: rgba(255, 80, 80, 0.15) !important;
        border-left: 5px solid #cc0000 !important;
        opacity: 0.85;
    }
    .position-indicator { font-size: 18px; font-weight: bold; margin-right: 10px; min-width: 40px; text-align: center; color: #000000; }
    .racing-animation { animation: pulse 2s infinite; }
    @keyframes pulse {
        0% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
        50% { box-shadow: 0 6px 25px rgba(102, 126, 234, 0.3); }
        100% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
    }
    .speed-indicator {
        position: absolute; right: 10px; top: 50%; transform: translateY(-50%);
        background: rgba(0, 0, 0, 0.1); border-radius: 10px;
        padding: 2px 8px; font-size: 10px; font-weight: bold; color: #000000;
    }
    .prob-bar-container {
        background: #f0f2f6; border-radius: 8px; height: 22px;
        overflow: hidden; margin: 3px 0; position: relative;
    }
    .prob-bar-fill {
        height: 100%; border-radius: 8px;
        display: flex; align-items: center; padding-left: 8px;
        font-size: 11px; font-weight: bold; color: #000;
        transition: width 0.6s ease;
    }
    </style>
""", unsafe_allow_html=True)

teams_drivers = {
    "Alpine": ["Gas", "Doo"],
    "Aston Martin": ["Alo", "Str"],
    "Audi": ["Hul", "Bor"],
    "Cadillac": ["Bot", "Per"],
    "Ferrari": ["Lec", "Ham"],
    "Haas": ["Oco", "Bea"],
    "McLaren": ["Nor", "Pia"],
    "Mercedes": ["Rus", "Ant"],
    "Racing Bulls": ["Law", "Lin"],
    "Red Bull": ["Ver", "Had"],
    "Williams": ["Sai", "Alb"]
}

team_colors = {
    "Alpine": "hsl(308, 100%, 34.4%)",
    "Aston Martin": "hsl(185, 99.6%, 31.7%)",
    "Audi": "hsl(0, 85%, 35%)",
    "Cadillac": "hsl(0, 0%, 10%)",
    "Ferrari": "hsl(0, 99.6%, 39.7%)",
    "Haas": "hsl(0, 99.6%, 28.2%)",
    "McLaren": "hsl(33, 99.6%, 42.4%)",
    "Mercedes": "hsl(165, 99.6%, 9.4%)",
    "Racing Bulls": "hsl(198, 99.6%, 80.3%)",
    "Red Bull": "hsl(247, 99.6%, 24.1%)",
    "Williams": "hsl(201, 99.6%, 32.2%)"
}

driver_colors = {}
for team, drivers_list in teams_drivers.items():
    color_parts = team_colors[team].replace('hsl(', '').replace(')', '').split(',')
    hue = float(color_parts[0])
    saturation = float(color_parts[1].replace('%', ''))
    lightness = float(color_parts[2].replace('%', ''))
    driver_colors[drivers_list[0]] = f"hsl({hue}, {saturation}%, {min(100, lightness + 5)}%)"
    driver_colors[drivers_list[1]] = f"hsl({hue}, {saturation}%, {max(0, lightness - 5)}%)"

drivers = []
for team, driver_list in teams_drivers.items():
    for driver in driver_list:
        drivers.append({"driver": driver, "team": team})

points_system = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# ── Session state init ──────────────────────────────────────────────────────────
if 'progress_values' not in st.session_state:
    st.session_state.progress_values = [0] * 22
if 'finish_order' not in st.session_state:
    st.session_state.finish_order = []
if 'current_race_dnfs' not in st.session_state:
    st.session_state.current_race_dnfs = []
if 'total_team_points' not in st.session_state:
    st.session_state.total_team_points = {team: 0 for team in teams_drivers}
if 'total_driver_points' not in st.session_state:
    st.session_state.total_driver_points = {driver['driver']: 0 for driver in drivers}
if 'team_wins' not in st.session_state:
    st.session_state.team_wins = {team: 0 for team in teams_drivers}
if 'team_podiums' not in st.session_state:
    st.session_state.team_podiums = {team: 0 for team in teams_drivers}
if 'driver_wins' not in st.session_state:
    st.session_state.driver_wins = {driver['driver']: 0 for driver in drivers}
if 'driver_podiums' not in st.session_state:
    st.session_state.driver_podiums = {driver['driver']: 0 for driver in drivers}
if 'driver_dnf_count' not in st.session_state:
    st.session_state.driver_dnf_count = {driver['driver']: 0 for driver in drivers}
if 'team_dnf_count' not in st.session_state:
    st.session_state.team_dnf_count = {team: 0 for team in teams_drivers}
if 'race_finished' not in st.session_state:
    st.session_state.race_finished = False
if 'races_completed' not in st.session_state:
    st.session_state.races_completed = 0
if 'race_summaries' not in st.session_state:
    st.session_state.race_summaries = []
if 'race_started' not in st.session_state:
    st.session_state.race_started = False
if 'driver_headstarts' not in st.session_state:
    st.session_state.driver_headstarts = {driver['driver']: 1 for driver in drivers}
if 'team_reliability' not in st.session_state:
    # Default reliability: 5% DNF chance per race per driver
    st.session_state.team_reliability = {team: 5 for team in teams_drivers}
if 'complete_race_history' not in st.session_state:
    st.session_state.complete_race_history = []


def roll_dnfs_for_race():
    """Determine which drivers DNF before the race starts."""
    dnf_list = []
    for driver_info in drivers:
        driver = driver_info['driver']
        team = driver_info['team']
        reliability_pct = st.session_state.team_reliability.get(team, 5)
        if random.randint(1, 100) <= reliability_pct:
            dnf_list.append(driver_info)
    return dnf_list


# ── TAB 1: Race & Results ───────────────────────────────────────────────────────
with tab1:
    if st.button("🏁 Start Race"):
        st.session_state.progress_values = [0] * 22
        for i, driver_info in enumerate(drivers):
            driver = driver_info['driver']
            headstart = st.session_state.driver_headstarts.get(driver, 1)
            st.session_state.progress_values[i] = min(100, headstart)
        st.session_state.finish_order = []
        st.session_state.race_finished = False
        st.session_state.race_started = True
        # Roll DNFs at race start
        st.session_state.current_race_dnfs = roll_dnfs_for_race()
        # Assign a DNF progress point (where they retire)
        for dnf_driver in st.session_state.current_race_dnfs:
            dnf_driver['dnf_progress'] = random.randint(5, 75)
        st.rerun()

    if st.session_state.race_started and not st.session_state.race_finished:
        # Show DNF warning if any
        if st.session_state.current_race_dnfs:
            dnf_names = ", ".join([d['driver'] for d in st.session_state.current_race_dnfs])
            st.error(f"💥 **Mechanical Failures This Race:** {dnf_names} — These drivers will retire!")

        st.markdown('<div class="race-container">', unsafe_allow_html=True)
        st.markdown("### 🏎️ Live Race Progress")

        progress_placeholders = []
        current_leaderboard = get_current_leaderboard()

        dnf_names_set = {d['driver'] for d in st.session_state.current_race_dnfs}

        for pos, driver_info in enumerate(current_leaderboard, 1):
            progress = driver_info['progress']
            driver = driver_info['driver']
            team = driver_info['team']
            is_finished = driver_info.get('finished', False)
            is_dnf = driver_info.get('dnf', False)

            base_color = driver_colors.get(driver, '#3498db')
            if base_color.startswith('hsl'):
                hsl_parts = base_color.replace('hsl(', '').replace(')', '').split(',')
                hue = hsl_parts[0].strip()
                saturation = hsl_parts[1].strip()
                lightness = float(hsl_parts[2].replace('%', '').strip())
                lighter_lightness = min(95, lightness + 20)
                light_color = f"hsl({hue}, {saturation}, {lighter_lightness}%)"
            else:
                light_color = base_color

            if is_dnf:
                position_emoji = "💥"
                status_text = "💥 RETIRED"
                status_subtext = "Mechanical Failure"
                row_class = "finished-row dnf-row"
                animation_class = ""
                dnf_progress = driver_info.get('progress', 0)
                progress_html = f'''
                <div class="driver-row {row_class}"
                     style="--driver-color: #cc0000; --driver-color-light: #ff4444;">
                    <div class="position-indicator">{position_emoji}</div>
                    <div class="driver-info">
                        <div class="driver-name" style="color:#cc0000;">{driver}</div>
                        <div class="team-name">{team}</div>
                    </div>
                    <div class="progress-container">
                        <div class="custom-progress-bar">
                            <div class="progress-fill" style="width: {dnf_progress}%; background: linear-gradient(90deg, #cc0000, #ff4444);">
                            </div>
                            <div class="progress-text">DNF @ {dnf_progress}%</div>
                        </div>
                    </div>
                    <div class="progress-status">
                        <div class="status-text" style="color:#cc0000;">{status_text}</div>
                        <div class="status-subtext">{status_subtext}</div>
                    </div>
                </div>'''
            elif is_finished:
                position_emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
                status_text = "🏁 FINISHED"
                status_subtext = "Race Complete"
                row_class = "finished-row"
                animation_class = ""
                progress_html = f'''
                <div class="driver-row {row_class} {animation_class}"
                     style="--driver-color: {base_color}; --driver-color-light: {light_color};">
                    <div class="position-indicator">{position_emoji}</div>
                    <div class="driver-info">
                        <div class="driver-name">{driver}</div>
                        <div class="team-name">{team}</div>
                    </div>
                    <div class="progress-container">
                        <div class="custom-progress-bar">
                            <div class="progress-fill" style="width: 100%;"></div>
                            <div class="progress-text">100%</div>
                        </div>
                    </div>
                    <div class="progress-status">
                        <div class="status-text">{status_text}</div>
                        <div class="status-subtext">{status_subtext}</div>
                    </div>
                </div>'''
            else:
                position_emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
                status_text = f"{progress:.1f}%"
                status_subtext = "Racing..."
                row_class = ""
                animation_class = "racing-animation" if progress > 50 else ""
                speed_kmh = int(200 + (progress / 100) * 150 + (pos * -5))
                progress_html = f'''
                <div class="driver-row {row_class} {animation_class}"
                     style="--driver-color: {base_color}; --driver-color-light: {light_color};">
                    <div class="position-indicator">{position_emoji}</div>
                    <div class="driver-info">
                        <div class="driver-name">{driver}</div>
                        <div class="team-name">{team}</div>
                    </div>
                    <div class="progress-container">
                        <div class="custom-progress-bar">
                            <div class="progress-fill" style="width: {progress}%;">
                                <div class="speed-indicator">{speed_kmh} km/h</div>
                            </div>
                            <div class="progress-text">{progress:.1f}%</div>
                        </div>
                    </div>
                    <div class="progress-status">
                        <div class="status-text">{status_text}</div>
                        <div class="status-subtext">{status_subtext}</div>
                    </div>
                </div>'''

            placeholder = st.empty()
            placeholder.markdown(progress_html, unsafe_allow_html=True)
            progress_placeholders.append((placeholder, driver_info))

        st.markdown('</div>', unsafe_allow_html=True)
        time.sleep(1)

        dnf_driver_names = {d['driver'] for d in st.session_state.current_race_dnfs}
        dnf_retire_points = {d['driver']: d.get('dnf_progress', 0) for d in st.session_state.current_race_dnfs}
        active_drivers_count = 22 - len(dnf_driver_names)

        while (st.session_state.race_started and
               any(v < 100 for i, v in enumerate(st.session_state.progress_values)
                   if drivers[i]['driver'] not in dnf_driver_names) and
               not st.session_state.race_finished):

            for i in range(22):
                drv_name = drivers[i]['driver']
                if drv_name in dnf_driver_names:
                    # Animate DNF drivers up to their retirement point then stop
                    retire_at = dnf_retire_points.get(drv_name, 0)
                    if st.session_state.progress_values[i] < retire_at:
                        st.session_state.progress_values[i] = min(retire_at,
                            st.session_state.progress_values[i] + random.randint(0, 3))
                    continue
                if st.session_state.progress_values[i] < 100:
                    increment = random.randint(0, 4)
                    st.session_state.progress_values[i] = min(100, st.session_state.progress_values[i] + increment)
                    if (st.session_state.progress_values[i] == 100 and
                            drv_name not in [d['driver'] for d in st.session_state.finish_order]):
                        st.session_state.finish_order.append(drivers[i])

            current_leaderboard = get_current_leaderboard()

            for idx, (placeholder, _) in enumerate(progress_placeholders):
                if idx < len(current_leaderboard):
                    driver_info = current_leaderboard[idx]
                    pos = idx + 1
                    progress = driver_info['progress']
                    driver = driver_info['driver']
                    team = driver_info['team']
                    is_finished = driver_info.get('finished', False)
                    is_dnf = driver_info.get('dnf', False)

                    base_color = driver_colors.get(driver, '#3498db')
                    if base_color.startswith('hsl'):
                        hsl_parts = base_color.replace('hsl(', '').replace(')', '').split(',')
                        hue = hsl_parts[0].strip()
                        saturation = hsl_parts[1].strip()
                        lightness = float(hsl_parts[2].replace('%', '').strip())
                        lighter_lightness = min(95, lightness + 20)
                        light_color = f"hsl({hue}, {saturation}, {lighter_lightness}%)"
                    else:
                        light_color = base_color

                    if is_dnf:
                        dnf_progress = driver_info.get('progress', 0)
                        progress_html = f'''
                        <div class="driver-row finished-row dnf-row"
                             style="--driver-color: #cc0000; --driver-color-light: #ff4444;">
                            <div class="position-indicator">💥</div>
                            <div class="driver-info">
                                <div class="driver-name" style="color:#cc0000;">{driver}</div>
                                <div class="team-name">{team}</div>
                            </div>
                            <div class="progress-container">
                                <div class="custom-progress-bar">
                                    <div class="progress-fill" style="width: {dnf_progress}%; background: linear-gradient(90deg, #cc0000, #ff4444);"></div>
                                    <div class="progress-text">DNF @ {dnf_progress}%</div>
                                </div>
                            </div>
                            <div class="progress-status">
                                <div class="status-text" style="color:#cc0000;">💥 RETIRED</div>
                                <div class="status-subtext">Mechanical Failure</div>
                            </div>
                        </div>'''
                    elif is_finished:
                        points_earned = points_system.get(pos, 0)
                        position_emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
                        progress_html = f'''
                        <div class="driver-row finished-row"
                             style="--driver-color: {base_color}; --driver-color-light: {light_color};">
                            <div class="position-indicator">{position_emoji}</div>
                            <div class="driver-info">
                                <div class="driver-name">{driver}</div>
                                <div class="team-name">{team}</div>
                            </div>
                            <div class="progress-container">
                                <div class="custom-progress-bar">
                                    <div class="progress-fill" style="width: 100%;"></div>
                                    <div class="progress-text">100%</div>
                                </div>
                            </div>
                            <div class="progress-status">
                                <div class="status-text">🏁 FINISHED</div>
                                <div class="status-subtext">{points_earned} pts</div>
                            </div>
                        </div>'''
                    else:
                        position_emoji = f"P{pos}"
                        speed_kmh = int(max(180, min(350, 200 + (progress / 100) * 150 + (pos * -3) + random.randint(-10, 10))))
                        animation_class = "racing-animation" if progress > 70 else ""
                        progress_html = f'''
                        <div class="driver-row {animation_class}"
                             style="--driver-color: {base_color}; --driver-color-light: {light_color};">
                            <div class="position-indicator">{position_emoji}</div>
                            <div class="driver-info">
                                <div class="driver-name">{driver}</div>
                                <div class="team-name">{team}</div>
                            </div>
                            <div class="progress-container">
                                <div class="custom-progress-bar">
                                    <div class="progress-fill" style="width: {progress}%;">
                                        <div class="speed-indicator">{speed_kmh} km/h</div>
                                    </div>
                                    <div class="progress-text">{progress:.1f}%</div>
                                </div>
                            </div>
                            <div class="progress-status">
                                <div class="status-text">{progress:.1f}%</div>
                                <div class="status-subtext">Racing...</div>
                            </div>
                        </div>'''

                    placeholder.markdown(progress_html, unsafe_allow_html=True)

            # Race ends when all non-DNF drivers finish
            finished_non_dnf = [d for d in st.session_state.finish_order if d['driver'] not in dnf_driver_names]
            if len(finished_non_dnf) == active_drivers_count:
                st.session_state.race_finished = True
                st.session_state.races_completed += 1
                st.session_state.race_started = False

                # Build complete race results including DNFs at the bottom
                complete_results = []
                for pos, driver_info in enumerate(st.session_state.finish_order, 1):
                    complete_results.append((pos, driver_info['driver'], driver_info['team']))
                dnf_start_pos = len(st.session_state.finish_order) + 1
                for driver_info in st.session_state.current_race_dnfs:
                    complete_results.append(("DNF", driver_info['driver'], driver_info['team']))

                complete_race_results = {
                    "race_number": st.session_state.races_completed,
                    "results": complete_results
                }
                st.session_state.complete_race_history.append(complete_race_results)

                # Award points (only finishers, not DNFs)
                for position, driver_info in enumerate(st.session_state.finish_order, 1):
                    if position <= 10:
                        pts = points_system.get(position, 0)
                        st.session_state.total_driver_points[driver_info['driver']] += pts
                        st.session_state.total_team_points[driver_info['team']] += pts
                    if position == 1:
                        st.session_state.driver_wins[driver_info['driver']] += 1
                        st.session_state.team_wins[driver_info['team']] += 1
                    if position <= 3:
                        st.session_state.driver_podiums[driver_info['driver']] += 1
                        st.session_state.team_podiums[driver_info['team']] += 1

                # Track DNF counts
                for dnf_info in st.session_state.current_race_dnfs:
                    st.session_state.driver_dnf_count[dnf_info['driver']] = \
                        st.session_state.driver_dnf_count.get(dnf_info['driver'], 0) + 1
                    st.session_state.team_dnf_count[dnf_info['team']] = \
                        st.session_state.team_dnf_count.get(dnf_info['team'], 0) + 1

                if len(st.session_state.finish_order) >= 3:
                    race_summary = {
                        "Race": st.session_state.races_completed,
                        "P1": f"{st.session_state.finish_order[0]['driver']} ({st.session_state.finish_order[0]['team']})",
                        "P2": f"{st.session_state.finish_order[1]['driver']} ({st.session_state.finish_order[1]['team']})",
                        "P3": f"{st.session_state.finish_order[2]['driver']} ({st.session_state.finish_order[2]['team']})",
                        "DNFs": len(st.session_state.current_race_dnfs)
                    }
                    st.session_state.race_summaries.append(race_summary)
                break

            time.sleep(1)

    if st.session_state.race_finished:
        st.markdown("---")

        # Show DNF summary for completed race
        if st.session_state.current_race_dnfs:
            dnf_names_display = ", ".join([f"**{d['driver']}** ({d['team']})" for d in st.session_state.current_race_dnfs])
            st.error(f"💥 **Race Retirements:** {dnf_names_display}")

        if len(st.session_state.finish_order) >= 3:
            st.markdown("### 🏆 Race Podium")
            podium_positions = [
                (st.session_state.finish_order[0], 1, "🥇", "rating-card-gold", "1st"),
                (st.session_state.finish_order[1], 2, "🥈", "rating-card-silver", "2nd"),
                (st.session_state.finish_order[2], 3, "🥉", "rating-card-bronze", "3rd")
            ]
            for driver_info, position, medal, card_class, position_text in podium_positions:
                pts = points_system.get(position, 0)
                driver_name = driver_info['driver']
                team_name = driver_info['team']
                total_points = st.session_state.total_driver_points[driver_name]
                total_wins = st.session_state.driver_wins[driver_name]
                total_podiums = st.session_state.driver_podiums[driver_name]
                st.markdown(f'''
                <div class="rating-card {card_class}">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">{medal} {position_text} - {driver_name}</div>
                            <div class="team-name">{team_name}</div>
                        </div>
                        <div class="rating-score">{pts} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Championship: {total_points} pts</span>
                        <span>Wins: {total_wins}</span>
                        <span>Podiums: {total_podiums}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="race-container">', unsafe_allow_html=True)
        st.markdown("### 🏁 Race Summary")
        st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
        if st.session_state.race_summaries:
            st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
            for idx, summary in enumerate(st.session_state.race_summaries):
                dnf_text = f" | 💥 {summary.get('DNFs', 0)} DNF(s)" if summary.get('DNFs', 0) > 0 else ""
                st.markdown(f'''
                <div class="leaderboard-item">
                    <span>Race {summary['Race']}</span>
                    <span>P1: {summary['P1']} | P2: {summary['P2']} | P3: {summary['P3']}{dnf_text}</span>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 2: Drivers' Championship + Probability Calculator ──────────────────────
with tab2:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏆 Drivers' Championship Hub")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")

    if st.session_state.races_completed > 0:
        sorted_driver_standings = sorted(
            st.session_state.total_driver_points.items(), key=lambda x: x[1], reverse=True)

        # ── Championship Leadership ─────────────────────────────────────────────
        st.markdown("#### 👑 Championship Leadership")
        leader_col1, leader_col2, leader_col3 = st.columns(3)
        for pos, (driver, points) in enumerate(sorted_driver_standings[:3], 1):
            team = next(d['team'] for d in drivers if d['driver'] == driver)
            wins = st.session_state.driver_wins[driver]
            podiums = st.session_state.driver_podiums[driver]
            rating = calculate_driver_rating(driver)
            card_class = "rating-card-gold" if pos == 1 else "rating-card-silver" if pos == 2 else "rating-card-bronze"
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉"
            position_text = "LEADER" if pos == 1 else f"+{sorted_driver_standings[0][1] - points}"
            col = leader_col1 if pos == 1 else leader_col2 if pos == 2 else leader_col3
            with col:
                st.markdown(f'''
                <div class="rating-card {card_class}">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">{medal} {driver}</div>
                            <div class="team-name">{team} • {position_text}</div>
                        </div>
                        <div class="rating-score">{points}</div>
                    </div>
                    <div class="rating-details">
                        <span>🏆 {wins}W • 🏅 {podiums}P</span>
                        <span>⭐ {rating:.1f}/10</span>
                        <span>📊 {points/st.session_state.races_completed:.1f} avg</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")

        # ── Championship Probability Calculator ────────────────────────────────
        st.markdown("#### 🎲 Championship Probability Calculator")
        st.markdown("*Monte Carlo simulation — 1,000 seasons simulated to estimate each driver's title chances*")

        TOTAL_RACES = 24
        races_left = max(0, TOTAL_RACES - st.session_state.races_completed)

        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("🏁 Races Done", st.session_state.races_completed)
        with col_info2:
            st.metric("📅 Races Remaining", races_left)
        with col_info3:
            max_pts_left = races_left * 25
            st.metric("💎 Max Points Left", max_pts_left)

        if races_left == 0:
            st.info("🏆 Season Complete! The championship has been decided.")
        else:
            with st.spinner("Running 1,000 championship simulations..."):
                probs, _ = simulate_championship(1000)

            # Sort by probability descending
            sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)

            # Split: contenders (>0%) vs mathematically eliminated (0%)
            contenders = [(d, p) for d, p in sorted_probs if p > 0]
            eliminated = [(d, p) for d, p in sorted_probs if p == 0]

            if contenders:
                st.markdown("##### 🏆 Title Contenders")
                prob_col1, prob_col2 = st.columns([2, 1])

                with prob_col1:
                    for driver, prob in contenders:
                        team = next(dr['team'] for dr in drivers if dr['driver'] == driver)
                        bar_color = driver_colors.get(driver, '#3498db')
                        current_pts = st.session_state.total_driver_points[driver]
                        gap_to_leader = sorted_driver_standings[0][1] - current_pts

                        # Probability tier label
                        if prob >= 60:
                            tier = "🔥 FAVOURITE"
                            tier_color = "#FFD700"
                        elif prob >= 30:
                            tier = "⚡ CONTENDER"
                            tier_color = "#FFA500"
                        elif prob >= 10:
                            tier = "🎯 OUTSIDE CHANCE"
                            tier_color = "#4CAF50"
                        else:
                            tier = "🌱 LONGSHOT"
                            tier_color = "#90CAF9"

                        st.markdown(f'''
                        <div style="background: rgba(255,255,255,0.95); border-radius: 10px;
                                    padding: 12px 15px; margin: 6px 0;
                                    border-left: 5px solid {bar_color};
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <div>
                                    <span style="font-weight: bold; font-size: 15px; color: #000;">{driver}</span>
                                    <span style="font-size: 12px; color: #555; margin-left: 8px;">{team}</span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <span style="background: {tier_color}; color: #000; border-radius: 6px;
                                                 padding: 2px 8px; font-size: 11px; font-weight: bold;">{tier}</span>
                                    <span style="font-size: 20px; font-weight: bold; color: #000;">{prob:.1f}%</span>
                                </div>
                            </div>
                            <div class="prob-bar-container">
                                <div class="prob-bar-fill" style="width: {prob}%; background: linear-gradient(90deg, {bar_color}, {bar_color}88);">
                                    {prob:.1f}%
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 11px;
                                        color: #555; margin-top: 5px;">
                                <span>📊 {current_pts} pts</span>
                                <span>{'🏆 LEADER' if gap_to_leader == 0 else f'Gap: -{gap_to_leader} pts'}</span>
                                <span>Max remaining: {current_pts + races_left * 25} pts</span>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                with prob_col2:
                    # Donut chart of probabilities
                    top_for_chart = contenders[:8]
                    if len(contenders) > 8:
                        others_prob = sum(p for _, p in contenders[8:])
                        top_for_chart = top_for_chart + [("Others", others_prob)]

                    labels = [d for d, _ in top_for_chart]
                    values = [p for _, p in top_for_chart]
                    colors_chart = [driver_colors.get(d, '#888') for d in labels]

                    fig_prob = go.Figure(go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.55,
                        marker=dict(colors=colors_chart, line=dict(color='#fff', width=2)),
                        textinfo='label+percent',
                        textfont=dict(size=11, color='black'),
                        showlegend=False
                    ))
                    fig_prob.update_layout(
                        height=340,
                        margin=dict(l=10, r=10, t=30, b=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        annotations=[dict(
                            text=f"<b>{races_left}</b><br>races<br>left",
                            x=0.5, y=0.5, font_size=14,
                            font_color='black', showarrow=False
                        )]
                    )
                    st.plotly_chart(fig_prob, use_container_width=True)

            if eliminated:
                with st.expander(f"❌ Mathematically Eliminated ({len(eliminated)} drivers)"):
                    elim_text = ", ".join([d for d, _ in eliminated])
                    st.markdown(f'''
                    <div style="background: rgba(255,100,100,0.1); border-radius: 8px; padding: 12px;
                                border-left: 4px solid #cc0000; color: #000;">
                        <strong>Cannot win the championship:</strong><br>
                        <span style="font-size: 13px;">{elim_text}</span><br><br>
                        <span style="font-size: 12px; opacity: 0.7;">
                            Even winning every remaining race would not give them enough points to overtake the leader.
                        </span>
                    </div>
                    ''', unsafe_allow_html=True)

        st.markdown("---")

        # ── Championship Battle Bar Chart ──────────────────────────────────────
        st.markdown("#### 📊 Championship Battle")
        top_drivers = sorted_driver_standings[:22]
        driver_chart_data = []
        for pos, (driver, points) in enumerate(top_drivers, 1):
            team = next(d['team'] for d in drivers if d['driver'] == driver)
            wins = st.session_state.driver_wins[driver]
            podiums = st.session_state.driver_podiums[driver]
            driver_chart_data.append({
                "Driver": driver,
                "Full_Name": f"P{pos} - {driver}",
                "Points": points,
                "Team": team,
                "Wins": wins,
                "Podiums": podiums,
                "Position": pos,
                "Championship_Gap": sorted_driver_standings[0][1] - points
            })

        if driver_chart_data:
            driver_df_chart = pd.DataFrame(driver_chart_data)
            fig = px.bar(
                driver_df_chart, x="Points", y="Full_Name", color="Team",
                text="Points", color_discrete_map=team_colors, orientation='h',
                title="Championship Standings - Points Battle"
            )
            fig.update_traces(
                textposition="outside", texttemplate="%{text} pts",
                marker_line_width=3, marker_line_color="rgba(0,0,0,0.4)",
                textfont=dict(size=12, color="black")
            )
            fig.update_layout(
                height=750, xaxis_title="Championship Points", yaxis_title="",
                title={'text': "Championship Standings - Points Battle", 'x': 0.5,
                       'xanchor': 'center', 'font': {'size': 18, 'color': '#2c3e50'}},
                plot_bgcolor='rgba(248, 249, 250, 0.95)',
                paper_bgcolor='rgba(248, 249, 250, 0.95)',
                xaxis=dict(gridcolor='rgba(128,128,128,0.2)', gridwidth=1, showgrid=True,
                           zeroline=True, zerolinecolor='rgba(128,128,128,0.4)', zerolinewidth=2,
                           tickfont=dict(size=11, color='#2c3e50'),
                           title_font=dict(size=14, color='#2c3e50')),
                yaxis=dict(categoryorder='total ascending',
                           tickfont=dict(size=11, color='#2c3e50'), showgrid=False),
                margin=dict(l=20, r=60, t=60, b=40), showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
            with stats_col1:
                total_points = sum(st.session_state.total_driver_points.values())
                st.metric("🏆 Total Points", total_points)
            with stats_col2:
                total_winners = len([d for d in st.session_state.driver_wins.values() if d > 0])
                st.metric("🏁 Race Winners", total_winners)
            with stats_col3:
                leader_dominance = (sorted_driver_standings[0][1] / total_points * 100) if total_points > 0 else 0
                st.metric("👑 Leader Share", f"{leader_dominance:.1f}%")
            with stats_col4:
                total_dnfs_season = sum(st.session_state.driver_dnf_count.values())
                st.metric("💥 Total DNFs", total_dnfs_season)

        st.markdown("---")

        # ── Race Results Table ─────────────────────────────────────────────────
        if (st.session_state.races_completed > 0 and
                len(st.session_state.complete_race_history) > 0):
            st.markdown("#### 📋 Race Results Table")
            st.markdown("*Complete finishing positions — DNF shown in red*")

            table_data = []
            for driver_info in drivers:
                driver = driver_info['driver']
                team = driver_info['team']
                row_data = {'Driver': driver, 'Team': team}
                for race_data in st.session_state.complete_race_history:
                    race_num = race_data['race_number']
                    position = None
                    for pos, race_driver, _ in race_data['results']:
                        if race_driver == driver:
                            position = pos
                            break
                    row_data[f'Race {race_num}'] = position if position is not None else "DNF"
                table_data.append(row_data)

            final_standings = sorted(st.session_state.total_driver_points.items(),
                                     key=lambda x: x[1], reverse=True)
            driver_order = [d for d, _ in final_standings]
            ordered_table_data = []
            for drv in driver_order:
                drv_data = next((d for d in table_data if d['Driver'] == drv), None)
                if drv_data:
                    ordered_table_data.append(drv_data)

            if ordered_table_data:
                df = pd.DataFrame(ordered_table_data)
                df.index = df.index + 1

                def style_position(val):
                    if isinstance(val, int):
                        if val == 1:
                            return 'background-color: #FFD700; color: #000000; font-weight: bold;'
                        elif val == 2:
                            return 'background-color: #C0C0C0; color: #000000; font-weight: bold;'
                        elif val == 3:
                            return 'background-color: #CD7F32; color: #000000; font-weight: bold;'
                        elif val <= 10:
                            return 'background-color: #E6F3FF; color: #000000;'
                        else:
                            return 'background-color: #FFF0E6; color: #000000;'
                    elif val == "DNF":
                        return 'background-color: #FF4444; color: #ffffff; font-weight: bold;'
                    return ''

                race_columns = [col for col in df.columns if col.startswith('Race ')]
                if race_columns:
                    styled_df = df.style.map(style_position, subset=race_columns)
                    table_height = len(df) * 35 + 50
                    st.dataframe(styled_df, use_container_width=True, height=table_height)

        st.markdown("---")

        # ── Teammate Battles ───────────────────────────────────────────────────
        st.markdown("#### 🤝 Constructor Battles & Teammate Analysis")
        battle_cols = st.columns(2)
        teams_processed = set()
        col_idx = 0

        for team, team_drivers_list in teams_drivers.items():
            if team not in teams_processed and col_idx < len(battle_cols):
                driver1, driver2 = team_drivers_list
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                driver1_wins = st.session_state.driver_wins[driver1]
                driver2_wins = st.session_state.driver_wins[driver2]
                driver1_podiums = st.session_state.driver_podiums[driver1]
                driver2_podiums = st.session_state.driver_podiums[driver2]

                if driver1_points >= driver2_points:
                    leader, trailer = driver1, driver2
                    leader_stats = {'points': driver1_points, 'wins': driver1_wins, 'podiums': driver1_podiums}
                    trailer_stats = {'points': driver2_points, 'wins': driver2_wins, 'podiums': driver2_podiums}
                else:
                    leader, trailer = driver2, driver1
                    leader_stats = {'points': driver2_points, 'wins': driver2_wins, 'podiums': driver2_podiums}
                    trailer_stats = {'points': driver1_points, 'wins': driver1_wins, 'podiums': driver1_podiums}

                gap = leader_stats['points'] - trailer_stats['points']
                total_team_points = driver1_points + driver2_points

                with battle_cols[col_idx]:
                    st.markdown(f'''
                    <div style="background: linear-gradient(90deg, {team_colors[team]}, {team_colors[team]}80);
                                border-radius: 10px; padding: 15px; margin-bottom: 15px; text-align: center;">
                        <h4 style="color: #ffffff; margin: 0; font-size: 18px;">🏗️ {team}</h4>
                        <p style="color: #ffffff; margin: 5px 0 0 0; font-size: 14px;">Team Total: {total_team_points} pts</p>
                    </div>
                    ''', unsafe_allow_html=True)

                    for position, (drv, stats) in enumerate([(leader, leader_stats), (trailer, trailer_stats)]):
                        is_leader = position == 0
                        icon = "👑" if is_leader else "🥈"
                        gap_text = "LEADING" if is_leader else f"-{gap} pts"
                        card_style = "border: 3px solid #FFD700;" if is_leader else "border: 2px solid #C0C0C0;"
                        efficiency = stats['points'] / st.session_state.races_completed if st.session_state.races_completed > 0 else 0
                        dnf_count = st.session_state.driver_dnf_count.get(drv, 0)
                        st.markdown(f'''
                        <div style="background: rgba(255,255,255,0.95); border-radius: 10px;
                                    padding: 15px; margin-bottom: 10px; {card_style}">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                <div>
                                    <strong style="color: #000000; font-size: 16px;">{icon} {drv}</strong>
                                    <div style="color: #000000; font-size: 12px; opacity: 0.8;">{gap_text}</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="color: #000000; font-size: 20px; font-weight: bold;">{stats['points']}</div>
                                    <div style="color: #000000; font-size: 11px;">points</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 12px; color: #000000;">
                                <span>🏆 {stats['wins']}W</span>
                                <span>🏅 {stats['podiums']}P</span>
                                <span>💥 {dnf_count} DNF</span>
                                <span>📊 {efficiency:.1f} avg</span>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                    battle_status = "🔥 INTENSE BATTLE" if gap <= 5 else "⚖️ CLOSE FIGHT" if gap <= 15 else "👑 CLEAR LEADER"
                    battle_color = "#FF4444" if gap <= 5 else "#FF8800" if gap <= 15 else "#4CAF50"
                    if gap == 0:
                        battle_status = "🔥 PERFECTLY TIED"
                        battle_color = "#FFA500"

                    st.markdown(f'''
                    <div style="background: {battle_color}; color: #000000; border-radius: 8px;
                                padding: 8px; text-align: center; font-weight: bold; font-size: 13px;">
                        {battle_status}
                    </div>
                    ''', unsafe_allow_html=True)

                teams_processed.add(team)
                col_idx += 1
                if col_idx == 2:
                    battle_cols = st.columns(2)
                    col_idx = 0

        st.markdown("---")
        st.markdown("#### 📋 Complete Championship Standings")
        st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
        for pos, (driver, points) in enumerate(sorted_driver_standings, 1):
            team = next(d['team'] for d in drivers if d['driver'] == driver)
            wins = st.session_state.driver_wins[driver]
            podiums = st.session_state.driver_podiums[driver]
            dnfs = st.session_state.driver_dnf_count.get(driver, 0)
            card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
            position_icon = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
            gap_to_leader = sorted_driver_standings[0][1] - points if pos > 1 else 0
            gap_text = f"(-{gap_to_leader})" if gap_to_leader > 0 else ""
            st.markdown(f'''
            <div class="leaderboard-item {card_class}">
                <div style="display: flex; align-items: center; min-width: 200px;">
                    <span style="margin-right: 10px; font-weight: bold;">{position_icon}</span>
                    <div>
                        <div style="font-weight: bold; color: #000000;">{driver}</div>
                        <div style="font-size: 12px; color: #000000; opacity: 0.7;">{team} {gap_text}</div>
                    </div>
                </div>
                <div style="display: flex; gap: 15px; align-items: center;">
                    <span style="font-weight: bold; color: #000000;">{points} pts</span>
                    <span style="font-size: 12px; color: #000000;">🏆{wins}W</span>
                    <span style="font-size: 12px; color: #000000;">🏅{podiums}P</span>
                    <span style="font-size: 12px; color: #cc0000;">💥{dnfs}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.markdown("#### 🏁 Championship Awaits")
        st.write("Complete some races to see the championship battle unfold!")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 3: Constructors' Championship ──────────────────────────────────────────
with tab3:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏗️ Constructors' Championship Standings")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")

    sorted_team_standings = sorted(st.session_state.total_team_points.items(), key=lambda x: x[1], reverse=True)
    if sorted_team_standings and st.session_state.races_completed > 0:
        st.markdown("#### 🥇 Top 3 Constructors")
        for pos, (team, points) in enumerate(sorted_team_standings[:3], 1):
            wins = st.session_state.team_wins[team]
            podiums = st.session_state.team_podiums[team]
            driver1, driver2 = teams_drivers[team]
            driver1_points = st.session_state.total_driver_points[driver1]
            driver2_points = st.session_state.total_driver_points[driver2]
            card_class = "rating-card-gold" if pos == 1 else "rating-card-silver" if pos == 2 else "rating-card-bronze"
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉"
            position_label = "1st" if pos == 1 else "2nd" if pos == 2 else "3rd"
            st.markdown(f'''
            <div class="rating-card {card_class}">
                <div class="rating-header">
                    <div>
                        <div class="driver-name">{medal} {position_label} - {team}</div>
                        <div class="team-name">{driver1}: {driver1_points} pts | {driver2}: {driver2_points} pts</div>
                    </div>
                    <div class="rating-score">{points} pts</div>
                </div>
                <div class="rating-details">
                    <span>Wins: {wins}</span>
                    <span>Podiums: {podiums}</span>
                    <span>Avg: {points/st.session_state.races_completed:.1f} pts/race</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("Complete some races to see standings!")

    st.markdown("---")
    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    st.markdown("#### 📊 Complete Constructors' Standings")
    for pos, (team, points) in enumerate(sorted_team_standings, 1):
        card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
        dnfs = st.session_state.team_dnf_count.get(team, 0)
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <span>{pos}. {team}</span>
            <span>{points} pts | 💥 {dnfs} DNF(s)</span>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🥧 Constructors' Points Distribution")
    team_chart_data = [
        {"Team": team, "Points": pts, "Color": team_colors[team]}
        for team, pts in sorted_team_standings if pts > 0
    ]
    if team_chart_data:
        team_df_chart = pd.DataFrame(team_chart_data)
        fig = px.pie(team_df_chart, values="Points", names="Team", color="Team",
                     color_discrete_map={r["Team"]: r["Color"] for _, r in team_df_chart.iterrows()})
        fig.update_traces(textposition="outside", textinfo="label+value")
        fig.update_layout(
            height=650,
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            font=dict(color="#000000"),
            plot_bgcolor='rgba(240, 242, 246, 0.95)',
            paper_bgcolor='rgba(240, 242, 246, 0.95)'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 👥 Team Member Contributions")
        team_contribution_data = []
        for team, team_pts in sorted_team_standings:
            if team_pts > 0:
                driver1, driver2 = teams_drivers[team]
                team_contribution_data.append({
                    "Team": team,
                    driver1: st.session_state.total_driver_points[driver1],
                    driver2: st.session_state.total_driver_points[driver2],
                    "Total": team_pts
                })
        if team_contribution_data:
            contrib_df = pd.DataFrame(team_contribution_data)
            driver_cols = [col for col in contrib_df.columns if col not in ["Team", "Total"]]
            fig_bar = px.bar(contrib_df, x="Team", y=driver_cols,
                             title="Points Contribution by Team Members",
                             labels={"value": "Points", "variable": "Driver"},
                             text_auto=True)
            for trace in fig_bar.data:
                trace.marker.color = driver_colors.get(trace.name, "#888888")
            fig_bar.update_layout(
                height=550, xaxis_title="Team", yaxis_title="Points",
                legend_title="Driver", barmode="stack",
                font=dict(color="#000000"),
                plot_bgcolor='rgba(240, 242, 246, 0.95)',
                paper_bgcolor='rgba(240, 242, 246, 0.95)',
                xaxis=dict(tickangle=-30, tickfont=dict(size=11, color='#2c3e50'))
            )
            fig_bar.update_traces(textposition="inside", textfont_size=10)
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No points data yet. Complete a race first!")

    st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 4: Stats ────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏆 Constructor Statistics")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")

    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    sorted_team_stats = sorted(
        st.session_state.team_wins.items(),
        key=lambda x: (st.session_state.team_wins[x[0]], st.session_state.team_podiums[x[0]]),
        reverse=True
    )
    for pos, (team, wins) in enumerate(sorted_team_stats, 1):
        podiums = st.session_state.team_podiums[team]
        points = st.session_state.total_team_points[team]
        dnfs = st.session_state.team_dnf_count.get(team, 0)
        avg = points / st.session_state.races_completed if st.session_state.races_completed > 0 else 0
        card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
        position_icon = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <div style="display: flex; align-items: center; min-width: 200px;">
                <span style="margin-right: 10px; font-weight: bold;">{position_icon}</span>
                <div>
                    <div style="font-weight: bold; color: #000000;">{team}</div>
                    <div style="font-size: 12px; color: #000000; opacity: 0.7;">{points} pts • {avg:.1f} avg/race</div>
                </div>
            </div>
            <div style="display: flex; gap: 15px; align-items: center;">
                <span style="font-size: 12px; color: #000000;">🏆 {wins}W</span>
                <span style="font-size: 12px; color: #000000;">🏅 {podiums}P</span>
                <span style="font-size: 12px; color: #cc0000;">💥 {dnfs} DNF</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.races_completed > 0:
        st.markdown("---")
        st.markdown("#### 📊 Constructor Wins & Podiums Chart")
        constructor_chart_data = [
            {"Team": team, "Wins": st.session_state.team_wins[team],
             "Podiums": st.session_state.team_podiums[team],
             "DNFs": st.session_state.team_dnf_count.get(team, 0)}
            for team, _ in sorted_team_stats
        ]
        if constructor_chart_data:
            constr_df = pd.DataFrame(constructor_chart_data)
            fig_constr = go.Figure()
            fig_constr.add_trace(go.Bar(
                name="Wins", x=constr_df["Team"], y=constr_df["Wins"],
                marker_color=[team_colors[t] for t in constr_df["Team"]],
                marker_line_width=2, marker_line_color="rgba(0,0,0,0.4)",
                text=constr_df["Wins"], textposition="outside"
            ))
            fig_constr.add_trace(go.Bar(
                name="Podiums", x=constr_df["Team"], y=constr_df["Podiums"],
                marker_color=[team_colors[t] for t in constr_df["Team"]],
                marker_opacity=0.4, marker_line_width=2, marker_line_color="rgba(0,0,0,0.3)",
                text=constr_df["Podiums"], textposition="outside"
            ))
            fig_constr.add_trace(go.Bar(
                name="DNFs", x=constr_df["Team"], y=constr_df["DNFs"],
                marker_color="#cc0000", marker_opacity=0.6,
                marker_line_width=2, marker_line_color="rgba(0,0,0,0.3)",
                text=constr_df["DNFs"], textposition="outside"
            ))
            fig_constr.update_traces(textfont_size=12, textfont_color="black")
            fig_constr.update_layout(
                barmode="group", height=480,
                title={'text': "Constructor Wins, Podiums & DNFs", 'x': 0.5,
                       'xanchor': 'center', 'font': {'size': 18, 'color': '#2c3e50'}},
                xaxis=dict(title="Team", tickangle=-30,
                           tickfont=dict(size=11, color='#2c3e50'),
                           title_font=dict(size=14, color='#2c3e50')),
                yaxis=dict(title="Count", gridcolor='rgba(128,128,128,0.2)',
                           tickfont=dict(size=11, color='#2c3e50'),
                           title_font=dict(size=14, color='#2c3e50')),
                plot_bgcolor='rgba(248, 249, 250, 0.95)',
                paper_bgcolor='rgba(248, 249, 250, 0.95)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=80, b=80)
            )
            st.plotly_chart(fig_constr, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🏆 Driver Statistics")

    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    sorted_driver_stats = sorted(
        st.session_state.driver_wins.items(),
        key=lambda x: (st.session_state.driver_wins[x[0]], st.session_state.driver_podiums[x[0]]),
        reverse=True
    )
    for pos, (driver, wins) in enumerate(sorted_driver_stats, 1):
        team = next(d['team'] for d in drivers if d['driver'] == driver)
        podiums = st.session_state.driver_podiums[driver]
        points = st.session_state.total_driver_points[driver]
        dnfs = st.session_state.driver_dnf_count.get(driver, 0)
        avg = points / st.session_state.races_completed if st.session_state.races_completed > 0 else 0
        rating = calculate_driver_rating(driver)
        card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
        position_icon = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <div style="display: flex; align-items: center; min-width: 220px;">
                <span style="margin-right: 10px; font-weight: bold;">{position_icon}</span>
                <div>
                    <div style="font-weight: bold; color: #000000;">{driver}</div>
                    <div style="font-size: 12px; color: #000000; opacity: 0.7;">{team} • ⭐ {rating:.1f}/10</div>
                </div>
            </div>
            <div style="display: flex; gap: 15px; align-items: center;">
                <span style="font-weight: bold; color: #000000;">{points} pts</span>
                <span style="font-size: 12px; color: #000000;">🏆 {wins}W</span>
                <span style="font-size: 12px; color: #000000;">🏅 {podiums}P</span>
                <span style="font-size: 12px; color: #cc0000;">💥 {dnfs}</span>
                <span style="font-size: 12px; color: #000000;">📊 {avg:.1f}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.races_completed > 0:
        st.markdown("---")
        st.markdown("#### 📊 Driver Wins, Podiums & DNFs Chart")
        driver_chart_data_tab4 = []
        for driver, wins in sorted_driver_stats:
            team = next(d['team'] for d in drivers if d['driver'] == driver)
            driver_chart_data_tab4.append({
                "Driver": driver, "Team": team,
                "Wins": wins,
                "Podiums": st.session_state.driver_podiums[driver],
                "DNFs": st.session_state.driver_dnf_count.get(driver, 0)
            })
        if driver_chart_data_tab4:
            drv_df = pd.DataFrame(driver_chart_data_tab4)
            fig_drv = go.Figure()
            fig_drv.add_trace(go.Bar(
                name="Wins", x=drv_df["Driver"], y=drv_df["Wins"],
                marker_color=[driver_colors.get(d, "#888") for d in drv_df["Driver"]],
                marker_line_width=2, marker_line_color="rgba(0,0,0,0.4)",
                text=drv_df["Wins"], textposition="outside",
                hovertemplate="<b>%{x}</b><br>Wins: %{y}<extra></extra>"
            ))
            fig_drv.add_trace(go.Bar(
                name="Podiums", x=drv_df["Driver"], y=drv_df["Podiums"],
                marker_color=[driver_colors.get(d, "#888") for d in drv_df["Driver"]],
                marker_opacity=0.4, marker_line_width=2, marker_line_color="rgba(0,0,0,0.3)",
                text=drv_df["Podiums"], textposition="outside",
                hovertemplate="<b>%{x}</b><br>Podiums: %{y}<extra></extra>"
            ))
            fig_drv.add_trace(go.Bar(
                name="DNFs", x=drv_df["Driver"], y=drv_df["DNFs"],
                marker_color="#cc0000", marker_opacity=0.6,
                marker_line_width=2, marker_line_color="rgba(0,0,0,0.3)",
                text=drv_df["DNFs"], textposition="outside",
                hovertemplate="<b>%{x}</b><br>DNFs: %{y}<extra></extra>"
            ))
            fig_drv.update_traces(textfont_size=11, textfont_color="black")
            fig_drv.update_layout(
                barmode="group", height=520,
                title={'text': "Driver Wins, Podiums & DNFs", 'x': 0.5,
                       'xanchor': 'center', 'font': {'size': 18, 'color': '#2c3e50'}},
                xaxis=dict(title="Driver", tickangle=-45,
                           tickfont=dict(size=10, color='#2c3e50'),
                           title_font=dict(size=14, color='#2c3e50')),
                yaxis=dict(title="Count", gridcolor='rgba(128,128,128,0.2)',
                           tickfont=dict(size=11, color='#2c3e50'),
                           title_font=dict(size=14, color='#2c3e50')),
                plot_bgcolor='rgba(248, 249, 250, 0.95)',
                paper_bgcolor='rgba(248, 249, 250, 0.95)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=80, b=100)
            )
            st.plotly_chart(fig_drv, use_container_width=True)

        # DNF Reliability Analysis
        st.markdown("---")
        st.markdown("#### 💥 DNF & Reliability Analysis")
        dnf_data = []
        for team, team_drivers_list in teams_drivers.items():
            for drv in team_drivers_list:
                dnf_count = st.session_state.driver_dnf_count.get(drv, 0)
                reliability_pct = st.session_state.team_reliability.get(team, 5)
                finish_rate = ((st.session_state.races_completed - dnf_count) /
                               st.session_state.races_completed * 100) if st.session_state.races_completed > 0 else 100
                dnf_data.append({
                    "Driver": drv, "Team": team,
                    "DNFs": dnf_count,
                    "Reliability Setting": reliability_pct,
                    "Finish Rate %": round(finish_rate, 1)
                })

        dnf_data.sort(key=lambda x: x["DNFs"], reverse=True)
        dnf_df = pd.DataFrame(dnf_data)
        dnf_df.index = dnf_df.index + 1

        fig_dnf = px.bar(
            dnf_df, x="Driver", y="DNFs", color="Team",
            text="DNFs", color_discrete_map=team_colors,
            title="Driver DNF Count This Season",
            hover_data=["Team", "Finish Rate %", "Reliability Setting"]
        )
        fig_dnf.update_traces(
            texttemplate="%{text}", textposition="outside",
            marker_line_width=2, marker_line_color="rgba(0,0,0,0.3)",
            textfont=dict(size=11, color="black")
        )
        fig_dnf.update_layout(
            height=420,
            title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 18, 'color': '#2c3e50'}},
            xaxis=dict(title="Driver", tickangle=-45, tickfont=dict(size=10, color='#2c3e50'),
                       title_font=dict(size=14, color='#2c3e50')),
            yaxis=dict(title="DNF Count", gridcolor='rgba(128,128,128,0.2)',
                       tickfont=dict(size=11, color='#2c3e50'),
                       title_font=dict(size=14, color='#2c3e50')),
            plot_bgcolor='rgba(248, 249, 250, 0.95)',
            paper_bgcolor='rgba(248, 249, 250, 0.95)',
            showlegend=False, margin=dict(l=20, r=20, t=80, b=100)
        )
        st.plotly_chart(fig_dnf, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 5: Driver Upgrades + Reliability ───────────────────────────────────────
with tab5:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🛠️ Driver Performance Tuning Center")

    tune_tab1, tune_tab2 = st.tabs(["🏎️ Driver Headstarts", "💥 Team Reliability"])

    with tune_tab1:
        st.markdown("Fine-tune each driver's starting advantage. Higher values = better race starts!")
        preset_col1, preset_col2, preset_col3, preset_col4 = st.columns(4)
        with preset_col1:
            if st.button("🟰 Equal Field (All 5%)", use_container_width=True):
                for driver_info in drivers:
                    st.session_state.driver_headstarts[driver_info['driver']] = 5
                st.rerun()
        with preset_col2:
            if st.button("🎲 Randomize All", use_container_width=True):
                for driver_info in drivers:
                    st.session_state.driver_headstarts[driver_info['driver']] = random.randint(1, 9)
                st.rerun()
        with preset_col3:
            if st.button("🔄 Reset to Default (All 1%)", use_container_width=True):
                for driver_info in drivers:
                    st.session_state.driver_headstarts[driver_info['driver']] = 1
                st.rerun()
        with preset_col4:
            if st.button("⚡ Boost Mode (All 9%)", use_container_width=True):
                for driver_info in drivers:
                    st.session_state.driver_headstarts[driver_info['driver']] = 9
                st.rerun()

        st.markdown("---")
        st.markdown("#### 🏎️ Individual Driver Tuning")
        team_columns = st.columns(2)
        for i, (team, team_drivers_list) in enumerate(teams_drivers.items()):
            with team_columns[i % 2]:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, {team_colors[team]}, {team_colors[team]}40); margin-bottom: 20px;">
                    <div class="rating-header">
                        <div><div class="driver-name" style="font-size: 1.4em; color: #ffffff;">🏁 {team}</div></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                for driver in team_drivers_list:
                    current_headstart = st.session_state.driver_headstarts.get(driver, 1)
                    st.markdown(f"**{driver}** - Current: {current_headstart}%")
                    new_headstart = st.slider(
                        f"Performance Boost for {driver}", min_value=1, max_value=9,
                        value=current_headstart, step=1, key=f"headstart_slider_{driver}_{team}",
                        help=f"Adjust {driver}'s starting advantage."
                    )
                    st.session_state.driver_headstarts[driver] = new_headstart
                    progress_width = (new_headstart / 9) * 100
                    boost_level = "🟢 Conservative" if new_headstart <= 3 else "🟡 Moderate" if new_headstart <= 6 else "🔴 Aggressive"
                    st.markdown(f'''
                    <div style="margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                            <span style="font-size: 12px; color: #000000;"><strong>{driver}</strong></span>
                            <span style="font-size: 12px; color: #000000;">{boost_level}</span>
                        </div>
                        <div style="background-color: #f0f0f0; border-radius: 15px; height: 20px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
                            <div style="background: linear-gradient(90deg, {driver_colors.get(driver, "#3498db")}, {driver_colors.get(driver, "#3498db")}80);
                                        height: 100%; width: {progress_width}%; border-radius: 15px; position: relative;">
                                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                                            font-size: 11px; font-weight: bold; color: #ffffff;">
                                    {new_headstart}% Boost
                                </div>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    st.markdown("---")

    with tune_tab2:
        st.markdown("### 💥 Team Reliability Settings")
        st.markdown("""
        Set the **DNF probability per race per driver** for each team.
        - **0%** = Perfect reliability (never breaks down)
        - **5%** = Default (realistic ~1 DNF every 20 races per driver)
        - **15%** = Unreliable (expect ~1 DNF every 7 races)
        - **30%** = Very unreliable (expect frequent retirements)
        """)

        rel_preset_col1, rel_preset_col2, rel_preset_col3, rel_preset_col4 = st.columns(4)
        with rel_preset_col1:
            if st.button("✅ Perfect Reliability (0%)", use_container_width=True, key="rel_perfect"):
                for team in teams_drivers:
                    st.session_state.team_reliability[team] = 0
                st.rerun()
        with rel_preset_col2:
            if st.button("🔧 Default (5%)", use_container_width=True, key="rel_default"):
                for team in teams_drivers:
                    st.session_state.team_reliability[team] = 5
                st.rerun()
        with rel_preset_col3:
            if st.button("⚠️ Unreliable (15%)", use_container_width=True, key="rel_unreliable"):
                for team in teams_drivers:
                    st.session_state.team_reliability[team] = 15
                st.rerun()
        with rel_preset_col4:
            if st.button("🎲 Randomize Reliability", use_container_width=True, key="rel_random"):
                for team in teams_drivers:
                    st.session_state.team_reliability[team] = random.choice([0, 3, 5, 8, 10, 15, 20])
                st.rerun()

        st.markdown("---")
        st.markdown("#### 🔧 Per-Team Reliability Sliders")
        rel_columns = st.columns(2)
        for i, (team, _) in enumerate(teams_drivers.items()):
            with rel_columns[i % 2]:
                current_rel = st.session_state.team_reliability.get(team, 5)
                driver1, driver2 = teams_drivers[team]
                d1_dnfs = st.session_state.driver_dnf_count.get(driver1, 0)
                d2_dnfs = st.session_state.driver_dnf_count.get(driver2, 0)

                # Reliability label
                if current_rel == 0:
                    rel_label = "✅ Perfect"
                    rel_color = "#27ae60"
                elif current_rel <= 5:
                    rel_label = "🟢 Reliable"
                    rel_color = "#2ecc71"
                elif current_rel <= 10:
                    rel_label = "🟡 Average"
                    rel_color = "#f39c12"
                elif current_rel <= 20:
                    rel_label = "🟠 Unreliable"
                    rel_color = "#e67e22"
                else:
                    rel_label = "🔴 Fragile"
                    rel_color = "#e74c3c"

                st.markdown(f'''
                <div style="background: linear-gradient(135deg, {team_colors[team]}, {team_colors[team]}50);
                            border-radius: 12px; padding: 15px; margin-bottom: 5px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #ffffff; font-weight: bold; font-size: 16px;">🏗️ {team}</span>
                        <span style="background: {rel_color}; color: #fff; border-radius: 8px;
                                     padding: 3px 10px; font-size: 12px; font-weight: bold;">{rel_label}</span>
                    </div>
                    <div style="color: #ffffff; font-size: 12px; margin-top: 5px;">
                        {driver1}: 💥 {d1_dnfs} DNFs this season &nbsp;|&nbsp; {driver2}: 💥 {d2_dnfs} DNFs this season
                    </div>
                </div>
                ''', unsafe_allow_html=True)

                new_rel = st.slider(
                    f"DNF chance per race — {team}",
                    min_value=0, max_value=30, value=current_rel, step=1,
                    key=f"reliability_{team}",
                    help=f"% chance each driver from {team} retires per race"
                )
                st.session_state.team_reliability[team] = new_rel

                # Visual bar
                bar_width = (new_rel / 30) * 100
                st.markdown(f'''
                <div style="background-color: #f0f0f0; border-radius: 10px; height: 18px; overflow: hidden; margin-bottom: 20px;">
                    <div style="background: linear-gradient(90deg, {rel_color}, {rel_color}88);
                                height: 100%; width: {bar_width}%; border-radius: 10px;
                                display: flex; align-items: center; padding-left: 8px;">
                        <span style="font-size: 10px; font-weight: bold; color: #fff;">{new_rel}% DNF Risk</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📊 Reliability Summary")
        rel_summary_data = []
        for team, _ in teams_drivers.items():
            rel = st.session_state.team_reliability.get(team, 5)
            total_dnfs = st.session_state.team_dnf_count.get(team, 0)
            expected_dnfs_per_race = (rel / 100) * 2  # 2 drivers
            rel_summary_data.append({
                "Team": team,
                "DNF Risk %": rel,
                "Season DNFs": total_dnfs,
                "Expected/Race": round(expected_dnfs_per_race, 2)
            })
        rel_summary_data.sort(key=lambda x: x["DNF Risk %"], reverse=True)
        rel_df = pd.DataFrame(rel_summary_data)
        st.dataframe(rel_df, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 6: Season Summary ───────────────────────────────────────────────────────
with tab6:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏁 Season Summary")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")

    if st.session_state.races_completed > 0:
        col1, col2 = st.columns(2)
        sorted_driver_standings_tab6 = sorted(
            st.session_state.total_driver_points.items(), key=lambda x: x[1], reverse=True)
        sorted_team_standings_tab6 = sorted(
            st.session_state.total_team_points.items(), key=lambda x: x[1], reverse=True)

        with col1:
            st.markdown("#### 🏆 Drivers' Championship Leaders")
            for i, (driver, points) in enumerate(sorted_driver_standings_tab6[:3]):
                team = next(d['team'] for d in drivers if d['driver'] == driver)
                wins = st.session_state.driver_wins[driver]
                podiums = st.session_state.driver_podiums[driver]
                card_class = "rating-card-gold" if i == 0 else "rating-card-silver" if i == 1 else "rating-card-bronze"
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                position = "1st" if i == 0 else "2nd" if i == 1 else "3rd"
                st.markdown(f'''
                <div class="rating-card {card_class}">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">{medal} {position} - {driver}</div>
                            <div class="team-name">{team}</div>
                        </div>
                        <div class="rating-score">{points} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Wins: {wins}</span>
                        <span>Podiums: {podiums}</span>
                        <span>Avg: {points/st.session_state.races_completed:.1f}/race</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🏗️ Constructors' Championship Leaders")
            for i, (team, points) in enumerate(sorted_team_standings_tab6[:3]):
                wins = st.session_state.team_wins[team]
                podiums = st.session_state.team_podiums[team]
                driver1, driver2 = teams_drivers[team]
                d1_pts = st.session_state.total_driver_points[driver1]
                d2_pts = st.session_state.total_driver_points[driver2]
                card_class = "rating-card-gold" if i == 0 else "rating-card-silver" if i == 1 else "rating-card-bronze"
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                position = "1st" if i == 0 else "2nd" if i == 1 else "3rd"
                st.markdown(f'''
                <div class="rating-card {card_class}">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">{medal} {position} - {team}</div>
                            <div class="team-name">{driver1}: {d1_pts} pts | {driver2}: {d2_pts} pts</div>
                        </div>
                        <div class="rating-score">{points} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Wins: {wins}</span>
                        <span>Podiums: {podiums}</span>
                        <span>Avg: {points/st.session_state.races_completed:.1f}/race</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📊 Season Statistics Overview")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("🏁 Total Races", st.session_state.races_completed)
        with col2:
            if sorted_driver_standings_tab6:
                leader = sorted_driver_standings_tab6[0][0]
                leader_team = next(d['team'] for d in drivers if d['driver'] == leader)
                st.metric("🏆 Champ Leader", leader, delta=f"({leader_team})")
        with col3:
            if sorted_team_standings_tab6:
                st.metric("🏗️ Constructor Leader", sorted_team_standings_tab6[0][0],
                          delta=f"{sorted_team_standings_tab6[0][1]} pts")
        with col4:
            total_pts = sum(st.session_state.total_driver_points.values())
            st.metric("💯 Total Points", total_pts)
        with col5:
            total_dnfs_s = sum(st.session_state.driver_dnf_count.values())
            st.metric("💥 Season DNFs", total_dnfs_s)

        st.markdown("---")
        st.markdown("#### 🏆 Race Winners Summary")
        if st.session_state.race_summaries:
            st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
            for idx, summary in enumerate(st.session_state.race_summaries):
                dnf_text = f" | 💥 {summary.get('DNFs', 0)} DNF(s)" if summary.get('DNFs', 0) > 0 else ""
                st.markdown(f'''
                <div class="leaderboard-item">
                    <span>Race {summary['Race']}</span>
                    <span>🏆 {summary['P1']} | 2nd: {summary['P2']} | 3rd: {summary['P3']}{dnf_text}</span>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🎖️ Major Awards & Recognitions")

        award_col1, award_col2, award_col3 = st.columns(3)
        with award_col1:
            most_wins_driver = max(st.session_state.driver_wins.items(), key=lambda x: x[1])
            if most_wins_driver[1] > 0:
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_wins_driver[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);">
                    <div class="rating-header">
                        <div><div class="driver-name">🏆 Race Winner King</div>
                        <div class="team-name">{most_wins_driver[0]} ({driver_team})</div></div>
                        <div class="rating-score">{most_wins_driver[1]}</div>
                    </div>
                    <div class="rating-details">
                        <span>Win Rate: {(most_wins_driver[1]/st.session_state.races_completed)*100:.1f}%</span>
                    </div>
                </div>''', unsafe_allow_html=True)

        with award_col2:
            most_dnf_driver = max(st.session_state.driver_dnf_count.items(), key=lambda x: x[1])
            if most_dnf_driver[1] > 0:
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_dnf_driver[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #636e72 0%, #2d3436 100%);">
                    <div class="rating-header">
                        <div><div class="driver-name" style="color:#fff;">💥 Unluckiest Driver</div>
                        <div class="team-name" style="color:#fff;">{most_dnf_driver[0]} ({driver_team})</div></div>
                        <div class="rating-score" style="color:#fff;">{most_dnf_driver[1]} DNFs</div>
                    </div>
                    <div class="rating-details" style="color:#fff;">
                        <span>Most retirements this season</span>
                    </div>
                </div>''', unsafe_allow_html=True)

        with award_col3:
            most_reliable_team = min(st.session_state.team_dnf_count.items(), key=lambda x: x[1])
            st.markdown(f'''
            <div class="rating-card" style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%);">
                <div class="rating-header">
                    <div><div class="driver-name">🔧 Most Reliable Team</div>
                    <div class="team-name">{most_reliable_team[0]}</div></div>
                    <div class="rating-score">{most_reliable_team[1]} DNFs</div>
                </div>
                <div class="rating-details">
                    <span>Fewest retirements</span>
                </div>
            </div>''', unsafe_allow_html=True)

    else:
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.write("Complete some races to see the season summary!")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

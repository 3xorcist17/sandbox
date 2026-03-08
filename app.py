import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Formula 1 Racing 🏎️🏁🚥🏆")
st.set_page_config(page_title="Formula 1 Racing", page_icon="🏎️", layout="wide")

# Updated CSS with grey/ash colors changed to black
st.markdown("""
    <style>
    div[data-testid="stTable"] {
        width: 100% !important;
    }
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
    
    .rating-card-gold {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000000;
    }
    
    .rating-card-silver {
        background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
        color: #000000;
    }
    
    .rating-card-bronze {
        background: linear-gradient(135deg, #CD7F32 0%, #B8860B 100%);
        color: #000000;
    }
    
    .rating-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .rating-score {
        font-size: 2.5em;
        font-weight: bold;
        text-align: right;
        color: #000000;
    }
    
    .rating-details {
        display: flex;
        justify-content: space-between;
        font-size: 0.9em;
        opacity: 0.9;
        color: #000000;
    }
    
    .driver-name {
        font-size: 1.3em;
        font-weight: bold;
        color: #000000;
    }
    
    .team-name {
        font-size: 1em;
        opacity: 0.8;
        color: #000000;
    }
    
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
    
    .driver-row:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    .driver-info {
        min-width: 150px;
        display: flex;
        flex-direction: column;
    }
    
    .progress-container {
        flex: 1;
        margin: 0 20px;
        position: relative;
    }
    
    .custom-progress-bar {
        width: 100%;
        height: 25px;
        background: linear-gradient(90deg, #ecf0f1 0%, #bdc3c7 100%);
        border-radius: 15px;
        overflow: hidden;
        position: relative;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--driver-color) 0%, var(--driver-color-light) 100%);
        border-radius: 15px;
        position: relative;
        transition: width 0.5s ease-out;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .progress-fill::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 50%;
        background: linear-gradient(90deg, 
            rgba(255,255,255,0.3) 0%, 
            rgba(255,255,255,0.1) 50%, 
            rgba(255,255,255,0.3) 100%);
        border-radius: 15px 15px 0 0;
    }
    
    .progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-weight: bold;
        font-size: 12px;
        color: #000000;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        z-index: 10;
    }
    
    .progress-status {
        min-width: 100px;
        text-align: right;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
    
    .status-text {
        font-weight: bold;
        font-size: 14px;
        color: #000000;
    }
    
    .status-subtext {
        font-size: 11px;
        color: #000000;
        margin-top: 2px;
    }
    
    .finished-row {
        background: rgba(255, 255, 255, 0.95);
        color: #000000;
    }
    
    .finished-row .driver-name,
    .finished-row .team-name,
    .finished-row .status-text,
    .finished-row .progress-text {
        color: #000000;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    .position-indicator {
        font-size: 18px;
        font-weight: bold;
        margin-right: 10px;
        min-width: 40px;
        text-align: center;
        color: #000000;
    }
    
    .racing-animation {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
        50% { box-shadow: 0 6px 25px rgba(102, 126, 234, 0.3); }
        100% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
    }
    
    .speed-indicator {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        background: rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        padding: 2px 8px;
        font-size: 10px;
        font-weight: bold;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# Team and driver data - UPDATED with Cadillac
teams_drivers = {
    "Alpine": ["Gas", "Doo"],
    "Aston Martin": ["Alo", "Str"],
    "Cadillac": ["Bot", "Per"],
    "Ferrari": ["Lec", "Ham"],
    "Haas": ["Oco", "Bea"],
    "McLaren": ["Nor", "Pia"],
    "Mercedes": ["Rus", "Ant"],
    "Racing Bulls": ["Had", "Law"],
    "Red Bull": ["Ver", "Tsu"],
    "Sauber": ["Hul", "Bor"],
    "Williams": ["Sai", "Alb"]
}

# Team colors - UPDATED with Cadillac (black and white theme)
team_colors = {
    "Alpine": "hsl(308, 100%, 34.4%)",
    "Aston Martin": "hsl(185, 99.6%, 31.7%)",
    "Cadillac": "hsl(0, 0%, 10%)",
    "Ferrari": "hsl(0, 99.6%, 39.7%)",
    "Haas": "hsl(0, 99.6%, 28.2%)",
    "McLaren": "hsl(33, 99.6%, 42.4%)",
    "Mercedes": "hsl(165, 99.6%, 9.4%)",
    "Racing Bulls": "hsl(198, 99.6%, 80.3%)",
    "Red Bull": "hsl(247, 99.6%, 24.1%)",
    "Sauber": "hsl(124, 99.6%, 31.4%)",
    "Williams": "hsl(201, 99.6%, 32.2%)"
}

# Driver colors (unchanged logic, now includes Bot and Per)
driver_colors = {}
for team, drivers_list in teams_drivers.items():
    color_parts = team_colors[team].replace('hsl(', '').replace(')', '').split(',')
    hue = float(color_parts[0])
    saturation = float(color_parts[1].replace('%', ''))
    lightness = float(color_parts[2].replace('%', ''))
    driver_colors[drivers_list[0]] = f"hsl({hue}, {saturation}%, {min(100, lightness + 5)}%)"
    driver_colors[drivers_list[1]] = f"hsl({hue}, {saturation}%, {max(0, lightness - 5)}%)"

# Flatten drivers list - now 22 drivers
drivers = []
for team, driver_list in teams_drivers.items():
    for driver in driver_list:
        drivers.append({"driver": driver, "team": team})

# Points system (unchanged)
points_system = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# Initialize session state - UPDATED to 22 drivers
if 'progress_values' not in st.session_state:
    st.session_state.progress_values = [0] * 22
if 'finish_order' not in st.session_state:
    st.session_state.finish_order = []
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

# Tab 1: Race & Results - UPDATED for 22 drivers
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
        st.rerun()

    if st.session_state.race_started and not st.session_state.race_finished:
        st.markdown('<div class="race-container">', unsafe_allow_html=True)
        st.markdown("### 🏎️ Live Race Progress")
        
        progress_placeholders = []
        current_leaderboard = get_current_leaderboard()
        
        for pos, driver_info in enumerate(current_leaderboard, 1):
            progress = driver_info['progress']
            driver = driver_info['driver']
            team = driver_info['team']
            is_finished = driver_info.get('finished', False)
            
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
            
            position_emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
            
            if is_finished:
                status_text = "🏁 FINISHED"
                status_subtext = "Race Complete"
                row_class = "finished-row"
                animation_class = ""
            else:
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
            </div>
            '''
            
            placeholder = st.empty()
            placeholder.markdown(progress_html, unsafe_allow_html=True)
            progress_placeholders.append((placeholder, driver_info))
        
        st.markdown('</div>', unsafe_allow_html=True)

        time.sleep(1)

        while (st.session_state.race_started and 
               any(value < 100 for value in st.session_state.progress_values) and 
               not st.session_state.race_finished):
            
            for i in range(22):  # Updated to 22
                if st.session_state.progress_values[i] < 100:
                    increment = random.randint(0, 4)
                    st.session_state.progress_values[i] = min(100, st.session_state.progress_values[i] + increment)
                    if st.session_state.progress_values[i] == 100 and drivers[i]['driver'] not in [d['driver'] for d in st.session_state.finish_order]:
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
                    
                    position_emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
                    
                    if is_finished:
                        status_text = "🏁 FINISHED"
                        status_subtext = "Race Complete"
                        row_class = "finished-row"
                        animation_class = ""
                    else:
                        status_text = f"{progress:.1f}%"
                        status_subtext = "Racing..."
                        row_class = ""
                        animation_class = "racing-animation" if progress > 70 else ""
                    
                    speed_kmh = int(max(180, min(350, 200 + (progress / 100) * 150 + (pos * -3) + random.randint(-10, 10))))
                    
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
                    </div>
                    '''
                    
                    placeholder.markdown(progress_html, unsafe_allow_html=True)
            
            if len(st.session_state.finish_order) == 22:  # Updated to 22
                st.session_state.race_finished = True
                st.session_state.races_completed += 1
                st.session_state.race_started = False
                
                if 'complete_race_history' not in st.session_state:
                    st.session_state.complete_race_history = []
                
                complete_race_results = {
                    "race_number": st.session_state.races_completed,
                    "results": [(pos + 1, driver_info['driver'], driver_info['team']) 
                               for pos, driver_info in enumerate(st.session_state.finish_order)]
                }
                st.session_state.complete_race_history.append(complete_race_results)
                
                for idx, (placeholder, _) in enumerate(progress_placeholders):
                    if idx < len(current_leaderboard):
                        driver_info = current_leaderboard[idx]
                        pos = idx + 1
                        driver = driver_info['driver']
                        team = driver_info['team']
                        base_color = driver_colors.get(driver, '#3498db')
                        
                        position_emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
                        
                        points = points_system.get(pos, 0)
                        status_text = f"🏁 FINISHED"
                        status_subtext = f"{points} points" if pos <= 10 else "0 points"
                        
                        progress_html = f'''
                        <div class="driver-row finished-row">
                            <div class="position-indicator">{position_emoji}</div>
                            <div class="driver-info">
                                <div class="driver-name">{driver}</div>
                                <div class="team-name">{team}</div>
                            </div>
                            <div class="progress-container">
                                <div class="custom-progress-bar">
                                    <div class="progress-fill" style="width: 100%;">
                                    </div>
                                    <div class="progress-text">100%</div>
                                </div>
                            </div>
                            <div class="progress-status">
                                <div class="status-text">{status_text}</div>
                                <div class="status-subtext">{status_subtext}</div>
                            </div>
                        </div>
                        '''
                        
                        placeholder.markdown(progress_html, unsafe_allow_html=True)
                
                for position, driver_info in enumerate(st.session_state.finish_order, 1):
                    if position <= 10:
                        points = points_system.get(position, 0)
                        st.session_state.total_driver_points[driver_info['driver']] += points
                        st.session_state.total_team_points[driver_info['team']] += points
                    if position == 1:
                        st.session_state.driver_wins[driver_info['driver']] += 1
                        st.session_state.team_wins[driver_info['team']] += 1
                    if position <= 3:
                        st.session_state.driver_podiums[driver_info['driver']] += 1
                        st.session_state.team_podiums[driver_info['team']] += 1
                
                if len(st.session_state.finish_order) >= 3:
                    race_summary = {
                        "Race": st.session_state.races_completed,
                        "P1": f"{st.session_state.finish_order[0]['driver']} ({st.session_state.finish_order[0]['team']})",
                        "P2": f"{st.session_state.finish_order[1]['driver']} ({st.session_state.finish_order[1]['team']})",
                        "P3": f"{st.session_state.finish_order[2]['driver']} ({st.session_state.finish_order[2]['team']})"
                    }
                    st.session_state.race_summaries.append(race_summary)
                break
            
            time.sleep(1)

    if st.session_state.race_finished:
        st.markdown("---")
        if len(st.session_state.finish_order) >= 3:
            st.markdown("### 🏆 Race Podium")
            
            podium_positions = [
                (st.session_state.finish_order[0], 1, "🥇", "rating-card-gold", "1st"),
                (st.session_state.finish_order[1], 2, "🥈", "rating-card-silver", "2nd"),
                (st.session_state.finish_order[2], 3, "🥉", "rating-card-bronze", "3rd")
            ]
            
            for driver_info, position, medal, card_class, position_text in podium_positions:
                points = points_system.get(position, 0)
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
                        <div class="rating-score">{points} pts</div>
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
        race_summary_data = []
        for summary in st.session_state.race_summaries:
            race_summary_data.append({
                "Race": summary["Race"],
                "P1": summary["P1"],
                "P2": summary["P2"],
                "P3": summary["P3"]
            })
        if race_summary_data:
            st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
            for idx, summary in enumerate(race_summary_data):
                card_class = "position-1" if idx == 0 else ""
                st.markdown(f'''
                <div class="leaderboard-item {card_class}">
                    <span>Race {summary['Race']}</span>
                    <span>P1: {summary['P1']} | P2: {summary['P2']} | P3: {summary['P3']}</span>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="rating-card">', unsafe_allow_html=True)
            st.write("No races completed yet.")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Enhanced Drivers' Championship with Actual Race Results
# Tab 2: Enhanced Drivers' Championship with Actual Race Results
with tab2:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏆 Drivers' Championship Hub")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
    
    if st.session_state.races_completed > 0:
        # Prepare data
        sorted_driver_standings = sorted(st.session_state.total_driver_points.items(), key=lambda x: x[1], reverse=True)
        
        # Championship Leadership Section
        st.markdown("#### 👑 Championship Leadership")
        leader_col1, leader_col2, leader_col3 = st.columns(3)
        
        for pos, (driver, points) in enumerate(sorted_driver_standings[:3], 1):
            team = next(d['team'] for d in drivers if d['driver'] == driver)
            wins = st.session_state.driver_wins[driver]
            podiums = st.session_state.driver_podiums[driver]
            rating = calculate_driver_rating(driver)
            
            card_class = "rating-card-gold" if pos == 1 else "rating-card-silver" if pos == 2 else "rating-card-bronze"
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉"
            position_text = "LEADER" if pos == 1 else f"+{sorted_driver_standings[0][1] - points}" if pos > 1 else ""
            
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
        
        # Championship Battle Visualization
        st.markdown("#### 📊 Championship Battle")
        
        top_drivers = sorted_driver_standings[:22]  # All 22 drivers
        driver_chart_data = []
        for pos, (driver, points) in enumerate(top_drivers, 1):
            team = next(d['team'] for d in drivers if d['driver'] == driver)
            wins = st.session_state.driver_wins[driver]
            podiums = st.session_state.driver_podiums[driver]
            driver_chart_data.append({
                "Driver": f"{driver}",
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
                driver_df_chart,
                x="Points",
                y="Full_Name",
                color="Team",
                text="Points",
                color_discrete_map=team_colors,
                orientation='h',
                title="Championship Standings - Points Battle"
            )
            
            fig.update_traces(
                textposition="outside",
                texttemplate="%{text} pts",
                marker_line_width=3,
                marker_line_color="rgba(0,0,0,0.4)",
                textfont=dict(size=12, color="black")
            )
            
            fig.update_layout(
                height=750,  # Increased from 650 to accommodate 22 drivers
                width=None,
                xaxis_title="Championship Points",
                yaxis_title="",
                title={
                    'text': "Championship Standings - Points Battle",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#2c3e50'}
                },
                plot_bgcolor='rgba(248, 249, 250, 0.95)',
                paper_bgcolor='rgba(248, 249, 250, 0.95)',
                xaxis=dict(
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    gridwidth=1,
                    showgrid=True,
                    zeroline=True,
                    zerolinecolor='rgba(128, 128, 128, 0.4)',
                    zerolinewidth=2,
                    tickfont=dict(size=11, color='#2c3e50'),
                    title_font=dict(size=14, color='#2c3e50')
                ),
                yaxis=dict(
                    categoryorder='total ascending',
                    tickfont=dict(size=11, color='#2c3e50'),
                    showgrid=False
                ),
                margin=dict(l=20, r=60, t=60, b=40),
                showlegend=False
            )
            
            fig.update_traces(
                marker=dict(
                    line=dict(width=2),
                    opacity=0.85
                )
            )
            
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'championship_standings',
                    'height': 750,
                    'width': 1200,
                    'scale': 1
                }
            })
            
            # Quick Stats Panel
            st.markdown("---")
            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
            
            with stats_col1:
                total_points = sum(st.session_state.total_driver_points.values())
                st.metric(
                    "🏆 Total Points",
                    total_points,
                    help="Total championship points awarded across all races"
                )
            
            with stats_col2:
                total_winners = len([d for d in st.session_state.driver_wins.values() if d > 0])
                st.metric(
                    "🏁 Race Winners",
                    total_winners,
                    help="Number of different drivers who have won races"
                )
            
            with stats_col3:
                leader_dominance = (sorted_driver_standings[0][1] / total_points * 100) if total_points > 0 else 0
                st.metric(
                    "👑 Leader Share",
                    f"{leader_dominance:.1f}%",
                    help="Percentage of total points held by championship leader"
                )
            
            with stats_col4:
                avg_points_per_race = total_points / st.session_state.races_completed if st.session_state.races_completed > 0 else 0
                st.metric(
                    "📊 Avg/Race",
                    f"{avg_points_per_race:.1f}",
                    help="Average points awarded per race"
                )
        
        st.markdown("---")
        
        # Race Results Table - Using ACTUAL race results
        if (st.session_state.races_completed > 0 and
            hasattr(st.session_state, 'complete_race_history') and
            len(st.session_state.complete_race_history) > 0):
            
            st.markdown("#### 📋 Race Results Table")
            st.markdown("*Complete finishing positions for all drivers in all races*")
            
            def create_actual_results_table():
                table_data = []
                
                for driver_info in drivers:  # Now iterates 22 drivers
                    driver = driver_info['driver']
                    team = driver_info['team']
                    row_data = {
                        'Driver': driver,
                        'Team': team
                    }
                    
                    for race_data in st.session_state.complete_race_history:
                        race_num = race_data['race_number']
                        race_results = race_data['results']
                        
                        position = None
                        for pos, race_driver, _ in race_results:
                            if race_driver == driver:
                                position = pos
                                break
                        
                        row_data[f'Race {race_num}'] = position if position is not None else "DNF"
                    
                    table_data.append(row_data)
                
                # Sort by current championship position
                final_standings = sorted(st.session_state.total_driver_points.items(), key=lambda x: x[1], reverse=True)
                driver_order = [d for d, _ in final_standings]
                
                ordered_table_data = []
                for driver in driver_order:
                    driver_data = next((d for d in table_data if d['Driver'] == driver), None)
                    if driver_data:
                        ordered_table_data.append(driver_data)
                
                return ordered_table_data
            
            table_data = create_actual_results_table()
            
            if table_data:
                df = pd.DataFrame(table_data)
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
                        return 'background-color: #FF6B6B; color: #000000; font-weight: bold;'
                    return ''
                
                race_columns = [col for col in df.columns if col.startswith('Race ')]
                if race_columns:
                    styled_df = df.style.applymap(style_position, subset=race_columns)
                    table_height = len(df) * 35 + 50  # 22 rows * 35 + header
                    st.dataframe(styled_df, use_container_width=True, height=table_height)
                else:
                    table_height = len(df) * 35 + 50
                    st.dataframe(df, use_container_width=True, height=table_height)
                
                st.markdown('''
                <div style="margin-top: 15px; padding: 15px; background: rgba(255, 255, 255, 0.9); border-radius: 10px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                    <h6 style="margin: 0 0 15px 0; color: #000000; text-align: center;">Position Legend</h6>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 8px; font-size: 11px;">
                        <div style="display: flex; align-items: center; gap: 8px; padding: 5px;">
                            <div style="width: 25px; height: 25px; background: #FFD700; border-radius: 4px; border: 2px solid #000000;"></div>
                            <span style="color: #000000; font-weight: bold;">1st Place</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px; padding: 5px;">
                            <div style="width: 25px; height: 25px; background: #C0C0C0; border-radius: 4px; border: 2px solid #000000;"></div>
                            <span style="color: #000000; font-weight: bold;">2nd Place</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px; padding: 5px;">
                            <div style="width: 25px; height: 25px; background: #CD7F32; border-radius: 4px; border: 2px solid #000000;"></div>
                            <span style="color: #000000; font-weight: bold;">3rd Place</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px; padding: 5px;">
                            <div style="width: 25px; height: 25px; background: #E6F3FF; border-radius: 4px;"></div>
                            <span style="color: #000000;">Points (4-10)</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px; padding: 5px;">
                            <div style="width: 25px; height: 25px; background: #FFF0E6; border-radius: 4px;"></div>
                            <span style="color: #000000;">No Points (11-22)</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px; padding: 5px;">
                            <div style="width: 25px; height: 25px; background: #FF6B6B; border-radius: 4px;"></div>
                            <span style="color: #000000; font-weight: bold;">DNF</span>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.warning("No race data available. Complete some races first!")
        else:
            st.info("Complete at least 1 race to see the race results table!")
        
        st.markdown("---")
        
        # Teammate Battles - now 11 teams
        st.markdown("#### 🤝 Constructor Battles & Teammate Analysis")
        
        battle_cols = st.columns(2)
        teams_processed = set()
        col_idx = 0
        
        for team, team_drivers in teams_drivers.items():
            if team not in teams_processed and col_idx < len(battle_cols):
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                driver1_wins = st.session_state.driver_wins[driver1]
                driver2_wins = st.session_state.driver_wins[driver2]
                driver1_podiums = st.session_state.driver_podiums[driver1]
                driver2_podiums = st.session_state.driver_podiums[driver2]
                
                if driver1_points >= driver2_points:
                    leader = driver1
                    trailer = driver2
                    leader_stats = {'points': driver1_points, 'wins': driver1_wins, 'podiums': driver1_podiums}
                    trailer_stats = {'points': driver2_points, 'wins': driver2_wins, 'podiums': driver2_podiums}
                else:
                    leader = driver2
                    trailer = driver1
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
                    
                    for position, (driver, stats) in enumerate([(leader, leader_stats), (trailer, trailer_stats)]):
                        is_leader = position == 0
                        icon = "👑" if is_leader else "🥈"
                        gap_text = "LEADING" if is_leader else f"-{gap} pts"
                        card_style = "border: 3px solid #FFD700;" if is_leader else "border: 2px solid #C0C0C0;"
                        
                        efficiency = stats['points'] / st.session_state.races_completed if st.session_state.races_completed > 0 else 0
                        
                        st.markdown(f'''
                        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 10px; 
                                    padding: 15px; margin-bottom: 10px; {card_style}">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                <div>
                                    <strong style="color: #000000; font-size: 16px;">{icon} {driver}</strong>
                                    <div style="color: #000000; font-size: 12px; opacity: 0.8;">{gap_text}</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="color: #000000; font-size: 20px; font-weight: bold;">{stats['points']}</div>
                                    <div style="color: #000000; font-size: 11px;">points</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 12px; color: #000000;">
                                <span>🏆 {stats['wins']} wins</span>
                                <span>🏅 {stats['podiums']} podiums</span>
                                <span>📊 {efficiency:.1f} avg</span>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    if gap == 0:
                        battle_status = "🔥 PERFECTLY TIED"
                        battle_color = "#FFA500"
                    elif gap <= 5:
                        battle_status = "🔥 INTENSE BATTLE"
                        battle_color = "#FF4444"
                    elif gap <= 15:
                        battle_status = "⚖️ CLOSE FIGHT"
                        battle_color = "#FF8800"
                    else:
                        battle_status = "👑 CLEAR LEADER"
                        battle_color = "#4CAF50"
                    
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
        
        # Full Championship Table
        st.markdown("---")
        st.markdown("#### 📋 Complete Championship Standings")
        
        st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
        for pos, (driver, points) in enumerate(sorted_driver_standings, 1):
            team = next(d['team'] for d in drivers if d['driver'] == driver)
            wins = st.session_state.driver_wins[driver]
            podiums = st.session_state.driver_podiums[driver]
            
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
                </div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.markdown("#### 🏁 Championship Awaits")
        st.write("Complete some races to see the championship battle unfold!")
        st.write("• Real-time standings updates")
        st.write("• Detailed performance analytics")
        st.write("• Constructor vs constructor battles")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Constructors' Championship Standings and Chart - REMOVED team member contribution section
# Tab 3: Constructors' Championship Standings and Chart
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
            position = "1st" if pos == 1 else "2nd" if pos == 2 else "3rd"
            
            st.markdown(f'''
            <div class="rating-card {card_class}">
                <div class="rating-header">
                    <div>
                        <div class="driver-name">{medal} {position} - {team}</div>
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
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.markdown("#### 🏁 No Data Available")
        st.write("Complete some races to see championship standings!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    st.markdown("#### 📊 Complete Constructors' Standings")
    team_standings_data = []
    for pos, (team, points) in enumerate(sorted_team_standings, 1):
        team_standings_data.append({"Position": pos, "Team": team, "Total Points": points})
        card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <span>{pos}. {team}</span>
            <span>{points} pts</span>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 🥧 Constructors' Points Distribution")
    team_chart_data = [
        {"value": points, "name": team, "itemStyle": {"color": team_colors[team]}}
        for team, points in sorted_team_standings if points > 0
    ]
    if team_chart_data:
        team_df_chart = pd.DataFrame([
            {"Team": item["name"], "Points": item["value"], "Color": item["itemStyle"]["color"]}
            for item in team_chart_data
        ])
        fig = px.pie(
            team_df_chart,
            values="Points",
            names="Team",
            color="Team",
            color_discrete_map={row["Team"]: row["Color"] for _, row in team_df_chart.iterrows()}
        )
        fig.update_traces(textposition="outside", textinfo="label+value")
        fig.update_layout(
            height=650,  # Slightly increased to fit 11 team labels cleanly
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,  # Pushed down slightly to avoid overlap with 11 legend items
                xanchor="center",
                x=0.5
            ),
            font=dict(color="#000000"),
            plot_bgcolor='rgba(240, 242, 246, 0.95)',
            paper_bgcolor='rgba(240, 242, 246, 0.95)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### 👥 Team Member Contributions")
        team_contribution_data = []
        for team, team_points in sorted_team_standings:
            if team_points > 0:
                driver1, driver2 = teams_drivers[team]
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                
                team_contribution_data.append({
                    "Team": team,
                    driver1: driver1_points,
                    driver2: driver2_points,
                    "Total": team_points
                })
        
        if team_contribution_data:
            contrib_df = pd.DataFrame(team_contribution_data)
            
            # Build y columns dynamically from all driver columns (excludes Team and Total)
            driver_cols = [col for col in contrib_df.columns if col not in ["Team", "Total"]]
            
            fig_bar = px.bar(
                contrib_df,
                x="Team",
                y=driver_cols,
                title="Points Contribution by Team Members",
                labels={"value": "Points", "variable": "Driver"},
                text_auto=True
            )
            
            # Assign correct driver colors per trace
            for trace in fig_bar.data:
                driver_name = trace.name
                trace.marker.color = driver_colors.get(driver_name, "#888888")
            
            fig_bar.update_layout(
                height=550,  # Slightly increased to accommodate 11 teams on x-axis
                xaxis_title="Team",
                yaxis_title="Points",
                legend_title="Driver",
                barmode="stack",
                font=dict(color="#000000"),
                plot_bgcolor='rgba(240, 242, 246, 0.95)',
                paper_bgcolor='rgba(240, 242, 246, 0.95)',
                xaxis=dict(
                    tickangle=-30,  # Angled labels so 11 team names don't overlap
                    tickfont=dict(size=11, color='#2c3e50')
                )
            )
            fig_bar.update_traces(textposition="inside", textfont_size=10)
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.write("No points data available yet. Please complete a race in the 'Race & Results' tab.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Constructors' and Drivers' Stats
# Tab 4: Constructors' and Drivers' Stats
with tab4:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏆 Constructor Statistics")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
    
    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    constructor_stats_data = []
    sorted_team_stats = sorted(
        st.session_state.team_wins.items(),
        key=lambda x: (st.session_state.team_wins[x[0]], st.session_state.team_podiums[x[0]]),
        reverse=True
    )
    for pos, (team, wins) in enumerate(sorted_team_stats, 1):
        podiums = st.session_state.team_podiums[team]
        points = st.session_state.total_team_points[team]
        avg = points / st.session_state.races_completed if st.session_state.races_completed > 0 else 0
        constructor_stats_data.append({
            "Position": pos,
            "Team": team,
            "Wins": wins,
            "Podiums": podiums,
            "Points": points
        })
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
                <span style="font-size: 12px; color: #000000;">🏆 {wins} Wins</span>
                <span style="font-size: 12px; color: #000000;">🏅 {podiums} Podiums</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Constructor wins & podiums bar chart
    if st.session_state.races_completed > 0:
        st.markdown("---")
        st.markdown("#### 📊 Constructor Wins & Podiums Chart")

        constructor_chart_data = []
        for team, wins in sorted_team_stats:
            podiums = st.session_state.team_podiums[team]
            constructor_chart_data.append({
                "Team": team,
                "Wins": wins,
                "Podiums": podiums
            })

        if constructor_chart_data:
            constr_df = pd.DataFrame(constructor_chart_data)

            fig_constr = go.Figure()
            fig_constr.add_trace(go.Bar(
                name="Wins",
                x=constr_df["Team"],
                y=constr_df["Wins"],
                marker_color=[team_colors[t] for t in constr_df["Team"]],
                marker_line_width=2,
                marker_line_color="rgba(0,0,0,0.4)",
                text=constr_df["Wins"],
                textposition="outside",
                textfont=dict(size=12, color="black")
            ))
            fig_constr.add_trace(go.Bar(
                name="Podiums",
                x=constr_df["Team"],
                y=constr_df["Podiums"],
                marker_color=[team_colors[t] + "80" for t in constr_df["Team"]],
                marker_line_width=2,
                marker_line_color="rgba(0,0,0,0.3)",
                text=constr_df["Podiums"],
                textposition="outside",
                textfont=dict(size=12, color="black")
            ))

            fig_constr.update_layout(
                barmode="group",
                height=480,
                title={
                    'text': "Constructor Wins & Podiums",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#2c3e50'}
                },
                xaxis=dict(
                    title="Team",
                    tickangle=-30,  # Angled so 11 names don't overlap
                    tickfont=dict(size=11, color='#2c3e50'),
                    title_font=dict(size=14, color='#2c3e50')
                ),
                yaxis=dict(
                    title="Count",
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    tickfont=dict(size=11, color='#2c3e50'),
                    title_font=dict(size=14, color='#2c3e50')
                ),
                plot_bgcolor='rgba(248, 249, 250, 0.95)',
                paper_bgcolor='rgba(248, 249, 250, 0.95)',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=20, r=20, t=80, b=80)
            )
            st.plotly_chart(fig_constr, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🏆 Driver Statistics")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
    
    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    driver_stats_data = []
    sorted_driver_stats = sorted(
        st.session_state.driver_wins.items(),
        key=lambda x: (st.session_state.driver_wins[x[0]], st.session_state.driver_podiums[x[0]]),
        reverse=True
    )
    for pos, (driver, wins) in enumerate(sorted_driver_stats, 1):
        team = next(d['team'] for d in drivers if d['driver'] == driver)
        podiums = st.session_state.driver_podiums[driver]
        points = st.session_state.total_driver_points[driver]
        avg = points / st.session_state.races_completed if st.session_state.races_completed > 0 else 0
        rating = calculate_driver_rating(driver)
        driver_stats_data.append({
            "Position": pos,
            "Driver": driver,
            "Team": team,
            "Wins": wins,
            "Podiums": podiums,
            "Points": points
        })
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
                <span style="font-size: 12px; color: #000000;">📊 {avg:.1f} avg</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Driver wins & podiums bar chart
    if st.session_state.races_completed > 0:
        st.markdown("---")
        st.markdown("#### 📊 Driver Wins & Podiums Chart")

        driver_chart_data = []
        for driver, wins in sorted_driver_stats:
            team = next(d['team'] for d in drivers if d['driver'] == driver)
            podiums = st.session_state.driver_podiums[driver]
            driver_chart_data.append({
                "Driver": driver,
                "Team": team,
                "Wins": wins,
                "Podiums": podiums
            })

        if driver_chart_data:
            drv_df = pd.DataFrame(driver_chart_data)

            fig_drv = go.Figure()
            fig_drv.add_trace(go.Bar(
                name="Wins",
                x=drv_df["Driver"],
                y=drv_df["Wins"],
                marker_color=[driver_colors.get(d, "#888888") for d in drv_df["Driver"]],
                marker_line_width=2,
                marker_line_color="rgba(0,0,0,0.4)",
                text=drv_df["Wins"],
                textposition="outside",
                textfont=dict(size=11, color="black"),
                hovertemplate="<b>%{x}</b><br>Wins: %{y}<br><extra></extra>"
            ))
            fig_drv.add_trace(go.Bar(
                name="Podiums",
                x=drv_df["Driver"],
                y=drv_df["Podiums"],
                marker_color=[driver_colors.get(d, "#888888") + "80" for d in drv_df["Driver"]],
                marker_line_width=2,
                marker_line_color="rgba(0,0,0,0.3)",
                text=drv_df["Podiums"],
                textposition="outside",
                textfont=dict(size=11, color="black"),
                hovertemplate="<b>%{x}</b><br>Podiums: %{y}<br><extra></extra>"
            ))

            fig_drv.update_layout(
                barmode="group",
                height=520,  # Taller to fit 22 drivers on x-axis
                title={
                    'text': "Driver Wins & Podiums",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#2c3e50'}
                },
                xaxis=dict(
                    title="Driver",
                    tickangle=-45,  # More angle needed for 22 driver names
                    tickfont=dict(size=10, color='#2c3e50'),
                    title_font=dict(size=14, color='#2c3e50')
                ),
                yaxis=dict(
                    title="Count",
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    tickfont=dict(size=11, color='#2c3e50'),
                    title_font=dict(size=14, color='#2c3e50')
                ),
                plot_bgcolor='rgba(248, 249, 250, 0.95)',
                paper_bgcolor='rgba(248, 249, 250, 0.95)',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=20, r=20, t=80, b=100)  # Extra bottom margin for 22 angled labels
            )
            st.plotly_chart(fig_drv, use_container_width=True)

        st.markdown("---")
        st.markdown("#### ⭐ Driver Ratings Overview")

        ratings_data = []
        for driver_info in drivers:  # All 22 drivers
            driver = driver_info['driver']
            team = driver_info['team']
            rating = calculate_driver_rating(driver)
            points = st.session_state.total_driver_points[driver]
            wins = st.session_state.driver_wins[driver]
            podiums = st.session_state.driver_podiums[driver]
            ratings_data.append({
                "Driver": driver,
                "Team": team,
                "Rating": round(rating, 2),
                "Points": points,
                "Wins": wins,
                "Podiums": podiums
            })

        ratings_data.sort(key=lambda x: x["Rating"], reverse=True)
        ratings_df = pd.DataFrame(ratings_data)
        ratings_df.index = ratings_df.index + 1

        fig_rating = px.bar(
            ratings_df,
            x="Driver",
            y="Rating",
            color="Team",
            text="Rating",
            color_discrete_map=team_colors,
            title="Driver Performance Ratings (out of 10)",
            hover_data=["Team", "Points", "Wins", "Podiums"]
        )
        fig_rating.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside",
            marker_line_width=2,
            marker_line_color="rgba(0,0,0,0.3)",
            textfont=dict(size=10, color="black")
        )
        fig_rating.update_layout(
            height=500,
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50'}
            },
            xaxis=dict(
                title="Driver",
                tickangle=-45,  # Angled for 22 names
                tickfont=dict(size=10, color='#2c3e50'),
                title_font=dict(size=14, color='#2c3e50')
            ),
            yaxis=dict(
                title="Rating (0-10)",
                range=[0, 11],
                gridcolor='rgba(128, 128, 128, 0.2)',
                tickfont=dict(size=11, color='#2c3e50'),
                title_font=dict(size=14, color='#2c3e50')
            ),
            plot_bgcolor='rgba(248, 249, 250, 0.95)',
            paper_bgcolor='rgba(248, 249, 250, 0.95)',
            showlegend=False,
            margin=dict(l=20, r=20, t=80, b=100)  # Extra bottom margin for angled labels
        )
        st.plotly_chart(fig_rating, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# Tab 5: Driver Upgrades
# Tab 5: Driver Upgrades
with tab5:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🛠️ Driver Performance Tuning Center")
    st.markdown("Fine-tune each driver's starting advantage with interactive sliders. Higher values give drivers better race starts!")
    
    # Quick preset buttons
    st.markdown("#### ⚡ Quick Presets")
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
    
    # 11 teams in 2 columns
    team_columns = st.columns(2)
    
    for i, (team, team_drivers) in enumerate(teams_drivers.items()):
        with team_columns[i % 2]:
            st.markdown(f'''
            <div class="rating-card" style="background: linear-gradient(135deg, {team_colors[team]}, {team_colors[team]}40); margin-bottom: 20px;">
                <div class="rating-header">
                    <div>
                        <div class="driver-name" style="font-size: 1.4em; color: #ffffff;">🏁 {team}</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            for driver in team_drivers:
                current_headstart = st.session_state.driver_headstarts.get(driver, 1)
                
                slider_key = f"headstart_slider_{driver}_{team}"
                
                st.markdown(f"**{driver}** - Current: {current_headstart}%")
                
                new_headstart = st.slider(
                    f"Performance Boost for {driver}",
                    min_value=1,
                    max_value=9,
                    value=current_headstart,
                    step=1,
                    key=slider_key,
                    help=f"Adjust {driver}'s starting advantage. Higher values = better race start!"
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
                    <div style="background-color: #f0f0f0; border-radius: 15px; height: 20px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);">
                        <div style="background: linear-gradient(90deg, {driver_colors.get(driver, '#3498db')}, {driver_colors.get(driver, '#3498db')}80); height: 100%; width: {progress_width}%; border-radius: 15px; position: relative; transition: width 0.3s ease;">
                            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 11px; font-weight: bold; color: #ffffff;">
                                {new_headstart}% Boost
                            </div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown("---")
    
    # Summary section
    st.markdown("#### 📊 Performance Summary & Analysis")
    
    headstart_values = list(st.session_state.driver_headstarts.values())
    avg_headstart = sum(headstart_values) / len(headstart_values)
    max_headstart = max(headstart_values)
    min_headstart = min(headstart_values)
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.metric(
            label="🎯 Average Boost",
            value=f"{avg_headstart:.1f}%",
            help="Average headstart across all 22 drivers"
        )
    
    with summary_col2:
        st.metric(
            label="⚡ Highest Boost",
            value=f"{max_headstart}%",
            help="Maximum headstart given to any driver"
        )
    
    with summary_col3:
        st.metric(
            label="🐌 Lowest Boost",
            value=f"{min_headstart}%",
            help="Minimum headstart given to any driver"
        )
    
    with summary_col4:
        boost_range = max_headstart - min_headstart
        st.metric(
            label="📈 Boost Range",
            value=f"{boost_range}%",
            help="Difference between highest and lowest headstart"
        )
    
    st.markdown("---")

    # Boost distribution chart across all 22 drivers
    st.markdown("#### 📊 Boost Distribution Chart")

    boost_chart_data = []
    for driver_info in drivers:  # All 22 drivers
        driver = driver_info['driver']
        team = driver_info['team']
        headstart = st.session_state.driver_headstarts.get(driver, 1)
        boost_chart_data.append({
            "Driver": driver,
            "Team": team,
            "Boost": headstart
        })

    boost_chart_data.sort(key=lambda x: x["Boost"], reverse=True)
    boost_df = pd.DataFrame(boost_chart_data)

    fig_boost = px.bar(
        boost_df,
        x="Driver",
        y="Boost",
        color="Team",
        text="Boost",
        color_discrete_map=team_colors,
        title="Driver Performance Boost Settings",
        labels={"Boost": "Boost %", "Driver": "Driver"}
    )
    fig_boost.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        marker_line_width=2,
        marker_line_color="rgba(0,0,0,0.3)",
        textfont=dict(size=10, color="black")
    )
    fig_boost.update_layout(
        height=480,
        title={
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        xaxis=dict(
            title="Driver",
            tickangle=-45,  # Angled for 22 names
            tickfont=dict(size=10, color='#2c3e50'),
            title_font=dict(size=14, color='#2c3e50')
        ),
        yaxis=dict(
            title="Boost %",
            range=[0, 11],
            gridcolor='rgba(128, 128, 128, 0.2)',
            tickfont=dict(size=11, color='#2c3e50'),
            title_font=dict(size=14, color='#2c3e50')
        ),
        plot_bgcolor='rgba(248, 249, 250, 0.95)',
        paper_bgcolor='rgba(248, 249, 250, 0.95)',
        showlegend=False,
        margin=dict(l=20, r=20, t=80, b=100)  # Extra bottom margin for 22 angled labels
    )
    st.plotly_chart(fig_boost, use_container_width=True)

    st.markdown("---")

    # Top boosted / most conservative split leaderboards
    st.markdown("#### 🏆 Boost Rankings")

    sorted_headstarts = sorted(
        [(driver, headstart, next(d['team'] for d in drivers if d['driver'] == driver))
         for driver, headstart in st.session_state.driver_headstarts.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    boost_col1, boost_col2 = st.columns(2)
    
    with boost_col1:
        st.markdown("##### 🥇 Highest Performance Boosts")
        st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
        for pos, (driver, headstart, team) in enumerate(sorted_headstarts[:11], 1):  # Top 11 of 22
            card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
            medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"{pos}."
            boost_level = "🟢" if headstart <= 3 else "🟡" if headstart <= 6 else "🔴"
            st.markdown(f'''
            <div class="leaderboard-item {card_class}">
                <div style="display: flex; align-items: center;">
                    <span style="margin-right: 8px;">{medal}</span>
                    <div>
                        <div style="font-weight: bold; color: #000000;">{driver}</div>
                        <div style="font-size: 11px; color: #000000; opacity: 0.7;">{team}</div>
                    </div>
                </div>
                <span>{boost_level} {headstart}% Boost</span>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with boost_col2:
        st.markdown("##### 🐌 Most Conservative Setups")
        st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
        conservative_drivers = sorted_headstarts[-11:][::-1]  # Bottom 11 of 22, reversed
        for pos, (driver, headstart, team) in enumerate(conservative_drivers, 1):
            boost_level = "🟢" if headstart <= 3 else "🟡" if headstart <= 6 else "🔴"
            st.markdown(f'''
            <div class="leaderboard-item">
                <div style="display: flex; align-items: center;">
                    <span style="margin-right: 8px;">{pos}.</span>
                    <div>
                        <div style="font-weight: bold; color: #000000;">{driver}</div>
                        <div style="font-size: 11px; color: #000000; opacity: 0.7;">{team}</div>
                    </div>
                </div>
                <span>{boost_level} {headstart}% Boost</span>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Team average boost analysis
    st.markdown("#### 🏗️ Team Boost Analysis")

    team_boost_data = []
    for team, team_drivers in teams_drivers.items():  # All 11 teams
        driver1, driver2 = team_drivers
        d1_boost = st.session_state.driver_headstarts.get(driver1, 1)
        d2_boost = st.session_state.driver_headstarts.get(driver2, 1)
        avg_boost = (d1_boost + d2_boost) / 2
        balance_gap = abs(d1_boost - d2_boost)
        team_boost_data.append({
            "Team": team,
            "Avg Boost": avg_boost,
            "Balance Gap": balance_gap,
            driver1: d1_boost,
            driver2: d2_boost
        })

    team_boost_data.sort(key=lambda x: x["Avg Boost"], reverse=True)

    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    for pos, tb in enumerate(team_boost_data, 1):
        team = tb["Team"]
        driver1, driver2 = teams_drivers[team]
        d1_boost = tb[driver1]
        d2_boost = tb[driver2]
        avg = tb["Avg Boost"]
        gap = tb["Balance Gap"]
        balance_label = "⚖️ Balanced" if gap == 0 else "📊 Close" if gap <= 2 else "📈 Uneven"
        card_class = "position-1" if pos == 1 else "position-2" if pos == 2 else "position-3" if pos == 3 else ""
        position_icon = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"P{pos}"
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <div style="display: flex; align-items: center; min-width: 200px;">
                <span style="margin-right: 10px; font-weight: bold;">{position_icon}</span>
                <div>
                    <div style="font-weight: bold; color: #000000;">{team}</div>
                    <div style="font-size: 11px; color: #000000; opacity: 0.7;">{driver1}: {d1_boost}% | {driver2}: {d2_boost}%</div>
                </div>
            </div>
            <div style="display: flex; gap: 12px; align-items: center;">
                <span style="font-weight: bold; color: #000000;">{avg:.1f}% avg</span>
                <span style="font-size: 11px; color: #000000;">{balance_label}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 💡 Strategy Recommendations")
    
    strategy_col1, strategy_col2, strategy_col3 = st.columns(3)
    
    with strategy_col1:
        st.markdown(f'''
        <div class="rating-card" style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); color: #000000;">
            <div class="rating-header">
                <div>
                    <div class="driver-name">🟢 Conservative (1-3%)</div>
                    <div class="team-name">Realistic Racing</div>
                </div>
            </div>
            <div style="font-size: 13px; line-height: 1.4; margin-top: 10px; color: #000000;">
                • Minimal advantage<br>
                • Pure skill-based racing<br>
                • Unpredictable outcomes<br>
                • Great for close competition
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with strategy_col2:
        st.markdown(f'''
        <div class="rating-card" style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); color: #000000;">
            <div class="rating-header">
                <div>
                    <div class="driver-name">🟡 Moderate (4-6%)</div>
                    <div class="team-name">Balanced Approach</div>
                </div>
            </div>
            <div style="font-size: 13px; line-height: 1.4; margin-top: 10px; color: #000000;">
                • Noticeable but fair advantage<br>
                • Rewards driver favorites<br>
                • Still allows comebacks<br>
                • Good for storylines
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with strategy_col3:
        st.markdown(f'''
        <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: #000000;">
            <div class="rating-header">
                <div>
                    <div class="driver-name">🔴 Aggressive (7-9%)</div>
                    <div class="team-name">Dominant Performance</div>
                </div>
            </div>
            <div style="font-size: 13px; line-height: 1.4; margin-top: 10px; color: #000000;">
                • Significant head start<br>
                • Favors top drivers heavily<br>
                • More predictable results<br>
                • Creates clear favorites
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 6: Season Summary - Enhanced with More Awards
# Tab 6: Season Summary
with tab6:
    st.markdown('<div class="race-container">', unsafe_allow_html=True)
    st.markdown("### 🏁 Season Summary")
    st.markdown(f"**Races Completed: {st.session_state.races_completed}**")
    
    if st.session_state.races_completed > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 Drivers' Championship Leaders")
            sorted_driver_standings = sorted(st.session_state.total_driver_points.items(), key=lambda x: x[1], reverse=True)
            for i, (driver, points) in enumerate(sorted_driver_standings[:3]):
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
                        <span>Avg: {points/st.session_state.races_completed:.1f} pts/race</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🏗️ Constructors' Championship Leaders")
            sorted_team_standings = sorted(st.session_state.total_team_points.items(), key=lambda x: x[1], reverse=True)
            for i, (team, points) in enumerate(sorted_team_standings[:3]):
                wins = st.session_state.team_wins[team]
                podiums = st.session_state.team_podiums[team]
                driver1, driver2 = teams_drivers[team]
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                
                card_class = "rating-card-gold" if i == 0 else "rating-card-silver" if i == 1 else "rating-card-bronze"
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                position = "1st" if i == 0 else "2nd" if i == 1 else "3rd"
                
                st.markdown(f'''
                <div class="rating-card {card_class}">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">{medal} {position} - {team}</div>
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
        
        st.markdown("---")
        st.markdown("#### 📊 Season Statistics Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🏁 Total Races",
                value=st.session_state.races_completed
            )
        
        with col2:
            if sorted_driver_standings:
                most_successful_driver = sorted_driver_standings[0][0]
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_successful_driver)
                st.metric(
                    label="🏆 Championship Leader",
                    value=f"{most_successful_driver}",
                    delta=f"({driver_team})"
                )
        
        with col3:
            if sorted_team_standings:
                most_successful_team = sorted_team_standings[0][0]
                st.metric(
                    label="🏗️ Constructor Leader",
                    value=f"{most_successful_team}",
                    delta=f"{sorted_team_standings[0][1]} pts"
                )
        
        with col4:
            total_points_awarded = sum(st.session_state.total_driver_points.values())
            st.metric(
                label="💯 Total Points Awarded",
                value=total_points_awarded
            )
        
        st.markdown("---")
        st.markdown("#### 🏆 Race Winners Summary")
        if st.session_state.race_summaries:
            st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
            for idx, summary in enumerate(st.session_state.race_summaries):
                card_class = "position-1" if idx == 0 else ""
                st.markdown(f'''
                <div class="leaderboard-item {card_class}">
                    <span>Race {summary['Race']}</span>
                    <span>Winner: {summary['P1']} | 2nd: {summary['P2']} | 3rd: {summary['P3']}</span>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="rating-card">', unsafe_allow_html=True)
            st.write("No race winners data available yet.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 🎖️ Major Awards & Recognitions")
        
        # Row 1: Top Performance Awards
        award_col1, award_col2, award_col3 = st.columns(3)
        
        with award_col1:
            most_wins_driver = max(st.session_state.driver_wins.items(), key=lambda x: x[1])
            if most_wins_driver[1] > 0:
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_wins_driver[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏆 Race Winner King</div>
                            <div class="team-name">{most_wins_driver[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{most_wins_driver[1]}</div>
                    </div>
                    <div class="rating-details">
                        <span>Win Rate: {(most_wins_driver[1]/st.session_state.races_completed)*100:.1f}%</span>
                        <span>Total Points: {st.session_state.total_driver_points[most_wins_driver[0]]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏆 Race Winner King</div>
                            <div class="team-name">No wins yet this season</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col2:
            most_podiums_driver = max(st.session_state.driver_podiums.items(), key=lambda x: x[1])
            if most_podiums_driver[1] > 0:
                driver_team = next(d['team'] for d in drivers if d['driver'] == most_podiums_driver[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🥇 Podium Master</div>
                            <div class="team-name">{most_podiums_driver[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{most_podiums_driver[1]}</div>
                    </div>
                    <div class="rating-details">
                        <span>Podium Rate: {(most_podiums_driver[1]/st.session_state.races_completed)*100:.1f}%</span>
                        <span>Total Points: {st.session_state.total_driver_points[most_podiums_driver[0]]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🥇 Podium Master</div>
                            <div class="team-name">No podiums yet this season</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col3:
            best_constructor = max(st.session_state.total_team_points.items(), key=lambda x: x[1])
            if best_constructor[1] > 0:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏗️ Constructor Champion</div>
                            <div class="team-name">{best_constructor[0]}</div>
                        </div>
                        <div class="rating-score">{best_constructor[1]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Wins: {st.session_state.team_wins[best_constructor[0]]}</span>
                        <span>Podiums: {st.session_state.team_podiums[best_constructor[0]]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏗️ Constructor Champion</div>
                            <div class="team-name">No points yet this season</div>
                        </div>
                        <div class="rating-score">0 pts</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 2: Performance Excellence Awards
        st.markdown("---")
        award_col4, award_col5, award_col6 = st.columns(3)
        
        with award_col4:
            consistent_driver = None
            consistent_points = 0
            for driver, points in sorted_driver_standings:
                if st.session_state.driver_wins[driver] == 0 and points > consistent_points:
                    consistent_driver = driver
                    consistent_points = points
            
            if consistent_driver:
                driver_team = next(d['team'] for d in drivers if d['driver'] == consistent_driver)
                podiums = st.session_state.driver_podiums[consistent_driver]
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🌟 Mr. Reliable</div>
                            <div class="team-name">{consistent_driver} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{consistent_points} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>No Wins, All Points</span>
                        <span>Podiums: {podiums}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🌟 Mr. Reliable</div>
                            <div class="team-name">No reliable driver yet</div>
                        </div>
                        <div class="rating-score">0 pts</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col5:
            highest_rated_driver = max(
                [(d['driver'], calculate_driver_rating(d['driver'])) for d in drivers],
                key=lambda x: x[1]
            )
            driver_team = next(d['team'] for d in drivers if d['driver'] == highest_rated_driver[0])
            rating = highest_rated_driver[1]
            points = st.session_state.total_driver_points[highest_rated_driver[0]]
            
            st.markdown(f'''
            <div class="rating-card" style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: #000000;">
                <div class="rating-header">
                    <div>
                        <div class="driver-name">⭐ Highest Rated</div>
                        <div class="team-name">{highest_rated_driver[0]} ({driver_team})</div>
                    </div>
                    <div class="rating-score">{rating:.1f}/10</div>
                </div>
                <div class="rating-details">
                    <span>Points: {points}</span>
                    <span>Elite Performance</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with award_col6:
            rookie_candidates = [(driver, points) for driver, points in sorted_driver_standings if points < 50 and points > 0]
            if rookie_candidates:
                best_rookie = max(rookie_candidates, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_rookie[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e67e22 0%, #d35400 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🌱 Rising Star</div>
                            <div class="team-name">{best_rookie[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_rookie[1]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Promising Talent</span>
                        <span>Future Champion</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e67e22 0%, #d35400 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🌱 Rising Star</div>
                            <div class="team-name">No rising star yet</div>
                        </div>
                        <div class="rating-score">0 pts</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 3: Special Recognition Awards
        st.markdown("---")
        award_col7, award_col8, award_col9 = st.columns(3)
        
        with award_col7:
            if len(st.session_state.race_summaries) >= 3:
                recent_winners = [summary["P1"].split(' (')[1].replace(')', '') for summary in st.session_state.race_summaries[-3:]]
                team_recent_wins = {}
                for team_name in recent_winners:
                    team_recent_wins[team_name] = team_recent_wins.get(team_name, 0) + 1
                
                if team_recent_wins:
                    most_improved_team = max(team_recent_wins.items(), key=lambda x: x[1])
                    team_total_wins = st.session_state.team_wins[most_improved_team[0]]
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #16a085 0%, #138d75 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">📈 Most Improved Team</div>
                                <div class="team-name">{most_improved_team[0]}</div>
                            </div>
                            <div class="rating-score">{most_improved_team[1]}/3</div>
                        </div>
                        <div class="rating-details">
                            <span>Recent Form</span>
                            <span>Total Wins: {team_total_wins}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #16a085 0%, #138d75 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">📈 Most Improved Team</div>
                                <div class="team-name">Need more races</div>
                            </div>
                            <div class="rating-score">0</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #16a085 0%, #138d75 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">📈 Most Improved Team</div>
                            <div class="team-name">Need more races</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col8:
            best_avg_driver = None
            best_avg = 0
            for driver, points in sorted_driver_standings:
                if points > 0:
                    avg = points / st.session_state.races_completed
                    if avg > best_avg:
                        best_avg = avg
                        best_avg_driver = driver
            
            if best_avg_driver:
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_avg_driver)
                total_points = st.session_state.total_driver_points[best_avg_driver]
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #8e44ad 0%, #7d3c98 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">⚡ Point Scoring Machine</div>
                            <div class="team-name">{best_avg_driver} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_avg:.1f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Avg/Race</span>
                        <span>Total: {total_points} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #8e44ad 0%, #7d3c98 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">⚡ Point Scoring Machine</div>
                            <div class="team-name">No points yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col9:
            underdog_candidates = []
            for driver_info in drivers:  # All 22 drivers
                driver = driver_info['driver']
                headstart = st.session_state.driver_headstarts.get(driver, 1)
                points = st.session_state.total_driver_points[driver]
                if points > 0:
                    efficiency_score = points / headstart
                    underdog_candidates.append((driver, efficiency_score, points, headstart))
            
            if underdog_candidates:
                best_underdog = max(underdog_candidates, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_underdog[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #d35400 0%, #ba4a00 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🦾 Underdog Hero</div>
                            <div class="team-name">{best_underdog[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_underdog[1]:.1f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Efficiency Score</span>
                        <span>{best_underdog[2]} pts @ {best_underdog[3]}%</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #d35400 0%, #ba4a00 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🦾 Underdog Hero</div>
                            <div class="team-name">No underdog yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 4: Team Excellence Awards
        st.markdown("---")
        award_col10, award_col11, award_col12 = st.columns(3)
        
        with award_col10:
            best_partnership = None
            smallest_gap = float('inf')
            for team, team_drivers in teams_drivers.items():  # All 11 teams
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                gap = abs(driver1_points - driver2_points)
                total_team_points = driver1_points + driver2_points
                
                if total_team_points > 0 and gap < smallest_gap:
                    smallest_gap = gap
                    best_partnership = (team, gap, total_team_points)
            
            if best_partnership:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🤝 Best Partnership</div>
                            <div class="team-name">{best_partnership[0]}</div>
                        </div>
                        <div class="rating-score">{best_partnership[1]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Gap Between Teammates</span>
                        <span>Team Total: {best_partnership[2]} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🤝 Best Partnership</div>
                            <div class="team-name">No partnerships yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col11:
            giant_killer = None
            best_teammate_beating_ratio = 0
            for team, team_drivers in teams_drivers.items():  # All 11 teams
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                driver1_headstart = st.session_state.driver_headstarts.get(driver1, 1)
                driver2_headstart = st.session_state.driver_headstarts.get(driver2, 1)
                
                if driver1_headstart < driver2_headstart and driver1_points > driver2_points:
                    ratio = driver1_points / driver2_points if driver2_points > 0 else 1
                    if ratio > best_teammate_beating_ratio:
                        best_teammate_beating_ratio = ratio
                        giant_killer = (driver1, team, driver1_points, driver2_points)
                elif driver2_headstart < driver1_headstart and driver2_points > driver1_points:
                    ratio = driver2_points / driver1_points if driver1_points > 0 else 1
                    if ratio > best_teammate_beating_ratio:
                        best_teammate_beating_ratio = ratio
                        giant_killer = (driver2, team, driver2_points, driver1_points)
            
            if giant_killer:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #cb4335 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🗡️ Giant Killer</div>
                            <div class="team-name">{giant_killer[0]} ({giant_killer[1]})</div>
                        </div>
                        <div class="rating-score">{best_teammate_beating_ratio:.1f}x</div>
                    </div>
                    <div class="rating-details">
                        <span>Beat Favored Teammate</span>
                        <span>{giant_killer[2]} vs {giant_killer[3]} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #e74c3c 0%, #cb4335 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🗡️ Giant Killer</div>
                            <div class="team-name">No giant killers yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col12:
            if st.session_state.race_summaries:
                comeback_scores = {}
                for summary in st.session_state.race_summaries:
                    p1_driver = summary["P1"].split(' (')[0]
                    p2_driver = summary["P2"].split(' (')[0]
                    p3_driver = summary["P3"].split(' (')[0]
                    comeback_scores[p1_driver] = comeback_scores.get(p1_driver, 0) + 3
                    comeback_scores[p2_driver] = comeback_scores.get(p2_driver, 0) + 2
                    comeback_scores[p3_driver] = comeback_scores.get(p3_driver, 0) + 1
                
                if comeback_scores:
                    comeback_king = max(comeback_scores.items(), key=lambda x: x[1])
                    driver_team = next(d['team'] for d in drivers if d['driver'] == comeback_king[0])
                    driver_wins = st.session_state.driver_wins[comeback_king[0]]
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">👑 Comeback King</div>
                                <div class="team-name">{comeback_king[0]} ({driver_team})</div>
                            </div>
                            <div class="rating-score">{comeback_king[1]}</div>
                        </div>
                        <div class="rating-details">
                            <span>Podium Score</span>
                            <span>Wins: {driver_wins}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">👑 Comeback King</div>
                                <div class="team-name">No comebacks yet</div>
                            </div>
                            <div class="rating-score">0</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">👑 Comeback King</div>
                            <div class="team-name">Need more races</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 5: Specialty Awards
        st.markdown("---")
        award_col13, award_col14, award_col15 = st.columns(3)
        
        with award_col13:
            speed_demons = []
            for driver_info in drivers:  # All 22 drivers
                driver = driver_info['driver']
                headstart = st.session_state.driver_headstarts.get(driver, 1)
                points = st.session_state.total_driver_points[driver]
                if headstart >= 7 and points > 20:
                    speed_demons.append((driver, headstart, points))
            
            if speed_demons:
                best_speed_demon = max(speed_demons, key=lambda x: x[2])
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_speed_demon[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">💨 Speed Demon</div>
                            <div class="team-name">{best_speed_demon[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_speed_demon[2]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>High Headstart: {best_speed_demon[1]}%</span>
                        <span>Still Delivers</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">💨 Speed Demon</div>
                            <div class="team-name">No speed demons yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col14:
            dark_horses = []
            for driver_info in drivers:  # All 22 drivers
                driver = driver_info['driver']
                headstart = st.session_state.driver_headstarts.get(driver, 1)
                points = st.session_state.total_driver_points[driver]
                wins = st.session_state.driver_wins[driver]
                if headstart <= 3 and (points > 30 or wins > 0):
                    dark_horses.append((driver, points, wins, headstart))
            
            if dark_horses:
                best_dark_horse = max(dark_horses, key=lambda x: (x[2], x[1]))
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_dark_horse[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%); color: #ffffff;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name" style="color: #ffffff;">🐎 Dark Horse</div>
                            <div class="team-name" style="color: #ffffff;">{best_dark_horse[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score" style="color: #ffffff;">{best_dark_horse[1]} pts</div>
                    </div>
                    <div class="rating-details" style="color: #ffffff;">
                        <span>Low Expectations</span>
                        <span>Wins: {best_dark_horse[2]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%); color: #ffffff;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name" style="color: #ffffff;">🐎 Dark Horse</div>
                            <div class="team-name" style="color: #ffffff;">No dark horses yet</div>
                        </div>
                        <div class="rating-score" style="color: #ffffff;">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col15:
            veterans = []
            for driver, points in sorted_driver_standings[1:6]:
                if points > 0:
                    consistency_score = points / st.session_state.races_completed
                    podiums = st.session_state.driver_podiums[driver]
                    veterans.append((driver, consistency_score, points, podiums))
            
            if veterans:
                best_veteran = max(veterans, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_veteran[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #9c88ff 0%, #8c7ae6 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🎖️ Veteran Excellence</div>
                            <div class="team-name">{best_veteran[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_veteran[1]:.1f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Consistent Performer</span>
                        <span>{best_veteran[2]} pts, {best_veteran[3]} podiums</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #9c88ff 0%, #8c7ae6 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🎖️ Veteran Excellence</div>
                            <div class="team-name">No veterans yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 6: Fun & Special Categories
        st.markdown("---")
        award_col16, award_col17, award_col18 = st.columns(3)
        
        with award_col16:
            lucky_charms = []
            for driver_info in drivers:  # All 22 drivers
                driver = driver_info['driver']
                points = st.session_state.total_driver_points[driver]
                wins = st.session_state.driver_wins[driver]
                podiums = st.session_state.driver_podiums[driver]
                if points > 15 and wins == 0 and podiums <= 1:
                    lucky_charms.append((driver, points))
            
            if lucky_charms:
                luckiest_driver = max(lucky_charms, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == luckiest_driver[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #00d2d3 0%, #00a8cc 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🍀 Lucky Charm</div>
                            <div class="team-name">{luckiest_driver[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{luckiest_driver[1]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Points Without Glory</span>
                        <span>Solid Finisher</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #00d2d3 0%, #00a8cc 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🍀 Lucky Charm</div>
                            <div class="team-name">No lucky drivers yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col17:
            perfect_storms = []
            for team, team_drivers in teams_drivers.items():  # All 11 teams
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                min_points = min(driver1_points, driver2_points)
                total_points = driver1_points + driver2_points
                
                if min_points > 20 and total_points > 60:
                    perfect_storms.append((team, total_points, min_points))
            
            if perfect_storms:
                best_storm = max(perfect_storms, key=lambda x: x[2])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ff9ff3 0%, #f368e0 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">⛈️ Perfect Storm</div>
                            <div class="team-name">{best_storm[0]}</div>
                        </div>
                        <div class="rating-score">{best_storm[1]} pts</div>
                    </div>
                    <div class="rating-details">
                        <span>Both Drivers Excel</span>
                        <span>Min: {best_storm[2]} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ff9ff3 0%, #f368e0 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">⛈️ Perfect Storm</div>
                            <div class="team-name">No perfect storms yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col18:
            overachievers = []
            for driver_info in drivers:  # All 22 drivers
                driver = driver_info['driver']
                headstart = st.session_state.driver_headstarts.get(driver, 1)
                points = st.session_state.total_driver_points[driver]
                if points > 0:
                    ratio = points / headstart
                    overachievers.append((driver, ratio, points, headstart))
            
            if overachievers:
                best_overachiever = max(overachievers, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == best_overachiever[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🚀 Overachiever</div>
                            <div class="team-name">{best_overachiever[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{best_overachiever[1]:.1f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Points/Headstart Ratio</span>
                        <span>{best_overachiever[2]} pts @ {best_overachiever[3]}%</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🚀 Overachiever</div>
                            <div class="team-name">No overachievers yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Row 7: Final Special Recognition
        st.markdown("---")
        award_col19, award_col20, award_col21 = st.columns(3)
        
        with award_col19:
            if st.session_state.race_summaries:
                first_time_winners = []
                seen_winners = set()
                for summary in st.session_state.race_summaries:
                    winner = summary["P1"].split(' (')[0]
                    if winner not in seen_winners:
                        first_time_winners.append(winner)
                        seen_winners.add(winner)
                
                if first_time_winners:
                    breakthrough_driver = first_time_winners[0]
                    driver_team = next(d['team'] for d in drivers if d['driver'] == breakthrough_driver)
                    total_wins = st.session_state.driver_wins[breakthrough_driver]
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #ff6348 0%, #ff3838 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">💥 Breakthrough Driver</div>
                                <div class="team-name">{breakthrough_driver} ({driver_team})</div>
                            </div>
                            <div class="rating-score">{total_wins}</div>
                        </div>
                        <div class="rating-details">
                            <span>First Season Winner</span>
                            <span>Made History</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="rating-card" style="background: linear-gradient(135deg, #ff6348 0%, #ff3838 100%); color: #000000;">
                        <div class="rating-header">
                            <div>
                                <div class="driver-name">💥 Breakthrough Driver</div>
                                <div class="team-name">No breakthroughs yet</div>
                            </div>
                            <div class="rating-score">0</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ff6348 0%, #ff3838 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">💥 Breakthrough Driver</div>
                            <div class="team-name">No breakthroughs yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col20:
            harmony_teams = []
            for team, team_drivers in teams_drivers.items():  # All 11 teams
                driver1, driver2 = team_drivers
                driver1_points = st.session_state.total_driver_points[driver1]
                driver2_points = st.session_state.total_driver_points[driver2]
                total_points = driver1_points + driver2_points
                
                if total_points > 0:
                    balance_score = min(driver1_points, driver2_points) / max(driver1_points, driver2_points) if max(driver1_points, driver2_points) > 0 else 0
                    harmony_teams.append((team, balance_score, total_points, min(driver1_points, driver2_points)))
            
            if harmony_teams:
                most_harmonious = max(harmony_teams, key=lambda x: (x[1], x[3]))
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🎵 Team Harmony</div>
                            <div class="team-name">{most_harmonious[0]}</div>
                        </div>
                        <div class="rating-score">{most_harmonious[1]:.2f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Perfect Balance</span>
                        <span>Total: {most_harmonious[2]} pts</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🎵 Team Harmony</div>
                            <div class="team-name">No harmony yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with award_col21:
            contenders = []
            for driver, points in sorted_driver_standings[:5]:
                podiums = st.session_state.driver_podiums[driver]
                wins = st.session_state.driver_wins[driver]
                if points > 25 and podiums >= 2:
                    championship_score = (wins * 3) + (podiums * 2) + (points * 0.1)
                    contenders.append((driver, championship_score, points, wins, podiums))
            
            if contenders:
                top_contender = max(contenders, key=lambda x: x[1])
                driver_team = next(d['team'] for d in drivers if d['driver'] == top_contender[0])
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #a55eea 0%, #8854d0 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏁 Championship Contender</div>
                            <div class="team-name">{top_contender[0]} ({driver_team})</div>
                        </div>
                        <div class="rating-score">{top_contender[1]:.0f}</div>
                    </div>
                    <div class="rating-details">
                        <span>Championship Score</span>
                        <span>{top_contender[3]}W {top_contender[4]}P</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="rating-card" style="background: linear-gradient(135deg, #a55eea 0%, #8854d0 100%); color: #000000;">
                    <div class="rating-header">
                        <div>
                            <div class="driver-name">🏁 Championship Contender</div>
                            <div class="team-name">No contenders yet</div>
                        </div>
                        <div class="rating-score">0</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Awards legend
        st.markdown("---")
        st.markdown("#### 📖 Awards Guide")

        awards_legend = [
            ("🏆 Race Winner King", "Driver with the most race wins"),
            ("🥇 Podium Master", "Driver with the most podium finishes"),
            ("🏗️ Constructor Champion", "Team with the most total points"),
            ("🌟 Mr. Reliable", "Most points without a single race win"),
            ("⭐ Highest Rated", "Best overall driver rating score (0-10)"),
            ("🌱 Rising Star", "Best performing driver with under 50 points"),
            ("📈 Most Improved Team", "Team with most wins in last 3 races"),
            ("⚡ Point Scoring Machine", "Highest average points per race"),
            ("🦾 Underdog Hero", "Best points-to-headstart efficiency"),
            ("🤝 Best Partnership", "Teammates with smallest points gap"),
            ("🗡️ Giant Killer", "Lower headstart driver who beats favored teammate"),
            ("👑 Comeback King", "Highest cumulative podium score across all races"),
            ("💨 Speed Demon", "High headstart (≥7%) driver delivering 20+ points"),
            ("🐎 Dark Horse", "Low headstart (≤3%) driver with 30+ pts or a win"),
            ("🎖️ Veteran Excellence", "Most consistent top-5 championship performer"),
            ("🍀 Lucky Charm", "15+ points with 0 wins and ≤1 podium"),
            ("⛈️ Perfect Storm", "Team with both drivers on 20+ pts and 60+ team total"),
            ("🚀 Overachiever", "Best points-to-headstart percentage ratio"),
            ("💥 Breakthrough Driver", "First unique race winner of the season"),
            ("🎵 Team Harmony", "Team with most balanced driver point distribution"),
            ("🏁 Championship Contender", "Top-5 driver with 25+ pts and 2+ podiums"),
        ]

        legend_col1, legend_col2 = st.columns(2)
        for idx, (award, description) in enumerate(awards_legend):
            with legend_col1 if idx % 2 == 0 else legend_col2:
                st.markdown(f'''
                <div style="background: rgba(255,255,255,0.9); border-radius: 8px; padding: 10px 14px;
                            margin-bottom: 8px; border-left: 4px solid #667eea;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.08);">
                    <div style="font-weight: bold; color: #000000; font-size: 13px;">{award}</div>
                    <div style="color: #000000; font-size: 11px; opacity: 0.75; margin-top: 2px;">{description}</div>
                </div>
                ''', unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="rating-card">', unsafe_allow_html=True)
        st.markdown("#### 🏁 No Data Available")
        st.write("Complete some races to see the season summary!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

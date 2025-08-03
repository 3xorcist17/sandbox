import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Formula 1 Racing 🏎️🏁🚥🏆")
st.set_page_config(page_title="Formula 1", layout="wide")

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
    
    .qualifying-container {
        background: linear-gradient(135deg, #2ecc71 0%, #000000 100%);
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
    
    .qualifying-row {
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
    
    .qualify-button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-left: 10px;
    }
    
    .qualify-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
    }
    
    .qualify-button:disabled {
        background: #95a5a6;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    .grid-position {
        font-size: 16px;
        font-weight: bold;
        color: #000000;
        margin-right: 15px;
        min-width: 30px;
        text-align: center;
    }
    
    .lap-time {
        font-size: 14px;
        font-weight: bold;
        color: #000000;
        min-width: 80px;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# Team and driver data (unchanged from original)
teams_drivers = {
    "Alpine": ["Gas", "Col"],
    "Aston Martin": ["Alo", "Str"],
    "Ferrari": ["Lec", "Ham"],
    "Haas": ["Oco", "Bea"],
    "McLaren": ["Nor", "Pia"],
    "Mercedes": ["Rus", "Ant"],
    "Racing Bulls": ["Had", "Law"],
    "Red Bull": ["Ver", "Tsu"],
    "Sauber": ["Hul", "Bor"],
    "Williams": ["Sai", "Alb"]
}

# Team colors (unchanged)
team_colors = {
    "Alpine": "hsl(308, 100%, 34.4%)",
    "Aston Martin": "hsl(185, 99.6%, 31.7%)",
    "Ferrari": "hsl(0, 99.6%, 39.7%)",
    "Haas": "hsl(0, 99.6%, 28.2%)",
    "McLaren": "hsl(33, 99.6%, 42.4%)",
    "Mercedes": "hsl(165, 99.6%, 9.4%)",
    "Racing Bulls": "hsl(198, 99.6%, 80.3%)",
    "Red Bull": "hsl(247, 99.6%, 24.1%)",
    "Sauber": "hsl(124, 99.6%, 31.4%)",
    "Williams": "hsl(201, 99.6%, 32.2%)"
}

# Driver colors (unchanged)
driver_colors = {}
for team, drivers_list in teams_drivers.items():
    color_parts = team_colors[team].replace('hsl(', '').replace(')', '').split(',')
    hue = float(color_parts[0])
    saturation = float(color_parts[1].replace('%', ''))
    lightness = float(color_parts[2].replace('%', ''))
    driver_colors[drivers_list[0]] = f"hsl({hue}, {saturation}%, {min(100, lightness + 5)}%)"
    driver_colors[drivers_list[1]] = f"hsl({hue}, {saturation}%, {max(0, lightness - 5)}%)"

# Flatten drivers list (unchanged)
drivers = []
for team, driver_list in teams_drivers.items():
    for driver in driver_list:
        drivers.append({"driver": driver, "team": team})

# Points system (unchanged)
points_system = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# Initialize session state (with qualifying additions)
if 'progress_values' not in st.session_state:
    st.session_state.progress_values = [0] * 20
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

# Qualifying session state
if 'qualifying_times' not in st.session_state:
    st.session_state.qualifying_times = {}
if 'qualifying_completed' not in st.session_state:
    st.session_state.qualifying_completed = {}
if 'starting_grid' not in st.session_state:
    st.session_state.starting_grid = list(range(20))  # Default order
if 'grid_positions' not in st.session_state:
    st.session_state.grid_positions = {}

# Functions (unchanged)
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
    
    for driver_info in st.session_state.finish_order:
        finished_drivers.append({
            'driver': driver_info['driver'],
            'team': driver_info['team'],
            'progress': 100,
            'finished': True
        })
    
    finished_driver_names = [d['driver'] for d in st.session_state.finish_order]
    for i, driver_info in enumerate(drivers):
        if driver_info['driver'] not in finished_driver_names:
            racing_drivers.append({
                'driver': driver_info['driver'],
                'team': driver_info['team'],
                'progress': st.session_state.progress_values[i],
                'finished': False,
                'index': i
            })
    
    racing_drivers.sort(key=lambda x: x['progress'], reverse=True)
    return finished_drivers + racing_drivers

def run_qualifying_lap(driver_index):
    """Run a qualifying lap for a specific driver"""
    driver_info = drivers[driver_index]
    driver = driver_info['driver']
    
    # Generate a random lap time (in seconds, between 75-85 seconds for realism)
    base_time = 80.0
    variation = random.uniform(-5.0, 5.0)  # ±5 seconds variation
    driver_skill = random.uniform(-2.0, 2.0)  # Driver skill factor
    
    lap_time = base_time + variation + driver_skill
    lap_time = round(lap_time, 3)
    
    st.session_state.qualifying_times[driver] = lap_time
    st.session_state.qualifying_completed[driver] = True
    
    return lap_time

def calculate_starting_grid():
    """Calculate starting grid based on qualifying times"""
    if not st.session_state.qualifying_times:
        return
    
    # Sort drivers by qualifying time (fastest first)
    sorted_times = sorted(st.session_state.qualifying_times.items(), key=lambda x: x[1])
    
    # Create grid positions
    for position, (driver, lap_time) in enumerate(sorted_times, 1):
        st.session_state.grid_positions[driver] = position
    
    # Update starting grid order
    driver_names = [driver['driver'] for driver in drivers]
    st.session_state.starting_grid = []
    
    for driver, _ in sorted_times:
        driver_index = next(i for i, d in enumerate(drivers) if d['driver'] == driver)
        st.session_state.starting_grid.append(driver_index)
    
    # Add any drivers who didn't qualify at the back
    for i, driver_info in enumerate(drivers):
        if i not in st.session_state.starting_grid:
            st.session_state.starting_grid.append(i)

def get_progress_multiplier(grid_position):
    """Get progress multiplier based on grid position"""
    if grid_position <= 3:
        return 1.10  # +10% faster
    elif grid_position <= 6:
        return 1.05  # +5% faster
    elif grid_position <= 10:
        return 1.00  # Normal
    elif grid_position <= 15:
        return 0.95  # -5% slower
    else:
        return 0.90  # -10% slower

# Create tabs - added Qualifying tab
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Qualifying",
    "Race & Results",
    "Drivers' Championship",
    "Constructors' Championship",
    "Team & Driver Stats",
    "Driver Upgrades",
    "Season Summary"
])

# Tab 1: Qualifying
with tab1:
    st.markdown('<div class="qualifying-container">', unsafe_allow_html=True)
    st.markdown("### 🏁 Qualifying Session")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**Individual Qualifying Runs**")
        
        # Display all drivers with their qualifying buttons
        for i, driver_info in enumerate(drivers):
            driver = driver_info['driver']
            team = driver_info['team']
            
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
            
            # Check if driver has completed qualifying
            completed = st.session_state.qualifying_completed.get(driver, False)
            lap_time = st.session_state.qualifying_times.get(driver, 0)
            grid_pos = st.session_state.grid_positions.get(driver, "-")
            
            if completed:
                status_text = f"{lap_time:.3f}s"
                status_subtext = f"Grid: P{grid_pos}"
                button_text = "✓ Completed"
            else:
                status_text = "Not Set"
                status_subtext = "Ready to Qualify"
                button_text = "🏁 Qualify"
            
            # Create qualifying row
            col_driver, col_button = st.columns([4, 1])
            
            with col_driver:
                qualifying_html = f'''
                <div class="qualifying-row" 
                     style="--driver-color: {base_color}; --driver-color-light: {light_color};">
                    <div class="grid-position">{grid_pos if grid_pos != "-" else "—"}</div>
                    <div class="driver-info">
                        <div class="driver-name">{driver}</div>
                        <div class="team-name">{team}</div>
                    </div>
                    <div class="progress-status" style="margin-left: auto;">
                        <div class="status-text">{status_text}</div>
                        <div class="status-subtext">{status_subtext}</div>
                    </div>
                </div>
                '''
                st.markdown(qualifying_html, unsafe_allow_html=True)
            
            with col_button:
                if st.button(button_text, key=f"qualify_{driver}", disabled=completed):
                    lap_time = run_qualifying_lap(i)
                    calculate_starting_grid()
                    st.rerun()
    
    with col2:
        st.markdown("**Qualifying Results**")
        
        if st.session_state.qualifying_times:
            # Sort by qualifying time
            sorted_results = sorted(st.session_state.qualifying_times.items(), key=lambda x: x[1])
            
            st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
            for pos, (driver, lap_time) in enumerate(sorted_results, 1):
                # Find team for this driver
                team = next(d['team'] for d in drivers if d['driver'] == driver)
                
                # Determine gap to pole
                if pos == 1:
                    gap_text = "POLE"
                    card_class = "position-1"
                else:
                    gap = lap_time - sorted_results[0][1]
                    gap_text = f"+{gap:.3f}s"
                    card_class = "position-2" if pos == 2 else "position-3" if pos == 3 else ""
                
                st.markdown(f'''
                <div class="leaderboard-item {card_class}">
                    <span>P{pos}. {driver} ({team})</span>
                    <span>{lap_time:.3f}s ({gap_text})</span>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No qualifying times set yet")
    
    # Reset qualifying button
    if st.button("🔄 Reset Qualifying"):
        st.session_state.qualifying_times = {}
        st.session_state.qualifying_completed = {}
        st.session_state.grid_positions = {}
        st.session_state.starting_grid = list(range(20))
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Race & Results (modified to use qualifying grid)
with tab2:
    # Check if qualifying is completed
    qualifying_done = len(st.session_state.qualifying_times) > 0
    
    if not qualifying_done:
        st.warning("⚠️ Please complete qualifying first before starting the race!")
    
    if st.button("🏁 Start Race", disabled=not qualifying_done):
        st.session_state.progress_values = [0] * 20
        
        # Use qualifying grid positions instead of random start
        if st.session_state.starting_grid:
            for i, driver_info in enumerate(drivers):
                driver = driver_info['driver']
                # Find grid position for this driver
                grid_position = st.session_state.grid_positions.get(driver, 20)
                
                # Apply grid position multiplier as starting advantage
                multiplier = get_progress_multiplier(grid_position)
                headstart = st.session_state.driver_headstarts.get(driver, 1)
                st.session_state.progress_values[i] = min(100, headstart * multiplier)
        else:
            # Fallback to original logic if no qualifying
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
            
            for i in range(20):
                if st.session_state.progress_values[i] < 100:
                    # Apply grid position multiplier
                    driver = drivers[i]['driver']
                    grid_position = st.session_state.grid_positions.get(driver, 20)
                    multiplier = get_progress_multiplier(grid_position)
                    
                    base_increment = random.randint(0, 4)
                    increment = base_increment * multiplier
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
            
            if len(st.session_state.finish_order) == 20:
                st.session_state.race_finished = True
                st.session_state.races_completed += 1
                st.session_state.race_started = False
                
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
                
                # Reset qualifying after race completion
                st.session_state.qualifying_times = {}
                st.session_state.qualifying_completed = {}
                st.session_state.grid_positions = {}
                st.session_state.starting_grid = list(range(20))
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

# Tab 3: Drivers' Championship (unchanged from original)
with tab3:
    st.markdown("### 🏆 Drivers' Championship Standings")
    
    driver_standings = []
    for driver_info in drivers:
        driver = driver_info['driver']
        team = driver_info['team']
        points = st.session_state.total_driver_points[driver]
        wins = st.session_state.driver_wins[driver]
        podiums = st.session_state.driver_podiums[driver]
        driver_standings.append({
            "Position": 0,
            "Driver": driver,
            "Team": team,
            "Points": points,
            "Wins": wins,
            "Podiums": podiums
        })
    
    driver_standings.sort(key=lambda x: (-x["Points"], -x["Wins"], -x["Podiums"]))
    
    for i, standing in enumerate(driver_standings):
        standing["Position"] = i + 1
    
    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    for standing in driver_standings:
        position = standing["Position"]
        card_class = "position-1" if position == 1 else "position-2" if position == 2 else "position-3" if position == 3 else ""
        
        medal = "🥇" if position == 1 else "🥈" if position == 2 else "🥉" if position == 3 else f"P{position}"
        
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <span>{medal} {standing["Driver"]} ({standing["Team"]})</span>
            <span>{standing["Points"]} pts | {standing["Wins"]} wins | {standing["Podiums"]} podiums</span>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Constructors' Championship (unchanged from original)
with tab4:
    st.markdown("### 🏁 Constructors' Championship Standings")
    
    team_standings = []
    for team in teams_drivers:
        points = st.session_state.total_team_points[team]
        wins = st.session_state.team_wins[team]
        podiums = st.session_state.team_podiums[team]
        team_standings.append({
            "Position": 0,
            "Team": team,
            "Points": points,
            "Wins": wins,
            "Podiums": podiums
        })
    
    team_standings.sort(key=lambda x: (-x["Points"], -x["Wins"], -x["Podiums"]))
    
    for i, standing in enumerate(team_standings):
        standing["Position"] = i + 1
    
    st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
    for standing in team_standings:
        position = standing["Position"]
        card_class = "position-1" if position == 1 else "position-2" if position == 2 else "position-3" if position == 3 else ""
        
        medal = "🥇" if position == 1 else "🥈" if position == 2 else "🥉" if position == 3 else f"P{position}"
        
        st.markdown(f'''
        <div class="leaderboard-item {card_class}">
            <span>{medal} {standing["Team"]}</span>
            <span>{standing["Points"]} pts | {standing["Wins"]} wins | {standing["Podiums"]} podiums</span>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 5: Team & Driver Stats (unchanged from original)
with tab5:
    st.markdown("### 📊 Team & Driver Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top Performing Drivers")
        top_drivers = sorted(drivers, key=lambda x: st.session_state.total_driver_points[x['driver']], reverse=True)[:5]
        
        for i, driver_info in enumerate(top_drivers, 1):
            driver = driver_info['driver']
            team = driver_info['team']
            points = st.session_state.total_driver_points[driver]
            wins = st.session_state.driver_wins[driver]
            
            st.markdown(f'''
            <div class="rating-card">
                <div class="rating-header">
                    <div>
                        <div class="driver-name">{i}. {driver}</div>
                        <div class="team-name">{team}</div>
                    </div>
                    <div class="rating-score">{points}</div>
                </div>
                <div class="rating-details">
                    <span>Points: {points}</span>
                    <span>Wins: {wins}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Top Performing Teams")
        top_teams = sorted(teams_drivers.keys(), key=lambda x: st.session_state.total_team_points[x], reverse=True)[:5]
        
        for i, team in enumerate(top_teams, 1):
            points = st.session_state.total_team_points[team]
            wins = st.session_state.team_wins[team]
            drivers_list = teams_drivers[team]
            
            st.markdown(f'''
            <div class="rating-card">
                <div class="rating-header">
                    <div>
                        <div class="driver-name">{i}. {team}</div>
                        <div class="team-name">{", ".join(drivers_list)}</div>
                    </div>
                    <div class="rating-score">{points}</div>
                </div>
                <div class="rating-details">
                    <span>Points: {points}</span>
                    <span>Wins: {wins}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)

# Tab 6: Driver Upgrades (unchanged from original)
with tab6:
    st.markdown("### ⚙️ Driver Upgrades")
    st.markdown("Adjust driver performance for the next race:")
    
    for driver_info in drivers:
        driver = driver_info['driver']
        team = driver_info['team']
        current_headstart = st.session_state.driver_headstarts.get(driver, 1)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{driver}** ({team})")
        with col2:
            new_headstart = st.slider(
                "Performance", 
                min_value=0.5, 
                max_value=3.0, 
                value=current_headstart, 
                step=0.1,
                key=f"headstart_{driver}",
                format="%.1fx"
            )
            st.session_state.driver_headstarts[driver] = new_headstart

# Tab 7: Season Summary (unchanged from original)
with tab7:
    st.markdown("### 📈 Season Summary")
    
    if st.session_state.races_completed > 0:
        st.markdown(f"**Season Progress: {st.session_state.races_completed} races completed**")
        
        # Championship leader
        if drivers:
            champion = max(drivers, key=lambda x: st.session_state.total_driver_points[x['driver']])
            champion_points = st.session_state.total_driver_points[champion['driver']]
            
            st.markdown(f'''
            <div class="rating-card rating-card-gold">
                <div class="rating-header">
                    <div>
                        <div class="driver-name">🏆 Championship Leader</div>
                        <div class="team-name">{champion['driver']} ({champion['team']})</div>
                    </div>
                    <div class="rating-score">{champion_points}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Recent race results
        if st.session_state.race_summaries:
            st.markdown("#### Recent Race Results")
            recent_races = st.session_state.race_summaries[-5:]  # Last 5 races
            
            st.markdown('<div class="leaderboard">', unsafe_allow_html=True)
            for race in reversed(recent_races):
                st.markdown(f'''
                <div class="leaderboard-item">
                    <span>Race {race['Race']}</span>
                    <span>🥇 {race['P1']} | 🥈 {race['P2']} | 🥉 {race['P3']}</span>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No races completed yet. Start your first race to see season statistics!")
    
    # Reset season button
    if st.button("🔄 Reset Season"):
        st.session_state.total_team_points = {team: 0 for team in teams_drivers}
        st.session_state.total_driver_points = {driver['driver']: 0 for driver in drivers}
        st.session_state.team_wins = {team: 0 for team in teams_drivers}
        st.session_state.team_podiums = {team: 0 for team in teams_drivers}
        st.session_state.driver_wins = {driver['driver']: 0 for driver in drivers}
        st.session_state.driver_podiums = {driver['driver']: 0 for driver in drivers}
        st.session_state.races_completed = 0
        st.session_state.race_summaries = []
        st.session_state.race_finished = False
        st.session_state.race_started = False
        st.session_state.qualifying_times = {}
        st.session_state.qualifying_completed = {}
        st.session_state.grid_positions = {}
        st.session_state.starting_grid = list(range(20))
        st.rerun()
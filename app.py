import streamlit as st
import pandas as pd

st.set_page_config(page_title="FairShare", page_icon="🚗", layout="centered")

if "_id_counter" not in st.session_state:
    st.session_state._id_counter = 0
if "passengers" not in st.session_state:
    st.session_state.passengers = []
if "stops" not in st.session_state:
    st.session_state.stops = []


def new_id():
    st.session_state._id_counter += 1
    return st.session_state._id_counter


st.title("🚗 FairShare")
st.caption("Split a shared ride's cost fairly, based on how far each person actually travels.")

mode = st.radio(
    "How are you splitting this?",
    ["Shared ride (one cab, sequential drop-offs)", "Independent distances (pooled cost)"],
    help=(
        "Shared ride: everyone starts together and gets dropped off one by one. Cost is split "
        "segment by segment, among whoever is still riding during that stretch — so the part "
        "everyone rides together is cheaper per person than the final solo stretch.\n\n"
        "Independent distances: each person's distance is its own separate trip, and you just "
        "want to split a pooled cost proportionally to those distances."
    ),
)
is_shared = mode.startswith("Shared")

st.divider()
st.subheader("Fare")

if is_shared:
    fare_mode = st.radio("Fare is entered as", ["Total fare (meter reading)", "Rate per km + base fare"], horizontal=True, label_visibility="collapsed")
    if fare_mode == "Rate per km + base fare":
        c1, c2 = st.columns(2)
        rate_per_km = c1.number_input("Rate per km (LKR)", min_value=0.0, value=80.0, step=5.0)
        base_fare = c2.number_input("Base / flag-down fare (LKR)", min_value=0.0, value=0.0, step=10.0)
        total_fare_input = None
    else:
        total_fare_input = st.number_input("Total fare (LKR)", min_value=0.0, value=1000.0, step=50.0)
        rate_per_km = None
        base_fare = 0.0
else:
    total_fare_input = st.number_input("Total transport cost (LKR)", min_value=0.0, value=1000.0, step=100.0)

st.divider()
st.subheader("Passengers")

with st.form("add_passenger_form", clear_on_submit=True):
    cols = st.columns([4, 1])
    new_name = cols[0].text_input("Name", placeholder="Add a passenger", label_visibility="collapsed", key="new_passenger_name")
    add_clicked = cols[1].form_submit_button("Add", width='stretch')
    if add_clicked and new_name.strip():
        st.session_state.passengers.append({"id": new_id(), "name": new_name.strip(), "distance": 10.0})

if not st.session_state.passengers:
    st.info("Add at least one passenger to get started.")

for p in list(st.session_state.passengers):
    if is_shared:
        row = st.columns([5, 1])
    else:
        row = st.columns([3, 2, 1])
    p["name"] = row[0].text_input("Name", value=p["name"], key=f"pname_{p['id']}", label_visibility="collapsed")
    if not is_shared:
        p["distance"] = row[1].number_input("Distance (km)", value=p["distance"], min_value=0.0, step=1.0, key=f"pdist_{p['id']}", label_visibility="collapsed")
    if row[-1].button("Remove", key=f"premove_{p['id']}", width='stretch'):
        st.session_state.passengers = [x for x in st.session_state.passengers if x["id"] != p["id"]]
        for s in st.session_state.stops:
            s["dropped"].discard(p["id"])
        st.rerun()

passengers = st.session_state.passengers

if is_shared:
    st.divider()
    st.subheader("Route")
    st.text_input("Pickup point", value=st.session_state.get("start_name", "Pickup point"), key="start_name")

    for idx, stop in enumerate(list(st.session_state.stops)):
        already_dropped = set()
        for s in st.session_state.stops[:idx]:
            already_dropped |= s["dropped"]
        remaining = [p for p in passengers if p["id"] not in already_dropped]

        with st.container(border=True):
            top = st.columns([4, 1])
            stop["name"] = top[0].text_input(
                "Stop name", value=stop["name"], key=f"sname_{stop['id']}", placeholder=f"Stop {idx + 1}", label_visibility="collapsed"
            )
            if top[1].button("Remove stop", key=f"sremove_{stop['id']}", width='stretch'):
                st.session_state.stops = [s for s in st.session_state.stops if s["id"] != stop["id"]]
                st.rerun()

            stop["distance"] = st.number_input(
                "Distance from previous stop (km)", value=stop["distance"], min_value=0.0, step=0.5, key=f"sdist_{stop['id']}"
            )

            if remaining:
                st.caption("Who gets off here?")
                dropped_here = set()
                cb_cols = st.columns(min(len(remaining), 4))
                for i, p in enumerate(remaining):
                    checked = cb_cols[i % len(cb_cols)].checkbox(
                        p["name"], value=(p["id"] in stop["dropped"]), key=f"sdrop_{stop['id']}_{p['id']}"
                    )
                    if checked:
                        dropped_here.add(p["id"])
                stop["dropped"] = dropped_here
            else:
                st.caption("Everyone has already been dropped off by this point.")
                stop["dropped"] = set()

    if st.button("+ Add stop", key="add_stop_btn"):
        st.session_state.stops.append({"id": new_id(), "name": "", "distance": 0.0, "dropped": set()})
        st.rerun()

st.divider()
st.subheader("Cost breakdown")

if not passengers:
    st.stop()

leg_rows = []
unassigned = []

if is_shared:
    stops = st.session_state.stops
    total_distance = sum(s["distance"] for s in stops)
    if fare_mode == "Rate per km + base fare":
        rate = rate_per_km
        base = base_fare
    else:
        rate = (total_fare_input / total_distance) if total_distance > 0 else 0.0
        base = 0.0
    total_cost = base + rate * total_distance

    costs = {p["id"]: (base / len(passengers) if passengers else 0.0) for p in passengers}
    remaining_ids = {p["id"] for p in passengers}
    for idx, s in enumerate(stops):
        seg_cost = s["distance"] * rate
        riders = list(remaining_ids)
        each = seg_cost / len(riders) if riders else 0.0
        for pid in riders:
            costs[pid] = costs.get(pid, 0.0) + each
        leg_rows.append(
            {
                "Stop": s["name"] or f"Stop {idx + 1}",
                "Distance (km)": round(s["distance"], 1),
                "Riders": len(riders),
                "Cost each (LKR)": round(each, 2),
            }
        )
        remaining_ids -= s["dropped"]
    unassigned = [p for p in passengers if p["id"] in remaining_ids]
else:
    total_distance = sum(p["distance"] for p in passengers)
    rate = (total_fare_input / total_distance) if total_distance > 0 else 0.0
    total_cost = total_fare_input
    costs = {p["id"]: p["distance"] * rate for p in passengers}

df = pd.DataFrame([{"Name": p["name"], "Cost Share (LKR)": round(costs.get(p["id"], 0.0), 2)} for p in passengers])

col1, col2 = st.columns(2)
col1.metric("Total cost", f"LKR {total_cost:,.2f}")
col2.metric("Total distance", f"{total_distance:.1f} km")

if total_distance == 0:
    st.error("Total distance must be greater than 0 km.")
else:
    st.dataframe(df, width='stretch', hide_index=True)
    st.bar_chart(df.set_index("Name")["Cost Share (LKR)"])

    if is_shared and unassigned:
        names = ", ".join(p["name"] for p in unassigned)
        verb = "hasn't" if len(unassigned) == 1 else "haven't"
        st.warning(f"{names} {verb} been dropped off yet in the route above — the totals won't be complete until everyone has a stop.")

    if is_shared and any(r["Distance (km)"] > 0 and r["Riders"] == 0 for r in leg_rows):
        st.warning("One or more stops have distance but no one left riding at that point — check the route order and drop-off assignments above.")

    if is_shared:
        with st.expander("Show the per-leg math"):
            st.dataframe(pd.DataFrame(leg_rows), width='stretch', hide_index=True)

    calculated_total = df["Cost Share (LKR)"].sum()
    st.caption(f"Verification: shares sum to LKR {calculated_total:,.2f} (should match total cost above, aside from rounding).")

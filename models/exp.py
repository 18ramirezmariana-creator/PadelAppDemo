# -------- Example input (replace this with your actual variable) ----------
# players_data = {"w": {"wins": 3, "points": 7},
#                 "d": {"wins": 2, "points": 6},
#                 "h": {"wins": 1, "points": 3},
#                 "n": {"wins": 1, "points": 3},
#                 "f": {"wins": 0, "points": 0}}
# --------------------------------------------------------------------------


players_data = st.session_state.players_data

# Convert to DataFrame
df = pd.DataFrame(players_data).T.reset_index()
df.columns = ["Player", "Wins", "Points"]

# Sort by points, then wins
df = df.sort_values(by=["Points", "Wins"], ascending=False).reset_index(drop=True)

# Display header
st.markdown("<h3 style='text-align:center;'>🏆 Tournament Results</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Congratulations to all participants!</p>", unsafe_allow_html=True)

# Create 3 columns for podium
col2, col1, col3 = st.columns([1, 1, 1])

# Define color styles
def podium_card(place, player, wins, points, color1, color2):
    st.markdown(f"""
        <div style="background: linear-gradient(145deg, {color1}, {color2});
                    border-radius: 20px;
                    padding: 30px;
                    text-align: center;
                    color: white;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
                    height: 260px;">
            <div style="font-size: 14px; background-color: rgba(255,255,255,0.2);
                        padding: 5px 15px; border-radius: 10px; display: inline-block;">
                {place}
            </div>
            <h2 style="margin-top: 20px;">{player}</h2>
            <p>{wins} Wins<br>{points} Points</p>
        </div>
    """, unsafe_allow_html=True)

# Get top 3
top3 = df.head(3)

# Display podium
with col1:
    podium_card("🥇 1st Place", top3.iloc[0]["Player"], top3.iloc[0]["Wins"], top3.iloc[0]["Points"], "#FFD700", "#E6B800")
with col2:
    if len(top3) > 1:
        podium_card("🥈 2nd Place", top3.iloc[1]["Player"], top3.iloc[1]["Wins"], top3.iloc[1]["Points"], "#C0C0C0", "#A9A9A9")
with col3:
    if len(top3) > 2:
        podium_card("🥉 3rd Place", top3.iloc[2]["Player"], top3.iloc[2]["Wins"], top3.iloc[2]["Points"], "#FF8C00", "#FF6600")

# Display others
others = df.iloc[3:]
if not others.empty:
    st.markdown("<br><h4>Other Participants</h4>", unsafe_allow_html=True)
    for idx, row in others.iterrows():
        st.markdown(f"""
            <div style="background-color: #F8F9FA;
                        border-radius: 10px;
                        margin-bottom: 10px;
                        padding: 10px 15px;">
                <b>{idx+1}ᵗʰ</b> — {row['Player']} &nbsp;&nbsp; {row['Wins']} wins, {row['Points']} pts
            </div>
        """, unsafe_allow_html=True)
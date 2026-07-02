import random
import streamlit as st
from collections import Counter

st.set_page_config(page_title="Hand Cricket", page_icon="🏏", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: #08080c; color: #f0f0f0; }
.stApp { background: radial-gradient(circle at 50% 0%, #10101a 0%, #08080c 55%); }
[data-testid="stSidebar"] { background: #111; border-right: 1px solid #1e1e1e; }

/* tighten Streamlit's own vertical rhythm so more fits on one screen */
div.block-container { padding-top: 0.6rem !important; padding-bottom: 1rem !important; max-width: 640px; }
div[data-testid="stVerticalBlock"] { gap: 0.4rem !important; }
div[data-testid="column"] { padding: 0 0.2rem !important; }

.page-title { display:flex; align-items:center; justify-content:space-between; padding: 0.1rem 0 0.4rem 0; }
.page-title h2 { font-family: 'Space Mono', monospace; font-size: 1.15rem; color: #fff; margin: 0; letter-spacing: -0.02em; }
.page-title p { font-size: 0.68rem; color: #4a4a55; margin: 0.1rem 0 0 0; }
.divider { border: none; border-top: 1px solid #1a1a22; margin: 0.5rem 0; }
.divider-tight { border: none; border-top: 1px solid #1a1a22; margin: 0.3rem 0; }

/* ── compact scoreboard card ─────────────────────────────────────────── */
.score-card {
    background: linear-gradient(180deg, #14141d 0%, #101018 100%);
    border: 1px solid #23232f; border-radius: 16px;
    padding: 0.7rem 0.9rem 0.55rem 0.9rem; margin: 0.3rem 0;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.02), 0 8px 24px -12px rgba(0,0,0,0.6);
}
.score-main { display: flex; align-items: center; justify-content: space-between; }
.team { flex: 1; text-align: center; }
.team-tag { font-size: 0.64rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; }
.team.you .team-tag { color: #34d399; }
.team.ai .team-tag { color: #60a5fa; }
.team-score { font-family: 'Space Mono', monospace; font-size: 1.8rem; font-weight: 700; color: #fff; line-height: 1.15; }
.team-sub { font-size: 0.66rem; color: #6b6b78; margin-top: -1px; }
.vs-pill {
    font-family: 'Space Mono', monospace; font-size: 0.62rem; font-weight: 700; color: #55555f;
    background: #1a1a24; border: 1px solid #26262f; border-radius: 999px;
    width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin: 0 0.4rem;
}
.score-strip { display: flex; gap: 0.4rem; margin-top: 0.6rem; }
.chip { flex: 1; background: #0d0d13; border: 1px solid #1e1e28; border-radius: 10px; padding: 0.32rem 0.2rem; text-align: center; }
.chip .cv { display:block; font-family: 'Space Mono', monospace; font-size: 0.92rem; font-weight: 700; color: #fff; line-height: 1.2; }
.chip .cl { display:block; font-size: 0.55rem; letter-spacing: 0.06em; text-transform: uppercase; color: #55555f; margin-top: 1px; }
.chip.hl .cv { color: #fbbf24; }

/* ── slim ball-event strip (replaces the tall banner during play) ──────── */
.ball-strip { display: flex; align-items: center; gap: 0.5rem; margin: 0.4rem 0 0.25rem 0; padding: 0.35rem 0.6rem;
    background: #0d0d13; border: 1px solid #1e1e28; border-radius: 10px; }
.ball-pill { font-family: 'Space Mono', monospace; font-weight: 700; font-size: 0.85rem; border-radius: 7px;
    padding: 0.12rem 0.5rem; flex-shrink: 0; }
.ball-pill.out    { background: #2a0d0d; color: #f87171; border: 1px solid #f87171; }
.ball-pill.runs   { background: #0d2418; color: #4ade80; border: 1px solid #4ade80; }
.ball-pill.dot    { background: #17172a; color: #a78bfa; border: 1px solid #a78bfa; }
.ball-pill.info   { background: #17171e; color: #7a7a86; border: 1px solid #26262f; }
.ball-text { font-size: 0.78rem; color: #c9c9d2; line-height: 1.2; }
.recent-strip { margin-left: auto; display:flex; gap: 0.22rem; flex-shrink: 0; }
.recent-dot { font-family: 'Space Mono', monospace; font-size: 0.62rem; font-weight: 700; color: #cfcfd8;
    background: #1a1a24; border: 1px solid #26262f; border-radius: 5px; width: 17px; height: 17px;
    display:flex; align-items:center; justify-content:center; }

.banner { text-align: center; padding: 0.9rem; border-radius: 12px; margin: 0.8rem 0; font-family: 'Space Mono', monospace; font-size: 1rem; font-weight: 700; }
.banner-out    { background: #450a0a; color: #f87171; border: 1px solid #f87171; }
.banner-runs   { background: #14532d; color: #4ade80; border: 1px solid #4ade80; }
.banner-dot    { background: #1e1b4b; color: #818cf8; border: 1px solid #818cf8; }
.banner-info   { background: #1a1a1a; color: #888;    border: 1px solid #222; font-size: 0.85rem; }
.banner-win    { background: #14532d; color: #4ade80; border: 1px solid #4ade80; font-size: 1.2rem; }
.banner-lose   { background: #450a0a; color: #f87171; border: 1px solid #f87171; font-size: 1.2rem; }
.banner-tie    { background: #422006; color: #facc15; border: 1px solid #facc15; font-size: 1.2rem; }

.stat-row { display: flex; gap: 0.6rem; margin: 0.5rem 0; }
.stat-box { background: #161616; border: 1px solid #222; border-radius: 10px; padding: 0.5rem 0.7rem; text-align: center; flex: 1; }
.stat-box .sv { font-family: 'Space Mono', monospace; font-size: 1.2rem; font-weight: 700; color: #fff; }
.stat-box .sl { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.1em; color: #555; }

/* ── shot pad ─────────────────────────────────────────────────────────── */
.pad-label { text-align:center; color:#55555f; font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.1em; margin: 0.35rem 0 0.35rem 0; }

div[data-testid="stButton"] > button {
    background: #14141c !important; color: #f0f0f0 !important;
    border: 1.5px solid #26262f !important; border-radius: 14px !important;
    font-family: 'Space Mono', monospace !important; font-weight: 700 !important; font-size: 1.15rem !important;
    padding: 0.65rem 0.5rem !important; transition: all 0.12s ease !important; width: 100% !important;
}
div[data-testid="stButton"] > button:hover { border-color: #4ade80 !important; background: #182018 !important; color: #4ade80 !important; }
div[data-testid="stButton"] > button:active { transform: scale(0.96); }
/* smaller, muted style for the bottom control row */
.controls-row div[data-testid="stButton"] > button {
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important; font-size: 0.78rem !important;
    padding: 0.45rem 0.3rem !important; color: #9a9aa5 !important; border-color: #1e1e28 !important;
}
.controls-row div[data-testid="stButton"] > button:hover { color: #fff !important; border-color: #3a3a48 !important; background: #16161e !important; }

div[data-testid="stSelectbox"] > div { background: #161616 !important; border-color: #2a2a2a !important; color: #f0f0f0 !important; }
div[data-testid="stNumberInput"] input { background: #161616 !important; color: #f0f0f0 !important; border: 2px solid #2a2a2a !important; border-radius: 10px !important; font-family: 'Space Mono', monospace !important; }
div[data-testid="stTextInput"] input {
    background: #161616 !important; color: #f0f0f0 !important; border: 2px solid #2a2a2a !important;
    border-radius: 10px !important; font-family: 'Space Mono', monospace !important;
    text-align: center !important; font-size: 1.4rem !important; padding: 0.6rem !important;
}
div[data-testid="stTextInput"] input:focus { border-color: #818cf8 !important; box-shadow: none !important; }
div[data-testid="stFormSubmitButton"] > button {
    background: #161616 !important; color: #f0f0f0 !important;
    border: 2px solid #2a2a2a !important; border-radius: 14px !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;
    padding: 0.7rem 0.5rem !important; transition: all 0.15s ease !important; width: 100% !important;
}
div[data-testid="stFormSubmitButton"] > button:hover { border-color: #fff !important; background: #202020 !important; }
.input-error { color: #f87171; font-size: 0.8rem; text-align: center; margin-top: -0.4rem; margin-bottom: 0.4rem; font-family: 'Space Grotesk', sans-serif; }
.catch-hint { text-align: center; color: #a78bfa; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem; }

.footer { text-align: center; margin-top: 0.6rem; font-size: 0.62rem; color: #2a2a30; letter-spacing: 0.06em; }
</style>
""", unsafe_allow_html=True)

# ── AI (your original logic) ────────────────────────────────────────────────
ai_patterns = {0:[4,5,6],1:[3,4,6],2:[2,6,5],3:[3,1,5],4:[4,5,1],5:[3,6,5],6:[6,3,4]}

def ai_bowler_choice(batter_history, target=None, score=0, balls_remaining=None):
    base = 0.85
    if target is not None and balls_remaining and balls_remaining > 0:
        rr = (target - score) / (balls_remaining / 6)
        base = 0.93 if rr >= 5 else (0.8 if rr <= 2 else base)
    if len(batter_history) >= 1 and random.random() < base:
        return random.choice(ai_patterns[batter_history[-1]])
    if len(batter_history) >= 3:
        freq = Counter(batter_history[-5:])
        favs = [n for n, _ in freq.most_common(2)]
        if favs: return random.choice(favs)
    return random.randint(0, 6)

def ai_batter_choice(bowler_history, score, target, balls_remaining, wickets_remaining, total_overs):
    balls_total = total_overs * 6
    balls_bowled = balls_total - balls_remaining
    if target is None:
        aggression = 0.3 + 0.5 * ((balls_bowled / balls_total) if balls_total else 0)
        if wickets_remaining <= 1: aggression *= 0.6
    else:
        rr = ((target - score) / (balls_remaining / 6)) if balls_remaining > 0 else 12
        aggression = min(1.0, max(0.05, rr / 6.0))
        if rr >= 5.5: aggression = max(aggression, 0.9)
        if wickets_remaining <= 1 and rr < 5: aggression *= 0.5
    aggression = max(0.0, min(1.0, aggression))
    weights = [max(1.0 + aggression * n * 1.5 - (1 - aggression) * (n * 0.3), 0.05) for n in range(7)]
    if len(bowler_history) >= 2:
        freq = Counter(bowler_history[-5:])
        avoidance = 0.5 if aggression < 0.8 else 0.2
        for n in [x for x, _ in freq.most_common(2)]:
            weights[n] *= (1 - avoidance)
    total_w = sum(weights)
    return random.choices(range(7), weights=[w/total_w for w in weights], k=1)[0]

def determine_dismissal_type(number, batter_history):
    """Classify a matching-number ball. 'catch_chance' hands control to the
    interactive catch mini-game instead of resolving the wicket immediately."""
    if random.random() < 0.10:
        return 'stumped'
    if 4 <= number <= 6:
        recent = batter_history[-5:]
        high_ratio = (sum(1 for n in recent if n in (4,5,6)) / len(recent)) if recent else 0
        if high_ratio >= 0.6 and random.random() < 0.55:
            return 'catch_chance'
        return 'bowled'
    elif 1 <= number <= 3:
        return 'run_out' if random.random() < 0.8 else 'survived_run_out'
    return 'bowled'

def format_score(score, wickets_lost, balls_bowled, total_overs):
    overs = balls_bowled // 6; balls = balls_bowled % 6
    return f"{score}/{wickets_lost} ({overs}.{balls}/{total_overs} ov)"

# ── Session state ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "phase": "setup",          # setup | toss | innings1 | innings2 | result
        "player_name": "Player",
        "total_wickets": 3,
        "total_overs": 2,
        "first_batter": None,
        "score": 0,
        "wickets_lost": 0,
        "balls_bowled": 0,
        "batter_history": [],
        "bowler_history": [],
        "target": None,
        "innings1_score": 0,
        "innings1_wickets": 0,
        "innings1_balls": 0,
        "innings1_batter": None,
        "last_event": None,
        "last_msg": "",
        "result_msg": "",
        "toss_result": None,
        "pending_catch": None,
        "catch_options": None,
        "input_error": False,
        "show_scorecard": False,
        "stats": {"player":{"runs":0,"balls":0,"outs":0,"balls_bowled":0,"runs_conceded":0,"catches":0,"runouts":0,"stumpings":0,"bowled":0},
                  "CricBot":{"runs":0,"balls":0,"outs":0,"balls_bowled":0,"runs_conceded":0,"catches":0,"runouts":0,"stumpings":0,"bowled":0}},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
s = st.session_state

def reset():
    keys = list(s.keys())
    for k in keys:
        del st.session_state[k]
    init_state()

def current_innings():
    return 1 if s.phase == "innings1" else 2

def who_is_batting():
    if s.phase == "innings1": return s.first_batter
    return "CricBot" if s.first_batter == "player" else "player"

def who_is_bowling():
    return "CricBot" if who_is_batting() == "player" else "player"

def balls_remaining():
    return s.total_overs * 6 - s.balls_bowled

def wickets_remaining():
    return s.total_wickets - s.wickets_lost

def process_ball(player_num):
    batter = who_is_batting()
    bowler = who_is_bowling()

    if batter == "player":
        batter_num = player_num
        bowler_num = ai_bowler_choice(s.batter_history, target=s.target, score=s.score, balls_remaining=balls_remaining())
    else:
        bowler_num = player_num
        batter_num = ai_batter_choice(s.bowler_history, score=s.score, target=s.target,
                                       balls_remaining=balls_remaining(),
                                       wickets_remaining=wickets_remaining(),
                                       total_overs=s.total_overs)

    s.batter_history.append(batter_num)
    s.bowler_history.append(bowler_num)
    s.balls_bowled += 1
    s.stats[batter]["balls"] += 1
    s.stats[bowler]["balls_bowled"] += 1

    if batter_num == bowler_num:
        dtype = determine_dismissal_type(batter_num, s.batter_history)
        if dtype == 'catch_chance':
            # Hold off resolving the wicket until the player plays the catch mini-game
            options = random.sample(range(0, 7), 3)
            s.pending_catch = {
                "batter": batter, "bowler": bowler,
                "batter_num": batter_num, "bowler_num": bowler_num,
            }
            s.catch_options = options
            s.last_event = "dot"
            s.last_msg = f"🏐 Big shot! It's up in the air — catch chance! ({batter_num} vs {bowler_num})"
            return  # wait for the mini-game before finishing this ball
        apply_dismissal(batter, bowler, batter_num, bowler_num, dtype)
    else:
        runs = batter_num
        s.score += runs
        s.stats[batter]["runs"] += runs
        s.stats[bowler]["runs_conceded"] += runs
        s.last_event = "runs"
        s.last_msg = f"+{runs} runs ({batter_num} vs {bowler_num})"

    check_innings_over()

def apply_dismissal(batter, bowler, batter_num, bowler_num, dtype):
    if dtype == 'survived_run_out':
        s.last_event = "survived"
        s.last_msg = f"Close! Survived! ({batter_num} vs {bowler_num})"
        return
    s.wickets_lost += 1
    s.stats[batter]["outs"] += 1
    if dtype == "caught":    s.stats[bowler]["catches"] += 1
    elif dtype == "run_out": s.stats[bowler]["runouts"] += 1
    elif dtype == "stumped": s.stats[bowler]["stumpings"] += 1
    else:                    s.stats[bowler]["bowled"] += 1
    label = {"caught": "Caught", "run_out": "Run Out", "stumped": "Stumped"}.get(dtype, "Bowled")
    s.last_event = "out"
    s.last_msg = f"OUT! {label}! ({batter_num} vs {bowler_num})"

def resolve_catch(player_choice):
    pc = s.pending_catch
    if not pc:
        return
    bot_choice = random.choice(s.catch_options)
    batter, bowler = pc["batter"], pc["bowler"]
    batter_num, bowler_num = pc["batter_num"], pc["bowler_num"]
    if player_choice == bot_choice:
        s.wickets_lost += 1
        s.stats[batter]["outs"] += 1
        s.stats[bowler]["catches"] += 1
        s.last_event = "out"
        s.last_msg = f"OUT! Caught! You picked {player_choice}, the fielder also picked {bot_choice}! ({batter_num} vs {bowler_num})"
    else:
        s.last_event = "survived"
        s.last_msg = f"🙌 Dropped! You picked {player_choice}, fielder picked {bot_choice} — survives, another chance! ({batter_num} vs {bowler_num})"
    s.pending_catch = None
    s.catch_options = None
    check_innings_over()

def check_innings_over():
    innings_over = False
    if s.target is not None and s.score >= s.target:
        innings_over = True
    elif s.wickets_lost >= s.total_wickets or s.balls_bowled >= s.total_overs * 6:
        innings_over = True
    if innings_over:
        end_innings()

def end_innings():
    if s.phase == "innings1":
        s.innings1_score   = s.score
        s.innings1_wickets = s.wickets_lost
        s.innings1_balls   = s.balls_bowled
        s.innings1_batter  = s.first_batter
        s.target           = s.score + 1
        # reset for innings 2
        s.score         = 0
        s.wickets_lost  = 0
        s.balls_bowled  = 0
        s.batter_history  = []
        s.bowler_history  = []
        s.phase = "innings2"
    else:
        # decide result
        second_batter = "CricBot" if s.first_batter == "player" else "player"
        if s.score >= s.target:
            margin = s.total_wickets - s.wickets_lost
            winner = second_batter
            s.result_msg = f"{'🏆 You Won!' if winner == 'player' else '💀 CricBot Won!'} (by {max(margin,0)} wicket{'s' if margin!=1 else ''})"
        elif s.score == s.target - 1:
            s.result_msg = "🤝 It's a TIE!"
        else:
            margin = s.target - s.score - 1
            winner = s.first_batter
            s.result_msg = f"{'🏆 You Won!' if winner == 'player' else '💀 CricBot Won!'} (by {margin} run{'s' if margin!=1 else ''})"
        s.phase = "result"

# ══════════════════════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-title">
    <h2>🏏 Hand Cricket</h2>
    <p>vs CricBot — numbers 0 to 6</p>
</div>""", unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SETUP ─────────────────────────────────────────────────────────────────────
if s.phase == "setup":
    name = st.text_input("Your name", value="Player", max_chars=20)
    c1, c2 = st.columns(2)
    with c1:
        wickets = st.number_input("Wickets", min_value=1, max_value=10, value=3, step=1)
    with c2:
        overs = st.number_input("Overs", min_value=1, max_value=20, value=2, step=1)
    if st.button("Start Match ▶", use_container_width=True):
        s.player_name   = name.strip() or "Player"
        s.total_wickets = int(wickets)
        s.total_overs   = int(overs)
        s.toss_result   = random.choice(["heads", "tails"])
        s.phase         = "toss"
        st.rerun()

# ── TOSS ──────────────────────────────────────────────────────────────────────
elif s.phase == "toss":
    st.markdown(f"<div class='banner banner-info'>🪙 Toss — call it!</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Heads", use_container_width=True):
            call = "heads"
            if call == s.toss_result:
                s.last_msg = f"It's {s.toss_result}! You won the toss — choose bat or bowl."
                s.phase = "toss_choice"
            else:
                s.last_msg = f"It's {s.toss_result}! You lost the toss."
                cricbot = random.choice(["bat", "bowl"])
                s.first_batter = "CricBot" if cricbot == "bat" else "player"
                s.phase = "innings1"
            st.rerun()
    with c2:
        if st.button("Tails", use_container_width=True):
            call = "tails"
            if call == s.toss_result:
                s.last_msg = f"It's {s.toss_result}! You won the toss — choose bat or bowl."
                s.phase = "toss_choice"
            else:
                s.last_msg = f"It's {s.toss_result}! You lost the toss."
                cricbot = random.choice(["bat", "bowl"])
                s.first_batter = "CricBot" if cricbot == "bat" else "player"
                s.phase = "innings1"
            st.rerun()

# ── TOSS CHOICE ───────────────────────────────────────────────────────────────
elif s.phase == "toss_choice":
    st.markdown(f"<div class='banner banner-info'>{s.last_msg}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏏 Bat First", use_container_width=True):
            s.first_batter = "player"; s.phase = "innings1"; st.rerun()
    with c2:
        if st.button("🎳 Bowl First", use_container_width=True):
            s.first_batter = "CricBot"; s.phase = "innings1"; st.rerun()

# ── INNINGS 1 & 2 ─────────────────────────────────────────────────────────────
elif s.phase in ("innings1", "innings2"):
    batter = who_is_batting()
    bowler = who_is_bowling()
    inn_num = current_innings()

    # ── figure out what to show for the YOU / AI team blocks ───────────────
    def team_block(who):
        currently_batting = (batter == who)
        if currently_batting:
            runs, wkts, balls = s.score, s.wickets_lost, s.balls_bowled
            sub = f"{balls//6}.{balls%6} ov"
        elif inn_num == 2 and s.innings1_batter == who:
            runs, wkts, balls = s.innings1_score, s.innings1_wickets, s.innings1_balls
            sub = f"{balls//6}.{balls%6} ov"
        else:
            runs, wkts = None, None
            sub = f"Target {s.target}" if s.target else "yet to bat"
        score_txt = f"{runs}-{wkts}" if runs is not None else "--"
        return score_txt, sub

    you_score, you_sub = team_block("player")
    ai_score, ai_sub = team_block("CricBot")

    rr = (s.score / (s.balls_bowled / 6)) if s.balls_bowled else 0.0
    if s.target:
        needed = max(s.target - s.score, 0)
        req_rr = (needed * 6 / balls_remaining()) if balls_remaining() > 0 else 0.0
        chip4_val, chip4_lbl = (f"{needed}", "NEED") if needed > 0 else ("WON", "STATUS")
    else:
        chip4_val, chip4_lbl = (str(balls_remaining()), "BALLS LEFT")

    # ── compact scoreboard card ─────────────────────────────────────────────
    st.markdown(f"""<div class='score-card'>
        <div class='score-main'>
            <div class='team you'>
                <div class='team-tag'>{s.player_name if len(s.player_name) <= 10 else 'YOU'}</div>
                <div class='team-score'>{you_score}</div>
                <div class='team-sub'>{you_sub}</div>
            </div>
            <div class='vs-pill'>VS</div>
            <div class='team ai'>
                <div class='team-tag'>CricBot</div>
                <div class='team-score'>{ai_score}</div>
                <div class='team-sub'>{ai_sub}</div>
            </div>
        </div>
        <div class='score-strip'>
            <div class='chip'><span class='cv'>{s.total_overs*6 - s.balls_bowled}</span><span class='cl'>Balls Left</span></div>
            <div class='chip'><span class='cv'>{wickets_remaining()}</span><span class='cl'>Wkts Left</span></div>
            <div class='chip'><span class='cv'>{rr:.2f}</span><span class='cl'>Run Rate</span></div>
            <div class='chip hl'><span class='cv'>{chip4_val}</span><span class='cl'>{chip4_lbl}</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── slim last-ball strip (replaces the old tall banner) ────────────────
    recent_html = "".join(f"<span class='recent-dot'>{n}</span>" for n in s.batter_history[-6:])
    if s.last_msg:
        cls = {"out":"out","runs":"runs","survived":"dot","dot":"dot"}.get(s.last_event, "info")
        pill_txt = {"out":"OUT","runs":"RUNS","survived":"SAFE","dot":"DOT"}.get(s.last_event, "•")
        st.markdown(f"""<div class='ball-strip'>
            <span class='ball-pill {cls}'>{pill_txt}</span>
            <span class='ball-text'>{s.last_msg}</span>
            <span class='recent-strip'>{recent_html}</span>
        </div>""", unsafe_allow_html=True)
    else:
        role = "batting" if batter == "player" else "bowling"
        st.markdown(f"""<div class='ball-strip'>
            <span class='ball-pill info'>GO</span>
            <span class='ball-text'>You're {role} — pick a number 0–6</span>
            <span class='recent-strip'>{recent_html}</span>
        </div>""", unsafe_allow_html=True)

    if s.pending_catch:
        # ── CATCH MINI-GAME ──────────────────────────────────────────────────
        st.markdown("<p class='catch-hint'>🏐 Catch chance! Match the fielder's pick to get the wicket</p>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, opt in enumerate(s.catch_options):
            with cols[i]:
                if st.button(str(opt), key=f"catch_{s.balls_bowled}_{opt}", use_container_width=True):
                    resolve_catch(opt)
                    st.rerun()
    else:
        # ── SHOT / BOWLING PAD ───────────────────────────────────────────────
        label = "Your batting shot" if batter == "player" else "Your bowling number"
        st.markdown(f"<p class='pad-label'>{label}</p>", unsafe_allow_html=True)
        rows = [[1, 2, 3], [4, 5, 6]]
        for row in rows:
            cols = st.columns(3, gap="small")
            for c, n in enumerate(row):
                with cols[c]:
                    if st.button(str(n), key=f"num_{s.balls_bowled}_{n}", use_container_width=True):
                        process_ball(n); st.rerun()
        if st.button("0", key=f"num_{s.balls_bowled}_0", use_container_width=True):
            process_ball(0); st.rerun()

    st.markdown('<hr class="divider-tight">', unsafe_allow_html=True)
    st.markdown('<div class="controls-row">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        if st.button("🔁 New", use_container_width=True):
            reset(); st.rerun()
    with c2:
        if st.button("📊 Scorecard", use_container_width=True):
            s.show_scorecard = not s.show_scorecard
            st.rerun()
    with c3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if s.show_scorecard:
        p = s.stats["player"]; c = s.stats["CricBot"]
        p_sr = f"{p['runs']/p['balls']*100:.0f}" if p['balls'] else "—"
        c_sr = f"{c['runs']/c['balls']*100:.0f}" if c['balls'] else "—"
        st.markdown(f"""<div class='stat-row'>
            <div class='stat-box'><div class='sl'>Your Runs</div><div class='sv' style='color:#4ade80'>{p['runs']}</div></div>
            <div class='stat-box'><div class='sl'>Strike Rate</div><div class='sv'>{p_sr}</div></div>
            <div class='stat-box'><div class='sl'>Bot Runs</div><div class='sv' style='color:#60a5fa'>{c['runs']}</div></div>
            <div class='stat-box'><div class='sl'>Strike Rate</div><div class='sv'>{c_sr}</div></div>
        </div>""", unsafe_allow_html=True)

# ── RESULT ────────────────────────────────────────────────────────────────────
elif s.phase == "result":
    css = "banner-win" if "Won" in s.result_msg and "You" in s.result_msg else ("banner-tie" if "TIE" in s.result_msg else "banner-lose")
    st.markdown(f"<div class='banner {css}'>{s.result_msg}</div>", unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # match stats
    p = s.stats["player"]; c = s.stats["CricBot"]
    p_sr = f"{p['runs']/p['balls']*100:.0f}" if p['balls'] else "—"
    c_sr = f"{c['runs']/c['balls']*100:.0f}" if c['balls'] else "—"
    p_eco = f"{p['runs_conceded']/(p['balls_bowled']/6):.1f}" if p['balls_bowled'] else "—"
    c_eco = f"{c['runs_conceded']/(c['balls_bowled']/6):.1f}" if c['balls_bowled'] else "—"

    st.markdown(f"<p style='color:#555;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;text-align:center;'>Match Stats</p>", unsafe_allow_html=True)
    st.markdown(f"""<div class='stat-row'>
        <div class='stat-box'><div class='sl'>Your Runs</div><div class='sv' style='color:#4ade80'>{p['runs']}</div></div>
        <div class='stat-box'><div class='sl'>Strike Rate</div><div class='sv'>{p_sr}</div></div>
        <div class='stat-box'><div class='sl'>Wickets</div><div class='sv' style='color:#f87171'>{p['outs']}</div></div>
        <div class='stat-box'><div class='sl'>Economy</div><div class='sv'>{p_eco}</div></div>
    </div>
    <div class='stat-row'>
        <div class='stat-box'><div class='sl'>Bot Runs</div><div class='sv' style='color:#818cf8'>{c['runs']}</div></div>
        <div class='stat-box'><div class='sl'>Strike Rate</div><div class='sv'>{c_sr}</div></div>
        <div class='stat-box'><div class='sl'>Wickets</div><div class='sv' style='color:#f87171'>{c['outs']}</div></div>
        <div class='stat-box'><div class='sl'>Economy</div><div class='sv'>{c_eco}</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if st.button("🔁 Play Again", use_container_width=True):
        reset()
        st.rerun()

st.markdown('<div class="footer">made by AhaD</div>', unsafe_allow_html=True)

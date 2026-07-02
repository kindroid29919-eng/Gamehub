import random
import streamlit as st
from collections import Counter

st.set_page_config(page_title="Hand Cricket", page_icon="🏏", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: #0a0a0f; color: #f0f0f0; }
.stApp { background: #0a0a0f; }
[data-testid="stSidebar"] { background: #111; border-right: 1px solid #1e1e1e; }

div.block-container { padding-top: 0.7rem !important; padding-bottom: 1.2rem !important; max-width: 640px; }
div[data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
div[data-testid="column"] { padding: 0 0.25rem !important; }

/* ── header ───────────────────────────────────────────────────────────── */
.page-header { display:flex; align-items:center; justify-content:space-between; padding: 0.2rem 0 0.6rem 0; }
.page-header .titles h2 { font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 700; color: #fff; margin: 0; }
.page-header .titles p { font-size: 0.78rem; color: #6b6b78; margin: 0.1rem 0 0 0; }
.divider { border: none; border-top: 1px solid #1a1a22; margin: 0.6rem 0; }
.divider-tight { border: none; border-top: 1px solid #1a1a22; margin: 0.4rem 0; }

/* ── team boxes (side by side, like the reference) ───────────────────── */
.team-row { display:flex; gap: 0.6rem; margin: 0.3rem 0 0.6rem 0; }
.team-box { flex:1; border-radius: 16px; padding: 0.9rem 0.5rem 0.8rem 0.5rem; text-align:center; background: #101018; }
.team-box.you { border: 1.5px solid #22c55e; }
.team-box.ai  { border: 1.5px solid #3b82f6; }
.team-box .tb-tag { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }
.team-box.you .tb-tag { color: #34d399; }
.team-box.ai .tb-tag { color: #60a5fa; }
.team-box .tb-score { font-family: 'Space Mono', monospace; font-size: 2.1rem; font-weight: 700; color: #fff; line-height: 1.25; margin-top: 0.15rem; }
.team-box .tb-sub { font-size: 0.72rem; color: #7a7a86; margin-top: 0.1rem; }
.vs-mid { display:flex; align-items:center; justify-content:center; }
.vs-pill {
    font-family: 'Space Mono', monospace; font-size: 0.66rem; font-weight: 700; color: #6b6b78;
    background: #16161f; border: 1px solid #26262f; border-radius: 999px;
    width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}

/* ── 5-item stat strip ───────────────────────────────────────────────── */
.stat-strip { display:flex; border: 1px solid #1e1e28; border-radius: 14px; padding: 0.65rem 0.2rem; margin: 0.5rem 0; background: #0d0d13; }
.stat-strip .si { flex:1; text-align:center; }
.stat-strip .si .siv { font-family: 'Space Mono', monospace; font-size: 1.1rem; font-weight: 700; color: #fff; }
.stat-strip .si .sil { font-size: 0.58rem; text-transform: uppercase; letter-spacing: 0.06em; color: #6b6b78; margin-top: 1px; }

/* ── last ball box ────────────────────────────────────────────────────── */
.lastball-box { display:flex; align-items:center; justify-content:space-between; border: 1px solid #1e1e28;
    border-radius: 14px; padding: 0.7rem 0.9rem; margin: 0.5rem 0; background: #0d0d13; }
.lb-left { display:flex; align-items:center; gap: 0.7rem; }
.lb-pill { font-family:'Space Mono', monospace; font-weight:700; font-size:1.15rem; border-radius:10px;
    width: 40px; height: 40px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.lb-pill.out    { background:#2a0d0d; color:#f87171; border:1.5px solid #f87171; }
.lb-pill.runs   { background:#1a2440; color:#818cf8; border:1.5px solid #818cf8; }
.lb-pill.dot    { background:#161620; color:#9a9aa5; border:1.5px solid #33333f; }
.lb-pill.survived { background:#1c2a1c; color:#4ade80; border:1.5px solid #4ade80; }
.lb-info { display:flex; flex-direction:column; }
.lb-label { font-size: 0.6rem; text-transform:uppercase; letter-spacing:0.08em; color:#6b6b78; }
.lb-text { font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:0.95rem; color:#e8e8ee; margin-top:1px; }
.lb-right { text-align:right; }
.lb-right .lb-label { text-align:right; }
.lb-right .tr-val { font-family:'Space Mono', monospace; font-size:1.35rem; font-weight:700; color:#4ade80; }

.banner { text-align: center; padding: 0.9rem; border-radius: 12px; margin: 0.8rem 0; font-family: 'Space Mono', monospace; font-size: 1rem; font-weight: 700; }
.banner-info   { background: #14141c; color: #ccc;    border: 1px solid #26262f; font-size: 0.92rem; }
.banner-win    { background: #14532d; color: #4ade80; border: 1px solid #4ade80; font-size: 1.2rem; }
.banner-lose   { background: #450a0a; color: #f87171; border: 1px solid #f87171; font-size: 1.2rem; }
.banner-tie    { background: #422006; color: #facc15; border: 1px solid #facc15; font-size: 1.2rem; }

.stat-row { display: flex; gap: 0.6rem; margin: 0.5rem 0; }
.stat-box { background: #161616; border: 1px solid #222; border-radius: 10px; padding: 0.5rem 0.7rem; text-align: center; flex: 1; }
.stat-box .sv { font-family: 'Space Mono', monospace; font-size: 1.2rem; font-weight: 700; color: #fff; }
.stat-box .sl { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.1em; color: #555; }

/* ── shot pad ─────────────────────────────────────────────────────────── */
.pad-label { text-align:center; color:#e8e8ee; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin: 0.6rem 0 0.05rem 0; }
.pad-sub { text-align:center; color:#6b6b78; font-size: 0.72rem; margin: 0 0 0.5rem 0; }

div[data-testid="stButton"] > button {
    background: #14141c !important; color: #f0f0f0 !important;
    border: 1.5px solid #26262f !important; border-radius: 14px !important;
    font-family: 'Space Mono', monospace !important; font-weight: 700 !important; font-size: 1.3rem !important;
    padding: 0.85rem 0.5rem !important; transition: all 0.12s ease !important; width: 100% !important;
}
div[data-testid="stButton"] > button:hover { border-color: #4ade80 !important; background: #182018 !important; color: #4ade80 !important; }
div[data-testid="stButton"] > button:active { transform: scale(0.96); }

.st-key-pad_top div[data-testid="stButton"] > button    { border-color: #22c55e !important; color: #d1fae5 !important; }
.st-key-pad_top div[data-testid="stButton"] > button:hover    { background:#102015 !important; }
.st-key-pad_bottom div[data-testid="stButton"] > button { border-color: #3b82f6 !important; color: #dbeafe !important; }
.st-key-pad_bottom div[data-testid="stButton"] > button:hover { background:#0f1b2e !important; }
.st-key-pad_zero div[data-testid="stButton"] > button    { border-color: #a78bfa !important; color: #ede9fe !important; }
.st-key-pad_zero div[data-testid="stButton"] > button:hover   { background:#1c1730 !important; }

/* smaller, muted style for the bottom control row */
.controls-row div[data-testid="stButton"] > button {
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important; font-size: 0.78rem !important;
    padding: 0.55rem 0.3rem !important; color: #9a9aa5 !important; border-color: #1e1e28 !important;
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
.catch-hint { text-align: center; color: #a78bfa; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin: 0.5rem 0 0.6rem 0; }

/* ── recent balls / this over rows ───────────────────────────────────── */
.balls-row-wrap { display:flex; gap: 0.8rem; margin: 0.7rem 0 0.2rem 0; }
.balls-col { flex:1; }
.balls-col-title { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.08em; color: #6b6b78; margin-bottom: 0.3rem; }
.balls-chips { display:flex; gap: 0.28rem; flex-wrap: wrap; align-items:center; }
.ball-chip { font-family: 'Space Mono', monospace; font-size: 0.66rem; font-weight: 700; color: #fff;
    border-radius: 50%; width: 24px; height: 24px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.ball-chip.v0 { background:#1a1a24; border: 1px solid #33333f; color:#9a9aa5; }
.ball-chip.v1, .ball-chip.v2, .ball-chip.v3 { background:#102015; border: 1px solid #22c55e; color:#4ade80; }
.ball-chip.v4, .ball-chip.v5 { background:#0f1b2e; border: 1px solid #3b82f6; color:#60a5fa; }
.ball-chip.v6 { background:#1c1730; border: 1px solid #a78bfa; color:#c4b5fd; }
.ball-chip.vw { background:#2a0d0d; border: 1px solid #f87171; color:#f87171; }
.this-over-sep { color:#3a3a48; font-size: 0.8rem; margin: 0 0.15rem; }

.footer { text-align: center; margin-top: 0.9rem; font-size: 0.68rem; color: #3a3a44; letter-spacing: 0.04em; }
.footer span { color:#f87171; }
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
    """Classify a matching-number ball.
    'catch_chance' / 'runout_chance' / 'stumped_chance' all hand control to the
    interactive 3-number mini-game instead of resolving the wicket immediately —
    the batter is only out if the fielding side's pick matches theirs."""
    if random.random() < 0.10:
        return 'stumped_chance'
    if 4 <= number <= 6:
        recent = batter_history[-5:]
        high_ratio = (sum(1 for n in recent if n in (4,5,6)) / len(recent)) if recent else 0
        if high_ratio >= 0.55 or random.random() < 0.4:
            return 'catch_chance'
        return 'bowled'
    elif 1 <= number <= 3:
        return 'runout_chance'
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
        "ball_log": [],            # list of {"display": "4"/"W"/"0", "type": "runs"/"out"/"dot"}
        "target": None,
        "innings1_score": 0,
        "innings1_wickets": 0,
        "innings1_balls": 0,
        "innings1_batter": None,
        "last_event": None,
        "last_msg": "",
        "last_display": "-",
        "result_msg": "",
        "toss_result": None,
        "pending_wicket": None,
        "wicket_options": None,
        "paused": False,
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
        if dtype in ('catch_chance', 'runout_chance', 'stumped_chance'):
            # Hold off resolving the wicket until the player plays the mini-game
            options = random.sample(range(0, 7), 3)
            s.pending_wicket = {
                "batter": batter, "bowler": bowler,
                "batter_num": batter_num, "bowler_num": bowler_num,
                "kind": dtype,
            }
            s.wicket_options = options
            s.last_event = "dot"
            label = {"catch_chance": "🏐 Big shot! It's up in the air",
                      "runout_chance": "🏃 Quick single — it's close!",
                      "stumped_chance": "🧤 Sharp work behind the stumps!"}[dtype]
            s.last_msg = f"{label} ({batter_num} vs {bowler_num})"
            s.last_display = str(batter_num)
            return  # wait for the mini-game before finishing this ball
        apply_dismissal(batter, bowler, batter_num, bowler_num, dtype)
    else:
        runs = batter_num
        s.score += runs
        s.stats[batter]["runs"] += runs
        s.stats[bowler]["runs_conceded"] += runs
        s.last_event = "runs" if runs > 0 else "dot"
        s.last_msg = f"+{runs} run{'s' if runs != 1 else ''} ({batter_num} vs {bowler_num})"
        s.last_display = str(runs)
        s.ball_log.append({"display": str(runs), "type": "runs" if runs > 0 else "dot"})

    check_innings_over()

def apply_dismissal(batter, bowler, batter_num, bowler_num, dtype):
    s.wickets_lost += 1
    s.stats[batter]["outs"] += 1
    if dtype == "caught":    s.stats[bowler]["catches"] += 1
    elif dtype == "run_out": s.stats[bowler]["runouts"] += 1
    elif dtype == "stumped": s.stats[bowler]["stumpings"] += 1
    else:                    s.stats[bowler]["bowled"] += 1
    label = {"caught": "Caught", "run_out": "Run Out", "stumped": "Stumped"}.get(dtype, "Bowled")
    s.last_event = "out"
    s.last_msg = f"OUT! {label}! ({batter_num} vs {bowler_num})"
    s.last_display = "W"
    s.ball_log.append({"display": "W", "type": "out"})

def resolve_wicket_chance(player_choice):
    pw = s.pending_wicket
    if not pw:
        return
    bot_choice = random.choice(s.wicket_options)
    batter, bowler = pw["batter"], pw["bowler"]
    batter_num, bowler_num = pw["batter_num"], pw["bowler_num"]
    kind_map = {"catch_chance": "caught", "runout_chance": "run_out", "stumped_chance": "stumped"}
    verb_map = {"catch_chance": "Caught", "runout_chance": "Run Out", "stumped_chance": "Stumped"}
    dtype = kind_map[pw["kind"]]
    verb = verb_map[pw["kind"]]
    if player_choice == bot_choice:
        s.wickets_lost += 1
        s.stats[batter]["outs"] += 1
        if dtype == "caught":    s.stats[bowler]["catches"] += 1
        elif dtype == "run_out": s.stats[bowler]["runouts"] += 1
        else:                    s.stats[bowler]["stumpings"] += 1
        s.last_event = "out"
        s.last_msg = f"OUT! {verb}! Fielder matched your pick — both chose {player_choice}! ({batter_num} vs {bowler_num})"
        s.last_display = "W"
        s.ball_log.append({"display": "W", "type": "out"})
    else:
        s.last_event = "survived"
        s.last_msg = f"🙌 Survived! You picked {player_choice}, fielder picked {bot_choice} — no run added. ({batter_num} vs {bowler_num})"
        s.last_display = "0"
        s.ball_log.append({"display": "0", "type": "dot"})
    s.pending_wicket = None
    s.wicket_options = None
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
        s.ball_log      = []
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

def ball_chip_html(entry):
    disp = entry["display"]
    cls = "vw" if disp == "W" else f"v{disp}"
    return f"<span class='ball-chip {cls}'>{disp}</span>"

# ══════════════════════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════════════════════
h1, h2 = st.columns([5, 1])
with h1:
    st.markdown("""
    <div class="titles">
        <h2>🏏 Hand Cricket</h2>
        <p>Play against AI</p>
    </div>""", unsafe_allow_html=True)
with h2:
    st.write("")
    if st.button("🔄", key="header_refresh", use_container_width=True):
        st.rerun()
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

    def team_block(who):
        currently_batting = (batter == who)
        if currently_batting:
            runs, wkts, balls = s.score, s.wickets_lost, s.balls_bowled
            sub = f"{balls//6}.{balls%6} OVERS"
        elif inn_num == 2 and s.innings1_batter == who:
            runs, wkts, balls = s.innings1_score, s.innings1_wickets, s.innings1_balls
            sub = f"{balls//6}.{balls%6} OVERS"
        else:
            runs, wkts = None, None
            sub = f"Target: {s.target}" if s.target else "yet to bat"
        score_txt = f"{runs}-{wkts}" if runs is not None else "--"
        return score_txt, sub

    you_score, you_sub = team_block("player")
    ai_score, ai_sub = team_block("CricBot")
    you_name = s.player_name if len(s.player_name) <= 10 else "YOU"

    st.markdown(f"""<div class='team-row'>
        <div class='team-box you'>
            <div class='tb-tag'>{you_name.upper()}</div>
            <div class='tb-score'>{you_score}</div>
            <div class='tb-sub'>{you_sub}</div>
        </div>
        <div class='team-box ai'>
            <div class='tb-tag'>CRICBOT</div>
            <div class='tb-score'>{ai_score}</div>
            <div class='tb-sub'>{ai_sub}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    ov_left_balls = balls_remaining()
    ov_left_txt = f"{ov_left_balls//6}.{ov_left_balls%6}"
    st.markdown(f"""<div class='stat-strip'>
        <div class='si'><div class='siv'>{inn_num} of 2</div><div class='sil'>Innings</div></div>
        <div class='si'><div class='siv'>{s.target if s.target else '--'}</div><div class='sil'>Target</div></div>
        <div class='si'><div class='siv'>{s.total_overs}</div><div class='sil'>Overs</div></div>
        <div class='si'><div class='siv'>{ov_left_txt}</div><div class='sil'>Overs Left</div></div>
        <div class='si'><div class='siv'>{wickets_remaining()}</div><div class='sil'>Wkts Left</div></div>
    </div>""", unsafe_allow_html=True)

    # ── last ball box ────────────────────────────────────────────────────
    if s.last_msg:
        pill_cls = {"out":"out","runs":"runs","dot":"dot","survived":"survived"}.get(s.last_event, "dot")
        text_map = {"out":"OUT!", "survived":"SURVIVED!"}
        if s.last_event in text_map:
            lb_text = text_map[s.last_event]
        elif s.last_display == "0":
            lb_text = "DOT BALL"
        elif s.last_display in ("4","6"):
            lb_text = "FOUR!" if s.last_display == "4" else "SIX!"
        elif s.last_display.isdigit():
            lb_text = f"{s.last_display} RUN{'S' if s.last_display != '1' else ''}"
        else:
            lb_text = ""
        st.markdown(f"""<div class='lastball-box'>
            <div class='lb-left'>
                <div class='lb-pill {pill_cls}'>{s.last_display}</div>
                <div class='lb-info'>
                    <div class='lb-label'>Last Ball</div>
                    <div class='lb-text'>{lb_text}</div>
                </div>
            </div>
            <div class='lb-right'>
                <div class='lb-label'>Total Runs</div>
                <div class='tr-val'>{s.score}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        role = "batting" if batter == "player" else "bowling"
        st.markdown(f"""<div class='lastball-box'>
            <div class='lb-left'>
                <div class='lb-pill dot'>•</div>
                <div class='lb-info'>
                    <div class='lb-label'>Get Ready</div>
                    <div class='lb-text'>You're {role} — pick a number 0–6</div>
                </div>
            </div>
            <div class='lb-right'>
                <div class='lb-label'>Total Runs</div>
                <div class='tr-val'>{s.score}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    if s.paused and not s.pending_wicket:
        st.markdown("<div class='banner banner-info'>⏸ Paused — tap Resume below to continue</div>", unsafe_allow_html=True)
    elif s.pending_wicket:
        kind_label = {"catch_chance": "Catch", "runout_chance": "Run Out", "stumped_chance": "Stumping"}[s.pending_wicket["kind"]]
        st.markdown(f"<p class='catch-hint'>⚡ {kind_label} chance! Match the fielder's pick to get the wicket</p>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, opt in enumerate(s.wicket_options):
            with cols[i]:
                if st.button(str(opt), key=f"wk_{s.balls_bowled}_{opt}", use_container_width=True):
                    resolve_wicket_chance(opt)
                    st.rerun()
    else:
        label = "Your batting shot" if batter == "player" else "Your bowling number"
        st.markdown(f"<p class='pad-label'>{label}</p>", unsafe_allow_html=True)
        st.markdown("<p class='pad-sub'>Choose any number from 0 to 6</p>", unsafe_allow_html=True)

        with st.container(key="pad_top"):
            cols = st.columns(3, gap="small")
            for c, n in enumerate([1, 2, 3]):
                with cols[c]:
                    if st.button(str(n), key=f"num_{s.balls_bowled}_{n}", use_container_width=True):
                        process_ball(n); st.rerun()
        with st.container(key="pad_bottom"):
            cols = st.columns(3, gap="small")
            for c, n in enumerate([4, 5, 6]):
                with cols[c]:
                    if st.button(str(n), key=f"num_{s.balls_bowled}_{n}", use_container_width=True):
                        process_ball(n); st.rerun()
        with st.container(key="pad_zero"):
            if st.button("0", key=f"num_{s.balls_bowled}_0", use_container_width=True):
                process_ball(0); st.rerun()

    # ── recent balls / this over ────────────────────────────────────────
    recent = s.ball_log[-6:]
    over_start = (s.balls_bowled // 6) * 6
    this_over = s.ball_log[over_start:]
    recent_html = "".join(ball_chip_html(b) for b in recent) if recent else "<span style='color:#3a3a44;font-size:0.7rem;'>—</span>"
    this_over_html = "".join(ball_chip_html(b) for b in this_over) if this_over else "<span style='color:#3a3a44;font-size:0.7rem;'>—</span>"
    st.markdown(f"""<div class='balls-row-wrap'>
        <div class='balls-col'>
            <div class='balls-col-title'>Recent Balls</div>
            <div class='balls-chips'>{recent_html}</div>
        </div>
        <div class='balls-col'>
            <div class='balls-col-title'>This Over</div>
            <div class='balls-chips'>{this_over_html}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider-tight">', unsafe_allow_html=True)
    st.markdown('<div class="controls-row">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        if st.button("🔁 New Game", use_container_width=True):
            reset(); st.rerun()
    with c2:
        pause_label = "▶ Resume" if s.paused else "⏸ Pause"
        if st.button(pause_label, use_container_width=True):
            s.paused = not s.paused
            st.rerun()
    with c3:
        if st.button("📊 Scorecard", use_container_width=True):
            s.show_scorecard = not s.show_scorecard
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

st.markdown('<div class="footer">made by AhaD <span>❤️</span></div>', unsafe_allow_html=True)

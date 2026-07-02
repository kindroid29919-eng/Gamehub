import random
import streamlit as st
from collections import Counter

st.set_page_config(page_title="Hand Cricket", page_icon="🏏", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: #0d0d0d; color: #f0f0f0; }
.stApp { background: #0d0d0d; }
[data-testid="stSidebar"] { background: #111; border-right: 1px solid #1e1e1e; }

.page-title { text-align: center; padding: 1rem 0 0.5rem 0; }
.page-title h2 { font-family: 'Space Mono', monospace; font-size: 1.3rem; color: #fff; margin: 0; letter-spacing: -0.02em; }
.page-title p { font-size: 0.75rem; color: #444; margin: 0.2rem 0 0 0; }
.divider { border: none; border-top: 1px solid #1e1e1e; margin: 0.9rem 0; }

.scoreboard { background: #161616; border: 1px solid #222; border-radius: 14px; padding: 1rem; text-align: center; margin: 0.5rem 0; }
.scoreboard .big { font-family: 'Space Mono', monospace; font-size: 2.2rem; font-weight: 700; color: #fff; line-height: 1; }
.scoreboard .small { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #555; margin-top: 0.2rem; }
.scoreboard .detail { font-size: 0.85rem; color: #888; margin-top: 0.3rem; }

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

div[data-testid="stButton"] > button {
    background: #161616 !important; color: #f0f0f0 !important;
    border: 2px solid #2a2a2a !important; border-radius: 14px !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;
    padding: 0.7rem 0.5rem !important; transition: all 0.15s ease !important; width: 100% !important;
}
div[data-testid="stButton"] > button:hover { border-color: #fff !important; background: #202020 !important; }
div[data-testid="stSelectbox"] > div { background: #161616 !important; border-color: #2a2a2a !important; color: #f0f0f0 !important; }
div[data-testid="stNumberInput"] input { background: #161616 !important; color: #f0f0f0 !important; border: 2px solid #2a2a2a !important; border-radius: 10px !important; font-family: 'Space Mono', monospace !important; }

.footer { text-align: center; margin-top: 1rem; font-size: 0.7rem; color: #333; letter-spacing: 0.06em; }
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

def determine_dismissal(number, batter_history):
    if random.random() < 0.10:
        return True, 'stumped'
    if 4 <= number <= 6:
        recent = batter_history[-5:]
        high_ratio = (sum(1 for n in recent if n in (4,5,6)) / len(recent)) if recent else 0
        if high_ratio >= 0.6 and random.random() < 0.35:
            return True, 'caught'
        return True, 'out'
    elif 1 <= number <= 3:
        return (True, 'run out') if random.random() < 0.8 else (False, 'survived run out')
    return True, 'out'

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
        is_out, dismissal = determine_dismissal(batter_num, s.batter_history)
        if is_out:
            s.wickets_lost += 1
            s.stats[batter]["outs"] += 1
            if dismissal == "caught":    s.stats[bowler]["catches"] += 1
            elif dismissal == "run out": s.stats[bowler]["runouts"] += 1
            elif dismissal == "stumped": s.stats[bowler]["stumpings"] += 1
            else:                        s.stats[bowler]["bowled"] += 1
            s.last_event = "out"
            s.last_msg = f"OUT! {'Stumped' if dismissal=='stumped' else 'Caught' if dismissal=='caught' else 'Run Out' if dismissal=='run out' else 'Wicket'}! ({batter_num} vs {bowler_num})"
        else:
            s.last_event = "survived"
            s.last_msg = f"Close! Survived! ({batter_num} vs {bowler_num})"
    else:
        runs = batter_num
        s.score += runs
        s.stats[batter]["runs"] += runs
        s.stats[bowler]["runs_conceded"] += runs
        s.last_event = "runs"
        s.last_msg = f"+{runs} runs ({batter_num} vs {bowler_num})"

    # check end of innings
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
    batter_label = s.player_name if batter == "player" else "CricBot"
    bowler_label = s.player_name if bowler == "player" else "CricBot"

    # target bar (innings 2)
    if s.target:
        needed = s.target - s.score
        st.markdown(f"<div class='banner banner-info'>🎯 Target: {s.target} &nbsp;|&nbsp; Need {needed} more from {balls_remaining()} ball{'s' if balls_remaining()!=1 else ''}</div>", unsafe_allow_html=True)

    # scoreboard
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class='scoreboard'>
            <div class='small'>Innings {inn_num} · {batter_label} batting</div>
            <div class='big'>{s.score}/{s.wickets_lost}</div>
            <div class='detail'>{s.balls_bowled//6}.{s.balls_bowled%6} / {s.total_overs} overs</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='scoreboard'>
            <div class='small'>Innings 1 result</div>
            <div class='big'>{s.innings1_score}/{s.innings1_wickets}</div>
            <div class='detail'>{s.innings1_balls//6}.{s.innings1_balls%6} / {s.total_overs} ov</div>
        </div>""" if inn_num == 2 else f"""<div class='scoreboard'>
            <div class='small'>Wickets remaining</div>
            <div class='big'>{wickets_remaining()}</div>
            <div class='detail'>{balls_remaining()} ball{'s' if balls_remaining()!=1 else ''} left</div>
        </div>""", unsafe_allow_html=True)

    # last event banner
    if s.last_msg:
        css = {"out":"banner-out","runs":"banner-runs","survived":"banner-dot"}.get(s.last_event, "banner-info")
        st.markdown(f"<div class='banner {css}'>{s.last_msg}</div>", unsafe_allow_html=True)
    else:
        role = "batting" if batter == "player" else "bowling"
        st.markdown(f"<div class='banner banner-info'>You are {role} — pick a number 0–6</div>", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # number pad 0-6
    if batter == "player":
        st.markdown("<p style='text-align:center;color:#555;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;'>Your batting shot</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center;color:#555;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;'>Your bowling number</p>", unsafe_allow_html=True)

    row1 = st.columns(4)
    row2 = st.columns(4)
    nums = [0,1,2,3,4,5,6]
    for i, n in enumerate(nums):
        col = row1[i] if i < 4 else row2[i-4]
        with col:
            if st.button(str(n), key=f"num_{n}", use_container_width=True):
                process_ball(n)
                st.rerun()

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

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

.page-title { text-align: center; padding: 0.4rem 0 0.15rem 0; }
.page-title h2 { font-family: 'Space Mono', monospace; font-size: 1.1rem; color: #fff; margin: 0; letter-spacing: -0.02em; }
.page-title p { font-size: 0.7rem; color: #444; margin: 0.1rem 0 0 0; }
.divider { border: none; border-top: 1px solid #1e1e1e; margin: 0.5rem 0; }

.scoreboard { background: #161616; border: 1px solid #222; border-radius: 14px; padding: 0.6rem; text-align: center; margin: 0.3rem 0; }
.scoreboard .big { font-family: 'Space Mono', monospace; font-size: 1.7rem; font-weight: 700; color: #fff; line-height: 1; }
.scoreboard .small { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: #555; margin-top: 0.15rem; }
.scoreboard .detail { font-size: 0.75rem; color: #888; margin-top: 0.2rem; }

.banner { text-align: center; padding: 0.55rem; border-radius: 12px; margin: 0.45rem 0; font-family: 'Space Mono', monospace; font-size: 0.9rem; font-weight: 700; }
.banner-out    { background: #450a0a; color: #f87171; border: 1px solid #f87171; }
.banner-runs   { background: #14532d; color: #4ade80; border: 1px solid #4ade80; }
.banner-dot    { background: #1e1b4b; color: #818cf8; border: 1px solid #818cf8; }
.banner-info   { background: #1a1a1a; color: #888;    border: 1px solid #222; font-size: 0.85rem; }
.banner-win    { background: #14532d; color: #4ade80; border: 1px solid #4ade80; font-size: 1.2rem; }
.banner-lose   { background: #450a0a; color: #f87171; border: 1px solid #f87171; font-size: 1.2rem; }
.banner-tie    { background: #422006; color: #facc15; border: 1px solid #facc15; font-size: 1.2rem; }

.stat-row { display: flex; gap: 0.5rem; margin: 0.35rem 0; }
.stat-box { background: #161616; border: 1px solid #222; border-radius: 10px; padding: 0.4rem 0.6rem; text-align: center; flex: 1; }
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
div[data-testid="stTextInput"] input {
    background: #161616 !important; color: #f0f0f0 !important; border: 2px solid #2a2a2a !important;
    border-radius: 10px !important; font-family: 'Space Mono', monospace !important;
    text-align: center !important; font-size: 1.2rem !important; padding: 0.4rem !important;
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
.catch-hint { text-align: center; color: #818cf8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.6rem; }

.footer { text-align: center; margin-top: 1rem; font-size: 0.7rem; color: #333; letter-spacing: 0.06em; }
</style>
""", unsafe_allow_html=True)

# ── AI (pro logic) ────────────────────────────────────────────────────────────
ai_patterns = {0:[4,5,6],1:[3,4,6],2:[2,6,5],3:[3,1,5],4:[4,5,1],5:[3,6,5],6:[6,3,4]}

def detect_cycle(history, max_cycle=3):
    """Look for a repeating cycle in someone's recent picks (e.g. 3,5,3,5,...
    or 2,4,6,2,4,6,...) and predict what comes next if the cycle holds.
    Returns the predicted next number, or None if no clean cycle is found.
    This generalizes the old 'same number twice in a row' check to any
    short repeating rhythm, which is the pattern real players fall into
    when they think a bot 'won't guess it twice'."""
    for cycle_len in range(1, max_cycle + 1):
        needed = cycle_len * 2
        if len(history) < needed:
            continue
        recent = history[-needed:]
        first_half, second_half = recent[:cycle_len], recent[cycle_len:]
        if first_half == second_half:
            return history[-cycle_len]
    return None

def ai_bowler_choice(batter_history, own_history=None, target=None, score=0, balls_remaining=None):
    """CricBot is bowling. batter_history = the human batter's past numbers.
    own_history = CricBot's own past bowling numbers (in this innings)."""
    own_history = own_history or []
    base = 0.85
    if target is not None and balls_remaining and balls_remaining > 0:
        rr = (target - score) / (balls_remaining / 6)
        base = 0.93 if rr >= 5 else (0.8 if rr <= 2 else base)
        # Death-over lockdown: defending a target with the batter still
        # needing a big rate near the end of the innings - stop guessing
        # broadly and hunt for the wicket far more aggressively.
        if balls_remaining <= 6 and rr >= 6:
            base = 0.97

    # Cycle read: the batter is rotating through a short repeating rhythm
    # (e.g. always going back to the same number, or alternating two
    # numbers). Predict the next number in the cycle and bowl it.
    cycle_pick = detect_cycle(batter_history)
    if cycle_pick is not None and random.random() < 0.85:
        return cycle_pick

    # Anti-exploit: don't let CricBot itself become predictable by
    # systematically avoiding its own last-bowled number. A player who
    # notices "the bot never repeats" will happily replay whatever it
    # just bowled to guarantee safety - so occasionally re-bowl it on
    # pure baseline unpredictability, on top of the reads below.
    if own_history and random.random() < 0.18:
        return own_history[-1]

    # Mirror read: the batter has started copying CricBot's own previous
    # ball(s) - a common exploit built on the assumption that the bot
    # never repeats a number. The longer the mirroring streak, the more
    # confidently CricBot repeats that same number to punish it.
    if own_history and batter_history and batter_history[-1] == own_history[-1]:
        mirror_len = 0
        for i in range(1, min(len(batter_history), len(own_history)) + 1):
            if batter_history[-i] == own_history[-i]:
                mirror_len += 1
            else:
                break
        if random.random() < min(0.9, 0.5 + 0.2 * mirror_len):
            return own_history[-1]

    # Spam read: the batter played the same number on the last two balls.
    # A human mashing one number is predictable - bowl that exact number
    # to punish the repeat instead of guessing randomly.
    if len(batter_history) >= 2 and batter_history[-1] == batter_history[-2]:
        if random.random() < 0.8:
            return batter_history[-1]

    # If the last ball collided (a wicket-taking ball), the same trick just
    # worked - re-bowl it since the batter may not expect it again.
    if own_history and batter_history and own_history[-1] == batter_history[-1]:
        if random.random() < 0.45:
            return own_history[-1]

    if len(batter_history) >= 1 and random.random() < base:
        return random.choice(ai_patterns[batter_history[-1]])
    if len(batter_history) >= 3:
        freq = Counter(batter_history[-5:])
        favs = [n for n, _ in freq.most_common(2)]
        if favs: return random.choice(favs)
    return random.randint(0, 6)

def ai_batter_choice(bowler_history, own_history=None, score=0, target=None,
                      balls_remaining=0, wickets_remaining=1, total_overs=1):
    """CricBot is batting. bowler_history = the human bowler's past numbers.
    own_history = CricBot's own past batting numbers (in this innings)."""
    own_history = own_history or []
    balls_total = total_overs * 6
    balls_bowled = balls_total - balls_remaining
    overs_left = balls_remaining / 6 if balls_remaining else 0

    if target is None:
        # First innings: build an innings, but ramp up hard in the closing
        # overs regardless of how things have gone so far.
        progress = (balls_bowled / balls_total) if balls_total else 0
        aggression = 0.3 + 0.5 * progress
        if balls_remaining <= 6:
            aggression = max(aggression, 0.75)
        if wickets_remaining <= 1: aggression *= 0.6
    else:
        # Second innings (chasing): play to the required run rate, not to
        # random chance. rr is "runs needed per over from here" - the
        # single most important number CricBot should react to.
        rr = ((target - score) / overs_left) if overs_left > 0 else 99
        runs_needed = target - score

        if runs_needed <= 0:
            aggression = 0.05  # already won, no need to risk anything
        else:
            aggression = min(1.0, max(0.05, rr / 6.0))
            # Required rate is climbing out of reach - urgency overrides
            # caution almost entirely; a dot ball here can lose the match.
            if rr >= 9:
                aggression = 0.97
            elif rr >= 6.5:
                aggression = max(aggression, 0.9)
            elif rr >= 5:
                aggression = max(aggression, 0.75)

            # Death-overs override: with only a handful of balls left,
            # CricBot must not "play it safe" and simply run out of overs.
            # This directly targets the old bug where CricBot finished an
            # innings with wickets and overs both unused.
            if balls_remaining <= 6 and runs_needed > 0:
                needed_per_ball = runs_needed / balls_remaining
                if needed_per_ball >= 1.5:
                    aggression = 0.97
                elif needed_per_ball >= 1.0:
                    aggression = max(aggression, 0.85)
                elif needed_per_ball >= 0.6:
                    aggression = max(aggression, 0.6)

            # Cruising: the target is comfortably in hand with plenty of
            # overs in the bank - no reason to risk wickets chasing boundaries.
            if rr <= 2.5 and overs_left >= 2:
                aggression = min(aggression, 0.35)

            # Last wicket standing: only throttle back if the rate is
            # actually gettable without risk; if the rate demands it,
            # CricBot has no choice but to keep swinging.
            if wickets_remaining <= 1 and rr < 4.5:
                aggression *= 0.55

    aggression = max(0.0, min(1.0, aggression))
    weights = [max(1.0 + aggression * n * 1.5 - (1 - aggression) * (n * 0.3), 0.05) for n in range(7)]

    # Cycle read: the bowler is rotating through a short repeating rhythm.
    # Predicting it means CricBot can dodge the number that would collide
    # (an out) while leaning into the rest.
    cycle_pick = detect_cycle(bowler_history)
    if cycle_pick is not None:
        weights[cycle_pick] *= 0.15

    # Spam read: the bowler repeated the same number on the last two balls.
    # A third repeat would collide and get CricBot out, so avoid that
    # number hard rather than risk it on a random weight.
    if len(bowler_history) >= 2 and bowler_history[-1] == bowler_history[-2]:
        weights[bowler_history[-1]] *= 0.1

    # Anti-exploit: don't let CricBot become predictably "safe" by always
    # avoiding the bowler's last number - occasionally play it anyway so a
    # bowler who assumes CricBot always dodges a repeat gets punished.
    if bowler_history and random.random() < 0.12:
        weights[bowler_history[-1]] *= 1.6

    # If CricBot's last shot beat the bowler and scored a boundary, repeat
    # it - it just worked, and the bowler may not counter it twice.
    if own_history and bowler_history and own_history[-1] != bowler_history[-1] and own_history[-1] >= 4:
        if random.random() < 0.35:
            weights[own_history[-1]] *= 1.8

    if len(bowler_history) >= 2:
        freq = Counter(bowler_history[-5:])
        avoidance = 0.5 if aggression < 0.8 else 0.2
        for n in [x for x, _ in freq.most_common(2)]:
            weights[n] *= (1 - avoidance)
    total_w = sum(weights)
    return random.choices(range(7), weights=[w/total_w for w in weights], k=1)[0]

def determine_dismissal_type(number, batter_history):
    """Classify a matching-number ball. Every outcome except 'bowled' hands
    control to an interactive mini-game (pick a number, match it and it's
    OUT) instead of resolving the wicket by a hidden coin flip."""
    if random.random() < 0.10:
        return 'stump_chance'
    if 4 <= number <= 6:
        recent = batter_history[-5:]
        high_ratio = (sum(1 for n in recent if n in (4,5,6)) / len(recent)) if recent else 0
        if high_ratio >= 0.6 and random.random() < 0.55:
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
        "target": None,
        "innings1_score": 0,
        "innings1_wickets": 0,
        "innings1_balls": 0,
        "innings1_batter": None,
        "last_event": None,
        "last_msg": "",
        "result_msg": "",
        "break_msg": "",
        "toss_result": None,
        "pending_dismissal": None,
        "dismissal_options": None,
        "input_error": False,
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
        bowler_num = ai_bowler_choice(s.batter_history, own_history=s.bowler_history,
                                       target=s.target, score=s.score, balls_remaining=balls_remaining())
    else:
        bowler_num = player_num
        batter_num = ai_batter_choice(s.bowler_history, own_history=s.batter_history,
                                       score=s.score, target=s.target,
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
        if dtype in ('catch_chance', 'runout_chance', 'stump_chance'):
            # Hold off resolving the wicket until the player plays the mini-game
            options = random.sample(range(0, 7), 3)
            s.pending_dismissal = {
                "type": dtype, "batter": batter, "bowler": bowler,
                "batter_num": batter_num, "bowler_num": bowler_num,
            }
            s.dismissal_options = options
            s.last_event = "dot"
            hint = {
                "catch_chance": "🏐 Big shot! It's up in the air — catch chance!",
                "runout_chance": "🏃 Quick single! Throw's coming in — run-out chance!",
                "stump_chance": "🧤 Keeper's up! Stumping chance!",
            }[dtype]
            s.last_msg = f"{hint} ({batter_num} vs {bowler_num})"
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
    # Only the instant 'bowled' outcome reaches here now — catch/run-out/
    # stumping all go through the interactive resolve_dismissal mini-game.
    s.wickets_lost += 1
    s.stats[batter]["outs"] += 1
    s.stats[bowler]["bowled"] += 1
    s.last_event = "out"
    s.last_msg = f"OUT! Bowled! ({batter_num} vs {bowler_num})"

def resolve_dismissal(player_choice):
    pd = s.pending_dismissal
    if not pd:
        return
    bot_choice = random.choice(s.dismissal_options)
    dtype = pd["type"]
    batter, bowler = pd["batter"], pd["bowler"]
    batter_num, bowler_num = pd["batter_num"], pd["bowler_num"]
    label = {"catch_chance": "Caught", "runout_chance": "Run Out", "stump_chance": "Stumped"}[dtype]
    stat_key = {"catch_chance": "catches", "runout_chance": "runouts", "stump_chance": "stumpings"}[dtype]
    action = {"catch_chance": "catch", "runout_chance": "run-out", "stump_chance": "stumping"}[dtype]

    # When CricBot is batting, the human is bowling AND fielding - so the
    # button the human clicks *is* their own fielding attempt, not some
    # separate "fielder" entity. Messaging needs to reflect that instead of
    # talking about "the fielder" in the third person.
    player_is_fielding = (bowler == "player")

    if player_choice == bot_choice:
        s.wickets_lost += 1
        s.stats[batter]["outs"] += 1
        s.stats[bowler][stat_key] += 1
        s.last_event = "out"
        if player_is_fielding:
            s.last_msg = f"OUT! {label}! You read it perfectly and took the {action} yourself! ({batter_num} vs {bowler_num})"
        else:
            s.last_msg = f"OUT! {label}! You picked {player_choice}, fielder also picked {bot_choice}! ({batter_num} vs {bowler_num})"
    else:
        s.last_event = "survived"
        if player_is_fielding:
            s.last_msg = f"😬 You dropped the {action}! You picked {player_choice}, it needed to be {bot_choice} — safe for now! ({batter_num} vs {bowler_num})"
        else:
            s.last_msg = f"🙌 Survived! You picked {player_choice}, fielder picked {bot_choice} — safe for now! ({batter_num} vs {bowler_num})"
    s.pending_dismissal = None
    s.dismissal_options = None
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
        batter_label = s.player_name if s.first_batter == "player" else "CricBot"
        overs_str = f"{s.balls_bowled//6}.{s.balls_bowled%6}"
        s.break_msg = (f"🏁 Innings 1 complete! {batter_label} scored {s.score}/{s.wickets_lost} "
                        f"from {overs_str} overs. Target for Innings 2: {s.target} runs.")
        # reset for innings 2
        s.score         = 0
        s.wickets_lost  = 0
        s.balls_bowled  = 0
        s.batter_history  = []
        s.bowler_history  = []
        s.last_event = None
        s.last_msg = ""
        s.phase = "innings_break"
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

# ── INNINGS BREAK ─────────────────────────────────────────────────────────────
elif s.phase == "innings_break":
    st.markdown(f"<div class='banner banner-info'>{s.break_msg}</div>", unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888;font-size:0.85rem;'>Innings 2 is about to begin.</p>", unsafe_allow_html=True)
    if st.button("▶ Start Innings 2", use_container_width=True):
        s.phase = "innings2"
        st.rerun()

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
        css = {"out":"banner-out","runs":"banner-runs","survived":"banner-dot","dot":"banner-dot"}.get(s.last_event, "banner-info")
        st.markdown(f"<div class='banner {css}'>{s.last_msg}</div>", unsafe_allow_html=True)
    else:
        role = "batting" if batter == "player" else "bowling"
        st.markdown(f"<div class='banner banner-info'>You are {role} — enter a number 0–6</div>", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if s.pending_dismissal:
        # ── DISMISSAL MINI-GAME (catch / run-out / stumping) ───────────────────
        player_is_fielding = s.pending_dismissal["bowler"] == "player"
        if player_is_fielding:
            hints = {
                "catch_chance": "🏐 Catch chance! Pick a number — match it and YOU take the catch",
                "runout_chance": "🏃 Run-out chance! Pick a number — match it and YOU pull off the run-out",
                "stump_chance": "🧤 Stumping chance! Pick a number — match it and YOU whip off the bails",
            }
        else:
            hints = {
                "catch_chance": "🏐 Catch chance! Pick a number — match the fielder's pick and it's OUT",
                "runout_chance": "🏃 Run-out chance! Pick a number — match the fielder's throw and it's OUT",
                "stump_chance": "🧤 Stumping chance! Pick a number — match the keeper's pick and it's OUT",
            }
        st.markdown(f"<p class='catch-hint'>{hints[s.pending_dismissal['type']]}</p>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, opt in enumerate(s.dismissal_options):
            with cols[i]:
                if st.button(str(opt), key=f"dismiss_{s.balls_bowled}_{opt}", use_container_width=True):
                    resolve_dismissal(opt)
                    st.rerun()
    else:
        # ── TYPE YOUR NUMBER ──────────────────────────────────────────────────
        label = "Your batting shot" if batter == "player" else "Your bowling number"
        st.markdown(f"<p style='text-align:center;color:#555;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;'>{label}</p>", unsafe_allow_html=True)
        with st.form(key=f"ball_form_{s.balls_bowled}", clear_on_submit=True):
            user_val = st.text_input("Enter a number (0-6)", key="ball_num_input",
                                      label_visibility="collapsed", placeholder="Type 0-6, then press Submit")
            submitted = st.form_submit_button("Submit ▶", use_container_width=True)
        if submitted:
            val = user_val.strip()
            if val.isdigit() and 0 <= int(val) <= 6:
                s.input_error = False
                process_ball(int(val))
                st.rerun()
            else:
                s.input_error = True
        if s.input_error:
            st.markdown("<p class='input-error'>⚠️ Please enter a valid number between 0 and 6.</p>", unsafe_allow_html=True)

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

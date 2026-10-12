# Krypto — Product Specification

## 1. Purpose

A single-player, timed, Python implementation of the card game Krypto. 
Each round deals five number cards and a target number from a
standard 56-card Krypto deck. The player combines as many of the five
cards as possible — using addition, subtraction, multiplication,
division, and up to three pairs of parentheses — into an expression that
evaluates exactly to the target. Score for a round equals the number of
hand cards used in an accepted expression (0 for a round ended by Give
Up or Exit). Round time is tracked as an up-counting stopwatch; best times 
and lifetime statistics are derived from a saved history of past rounds.
/
## 2. Non-Goals

- No multiplayer, no networking, no accounts.
- No countdown timer or time-based auto-fail — the stopwatch never ends a
  round on its own; only a correct Submit, a Give Up, or an Exit does.
- No solver — the app never computes, stores, or reveals its own solution
  to a deal.
- No free-typed expression entry — all input is clicks on card/operator/
  parenthesis buttons (§4).
- No database — persistence is a single flat, human-readable history
  file (§6).
- No web server, no browser dependency.
- No theming/skins, sound, animation, or high-DPI-specific handling.
- No keyboard shortcuts — mouse/click only.
- No in-app auto-update mechanism.

## 3. Game Rules (Authoritative)

The table below is verified against the published Krypto rules.

**Deck composition (56 cards total):**

| Values | Copies each | Subtotal |
|---|---|---|
| 1–6 | 3 | 18 |
| 7–10 | 4 | 16 |
| 11–17 | 2 | 14 |
| 18–25 | 1 | 8 |
| **Total** | | **56** |

- One deal draws 6 cards without replacement: 1 **target** card + 5
  **hand** cards.
- Hand-card order is fixed for the round and matches on-screen position.
  This matters because a hand can contain duplicate values (e.g. two
  3s) — duplicates are told apart only by which position they're in,
  never by any other identity.
- Allowed operations: `+ - * /`, plus up to 3 pairs of parentheses (the
  logical maximum for 5 operands, e.g. `(((a+b)*c)-d)+e`).
- **Scoring (house rule, deliberately overriding official Krypto):**
  official rules require using all 5 cards; this implementation instead
  scores however many of the 5 cards (1–5) were used in a correct
  expression. A confirmed Give Up or Exit scores 0.
- **Win condition:** the computed result must equal the target exactly.
  Evaluation must be exact — a mathematically correct solution must never
  be rejected due to rounding/precision error.
- **Intermediate-value legality** this build is
  *permissive* — negative and non-integer values may occur mid-
  calculation; only the *final* result must equal the integer target
  exactly. The stricter official "International Rules" variant (every
  intermediate value must be a non-negative whole number) is not
  implemented — see §9.

## 4. Input Model

- All input is click-driven: the player clicks card, operator (`+ - *
  /`), and parenthesis buttons to build an expression left to right. No
  free typing at any point.
- Each hand card can be placed at most once; placing it disables that
  card's button until it's removed.
- Three ways to remove tokens: click the most-recently-placed token to pop
  it off (undo, one at a time), the Undo button, or a single Clear button 
  that wipes the whole expression.
- Up to 3 opening and 3 closing parentheses may be placed (§3).
- The expression area has a fixed maximum length of 15 symbols (5
  numbers + 4 operators + 6 parentheses — the worst case allowed by the
  rules above), rather than growing or scrolling. Once 15 symbols are
  placed, no further symbol can be added until Undo or Clear frees space.
- Submit is always available; there is no live well-formedness checking
  as the expression is built. An incomplete or invalid expression simply
  fails on Submit with an error message — the player can keep adjusting.

## 5. Packaging & Distribution

- **Goal:** runs standalone with no separate Python installation on the
  end user's machine — double-click and go.
- **OS scope** Linux is priority, but a Windows build is a stretch goal 
  within the effort budget — see §9.
- The history file (§6) is located next to wherever the program itself
  is — never a hardcoded location — so the app works no matter where
  it's copied or run from.
- The history file is personal to each install and is never part of the
  distributed source — a fresh install/clone starts with no history.
- **Effort budget:** ~50–100 hours of total development time. This is a
  hard scope constraint — cut or simplify features rather than let the
  budget grow.

## 6. Persistence — History & Stats

- One entry is recorded per **concluded** round only — a win, an Exit, 
  or a Give Up. A failed Submit attempt records nothing.
- Each entry captures: timestamp, target, the hand dealt, result
  (win/give-up), number of cards used, and time taken.
- A single unreadable or corrupted entry must not prevent the rest of
  the history from being read, and must not crash the stats view.
- No pruning or size limit is needed — at realistic play volumes the
  history file stays small (well under a few MB even after tens of
  thousands of rounds).

## 7. GUI Design

### 7.1 Game Layout

```
+----------------------------------------------------------+
|  Krypto                                          [Stats] |
+----------------------------------------------------------+
|   Target: 17                        Time: 00:42.7        |
+----------------------------------------------------------+
|   Hand:   [ 3 ] [ 5 ] [ 8 ] [ 12 ] [ 21 ]                 |
+----------------------------------------------------------+
|   Ops:    [ + ] [ - ] [ * ] [ / ]   [ ( ]  [ ) ]          |
+----------------------------------------------------------+
|   Expr:  [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]    |
+----------------------------------------------------------+
|   [Clear]      [Undo]      [Submit]      [Give Up]       |
|                                                           |
|   (status message line — result/errors appear here)       |
+----------------------------------------------------------+
|              [ Start New Game ] [ Exit ]                 |
+----------------------------------------------------------+
```

- The window has a fixed size and does not resize, keeping the layout
  predictable.
- A Stats button is always visible and available, regardless of round
  state, and opens a separate view (§7.4). Opening it does not pause the
  active round's timer — there is no pause/resume mechanism.

### 7.2 Round Lifecycle & Button Availability

A round is either **not started**, **in progress**, **won**, or **given
up**. The app launches in the not started state — no deal happens until
the user clicks "Start New Game", which loads a fresh deal and starts
the timer.

| Control | Available when |
|---|---|
| Each hand-card button | In progress and not yet placed; re-enabled if removed from expression |
| `+ - * /` buttons | In progress and fewer than 15 symbols placed |
| `(` button | In progress, fewer than 15 symbols placed, fewer than 3 open parentheses placed so far |
| `)` button | In progress, fewer than 15 symbols placed, at least one currently-unclosed `(` exists |
| Undo | In progress and the expression is non-empty |
| Clear | In progress and the expression is non-empty |
| Submit | Always, while in progress (even on an empty expression — fails gracefully, see §3) |
| Give Up | Always, while in progress, asks for Yes/No confirmation |
| Start New Game | Only before any game has been played or once the round is won or given up — **never** mid-round |
| Stats | Always |
| Exit | Always, asks for Yes/No confirmation, then quits mid-round, records the game as a "Give Up", and closes the GUI |

- Every round ends exactly one of three ways: a correct Submit, an Exit, 
  or a Give Up.
- Once a round is won or given up, all input controls disable; the
  expression, target, and final time stay on screen exactly as they were
  at that moment, until Start New Game is clicked.

### 7.3 Submit / Give Up / Exit Behavior

- **Submit:** on success — stop the timer, record a win (§6), show a
  success message (e.g. "Solved with 4 cards in 42.7s!"). On failure
  (wrong result or invalid expression) — stay in progress, show an error
  message, leave the expression and timer untouched so the player can
  keep adjusting. If the expression was valid but the answer is wrong,
  display the result of their expression to the user.
  
- **Give Up:** asks for Yes/No confirmation. "No" changes nothing. "Yes"
  — stop the timer, record a give-up with a score of 0 (§6), show a
  neutral message but never a correct solution (§2).

- **Exit:** During an active game, Exit asks for Yes/No confirmation, 
  same as Give Up. "No" changes nothing. "Yes" — stop the timer, record 
  a give-up with a score of 0 (§6), then close the GUI entirely. Exit 
  only records a result if a game was in progress --- if there is no 
  active game then just close the GUI. 

### 7.4 Stats Behavior

Opened via the always-available Stats button. Recomputed fresh from the 
history (§6) every time it's opened. Shows: games played, a breakdown of 
wins by cards used (1–5) with count per row, and a give-up / exit count. 
Best times should only be shown for the top 10 games that successfully 
achieved the target result with all 5 hand-cards. 

- Stats are always computed fresh from the full history, not cached
  separately, so there's no separate state that can drift out of sync:
  - Games played = total rounds recorded.
  - Wins broken down by cards used (1–5).
  - Give-up and Exit count.
  - Best time *per cards-used group* — only the best times for the 
    5-card wins are displayed.

### 7.5 Stats GUI
```
+----------------------------------------------------------+
|                         Stats                             |
+----------------------------------------------------------+
|   Final Score                                Count        |
+----------------------------------------------------------+
|   0                                           235         |
+----------------------------------------------------------+
|   1                                           498         |
+----------------------------------------------------------+
|   2                                          1038         |
+----------------------------------------------------------+
|   3                                          2842         |
+----------------------------------------------------------+
|   4                                          4234         |
+----------------------------------------------------------+
|   5                                          8388         |
+----------------------------------------------------------+
|                                                           |
+----------------------------------------------------------+
|   Total Games Played                        17235         |
+----------------------------------------------------------+
|   Average Final Score                       4.060         |
+----------------------------------------------------------+
|   Average Time (5 card wins only)          63.345 sec     |
+----------------------------------------------------------+
|   Top 10 Best Times (5 card wins only)                    |
|       Date-Time         Target     Hand      Time (sec)   |
|   2026-05-23T00:00:00     17    1,3,6,12,21     23.5      |
|   2026-08-07T00:00:00     2     3,5,11,15,17    26.7      |
|   2026-04-12T00:00:00     21    10,15,18,22,23  32.7      |
|   2026-07-13T00:00:00     15    2,6,7,22,25     33.1      |
|   2026-05-22T00:00:00     3     1,10,19,22,23   34.3      |
|   2026-05-08T00:00:00     5     2,9,18,21,22    34.6      |
|   2026-06-24T00:00:00     22    3,8,17,20,24    36.1      |
|   2026-01-20T00:00:00     5     4,7,11,19,25    41.8      |
|   2026-03-01T00:00:00     11    5,6,12,18,21    44.3      |
|   2026-04-11T00:00:00     16    6,11,13,17,19   45.5      |
|                                                           |
+----------------------------------------------------------+
|                         [ Close ]                         |
+----------------------------------------------------------+
```

## 8. Testing Requirements

- Automated tests must cover dealing, expression evaluation, and
  persistence/stats logic.
- The GUI itself must also be automatically tested, not skipped — including
  in continuous integration, where GUI tests must run without requiring
  a physical display.

## 9. Explicitly Rejected / Considered-and-Discarded Ideas

Recorded so these don't get re-litigated later:

- **CLI program** — rejected for a single Tkinter GUI.
- **Free-typed expression entry** (full text box or per-character boxes) — 
  rejected as the primary mechanism in favor of fully click-driven input, 
  partly because it avoids ever needing to parse or validate arbitrary 
  user-typed text (§4). Not ruled out as a fallback if the click UI proves 
  infeasible.
- **All-5-cards-mandatory scoring** (the official rule) — deliberately
  overridden; this build scores 1–5 cards used, 0 for a give-up / exit (§3).
- **Countdown timer / time-based auto-fail** — rejected; stopwatch only.
- **Computer-generated solution on Give Up** — rejected as too much
  effort; no solution is ever revealed.
- **A database for stats/scores** — rejected; a flat history file is
  sufficient for this data shape.
- **Skipping automated tests for the GUI** — rejected; the GUI must be
  tested like everything else.
- **Multiplayer** — out of scope for this version.
- **Silent mid-round abandon via New Game** — considered and rejected;
  New Game is simply unavailable until the round concludes, removing any
  ambiguity about whether an abandoned round should count as a failure.
- **Unlimited/dynamically growing expression area** — rejected; a fixed
  maximum-length row was chosen instead (§4).
- **Strict "International Rules"** (forbidding fractional/negative
  intermediate results) — not implemented; this build only checks
  the final result against the target.

## 10. Open Questions

- Windows build in scope?
- GUI visual polish (colors, fonts, exact sizing) — left to iterate
  against a working prototype.
- Intermediate-value strictness (§3) — permissive mode chosen as the
  simpler default; confirm whether a strict "International Rules" mode
  is wanted instead, or as an optional toggle.

## 11. Definition of Done (Acceptance Criteria)

- [ ] A new deal (target + 5 hand cards) is presented per click of 
      "Start New Game".
- [ ] The player can build an expression by clicking only.
- [ ] Undo and Clear both work.
- [ ] Submit accepts an expression if it evaluates exactly to the
      target.
- [ ] Score equals the number of distinct hand cards used in an accepted
      expression.
- [ ] The timer runs as an up-counting stopwatch from deal to
      Submit-success or confirmed Give Up / exit, and never auto-fails 
      a round.
- [ ] Give Up and Exit require Yes/No confirmation; declining leaves the 
      round untouched. Confirming Give Up stops the timer, records a 0-score 
      give-up, and freezes the screen until "Start New Game" is clicked.
      Confirming Exit on an active game stops the timer, records a 0-score 
      give-up, and closes the GUI. Confirming Exit on outside of an active 
      game simply closes the GUI.
- [ ] Start New Game is unavailable during an active round and available
      only before any games have been played or after a round concludes.
- [ ] Every concluded round is recorded to history. 
- [ ] The history file is stored alongside the program itself.
- [ ] The Stats view correctly derives totals, the per-cards-used win
      breakdown, and best times solely from the recorded history.
- [ ] The app runs standalone with no separate Python install required.
- [ ] The full automated test suite, including GUI tests, passes.

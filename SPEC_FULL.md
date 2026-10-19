# Krypto — Product Specification

## 1. Purpose

A single-player, timed, Python implementation of the card game Krypto. 
Each round deals five number cards and a target number from a
standard 56-card Krypto deck. The player combines as many of the five
cards as possible — using addition, subtraction, multiplication,
division, and up to three pairs of parentheses — into an expression that
evaluates exactly to the target. Score for a round equals the number of
hand cards used in an accepted expression (0 for a round ended by Give
Up or Exit). Round time is tracked as an up-counting stopwatch; best
times and lifetime statistics are derived from a saved history of past
rounds.

## 2. Non-Goals

- No multiplayer, no networking, no accounts.
- No countdown timer or time-based auto-fail — the stopwatch never ends 
  a round on its own; only a correct Submit, a confirmed Give Up, or a
  confirmed Exit does.
- No solver — the app never computes, stores, or reveals its own solution
  to a deal.
- No free-typed expression entry — all input is clicks on card/operator/
  parenthesis buttons (§4).
- No web server, no browser dependency.
- No theming/skins, sound, animation, or high-DPI-specific handling.
- No keyboard shortcuts — mouse/click only.
- No in-app auto-update mechanism.

## 3. Packaging & Distribution

- **Goal:** runs standalone with no separate Python installation on the
  end user's machine — double-click and go.
- **OS scope:** both a Linux build and a Windows build are in scope.
- The history file (§6) is located next to wherever the program itself
  is — never a hardcoded location — so the app works no matter where
  it's copied or run from.
- The history file is personal to each install and is never part of the
  distributed source — a fresh install/clone starts with no history.

## 4. Game Rules (Authoritative)

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
- **Valid expressions:** anything that breaks these rules fails on
  Submit as an invalid expression (§5, §7.3).
  - Each hand card is its own number: two cards cannot sit side by side, 
  so cards are never joined into a multi-digit number (a 3 next to a 5 
  cannot be interpreted as 35).
  - An operator must come right after a card or a closing parenthesis, 
  so an expression cannot start with an operator, and an operator cannot
  follow an opening parenthesis or another operator. This means a
  negative number can only come from subtraction (`3-5`), never be
  written directly (`-3`).
  - Parentheses cannot be empty.
- **Intermediate-value legality** this build is *permissive* — negative 
  and non-integer values may occur mid-calculation; only the *final* 
  result must equal the integer target exactly. The stricter official 
  "International Rules" variant (every intermediate value must be a 
  non-negative whole number) is not implemented — see §9.
- **Win condition:** the computed result must equal the target exactly.
  Evaluation must be exact — a mathematically correct solution must never
  be rejected due to rounding/precision error.
- **Scoring (house rule, deliberately overriding official Krypto):**
  official rules require using all 5 cards; this implementation instead
  scores however many of the 5 cards (1–5) were used in a correct
  expression. A confirmed Give Up or Exit scores 0.

## 5. Input Model

- All input is click-driven: the player clicks card, operator (`+ - *
  /`), and parenthesis buttons to build an expression left to right. No
  free typing at any point.
- The expression area itself is display-only and is never clicked, either 
  to add or to remove tokens.
- Each hand card can be placed at most once; placing it disables that
  card's button until it's removed from the expression.
- Two ways to remove tokens from the expression:
  - an Undo button that removes the most-recently-placed token, one at a 
  time, or 
  - a Clear button that wipes the whole expression.
- Up to 3 opening and 3 closing parentheses may be placed (§4).
- The expression area has a fixed maximum length of 15 symbols (5
  numbers + 4 operators + 6 parentheses — the worst case allowed by the
  rules above), rather than growing or scrolling. Once 15 symbols are
  placed, no more symbols can be added until Undo or Clear frees space.
- Submit is always available while a round is in progress, whatever the
  expression looks like; there is no live well-formedness checking as 
  the expression is built. An incomplete or invalid expression simply 
  fails on Submit with an error message — the player can keep adjusting.

## 6. Persistence — History & Stats

- Persistence is a single flat, human-readable history file located in 
  the same folder next to the program itself.
- One entry is recorded in the history file per **concluded** round only:
  - a win, 
  - a confirmed "Give Up", or 
  - a confirmed "Exit" while a round is in progress.
- A failed "Submit" attempt (incorrect result or invalid expression) 
  records nothing, and neither does "Exit" when no round is in progress.
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
|  Krypto                            [How to Play] [Stats] |
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
- The "Stats" and "How to Play" buttons are always visible, but available
  only when no round is in progress (not started, won, or given up), so
  the timer is never running while either window is open. "Stats" opens 
  a separate view (§7.4); "How to Play" opens a separate text window 
  (§7.6, §7.7). Each window is modal: the main window cannot be used 
  until the window is closed with its Close button. There is no 
  pause/resume mechanism.

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
| Submit | Only while in progress; even on an empty expression this fails gracefully, see §5 |
| Give Up | Only while in progress; asks for Yes/No confirmation |
| Start New Game | Only when no round is in progress (not started, won, or given up) — **never** mid-round |
| Stats | Only when no round is in progress (not started, won, or given up) |
| How to Play | Only when no round is in progress (not started, won, or given up) |
| Exit | Always. While a round is in progress: asks for Yes/No confirmation, records a give-up, and closes the GUI. Otherwise: closes the GUI immediately, with no give-up recorded |

- There is deliberately no way to leave a round unrecorded. Since "Start
  New Game" is unavailable during an active round, every round ends in
  exactly one of three ways: a correct "Submit", a confirmed "Give Up", 
  or a confirmed "Exit" (which records a give-up and closes the app).
- Once a round is won or given up, all input controls disable; the
  expression, target, and final time stay on screen exactly as they were
  at that moment, until "Start New Game" is clicked.
- The window's own close button (the X in the title bar) is not a row in
  the table above. It behaves exactly like "Exit" (§7.3).

### 7.3 Submit / Give Up / Exit Behavior

- **Submit:**
  - On success — stop the timer, record a win (§6), show a success 
  message (e.g. "Solved with 4 cards in 42.7s!"). 
  - On failure for wrong result — stay in progress, show an error message 
  that displays the result of their expression to the user, leave the 
  expression and timer untouched so the player can keep adjusting.
  - On failure for invalid expression — stay in progress, show an error
  message, leave the expression and timer untouched so the player can
  keep adjusting.
  
- **Give Up:** asks for Yes/No confirmation. "No" changes nothing. "Yes"
  — stop the timer, record a give-up with a score of 0 (§6), show a
  neutral message but never a correct solution (§2).

- **Exit:**
  - When a round is in progress, it asks for Yes/No confirmation, same 
  as "Give Up". "No" changes nothing. "Yes" — stop the timer, record a 
  give-up with a score of 0 (§6), then close the GUI entirely.
  - When no round is in progress (not started, won, or given up), it 
  just closes the window, with no give-up recorded.
  - The window's own close button (the X in the title bar) behaves 
  exactly like the Exit button in every case above.

### 7.4 "Stats" Behavior

Opened via the "Stats" button, which is available only when no round is 
in progress. Recomputed fresh from the history (§6) every time it's 
opened, not cached separately, so there's no separate state that can 
drift out of sync. 
Shows:
  - a give-up / exit count,
  - a breakdown of wins by cards used (1–5) with count, 
  - games played = total rounds recorded, 
  - average score,
  - average time (for 5-card wins only),
  - best times (for the top 10 5-card wins only). 

### 7.5 "Stats" GUI
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

### 7.6 "How to Play" Text Box Behavior

Opened via the "How to Play" button, in the top bar next to "Stats", 
which is available only when no round is in progress. It appears as a
separate, modal, read-only window containing the rules text and a Close
button. Like the "Stats" window, it can only be open while no round is
running, so it never affects the timer. The text covers the rules of this
version of Krypto, not necessarily how to use the buttons; the layout is 
expected to be largely self-explanatory.

### 7.7 "How to Play" Text Box Display

```
+----------------------------------------------------------+
|                       How to Play                        |
+----------------------------------------------------------+
|  - Each round deals a target number and five hand cards  |
|    (1 to 25) from a 56-card deck.                        |
|  - Combine the hand cards with the aritmetic operators   |
|    (+ - * /) and parentheses to make an expression that  |
|    equals the target exactly.                            |
|  - Each hand card can only be used once. You do not have |
|    to use all five cards. Your score is the number of    |
|    cards you used, from 1 to 5.                          |
|  - Negative and fractional values are allowed in the     |
|    middle of a calculation. Only the final result has    |
|    to equal the target.                                  |
|  - Give Up and Exit end the round with a score of 0.     |
|  - The timer counts up from the moment you click Start   |
|    New Game, and stops when you solve the round or give  |
|    up.                                                   |
+----------------------------------------------------------+
|                        [ Close ]                         |
+----------------------------------------------------------+
```

## 8. Testing Requirements

- At a minimum, tests must at least cover:
  - dealing, 
  - expression evaluation, 
  - persistence/stats logic
  - the GUI itself

## 9. Explicitly Rejected / Considered-and-Discarded Ideas

Recorded so these don't get re-litigated later:

- **CLI program** — rejected for a single Tkinter GUI.
- **Free-typed expression entry** (full text box or per-character boxes) — 
  rejected as the primary mechanism in favor of fully click-driven input, 
  partly because it avoids ever needing to parse or validate arbitrary 
  user-typed text (§5). Not ruled out as a fallback if the click UI proves 
  infeasible.
- **All-5-cards-mandatory scoring** (the official rule) — deliberately
  overridden; this build scores 1–5 cards used, 0 for a give-up / exit (§4).
- **Countdown timer / time-based auto-fail** — rejected; stopwatch only.
- **Computer-generated solution on Give Up** — rejected as too much
  effort; no solution is ever revealed.
- **Multiplayer** — out of scope for this version.
- **Silent mid-round abandon via New Game** — considered and rejected;
  New Game is simply unavailable until the round concludes, removing any
  ambiguity about whether an abandoned round should count as a failure.
- **Unlimited/dynamically growing expression area** — rejected; a fixed
  maximum-length row was chosen instead (§5).
- **Strict "International Rules"** (forbidding fractional/negative
  intermediate results) — not implemented; this build only checks
  the final result against the target.

## 10. Open Questions

- GUI visual polish (colors, fonts, exact sizing) — left to iterate
  against a working prototype.

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
      Submit-success, confirmed Give Up, or confirmed Exit, and never
      auto-fails a round.
- [ ] Give Up requires Yes/No confirmation; declining leaves the round
      untouched; confirming stops the timer, records a 0-score give-up,
      and freezes the screen until "Start New Game" is clicked.
- [ ] While a round is in progress, Exit requires Yes/No confirmation;
      declining leaves the round untouched; confirming stops the timer,
      records a 0-score give-up, and closes the GUI.
- [ ] When no round is in progress, Exit closes the GUI immediately,
      with no give-up recorded.
- [ ] The GUI window's close button behaves identically to Exit, in 
      every round state.
- [ ] Start New Game is unavailable during an active round, and available
      whenever no round is in progress (at launch, and after a round
      concludes).
- [ ] Every concluded round is recorded to history. 
- [ ] The history file is stored alongside the program itself.
- [ ] The Stats view correctly derives totals, the per-cards-used win
      breakdown, and best times solely from the recorded history.
- [ ] The How to Play button opens a read-only window showing the rules
      text from §7.7. It is available only when no round is in progress,
      and the window is modal.
- [ ] The app runs standalone with no separate Python install required.
- [ ] The full automated test suite, including GUI tests, passes.

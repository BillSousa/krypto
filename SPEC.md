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

## 7. GUI Design

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

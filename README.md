## **Krypto**

[![Tests](https://raw.githubusercontent.com/BillSousa/krypto/main/.github/badges/tests-badge.svg)](https://github.com/BillSousa/krypto/actions)
[![Tests](https://raw.githubusercontent.com/BillSousa/krypto/main/.github/badges/coverage-badge.svg)](https://github.com/BillSousa/krypto/actions) 

[![Test Status 315](https://github.com/BillSousa/krypto/actions/workflows/matrix-tests-py315.yml/badge.svg)](https://github.com/BillSousa/krypto/actions/workflows/matrix-tests-py315.yml)
[![Test Status 314](https://github.com/BillSousa/krypto/actions/workflows/matrix-tests-py314.yml/badge.svg)](https://github.com/BillSousa/krypto/actions/workflows/matrix-tests-py314.yml)
[![Test Status 313](https://github.com/BillSousa/krypto/actions/workflows/matrix-tests-py313.yml/badge.svg)](https://github.com/BillSousa/krypto/actions/workflows/matrix-tests-py313.yml)
[![Test Status 312](https://github.com/BillSousa/krypto/actions/workflows/matrix-tests-py312.yml/badge.svg)](https://github.com/BillSousa/krypto/actions/workflows/matrix-tests-py312.yml)
[![Test Status 311](https://github.com/BillSousa/krypto/actions/workflows/matrix-tests-py311.yml/badge.svg)](https://github.com/BillSousa/krypto/actions/workflows/matrix-tests-py311.yml)


### Project Overview
"Krypto" is a digital implementation of the classic mathematics card game. 
This project builds executable programs that can run a Python-based Krypto 
game GUI on Linux and Windows, on your desktop or laptop device (untested 
on tablet).

### How To Download and Install
Windows and Linux: There is no formal "Install" procedure. Simply 
download the Krypto executable, put it in a folder of your choosing on 
your computer, and run the program to play.]
To download the executable, you will need to go to the latest release 
page on the Krypto GitHub repo. https://github.com/BillSousa/krypto/releases/latest \
Once on the Krypto release page: 
- Under the "Assets" heading find the Krypto executables.
  - The Windows executable is krypto-windows.exe.
  - The Linux executable is krypto-linux.
<<<VERIFY ON WINDOWS>>>
- Click the appropriate executable. A window will come up, 
  - select "Save", 
  - another window will come up, 
  - navigate to your desired save location (e.g. Desktop), and 
  - select "Save".

### Technical Considerations 
Windows and Linux: \
The Krypto computer game is able to keep track of the results of previous 
games. This is done via a txt file called "krypto_history.txt" that is 
stored in the same directory as the Krypto executable. When you run the 
Krypto game for the first time a new krypto_history file will automatically 
be generated. If you delete the history file you will lose your previous 
results but the program will recreate the history file the next time you 
run the program. If you move the Krypto executable to a new location that 
does not have a history file, the program will recreate the history file 
the next time you run the program.

### Setting up
Windows:
<<<VERIFY ON WINDOWS>>>
Linux:
After downloading, configure permissions so that the Krypto executable 
can run on your device.
- Right-click the executable and select "Properties". Look for an entry 
called "Executable as Program". Ensure the toggle is turned on. If this 
option does not exist under your "Properties" then disregard this step.
- Open a terminal in the folder where you saved the Krypto executable. 
In the terminal, run `chmod +x krypto-linux`.

### How to Run the Krypto Executable
- Do not double-click the executable.\ <<<WHY NOT>>>
Windows: <<<VERIFY ON WINDOWS>>>
Linux: Right-click, click "Run as a program"

### The Gameplay Interface / How to Play a Game
The Krypto interface is a single simple window.

In the upper right-hand corner are 2 buttons, "Stats" and "How To Play".
- "Stats": This button is only available when a game is not currently 
running and is grayed out during a game. When clicked, a new window pops 
out that summarizes results from previous games. Stats can only be 
calculated when the krypto_history.txt exists and is in the same folder 
as the Krypto executable. See the Technical Consideration section, above. 
If the history file does not exist, placeholder values are displayed in 
the absence of actual numbers.
- "How To Play": This button is only available when a game is not currently 
running and is grayed out during a game. When clicked, a new window pops 
out that provides a brief, non-technical summary of how this version of 
Krypto is played. See the House Krypto Rules section, below, for that 
exact same summary. The technical summary of how this Krypto game is 
played is what you are currently reading.

In the lower left-hand corner are 2 buttons, "Start New Game" and "Exit".
- "Start New Game": This button is only available when a game is not 
currently running and is grayed out during a game. When clicked, the 
play area is activated with a fresh draw from the digital Krypto deck and 
the timer starts counting.
- "Exit": This button is available at all times. When clicked while a 
game is not currently running, the game window is simply closed without 
any change to the krypto_history.txt file. When clicked while a game is 
running, the game is stopped, a score of 0 is recorded to the history 
file, and the game window is closed. The "X" button in the upper right 
of the game window also has the same functionality.

The center of the play area activates when "Start New Game" is clicked. 
- Top-most, the target card is drawn off the top of the digital Krypto 
deck and is displayed to the right of "Target". On the same line to the 
far right, the timer begins to count upward.
- The next line presented in the play area is the "Hand", which is are 
the 5 cards dealt to you from the digital Krypto deck at the start of the 
game.
- Directly below the "Hand" line are the "Ops" characters, which are 
the mathematical operators and parentheses that are used in conjunction 
with the "Hand" cards to build an expression.
- Below the "Ops" operators is "Expr", the real-time display of the 
expression as it is being built by you. **Click (not drag) the number and 
operator symbols to construct a valid expression that evaluates to the 
"Target".** The Krypto program has some understanding of what constitutes 
a valid mathematical expression. It will gray out invalid next characters 
and leave valid characters available as you construct the expression. 
- Finally, directly below the "Expr" row are 4 buttons: "Clear", "Undo", 
"Submit", and "Give Up".
  - If you want to restart your expression from scratch, click "Clear" 
  to wipe the entire expression area in one click.
  - If you want to erase the last character selected, click "Undo".
  - **When you are ready to submit your expression as final, click 
  "Submit". The Krypto program will compute the output of your expression 
  and compare it against the target. If the output of the expression 
  matches the target, the game is ended, a congratulatory message is 
  displayed at the bottom of the play area, the timer is stopped, and 
  the result of the game is logged to the krypto_history.txt file. If 
  the output and the target do not match, the game continues, and a 
  message is shown at the bottom of the play area informing of the error 
  and the actual calculated output of the expression.**

### House Krypto Rules 
**Note:** The exact information below can be found in the built-in Krypto
game instructions. On the Krypto game interface, in the upper right-hand 
corner, locate the "How To Play" button.
- Each round deals a target number and five hand cards (1 to 25) from a 
  56-card deck.
- Combine the hand cards with the arithmetic operators (+ - * /) and
  parentheses to make an expression that equals the target exactly.
- Each hand card can only be used once. You do not have to use all five
  cards. Your score is the number of cards you used, from 1 to 5.
- Negative and fractional values are allowed in the middle of a calculation.
  Only the final result has to equal the target.
- Give Up and Exit end the round with a score of 0.
- The timer counts up from the moment you click Start New Game, and stops 
  when you solve the round or give up.

### Troubleshooting
Windows:
<<< NORTON BLOCKING THE PROGRAM >>>
Linux:
xxx 

### Tips and Pointers
Windows:
xxx
Linux:
xxx

### README Changelog
26_11_15: First release




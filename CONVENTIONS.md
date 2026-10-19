# Krypto — Guidance for Aider and Qwen
This document is to be strictly followed always unless otherwise explicitly  
permitted by the human.

## Project Overview
This project builds 2 fully Python-based executable programs called "Krypto" 
that can run on Linux and Windows. "Krypto" is an implementation of the 
classic mathematics card game of the same name. See SPEC_FULL.md for brief, 
non-exhaustive discussion of the rules of Krypto.

## Other Reference Material
SPEC_FULL.md contains the complete, deliberated product specification. It 
should be treated as authoritative for anything it covers.

## Teamwork Protocol
- Keep responses concise — Be non-verbose and do not use lengthy preambles 
or summaries.
- Do not repeat back large chunks of code unless asked.
- When you are asked to read and understand something, do not provide a 
summary back unless you are explicitly told to do so.

## Context Management
This section provides tips for managing the context window for the AI-assisted 
development workflow.
The realistic context window for the AI coding harness is ~32K tokens because 
the dev hardware is CPU only with 24GB of DRAM. This single constraint shapes 
most of the decisions below.
- Produce small, single-responsibility modules so any one file comfortably 
fits in Aider's context window against the ~32K-token budget.
- Do not tell Aider to save anything to system context or memory unless the 
human tells you to or unless you ask for and explicitly get permission.
- When implementing a module that calls another, add only the signatures and 
docstrings of the dependency to context, not its full body. The model only 
needs the contract to wire a correct call.

## Difficult Tasks
Only try to complete a task twice. If you cannot complete the task after 2 
tries, stop and ask the human for help. Report what you are trying to do, 
what steps you have tried, how those attempts have failed, and ask for help 
instead of hopelessly retrying the same things over and over.

## Python Standards
- Language: Python only.
- Python >=3.11
- Follow PEP8.
- Full type hints on all function and method signatures.
- Docstrings on all classes, methods, and functions (numpydoc style) stating 
purpose, params, return, and raises.
- Consistent naming (`snake_case` for functions, `PascalCase` for classes)
- Max line length: 79 characters, with some latitude when it "makes sense".
- Explicit, straightforward code over compact one-liners.
- Use f-strings, not `.format()` or `%`.
- Prefer `pathlib.Path` over `os.path`.
- When creating classes and functions, put only one class or function in a 
file. Do not put multiple classes and/or functions in a single file.
- Imports: always absolute, anchored at the `krypto` package (e.g. 
`from krypto.build_deck import build_deck`). Never relative imports 
(`from .build_deck import ...`) and never bare imports 
(`from build_deck import ...`). This relies on `krypto` being installed 
into the `.venv` as an editable install via `pyproject.toml`.

## Test
- Only use pytest for testing.
- All tests go in the /tests folder at the project root.
- Mirror the `/src` folder structure inside `/tests`.
- A test file's location should match the source file it tests (e.g. 
`src/krypto/derive_stats.py` → `tests/test_derive_stats.py`).
- Create a test file with thorough tests for every py file that you create. 
This means all functional script as well as supporting classes and functions.

## Environment
- Package manager: `uv` with `pyproject.toml`.
- Virtual environment: `.venv/` in project root.
- NEVER use the system python, only use the .venv in the project root.
- Never use `sudo pip`.
- Update `pyproject.toml` immediately if you make dependency changes.

## Git
- Never commit: `.venv/`, `__pycache__/`, `.env`, `*.pyc`
- Never push directly to main
- When writing commit messages, start the message with the date and time, 
using "YY_MM_DD_hh_mm_ss" format, e.g, "26_07_26_15_58_00 first commit". 
- Do NOT use emojis in commit messages.

## Project change policy
If a program file does not exist and you need to create it, follow this 
procedure:
- Create a *file listing* for it
- Present the *file listing* to the human for review
- If the human approves the *file listing*, then create the file and write 
the code.
But if a program file already exists and you need to edit it, follow this 
procedure:
- Create a *file listing* with the changes you want to make
- Present the *file listing* to the human for review
- If you have received approval from the human, create a backup copy of the 
file to be edited before modifying the original file. Give the backup an 
intuitive name, e.g., if the file is named "_validation.py", then call the 
copy "_validation_backup.py".
- Make the required edits to the original file, not the copy.
- Inform the human that the changes are finished.
Adherence to this policy is subject to the human's discretion. The human 
may, from time to time, at his discretion, give you permission to bypass 
these change policies completely and/or give you permission to make edits 
without making a copy first.

## Maintaining CONVENTIONS.md (this document)
Change rules for CONVENTIONS.md --- Do not modify CONVENTIONS.md unless you 
have explicit approval from the human. If you would like to make changes to 
CONVENTIONS.md, follow this procedure:
- Create a *file listing* with your proposed changes
- Present the *file listing* to the human and explicitly ask for permission 
to make the changes.
- If the human approves any or all of the changes, then modify CONVENTIONS.md 
with only the approved changes.
You do not need to follow the backup copy policy for this file.

## Maintaining SPEC_FULL.md
Change rules for SPEC_FULL.md --- Do not modify SPEC_FULL.md unless you have 
explicit approval from the human. If you would like to make changes to 
SPEC_FULL.md, including in those cases discussed immediately below, then 
follow this procedure:
- Create a *file listing* with your proposed changes
- Present the *file listing* to the human and explicitly ask for permission 
to make the changes.
- If the human approves any or all of the changes, then modify SPEC_FULL.md 
with only the approved changes.
You do not need to follow the backup copy policy for this file.
Causes to change SPEC_FULL.md --- If a design decision changes during 
development (rejected approach, new rule discovered),  
**update SPEC_FULL.md to reflect it**. If something gets tried and discarded, 
add it to the "Explicitly Rejected" SPEC_FULL.md section (§9) so it doesn't 
get re-proposed later. Treat SPEC_FULL.md as a living document, not a 
one-time handoff.

## Maintaining IMPLEMENTATION_FULL.md
Change rules for IMPLEMENTATION_FULL.md --- Do not modify IMPLEMENTATION_FULL.md 
unless you have explicit approval from the human. If you would like to make 
changes to IMPLEMENTATION_FULL.md, including in those cases discussed 
immediately below, then follow this procedure:
- Create a *file listing* with your proposed changes
- Present the *file listing* to the human and explicitly ask for permission 
to make the changes.
- If the human approves any or all of the changes, then modify IMPLEMENTATION_FULL.md 
with only the approved changes.
You do not need to follow the backup copy policy for this file.
Causes to change IMPLEMENTATION_FULL.md --- If an implementation detail changes 
during development (rejected approach, new rule discovered), 
**update IMPLEMENTATION_FULL.md to reflect it**. Treat IMPLEMENTATION_FULL.md 
as a living document, not a one-time handoff.


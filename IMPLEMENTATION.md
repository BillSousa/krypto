# Krypto — Python Implementation Notes

Companion to `SPEC.md`. `SPEC.md` defines what the game does and how it
behaves; this file covers how it gets built.

## Minimum Supported Python Version
>=3.11

## Module Strategy
Small, single-responsibility modules. One function or class per file.
Test files should mirror source files 1:1.

## Packaging
- Packaging: PyInstaller, producing a Windows `.exe` and a Linux binary
  (built on Linux), both reading the same history file from a shared folder.

## Project layout
```
src/
  krypto/
    __init__.py
    build_deck.py
    deal.py
    build_expr_string.py
    is_valid_expr_str.py
    evaluate.py
    get_history_path.py
    append_result.py
    load_history.py
    derive_stats.py
    derive_best_times.py
    get_available_controls.py
    gui.py
    stats_window.py
    main.py
tests/
  test_build_deck.py
  test_deal.py
  test_build_expr_string.py
  test_is_valid_expr_str.py
  test_evaluate.py
  test_get_history_path.py
  test_append_result.py
  test_load_history.py
  test_derive_stats.py
  test_derive_best_times.py
  test_get_available_controls.py
  test_gui.py
  test_stats_window.py
  test_main.py
  test_integration_append_load.py
  test_integration_deal_build_evaluate.py
  test_integration_load_derive.py
```

## Module Breakdown
Each file below holds exactly one function (or, for `gui.py` and
`stats_window.py`, one class). All function modules are stateless
functions — no classes.

### build_deck.py
See /implementation/build_deck.md

### deal.py
See /implementation/deal.md

### build_expr_string.py
See /implementation/build_expr_string.md

### is_valid_expr_str.py
See /implementation/is_valid_expr_str.md

### evaluate.py
See /implementation/evaluate.md

### get_history_path.py
See /implementation/get_history_path.md

### append_result.py
See /implementation/append_result.md

### load_history.py
See /implementation/load_history.md

### derive_stats.py
See /implementation/derive_stats.md

### derive_best_times.py
See /implementation/derive_best_times.md

### get_available_controls.py
See /implementation/get_available_controls.md

### gui.py
See /implementation/gui.md

### stats_window.py
See /implementation/stats_window.md

### main.py
See /implementation/main.md

## Testing & CI
- `pytest` across all modules.

### test_build_deck.py
See /implementation/test_build_deck.md

### test_deal.py
See /implementation/test_deal.md

### test_build_expr_string.py
See /implementation/test_build_expr_string.md

### test_is_valid_expr_str.py
See /implementation/test_is_valid_expr_str.md

### test_evaluate.py
See /implementation/test_evaluate.md

### test_get_history_path.py
See /implementation/test_get_history_path.md

### test_append_result.py
See /implementation/test_append_result.md

### test_load_history.py
See /implementation/test_load_history.md

### test_derive_stats.py
See /implementation/test_derive_stats.md

### test_derive_best_times.py
See /implementation/test_derive_best_times.md

### test_get_available_controls.py
See /implementation/test_get_available_controls.md

### test_gui.py
See /implementation/test_gui.md

### test_stats_window.py
See /implementation/test_stats_window.md

### test_main.py
See /implementation/test_main.md

### test_integration_append_load.py
See /implementation/test_integration_append_load.md

### test_integration_deal_build_evaluate.py
See /implementation/test_integration_deal_build_evaluate.md

### test_integration_load_derive.py
See /implementation/test_integration_load_derive.md



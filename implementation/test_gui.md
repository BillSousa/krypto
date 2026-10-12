GUI tests run headless via a virtual display in CI, e.g.:
```
xvfb-run -a uv run pytest tests/ --doctest-modules -v --maxfail=1 --disable-warnings
```
```
<<<pytest>>>
```

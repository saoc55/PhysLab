# PhysLab

Classical physics simulator and learning tool. Python standard library + tkinter, no physics libraries.

Requirements, class specs and acceptance criteria live in the "PhysLab: Requirements & Build Guide" doc.

## Setup (Windows)

```
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Run

```
python -m physlab
pytest -q
```

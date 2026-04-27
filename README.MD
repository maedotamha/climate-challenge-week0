# climate-challenge-week0

Starter setup for the Climate Challenge Week 0 tasks.

## 1) Clone repository

```bash
git clone <your-repo-url>
cd climate-challenge-week0
```

## 2) Create and activate virtual environment (venv)

### Windows (PowerShell)

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3) Install dependencies

```bash
pip install -r requirements.txt
```

## 4) Run a quick check

```bash
python --version
```

## 5) Expected project structure

```text
.vscode/
.github/workflows/
notebooks/
scripts/
src/
tests/
.gitignore
README.MD
requirements.txt
```

## Notes

- CI workflow at `.github/workflows/ci.yml` runs on pushes and pull requests targeting `main`.
- `data/`, `.csv` files, and `.ipynb_checkpoints/` are ignored by git.

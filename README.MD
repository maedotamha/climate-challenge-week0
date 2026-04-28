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

## Bonus: Streamlit Dashboard

### Development process

- Built a lightweight Streamlit app in `app/main.py` and helper functions in `app/utils.py`.
- Added interactive controls for country filtering, year-range filtering, and variable selection.
- Added two core visualizations:
  - Monthly trend line chart (selected variable by country)
  - Precipitation distribution boxplot (`PRECTOTCORR`) by country
- The app reads local CSVs from `data/` and supports both raw (`<country>.csv`) and cleaned (`<country>_clean.csv`) files.

### Run locally

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

### Streamlit Community Cloud deployment

1. Push the repository to GitHub (without committing data files).
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create a new app and connect your GitHub repository.
4. Set the entrypoint to `app/main.py`.
5. Deploy and verify selectors/charts render correctly.

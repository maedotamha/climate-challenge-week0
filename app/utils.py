from pathlib import Path

import numpy as np
import pandas as pd


COUNTRIES = ["ethiopia", "kenya", "sudan", "tanzania", "nigeria"]


def parse_nasa_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    elif {"YEAR", "DOY"}.issubset(df.columns):
        df["Date"] = pd.to_datetime(
            df["YEAR"] * 1000 + df["DOY"],
            format="%Y%j",
            errors="coerce",
        )
    else:
        raise ValueError("Missing required date fields: Date or YEAR+DOY.")
    df["Year"] = df["Date"].dt.year
    return df


def basic_clean(df: pd.DataFrame, country_name: str) -> pd.DataFrame:
    df = df.copy()
    df["Country"] = country_name.title()
    df = df.replace(-999, np.nan)
    df = parse_nasa_dates(df)
    df = df.drop_duplicates()
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def load_country_data(data_dir: Path, country: str) -> pd.DataFrame:
    clean_path = data_dir / f"{country}_clean.csv"
    raw_path = data_dir / f"{country}.csv"

    if clean_path.exists():
        df = pd.read_csv(clean_path)
    elif raw_path.exists():
        df = pd.read_csv(raw_path)
    else:
        raise FileNotFoundError(f"No CSV found for country: {country}")

    return basic_clean(df, country)


def load_all_countries(data_dir: Path, countries: list[str]) -> pd.DataFrame:
    frames = []
    for country in countries:
        frames.append(load_country_data(data_dir, country))
    df_all = pd.concat(frames, ignore_index=True)
    return df_all

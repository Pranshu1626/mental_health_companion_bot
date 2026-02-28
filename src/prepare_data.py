import pandas as pd
import os

RAW_PATH = "data/raw"
OUT_PATH = "data/processed/dataset.csv"

def merge_datasets():
    files = [
        "goemotions_1.csv",
        "goemotions_2.csv",
        "goemotions_3.csv"
    ]

    dfs = []

    for f in files:
        path = os.path.join(RAW_PATH, f)
        df = pd.read_csv(path)
        dfs.append(df)

    merged = pd.concat(dfs, ignore_index=True)

    os.makedirs("data/processed", exist_ok=True)
    merged.to_csv(OUT_PATH, index=False)

    print("Merged dataset saved:", merged.shape)
    
    emotion_cols = merged.columns[9:]

    merged["label"] = merged[emotion_cols].idxmax(axis=1)

    final = merged[["text", "label"]]

    final.to_csv(OUT_PATH, index=False)
    print("Final dataset saved:", final.shape)

if __name__ == "__main__":
    merge_datasets()

    
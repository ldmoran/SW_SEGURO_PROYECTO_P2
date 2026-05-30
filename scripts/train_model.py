import argparse
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

from feature_extraction import extract_features


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, help="CSV with columns: code,label")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.dataset)
    if "code" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset must contain code and label columns")

    codes = df["code"].astype(str).tolist()
    feature_rows = [extract_features(code) for code in codes]
    feature_names = list(feature_rows[0].keys()) if feature_rows else []
    numeric = np.array([[row[k] for k in feature_names] for row in feature_rows], dtype=float)
    y = df["label"].astype(int).to_numpy()

    vectorizer = TfidfVectorizer(
        token_pattern=r"[A-Za-z_][A-Za-z0-9_]*",
        ngram_range=(1, 2),
        min_df=2,
        max_features=8000,
    )
    X_text = vectorizer.fit_transform(codes)
    X_num = csr_matrix(numeric)
    X = hstack([X_text, X_num], format="csr")

    model = LogisticRegression(max_iter=2000, class_weight="balanced")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    print(f"Accuracy CV mean: {scores.mean():.4f}")

    model.fit(X, y)
    joblib.dump(
        {"model": model, "feature_names": feature_names, "vectorizer": vectorizer},
        args.out,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

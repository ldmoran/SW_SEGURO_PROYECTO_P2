import argparse
import json
import os
import subprocess
from typing import List

import joblib
import numpy as np
from scipy.sparse import csr_matrix, hstack

from feature_extraction import extract_features, pick_vuln_type


def _run_git(args: List[str], repo: str) -> str:
    result = subprocess.run(
        ["git"] + args,
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def _changed_files(base: str, head: str, repo: str) -> List[str]:
    out = _run_git(["diff", "--name-only", f"{base}..{head}"], repo)
    files = [line.strip() for line in out.splitlines() if line.strip()]
    return [f for f in files if f.endswith(".java")]


def _file_content_at(ref: str, path: str, repo: str) -> str:
    return _run_git(["show", f"{ref}:{path}"], repo)


def _numeric_features(code: str) -> np.ndarray:
    features = extract_features(code)
    keys = list(features.keys())
    return np.array([features[k] for k in keys], dtype=float), keys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--threshold", type=float, default=float(os.getenv("MODEL_THRESHOLD", "0.5")))
    args = parser.parse_args()

    if not os.path.exists(args.model):
        raise FileNotFoundError(f"Model not found: {args.model}")

    files = _changed_files(args.base, args.head, args.repo)
    codes = [_file_content_at(args.head, path, args.repo) for path in files]

    if not codes:
        report = {
            "label": "SEGURO",
            "probability": 0.0,
            "details": "Sin archivos Java modificados.",
            "vuln_type": "none",
        }
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f)
        return 0

    data = joblib.load(args.model)
    model = data["model"] if isinstance(data, dict) else data
    vectorizer = data.get("vectorizer") if isinstance(data, dict) else None

    combined_code = "\n".join(codes)
    numeric, _ = _numeric_features(combined_code)

    if vectorizer is not None:
        X_text = vectorizer.transform([combined_code])
        X_num = csr_matrix(numeric.reshape(1, -1))
        features = hstack([X_text, X_num], format="csr")
    else:
        features = numeric.reshape(1, -1)

    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(features)[0][1])
    else:
        prob = float(model.predict(features)[0])

    label = "VULNERABLE" if prob >= args.threshold else "SEGURO"
    feature_map = extract_features("\n".join(codes))
    vuln_type = pick_vuln_type(feature_map)

    report = {
        "label": label,
        "probability": round(prob, 4),
        "details": f"Archivos analizados: {len(files)}. Tipo estimado: {vuln_type}.",
        "vuln_type": vuln_type,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

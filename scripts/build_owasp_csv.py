import argparse
import csv
from pathlib import Path


def load_expected_results(csv_path: Path) -> dict:
    mapping = {}
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            test_name = row[0].strip()
            is_vuln = row[2].strip().lower() == "true"
            mapping[test_name] = 1 if is_vuln else 0
    return mapping


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", required=True, help="Ruta a BenchmarkJava-master")
    parser.add_argument("--out", required=True, help="Ruta CSV salida")
    args = parser.parse_args()

    root = Path(args.benchmark)
    expected_csv = root / "expectedresults-1.2.csv"
    test_dir = root / "src" / "main" / "java" / "org" / "owasp" / "benchmark" / "testcode"

    if not expected_csv.exists():
        raise FileNotFoundError(f"No existe: {expected_csv}")
    if not test_dir.exists():
        raise FileNotFoundError(f"No existe: {test_dir}")

    mapping = load_expected_results(expected_csv)

    rows = []
    for java_file in sorted(test_dir.glob("BenchmarkTest*.java")):
        name = java_file.stem
        label = mapping.get(name)
        if label is None:
            continue
        code = java_file.read_text(encoding="utf-8", errors="ignore")
        rows.append({"code": code, "label": label})

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["code", "label"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV generado: {out_path} ({len(rows)} filas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

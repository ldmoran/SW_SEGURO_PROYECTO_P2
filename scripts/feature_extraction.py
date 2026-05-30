import os
import re
from typing import Dict, List

import javalang

DANGEROUS_PATTERNS: Dict[str, List[str]] = {
    "command_injection": [
        r"Runtime\.getRuntime\(\)\.exec",
        r"new\s+ProcessBuilder",
        r"ProcessBuilder\(",
        r"\.exec\(",
    ],
    "sql_injection": [
        r"createStatement\(",
        r"Statement\.execute",
        r"executeQuery\(",
        r"executeUpdate\(",
    ],
    "deserialization": [
        r"ObjectInputStream",
        r"readObject\(",
    ],
}

SANITIZATION_PATTERNS: List[str] = [
    r"PreparedStatement",
    r"setString\(",
    r"setInt\(",
    r"sanitize",
    r"escapeHtml",
    r"encodeForHTML",
    r"ESAPI\.encoder",
]

TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _max_ast_depth(code: str) -> int:
    if os.getenv("DISABLE_AST", "0") == "1":
        return 0
    try:
        tree = javalang.parse.parse(code)
    except (javalang.parser.JavaSyntaxError, IndexError, TypeError):
        return 0

    max_depth = 0
    stack = [(tree, 1)]
    while stack:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)
        for _, child in node:
            if child is not None:
                stack.append((child, depth + 1))
    return max_depth


def _count_patterns(code: str, patterns: List[str]) -> int:
    return sum(len(re.findall(p, code)) for p in patterns)


def extract_features(code: str) -> Dict[str, float]:
    tokens = TOKEN_RE.findall(code)
    token_count = len(tokens)
    unique_token_count = len(set(tokens))
    avg_token_length = sum(len(t) for t in tokens) / token_count if token_count else 0.0

    dangerous_counts = {
        name: _count_patterns(code, patterns) for name, patterns in DANGEROUS_PATTERNS.items()
    }
    dangerous_total = sum(dangerous_counts.values())
    sanitization_count = _count_patterns(code, SANITIZATION_PATTERNS)

    return {
        "token_count": float(token_count),
        "unique_token_count": float(unique_token_count),
        "avg_token_length": float(avg_token_length),
        "ast_max_depth": float(_max_ast_depth(code)),
        "dangerous_total": float(dangerous_total),
        "sanitization_count": float(sanitization_count),
        "dangerous_to_sanitization": float(dangerous_total) / float(sanitization_count + 1),
        "command_injection_hits": float(dangerous_counts.get("command_injection", 0)),
        "sql_injection_hits": float(dangerous_counts.get("sql_injection", 0)),
        "deserialization_hits": float(dangerous_counts.get("deserialization", 0)),
    }


def pick_vuln_type(features: Dict[str, float]) -> str:
    candidates = {
        "command_injection": features.get("command_injection_hits", 0.0),
        "sql_injection": features.get("sql_injection_hits", 0.0),
        "deserialization": features.get("deserialization_hits", 0.0),
    }
    vuln = max(candidates, key=candidates.get)
    return vuln if candidates[vuln] > 0 else "unknown"

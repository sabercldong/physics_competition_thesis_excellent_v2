from __future__ import annotations

import argparse
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "04_framework/pilot_coding.csv"
DEFAULT_OUTPUT = ROOT / "07_analysis/results/generated/reliability_by_dimension.csv"
DEFAULT_DISAGREEMENTS = ROOT / "07_analysis/results/generated/reliability_disagreements.csv"


def _resolve(path_text: str | None, default: Path) -> Path:
    if not path_text:
        return default
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def _normalise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Support both formal coding and round-template style column names."""
    rename = {}
    if "coder" not in df.columns and "rater_id" in df.columns:
        rename["rater_id"] = "coder"
    if "present" not in df.columns and "present_yes_no" in df.columns:
        rename["present_yes_no"] = "present"
    if "level" not in df.columns and "level_if_present" in df.columns:
        rename["level_if_present"] = "level"
    out = df.rename(columns=rename).copy()
    if "sample_id" not in out.columns:
        out["sample_id"] = ""
    return out


def _normalise_present(value: object) -> str:
    text = str(value).strip()
    if text in {"1", "True", "true", "yes", "Yes", "Y", "y", "是"}:
        return "是"
    if text in {"0", "False", "false", "no", "No", "N", "n", "否", "未出现"}:
        return "否"
    return text


def _normalise_level(value: object, present: str) -> str:
    if present == "否":
        return "未出现"
    text = str(value).strip()
    return text if text and text.lower() != "nan" else "未定"


def _cohen_kappa(a: pd.Series, b: pd.Series, labels: list[str], weights: str | None = None) -> float:
    pairs = [(x, y) for x, y in zip(a.tolist(), b.tolist(), strict=False) if x in labels and y in labels]
    n = len(pairs)
    if n == 0:
        return float("nan")
    label_index = {label: i for i, label in enumerate(labels)}
    if weights == "quadratic":
        denominator = (len(labels) - 1) ** 2
        if denominator == 0:
            return 1.0

        def weight(x: str, y: str) -> float:
            return ((label_index[x] - label_index[y]) ** 2) / denominator

        observed = sum(weight(x, y) for x, y in pairs) / n
        counts_a = {label: sum(x == label for x, _ in pairs) for label in labels}
        counts_b = {label: sum(y == label for _, y in pairs) for label in labels}
        expected = 0.0
        for x in labels:
            for y in labels:
                expected += (counts_a[x] / n) * (counts_b[y] / n) * weight(x, y)
        return 1 - observed / expected if expected else 1.0

    observed = sum(x == y for x, y in pairs) / n
    counts_a = {label: sum(x == label for x, _ in pairs) for label in labels}
    counts_b = {label: sum(y == label for _, y in pairs) for label in labels}
    expected = sum((counts_a[label] / n) * (counts_b[label] / n) for label in labels)
    if math.isclose(1 - expected, 0.0):
        return 1.0
    return (observed - expected) / (1 - expected)


def _metric_rows(df: pd.DataFrame, coders: list[str]) -> list[dict[str, object]]:
    rows = []
    dimensions = ["全部"] + sorted(df["dimension"].dropna().unique().tolist())
    for dim in dimensions:
        sub = df if dim == "全部" else df[df["dimension"] == dim]
        wide_p = sub.pivot_table(
            index=["sample_id", "item_id", "dimension"],
            columns="coder",
            values="present",
            aggfunc="first",
        ).dropna(subset=coders)
        if len(wide_p):
            present_agreement = (wide_p[coders[0]] == wide_p[coders[1]]).mean()
            present_kappa = _cohen_kappa(wide_p[coders[0]], wide_p[coders[1]], labels=["否", "是"])
        else:
            present_agreement = float("nan")
            present_kappa = float("nan")

        both_present_index = wide_p[(wide_p[coders[0]] == "是") & (wide_p[coders[1]] == "是")].index
        wide_l = sub.pivot_table(
            index=["sample_id", "item_id", "dimension"],
            columns="coder",
            values="level",
            aggfunc="first",
        ).reindex(both_present_index).dropna(subset=coders)
        if len(wide_l):
            level_agreement = (wide_l[coders[0]] == wide_l[coders[1]]).mean()
            weighted_kappa = _cohen_kappa(
                wide_l[coders[0]],
                wide_l[coders[1]],
                labels=["L1", "L2", "L3", "L4"],
                weights="quadratic",
            )
        else:
            level_agreement = float("nan")
            weighted_kappa = float("nan")

        rows.append(
            {
                "dimension": dim,
                "n_presence_pairs": len(wide_p),
                "presence_agreement": present_agreement,
                "presence_kappa": present_kappa,
                "n_level_pairs_both_present": len(wide_l),
                "level_agreement": level_agreement,
                "weighted_kappa_level": weighted_kappa,
            }
        )
    return rows


def _disagreement_rows(df: pd.DataFrame, coders: list[str]) -> list[dict[str, object]]:
    rows = []
    wide = df.pivot_table(
        index=["sample_id", "item_id", "dimension"],
        columns="coder",
        values=["present", "level", "evidence"],
        aggfunc="first",
    )
    for key, row in wide.iterrows():
        sample_id, item_id, dimension = key
        try:
            p_a = row[("present", coders[0])]
            p_b = row[("present", coders[1])]
            l_a = row[("level", coders[0])]
            l_b = row[("level", coders[1])]
        except KeyError:
            continue
        types = []
        if pd.notna(p_a) and pd.notna(p_b) and p_a != p_b:
            types.append("维度存在性")
        if p_a == "是" and p_b == "是" and pd.notna(l_a) and pd.notna(l_b) and l_a != l_b:
            types.append("等级")
        if not types:
            continue
        rows.append(
            {
                "sample_id": sample_id,
                "item_id": item_id,
                "dimension": dimension,
                "disagreement_type": "；".join(types),
                f"{coders[0]}_present": p_a,
                f"{coders[0]}_level": l_a,
                f"{coders[1]}_present": p_b,
                f"{coders[1]}_level": l_b,
                f"{coders[0]}_evidence": row.get(("evidence", coders[0]), ""),
                f"{coders[1]}_evidence": row.get(("evidence", coders[1]), ""),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="计算两名评分者的试编码一致性。")
    parser.add_argument("--input", help="输入CSV，默认读取04_framework/pilot_coding.csv。")
    parser.add_argument("--output", help="一致性统计输出CSV。")
    parser.add_argument("--disagreements", help="分歧明细输出CSV。")
    parser.add_argument("--allow-simulated", action="store_true", help="允许处理Codex模拟评分者数据，并在控制台标注边界。")
    args = parser.parse_args()

    input_path = _resolve(args.input, DEFAULT_INPUT)
    output_path = _resolve(args.output, DEFAULT_OUTPUT)
    disagreement_path = _resolve(args.disagreements, DEFAULT_DISAGREEMENTS)

    if not input_path.exists():
        print(f"输入文件不存在：{input_path}")
        return

    df = _normalise_columns(pd.read_csv(input_path))
    if df.empty:
        print(f"{input_path} 为空，未计算一致性。")
        return

    required = {"item_id", "coder", "dimension", "present", "level"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"缺少字段: {sorted(missing)}")

    df["present"] = df["present"].map(_normalise_present)
    df["level"] = [
        _normalise_level(level, present) for level, present in zip(df["level"], df["present"], strict=False)
    ]

    coders = sorted(df["coder"].dropna().unique().tolist())
    if len(coders) != 2:
        raise ValueError(f"当前脚本要求恰好两名评分者，实际为 {len(coders)} 名：{coders}")

    if any(str(coder).startswith("Codex-Sim") for coder in coders) and not args.allow_simulated:
        raise ValueError("检测到Codex模拟评分者数据。若仅用于压力测试，请加 --allow-simulated。")

    metrics = pd.DataFrame(_metric_rows(df, coders))
    disagreements = pd.DataFrame(_disagreement_rows(df, coders))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    disagreement_path.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output_path, index=False, encoding="utf-8-sig")
    disagreements.to_csv(disagreement_path, index=False, encoding="utf-8-sig")

    print(f"已生成一致性统计：{output_path}")
    print(f"已生成分歧明细：{disagreement_path}")
    if args.allow_simulated:
        print("注意：本次输入允许Codex模拟评分者数据，只能用于流程压力测试，不能作为正式一致性结果。")


if __name__ == "__main__":
    main()

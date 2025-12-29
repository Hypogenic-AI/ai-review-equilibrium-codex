"""Analyze review disagreement and revision improvements."""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = WORKSPACE_ROOT / "results"
MODEL_OUTPUTS_DIR = RESULTS_DIR / "model_outputs"
ANALYSIS_DIR = RESULTS_DIR / "analysis"
PLOTS_DIR = RESULTS_DIR / "plots"
CONFIG_PATH = RESULTS_DIR / "config.json"

REVIEWS_PATH = MODEL_OUTPUTS_DIR / "reviews.jsonl"
REVISIONS_PATH = MODEL_OUTPUTS_DIR / "revisions.jsonl"
JUDGMENTS_PATH = MODEL_OUTPUTS_DIR / "judgments.jsonl"
SAMPLES_PATH = RESULTS_DIR / "sample_papers.jsonl"


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def dedupe(rows: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
    seen = {}
    for row in rows:
        key = tuple(row.get(k) for k in keys)
        seen[key] = row
    return list(seen.values())


def to_int(value: Any) -> float:
    if value is None:
        return float("nan")
    if isinstance(value, (int, float)):
        return float(value)
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    return float(digits) if digits else float("nan")


def main() -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    samples = read_jsonl(SAMPLES_PATH)
    reviews = dedupe(read_jsonl(REVIEWS_PATH), ["paper_id", "model"])
    revisions = dedupe(read_jsonl(REVISIONS_PATH), ["paper_id", "condition"])
    judgments = dedupe(read_jsonl(JUDGMENTS_PATH), ["paper_id", "variant"])

    sample_df = pd.DataFrame(samples)
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8")) if CONFIG_PATH.exists() else {}
    reviewer_models = config.get("reviewer_models")
    review_df = pd.DataFrame(reviews)
    if reviewer_models:
        review_df = review_df[review_df["model"].isin(reviewer_models)]
    review_df["score"] = review_df["response"].apply(lambda r: to_int(r.get("score")))

    # Review disagreement metrics
    disagreement_rows = []
    similarity_rows = []
    for paper in samples:
        paper_id = paper["paper_id"]
        paper_reviews = review_df[review_df["paper_id"] == paper_id]
        scores = paper_reviews["score"].dropna().tolist()
        if scores:
            disagreement_rows.append(
                {
                    "paper_id": paper_id,
                    "score_variance": float(np.var(scores, ddof=1)) if len(scores) > 1 else 0.0,
                    "score_mean": float(np.mean(scores)),
                }
            )

        # Suggestions similarity
        suggestion_texts = []
        models = []
        for _, row in paper_reviews.iterrows():
            suggestions = row["response"].get("suggestions", [])
            if isinstance(suggestions, list):
                text = " ".join(suggestions)
            else:
                text = str(suggestions)
            suggestion_texts.append(text)
            models.append(row["model"])

        if len(suggestion_texts) >= 2:
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf = vectorizer.fit_transform(suggestion_texts)
            sim_matrix = cosine_similarity(tfidf)
            pair_sims = []
            for (i, j) in combinations(range(len(models)), 2):
                pair_sims.append(sim_matrix[i, j])
                similarity_rows.append(
                    {
                        "paper_id": paper_id,
                        "model_a": models[i],
                        "model_b": models[j],
                        "similarity": float(sim_matrix[i, j]),
                    }
                )

            if pair_sims:
                disagreement_rows[-1]["suggestion_similarity_mean"] = float(
                    np.mean(pair_sims)
                )

    disagreement_df = pd.DataFrame(disagreement_rows)

    # Revision quality improvements
    judgment_df = pd.DataFrame(judgments)
    for metric in ["clarity", "novelty", "overall"]:
        judgment_df[metric] = judgment_df["response"].apply(lambda r: to_int(r.get(metric)))

    pivot = judgment_df.pivot(index="paper_id", columns="variant", values=["clarity", "novelty", "overall"])
    pivot.columns = [f"{metric}_{variant}" for metric, variant in pivot.columns]
    pivot = pivot.reset_index()

    for metric in ["clarity", "novelty", "overall"]:
        pivot[f"delta_{metric}_single"] = pivot[f"{metric}_single"] - pivot[f"{metric}_original"]
        pivot[f"delta_{metric}_multi"] = pivot[f"{metric}_multi"] - pivot[f"{metric}_original"]

    stats_rows = []
    for metric in ["clarity", "novelty", "overall"]:
        delta_single = pivot[f"delta_{metric}_single"].dropna()
        delta_multi = pivot[f"delta_{metric}_multi"].dropna()
        t_stat, p_val = stats.ttest_rel(delta_single, delta_multi)
        diff = delta_multi.values - delta_single.values
        cohen_d = float(np.mean(diff) / np.std(diff, ddof=1)) if len(diff) > 1 else float("nan")
        stats_rows.append(
            {
                "metric": metric,
                "mean_delta_single": float(np.mean(delta_single)),
                "mean_delta_multi": float(np.mean(delta_multi)),
                "t_stat": float(t_stat),
                "p_value": float(p_val),
                "cohen_d": cohen_d,
            }
        )

    stats_df = pd.DataFrame(stats_rows)

    # Save metrics
    data_quality = {
        "sample_size": int(sample_df.shape[0]),
        "missing_title": int(sample_df["title"].isna().sum()),
        "missing_abstract": int(sample_df["abstract"].isna().sum()),
        "missing_decision": int(sample_df["decision"].isna().sum()),
        "decision_counts": sample_df["decision"].value_counts().to_dict(),
        "year_counts": sample_df["year"].value_counts().to_dict(),
    }

    metrics = {
        "data_quality": data_quality,
        "review_disagreement": disagreement_df.describe().to_dict(),
        "suggestion_similarity": pd.DataFrame(similarity_rows).describe().to_dict(),
        "improvement_stats": stats_rows,
    }
    (ANALYSIS_DIR / "metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )

    # Plots
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(8, 4))
    sns.boxplot(data=review_df, x="model", y="score")
    plt.title("Review Score Distribution by Model")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "review_scores_by_model.png")
    plt.close()

    if not disagreement_df.empty and "suggestion_similarity_mean" in disagreement_df:
        plt.figure(figsize=(6, 4))
        sns.histplot(disagreement_df["suggestion_similarity_mean"].dropna(), bins=15, kde=True)
        plt.title("Mean Suggestion Similarity Across Models")
        plt.xlabel("Cosine Similarity")
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "suggestion_similarity.png")
        plt.close()

    delta_long = pivot.melt(
        id_vars="paper_id",
        value_vars=[
            "delta_clarity_single",
            "delta_clarity_multi",
            "delta_novelty_single",
            "delta_novelty_multi",
            "delta_overall_single",
            "delta_overall_multi",
        ],
        var_name="metric",
        value_name="delta",
    )
    plt.figure(figsize=(8, 4))
    sns.barplot(data=delta_long, x="metric", y="delta", errorbar="se")
    plt.title("Average Quality Improvement (Delta)")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "quality_improvements.png")
    plt.close()

    # Save summary tables
    disagreement_df.to_csv(ANALYSIS_DIR / "review_disagreement.csv", index=False)
    stats_df.to_csv(ANALYSIS_DIR / "improvement_stats.csv", index=False)


if __name__ == "__main__":
    main()

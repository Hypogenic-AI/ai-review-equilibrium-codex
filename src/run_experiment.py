"""Run review, revision, and judging experiments with real LLMs."""
from __future__ import annotations

import json
import os
import random
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np
from datasets import load_from_disk

from llm_client import chat_completion, extract_json

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = WORKSPACE_ROOT / "results"
MODEL_OUTPUTS_DIR = RESULTS_DIR / "model_outputs"

REVIEWS_PATH = MODEL_OUTPUTS_DIR / "reviews.jsonl"
REVISIONS_PATH = MODEL_OUTPUTS_DIR / "revisions.jsonl"
JUDGMENTS_PATH = MODEL_OUTPUTS_DIR / "judgments.jsonl"
SAMPLES_PATH = RESULTS_DIR / "sample_papers.jsonl"
CONFIG_PATH = RESULTS_DIR / "config.json"

REVIEWER_MODELS = [
    "anthropic/claude-sonnet-4.5",
    "openai/gpt-4.1",
]
SINGLE_REVIEWER = "anthropic/claude-sonnet-4.5"
AUTHOR_MODEL = "openai/gpt-4.1"
JUDGE_MODEL = "openai/gpt-4.1-mini"

SAMPLE_SIZE = 50
SEED = 42


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def append_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")


def build_review_prompt(title: str, abstract: str) -> List[Dict[str, str]]:
    system = (
        "You are a rigorous ICLR reviewer. Provide concise, concrete feedback. "
        "Respond in JSON with keys: score (1-10 integer), strengths (list), "
        "weaknesses (list), suggestions (list), summary (string)."
    )
    user = (
        f"Title: {title}\n\nAbstract: {abstract}\n\n"
        "Return only JSON."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def build_revision_prompt(title: str, abstract: str, feedback: str) -> List[Dict[str, str]]:
    system = (
        "You are the paper's author revising the abstract. "
        "Improve clarity, novelty framing, and technical precision while staying "
        "faithful to the original claims. Keep length similar (150-250 words). "
        "Respond in JSON with keys: revised_abstract (string), change_log (list)."
    )
    user = (
        f"Title: {title}\n\nOriginal Abstract: {abstract}\n\n"
        f"Reviewer Feedback:\n{feedback}\n\nReturn only JSON."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def build_judge_prompt(title: str, abstract: str) -> List[Dict[str, str]]:
    system = (
        "You are a meta-reviewer scoring paper abstracts. "
        "Rate the abstract on clarity, novelty, and overall quality, each 1-10. "
        "Provide a brief justification. Respond in JSON with keys: clarity, "
        "novelty, overall, justification."
    )
    user = (
        f"Title: {title}\n\nAbstract: {abstract}\n\nReturn only JSON."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def call_json(
    model: str,
    messages: List[Dict[str, str]],
    temperature: float,
    max_tokens: int,
) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
    content, usage = chat_completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )
    try:
        parsed = extract_json(content)
        return parsed, content, usage
    except Exception:
        repair_messages = [
            {
                "role": "system",
                "content": "You are a JSON repair tool. Return valid JSON only.",
            },
            {"role": "user", "content": f"Fix to valid JSON: {content}"},
        ]
        repair_content, repair_usage = chat_completion(
            model=model,
            messages=repair_messages,
            temperature=0.0,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
        )
        try:
            parsed = extract_json(repair_content)
        except Exception:
            parsed = {
                "parse_error": True,
                "raw": repair_content or content,
            }
        merged_usage = {}
        for key in set(usage) | set(repair_usage):
            merged_usage[key] = (usage.get(key) or 0) + (repair_usage.get(key) or 0)
        return parsed, repair_content, merged_usage


def main() -> None:
    set_seed(SEED)
    MODEL_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_from_disk("datasets/openreview_iclr_peer_reviews")["raw"]
    indices = list(range(len(dataset)))
    random.shuffle(indices)
    sample_indices = indices[:SAMPLE_SIZE]

    sample_rows = []
    for idx in sample_indices:
        row = dataset[idx]
        sample_rows.append(
            {
                "paper_id": row["paper_id"],
                "title": row["title"],
                "abstract": row["abstract"],
                "year": row["year"],
                "decision": row["decision"],
            }
        )

    with SAMPLES_PATH.open("w", encoding="utf-8") as handle:
        for row in sample_rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")

    existing_reviews = {
        (r["paper_id"], r["model"]): r for r in read_jsonl(REVIEWS_PATH)
    }
    existing_revisions = {
        (r["paper_id"], r["condition"]): r for r in read_jsonl(REVISIONS_PATH)
    }
    existing_judgments = {
        (r["paper_id"], r["variant"]): r for r in read_jsonl(JUDGMENTS_PATH)
    }

    # Drop reviews for models not in the current configuration.
    for key, value in list(existing_reviews.items()):
        if value.get("model") not in REVIEWER_MODELS:
            existing_reviews.pop(key, None)

    # Drop invalid reviews missing core keys to allow re-run.
    for key, value in list(existing_reviews.items()):
        response = value.get("response", {})
        if not isinstance(response, dict) or not all(
            k in response for k in ("score", "strengths", "weaknesses", "suggestions")
        ):
            existing_reviews.pop(key, None)

    # Drop invalid revisions that lack revised_abstract to allow re-run.
    for key, value in list(existing_revisions.items()):
        response = value.get("response", {})
        if not isinstance(response, dict) or not response.get("revised_abstract"):
            existing_revisions.pop(key, None)

    # Drop invalid judgments missing core metrics to allow re-run.
    for key, value in list(existing_judgments.items()):
        response = value.get("response", {})
        if value.get("model") != JUDGE_MODEL or not isinstance(response, dict) or not all(
            k in response for k in ("clarity", "novelty", "overall")
        ):
            existing_judgments.pop(key, None)

    review_usage = defaultdict(int)

    for paper in sample_rows:
        title = paper["title"]
        abstract = paper["abstract"]
        paper_id = paper["paper_id"]

        for model in REVIEWER_MODELS:
            if (paper_id, model) in existing_reviews:
                continue
            messages = build_review_prompt(title, abstract)
            parsed, content, usage = call_json(
                model=model,
                messages=messages,
                temperature=0.2,
                max_tokens=800,
            )
            if not isinstance(parsed, dict) or not all(
                k in parsed for k in ("score", "strengths", "weaknesses", "suggestions")
            ):
                strict_system = (
                    "Return only JSON with keys score (1-10 integer), strengths "
                    "(list), weaknesses (list), suggestions (list), summary (string)."
                )
                strict_messages = [
                    {"role": "system", "content": strict_system},
                    {"role": "user", "content": messages[1]["content"]},
                ]
                parsed, content, usage = call_json(
                    model=model,
                    messages=strict_messages,
                    temperature=0.2,
                    max_tokens=800,
                )
            record = {
                "paper_id": paper_id,
                "model": model,
                "response": parsed,
                "raw": content,
                "usage": usage,
                "timestamp": datetime.utcnow().isoformat(),
            }
            append_jsonl(REVIEWS_PATH, [record])
            existing_reviews[(paper_id, model)] = record
            for key, val in usage.items():
                if val is not None:
                    review_usage[key] += val

        # Build feedback strings
        reviewer_feedback = []
        for model in REVIEWER_MODELS:
            review = existing_reviews[(paper_id, model)]["response"]
            suggestions = review.get("suggestions", [])
            if isinstance(suggestions, list):
                suggestions_text = "\n".join(f"- {s}" for s in suggestions)
            else:
                suggestions_text = str(suggestions)
            reviewer_feedback.append(
                f"Reviewer ({model}) suggestions:\n{suggestions_text}"
            )

        feedback_multi = "\n\n".join(reviewer_feedback)
        feedback_single = None
        for model in REVIEWER_MODELS:
            if model == SINGLE_REVIEWER:
                feedback_single = reviewer_feedback[REVIEWER_MODELS.index(model)]
                break

        revision_inputs = [
            ("single", feedback_single),
            ("multi", feedback_multi),
        ]

        for condition, feedback in revision_inputs:
            if (paper_id, condition) in existing_revisions:
                continue
            messages = build_revision_prompt(title, abstract, feedback)
            parsed, content, usage = call_json(
                model=AUTHOR_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=900,
            )
            if not isinstance(parsed, dict) or not parsed.get("revised_abstract"):
                strict_system = (
                    "Return only JSON with keys revised_abstract (string) and "
                    "change_log (list). No extra text."
                )
                strict_messages = [
                    {"role": "system", "content": strict_system},
                    {"role": "user", "content": messages[1]["content"]},
                ]
                parsed, content, usage = call_json(
                    model=AUTHOR_MODEL,
                    messages=strict_messages,
                    temperature=0.2,
                    max_tokens=900,
                )
            record = {
                "paper_id": paper_id,
                "condition": condition,
                "model": AUTHOR_MODEL,
                "response": parsed,
                "raw": content,
                "usage": usage,
                "timestamp": datetime.utcnow().isoformat(),
            }
            append_jsonl(REVISIONS_PATH, [record])
            existing_revisions[(paper_id, condition)] = record

        # Judge original and revised abstracts
        variants: List[Tuple[str, str]] = [
            ("original", abstract),
            (
                "single",
                existing_revisions[(paper_id, "single")]["response"][
                    "revised_abstract"
                ],
            ),
            (
                "multi",
                existing_revisions[(paper_id, "multi")]["response"][
                    "revised_abstract"
                ],
            ),
        ]

        for variant, text in variants:
            if (paper_id, variant) in existing_judgments:
                continue
            messages = build_judge_prompt(title, text)
            parsed, content, usage = call_json(
                model=JUDGE_MODEL,
                messages=messages,
                temperature=0.0,
                max_tokens=400,
            )
            record = {
                "paper_id": paper_id,
                "variant": variant,
                "model": JUDGE_MODEL,
                "response": parsed,
                "raw": content,
                "usage": usage,
                "timestamp": datetime.utcnow().isoformat(),
            }
            append_jsonl(JUDGMENTS_PATH, [record])
            existing_judgments[(paper_id, variant)] = record

    config = {
        "seed": SEED,
        "sample_size": SAMPLE_SIZE,
        "reviewer_models": REVIEWER_MODELS,
        "single_reviewer": SINGLE_REVIEWER,
        "author_model": AUTHOR_MODEL,
        "judge_model": JUDGE_MODEL,
        "timestamp": datetime.utcnow().isoformat(),
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

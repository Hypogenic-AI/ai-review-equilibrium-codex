# AI Reviewing Equilibrium Report

## 1. Executive Summary
This study asks whether different LLM reviewers give meaningfully different peer-review feedback and whether aggregating multiple model reviews changes abstract revisions compared with a single reviewer. We find consistent reviewer disagreement: GPT-4.1 scores abstracts higher than Claude Sonnet 4.5 (mean 7.18 vs 5.84), and suggestion similarity is modest (mean cosine similarity 0.221). In this setup, aggregated feedback does not improve judged abstract quality more than a single reviewer; single-reviewer revisions slightly outperform multi-reviewer revisions across clarity, novelty, and overall scores, but differences are not statistically significant.

Practical implication: multi-model review adds diversity but does not automatically translate to better revisions in a single-step abstract rewrite. If multi-model feedback is used, it likely needs additional aggregation or synthesis to translate disagreement into improvement.

## 2. Goal
We tested the hypothesis that different AI models provide distinct opinions when reviewing papers and that multi-model review dynamics change revision outcomes. This matters for deploying AI reviewing pipelines: if models systematically disagree or if aggregation does not improve revisions, stakeholders need to design better mediation or selection strategies.

## 3. Data Construction

### Dataset Description
- Source: HuggingFace `smallari/openreview-iclr-peer-reviews`
- Version: local snapshot in `datasets/openreview_iclr_peer_reviews`
- Size: 19,076 papers (we sampled 50)
- Fields used: title, abstract, decision, year
- Known biases: dataset reflects ICLR submissions, with uneven decision distributions

### Example Samples
```
ID: o9YC0B6P2m
Title: Scaling Law with Learning Rate Annealing
Abstract (truncated): We find that the cross-entropy loss curves of neural language models empirically adhere to a scaling law with learning rate (LR) annealing over training steps...
```
```
ID: 708lti8yfI
Title: Representation of solutions of second-order linear equations in Barron space via Green's functions
Abstract (truncated): AI-based methods for solving high-dimensional partial differential equations (PDEs) have garnered significant attention...
```
```
ID: X5qi6fnnw7
Title: Conservative World Models
Abstract (truncated): Zero-shot reinforcement learning (RL) promises to provide agents that can perform any task in an environment after an offline pre-training phase...
```

### Data Quality
- Missing values: title 0/50, abstract 0/50
- Missing decision labels: 12/50
- Decision distribution (non-missing): Reject 22, Accept 10, Accept (poster) 5, Accept (spotlight) 1
- Year distribution: 2025 = 32, 2024 = 18

### Preprocessing Steps
1. Loaded dataset from disk and sampled 50 papers with a fixed seed.
2. Extracted title and abstract fields; no further cleaning performed.

### Train/Val/Test Splits
Not applicable (analysis-only study; sampled papers are evaluated uniformly).

## 4. Experiment Description

### Methodology
#### High-Level Approach
We compare two reviewer models (Claude Sonnet 4.5 and GPT-4.1) on the same abstracts and quantify disagreement. We then revise abstracts using a fixed author model (GPT-4.1) under two conditions: single reviewer feedback (Claude only) and aggregated feedback (Claude + GPT-4.1). A separate judge model (GPT-4.1-mini) scores original and revised abstracts.

#### Why This Method?
- Multi-model review comparison is a direct test of diversity.
- Single vs multi-reviewer revision tests the dynamics of feedback aggregation.
- LLM judge scoring provides a scalable proxy for quality improvement.

### Implementation Details
#### Tools and Libraries
- numpy 2.4.0
- pandas 2.3.3
- scipy 1.16.3
- scikit-learn 1.8.0
- datasets 4.4.2
- openai 2.14.0

#### Algorithms/Models
- Reviewers: `anthropic/claude-sonnet-4.5`, `openai/gpt-4.1`
- Author: `openai/gpt-4.1`
- Judge: `openai/gpt-4.1-mini`

#### Hyperparameters
| Parameter | Value | Selection Method |
|-----------|-------|------------------|
| temperature (review) | 0.2 | fixed |
| temperature (revision) | 0.3 | fixed |
| temperature (judge) | 0.0 | fixed |
| max_tokens | 400-900 | fixed |
| sample_size | 50 | feasibility constraint |

#### Analysis Pipeline
1. Collect structured reviews from both reviewer models.
2. Compute score variance and suggestion similarity.
3. Generate single-reviewer and multi-reviewer revisions.
4. Judge original and revised abstracts.
5. Run paired t-tests and compute effect sizes.

### Experimental Protocol
#### Reproducibility Information
- Runs: 1 per condition (temperature low, deterministic judge)
- Seed: 42
- Hardware: CPU-only
- Runtime: ~20-25 minutes for 50 papers

#### Evaluation Metrics
- Score variance: disagreement in reviewer scores
- Suggestion similarity: TF-IDF cosine similarity across reviewer suggestions
- Improvement delta: judge score (revised - original) for clarity, novelty, overall

### Raw Results
#### Reviewer Score Summary
| Model | Mean Score | Std | N |
|-------|------------|-----|---|
| Claude Sonnet 4.5 | 5.84 | 1.02 | 50 |
| GPT-4.1 | 7.18 | 1.14 | 50 |

#### Improvement Statistics
| Metric | Mean Delta (Single) | Mean Delta (Multi) | p-value | Cohen's d |
|--------|-----------------|----------------|--------:|----------:|
| Clarity | 0.54 | 0.46 | 0.159 | -0.20 |
| Novelty | 0.54 | 0.52 | 0.743 | -0.05 |
| Overall | 0.20 | 0.14 | 0.083 | -0.25 |

#### Visualizations
- Review scores by model: `results/plots/review_scores_by_model.png`
- Suggestion similarity distribution: `results/plots/suggestion_similarity.png`
- Quality improvements: `results/plots/quality_improvements.png`

#### Output Locations
- Raw model outputs: `results/model_outputs/`
- Metrics summary: `results/analysis/metrics.json`
- Plots: `results/plots/`

## 5. Result Analysis

### Key Findings
1. Reviewer disagreement is substantial: average score variance is 1.03 with mean suggestion similarity 0.221, showing only modest overlap in feedback.
2. GPT-4.1 is consistently more positive than Claude Sonnet 4.5 by ~1.34 points on average.
3. Multi-reviewer feedback does not significantly improve judged abstract quality compared with single-reviewer feedback; deltas are slightly smaller under multi-reviewer conditions.

### Hypothesis Testing Results
- H1 (Diversity): Supported. Score variance > 0 and suggestion similarity around 0.22 indicate meaningful diversity.
- H2 (Dynamics): Not supported. Multi-reviewer feedback does not improve revisions more than single reviewer feedback (p-values > 0.05).
- H3 (Stability): Not supported. No clear reduction in variance was observed.

### Comparison to Baselines
Single reviewer revisions act as the baseline. Multi-reviewer aggregation does not outperform this baseline on any metric and shows small negative effect sizes.

### Visualizations
See `results/plots/review_scores_by_model.png`, `results/plots/suggestion_similarity.png`, and `results/plots/quality_improvements.png`.

### Surprises and Insights
- The largest gain from revisions appears in clarity and novelty, but multi-reviewer aggregation does not amplify these gains.
- The divergence in score levels suggests strong reviewer calibration differences across models.

### Error Analysis
Some reviews and revisions required JSON repair due to partial outputs. All missing entries were regenerated using stricter JSON prompts. Remaining error cases are recorded in raw outputs and do not affect the final deduplicated metrics.

### Limitations
- Judging is performed by GPT-4.1-mini; human evaluation is not included.
- Author model and one reviewer share the same base model family (OpenAI), which may bias revision behavior.
- Only abstracts are evaluated; full paper review dynamics could differ.
- Single-round revision only; multi-round reviewer-author interaction may yield different dynamics.

## 6. Conclusions
Different LLMs provide distinct peer-review feedback, reflected in score variance and low suggestion overlap. However, aggregating multiple model reviews does not yield stronger single-step abstract improvements in this study. This suggests that multi-model review pipelines need explicit synthesis or conflict-resolution mechanisms to translate diversity into gains.

### Confidence in Findings
Moderate. The signals are consistent across 50 papers, but stronger evidence would come from human evaluation or multi-round revision studies.

## 7. Next Steps
1. Add a structured synthesis step that merges or reconciles reviewer disagreements before revision.
2. Evaluate multi-round reviewer-author interactions to test equilibrium dynamics.
3. Extend evaluation to full-paper sections (intro, methods) with human raters.
4. Test other reviewer combinations and judge models to assess robustness.

## References
- Jin et al. (2024) AgentReview: Exploring Peer Review Dynamics with LLM Agents.
- Tan et al. (2024) Peer Review as a Multi-Turn and Long-Context Dialogue.
- Chu et al. (2024) PRE: A Peer Review Based LLM Evaluator.
- Sukpanichnant et al. (2024) PeerArg: Argumentative Peer Review with LLMs.
- Ning et al. (2024) PiCO: Consistency Optimization in LLM Peer Review.
- Chen et al. (2024) Auto-PRE.
- Vasu et al. (2025) Justice in Judgment.
- Ye et al. (2024) Risks of Utilizing LLMs in Scholarly Peer Review.

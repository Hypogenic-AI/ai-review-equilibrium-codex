## Research Question
Do different AI models provide distinct peer-review feedback on the same paper, and does combining multiple model reviews change the magnitude or direction of paper improvements compared with a single-model review?

## Background and Motivation
AI-assisted peer review promises faster feedback and scalable quality control, but little is known about how heterogeneous LLM reviewers disagree and how those disagreements affect iterative paper improvement. Prior work focuses on multi-agent simulation and peer-review-inspired evaluation, yet equilibrium-like dynamics (disagreement, convergence, and improvement under multi-model feedback) remain understudied. This study aims to quantify review diversity across models and measure whether multi-model feedback yields measurably different improvements than single-model feedback.

## Hypothesis Decomposition
1. H1 (Diversity): Reviews from different LLMs on the same paper exhibit measurable disagreement in scores and content.
2. H2 (Dynamics): Multi-model feedback leads to different (and potentially larger) improvements in paper quality than single-model feedback.
3. H3 (Stability): Aggregated feedback reduces variance in judged quality across revisions compared with single-model feedback.

Independent variables:
- Reviewer model identity (e.g., GPT-4.1 vs Claude Sonnet 4.5 vs Gemini 2.5 Pro).
- Review condition (single-model feedback vs multi-model aggregated feedback).

Dependent variables:
- Review score variance and textual similarity between review suggestions.
- Revision quality improvements (LLM-judge ratings: clarity, novelty, overall quality).
- Variance of judged quality across conditions.

Success criteria:
- Significant disagreement across models (score variance > 0 and suggestion similarity below threshold).
- Statistically significant difference in improvement between single-model and multi-model feedback (p < 0.05).

Alternative explanations:
- Differences driven by prompt sensitivity rather than model identity.
- Judge model bias toward its own feedback style.
- Dataset bias in abstracts influencing review tone.

## Proposed Methodology

### Approach
Use real LLM APIs to generate reviews for the same set of ICLR paper abstracts from two datasets. Measure disagreement (score variance, suggestion similarity). Then run a controlled revision experiment where the same author model revises abstracts using either a single review or aggregated multi-model feedback, and compare improvements using a separate judge model.

### Experimental Steps
1. Load OpenReview ICLR peer review dataset; sample N paper abstracts with titles.
2. For each paper, collect structured reviews from multiple LLMs using identical prompts.
3. Quantify disagreement using score variance and TF-IDF cosine similarity on “suggestions” sections.
4. Revision experiment:
   - Condition A: single-model review (choose one reviewer model).
   - Condition B: aggregated feedback from all reviewer models.
   - Use a fixed author model to rewrite abstracts.
5. Evaluate original vs revised abstracts with a separate judge model using a rubric for clarity, novelty, and overall quality.
6. Run statistical tests comparing improvements and variance between conditions.

### Baselines
- Single LLM reviewer (no aggregation).
- Majority-vote/mean-score aggregation (for review-score agreement).
- Original abstract quality as baseline for revision improvement.

### Evaluation Metrics
- Review disagreement: score variance, pairwise cosine similarity of suggestions.
- Improvement: delta in judge scores (revised minus original) across criteria.
- Stability: variance of judge scores across runs/conditions.

### Statistical Analysis Plan
- Paired t-test or Wilcoxon signed-rank for improvement deltas between conditions.
- ANOVA or Kruskal-Wallis for multi-model score differences.
- Report p-values, 95% confidence intervals, and effect sizes (Cohen’s d).
- Significance threshold: alpha = 0.05 with Holm correction for multiple comparisons.

## Expected Outcomes
- Support for H1: measurable disagreement across models (low suggestion similarity, score variance).
- Support for H2: aggregated feedback yields larger improvement deltas than single-model feedback.
- Support for H3: reduced variance in judged quality for multi-model feedback.

## Timeline and Milestones
- Phase 1 (Planning): 0.5 day
- Phase 2 (Setup + Data checks): 0.5 day
- Phase 3 (Implementation): 1 day
- Phase 4 (Experimentation): 1 day
- Phase 5 (Analysis): 0.5 day
- Phase 6 (Documentation): 0.5 day

## Potential Challenges
- API cost and rate limits: mitigate by sampling N=60 papers.
- Judge bias: use a different model for judging than reviewer models.
- Prompt drift: standardize prompts and record full prompt text.
- Stochasticity: run with temperature=0.2 and fixed seeds.

## Success Criteria
- All experiments run on at least 50 papers.
- Statistically significant differences where hypothesized.
- Reproducible scripts with logged prompts, seeds, and model metadata.
- REPORT.md with actual quantitative results and visualizations.

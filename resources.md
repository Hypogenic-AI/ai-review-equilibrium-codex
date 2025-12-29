# Resources Catalog

## Summary
This document catalogs all resources gathered for the research project, including papers, datasets, and code repositories.

### Papers
Total papers downloaded: 8

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| AgentReview: Exploring Peer Review Dynamics with LLM Agents | Jin et al. | 2024 | papers/2406.12708_AgentReview_Exploring_Peer_Review_Dynamics_with_LLM_Agents.pdf | Multi-agent peer review simulation |
| Peer Review as A Multi-Turn and Long-Context Dialogue with Role-Based Interactions | Tan et al. | 2024 | papers/2406.05688_Peer_Review_as_Multi_Turn_Long_Context_Dialogue.pdf | Role-based multi-turn review |
| PRE: A Peer Review Based Large Language Model Evaluator | Chu et al. | 2024 | papers/2401.15641_PRE_Peer_Review_Based_LLM_Evaluator.pdf | Peer-review-inspired LLM evaluation |
| PeerArg: Argumentative Peer Review with LLMs | Sukpanichnant et al. | 2024 | papers/2409.16813_PeerArg_Argumentative_Peer_Review_with_LLMs.pdf | Argumentation-based review pipeline |
| PiCO: Peer Review in LLMs based on the Consistency Optimization | Ning et al. | 2024 | papers/2402.01830_PiCO_Peer_Review_in_LLMs_Consistency_Optimization.pdf | Consistency-based review evaluation |
| Auto-PRE: An Automatic and Cost-Efficient Peer-Review Framework for Language Generation Evaluation | Chen et al. | 2024 | papers/2410.12265_Auto_PRE_Automatic_Peer_Review_Framework.pdf | Automated peer review for eval |
| Justice in Judgment: Unveiling (Hidden) Bias in LLM-assisted Peer Reviews | Vasu et al. | 2025 | papers/2509.13400_Justice_in_Judgment_Bias_in_LLM_Assisted_Peer_Reviews.pdf | Bias and fairness audit |
| Are We There Yet? Revealing the Risks of Utilizing Large Language Models in Scholarly Peer Review | Ye et al. | 2024 | papers/2412.01708_Risks_of_Utilizing_LLMs_in_Peer_Review.pdf | Risk analysis of LLM review |

See papers/README.md for detailed descriptions.

### Datasets
Total datasets downloaded: 2

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| OpenReview ICLR Peer Reviews | HuggingFace `smallari/openreview-iclr-peer-reviews` | 19,076 | Review analysis | datasets/openreview_iclr_peer_reviews/ | Raw ICLR reviews and decisions |
| ICLR Peer Reviews (LLM + Human) | HuggingFace `JerMa88/ICLR_Peer_Reviews` | 15,821 | LLM detection / review analysis | datasets/iclr_peer_reviews/ | Includes LLM traces and scores |

See datasets/README.md for detailed descriptions.

### Code Repositories
Total repositories cloned: 2

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| AgentReview | https://github.com/Ahren09/AgentReview | Multi-agent review simulation | code/AgentReview/ | LLM-agent review dynamics |
| openreview-py | https://github.com/openreview/openreview-py | OpenReview data access | code/openreview-py/ | API client for OpenReview |

See code/README.md for detailed descriptions.

## Resource Gathering Notes

### Search Strategy
- Queried arXiv for LLM peer review, multi-agent review, and evaluation frameworks.
- Searched HuggingFace datasets for peer-review corpora.
- Looked for official implementations on GitHub for multi-agent review simulation and data access.

### Selection Criteria
- Direct relevance to LLM-based peer review and multi-model dynamics.
- Availability of PDFs and datasets without paywalls.
- Preference for datasets derived from OpenReview/ICLR peer review data.

### Challenges Encountered
- HuggingFace dataset `Intel/AI-Peer-Review-Detection` could not be loaded (no data files in the dataset repo at the pinned revision). Alternative dataset selected.

### Gaps and Workarounds
- Some papers lack explicit dataset details in abstracts; further inspection of PDFs may be needed.
- Used OpenReview-derived datasets as primary data sources to support experiments.

## Recommendations for Experiment Design

1. **Primary dataset(s)**: OpenReview ICLR peer reviews for realistic review content; ICLR peer reviews (LLM + Human) for AI-vs-human comparisons.
2. **Baseline methods**: Single LLM reviewer, majority-vote aggregation, and a human-review reference baseline.
3. **Evaluation metrics**: Correlation with human scores, accept/reject prediction accuracy, agreement/stability across reviewers, and bias audits.
4. **Code to adapt/reuse**: AgentReview for multi-agent simulation; openreview-py for fetching additional review data.

## Research Execution Notes (This Run)

- Dataset used: `datasets/openreview_iclr_peer_reviews` (50-paper sample, seed 42).
- Reviewer models: `anthropic/claude-sonnet-4.5`, `openai/gpt-4.1`.
- Author model: `openai/gpt-4.1`; Judge model: `openai/gpt-4.1-mini`.
- Outputs stored under `results/model_outputs/` with analysis artifacts in `results/analysis/` and plots in `results/plots/`.
- See `REPORT.md` for results and `README.md` for reproduction steps.

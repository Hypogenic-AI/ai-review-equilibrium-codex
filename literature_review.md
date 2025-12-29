# Literature Review

## Research Area Overview
This topic examines how large language models (LLMs) act as peer reviewers, how multiple models interact in review dynamics, and what biases or risks arise when automated review is used at scale. Recent work focuses on treating review as an interactive, multi-agent process, using peer-review-inspired evaluation frameworks, and auditing LLM-generated reviews for reliability and fairness.

## Key Papers

### Paper 1: AgentReview: Exploring Peer Review Dynamics with LLM Agents
- **Authors**: Yiqiao Jin, Qinlin Zhao, Yiyang Wang, Hao Chen, Kaijie Zhu, Yijia Xiao, et al.
- **Year**: 2024
- **Source**: arXiv 2406.12708
- **Key Contribution**: Simulates peer review dynamics using LLM agents to explore interaction effects and latent variables in review processes.
- **Methodology**: Multi-agent LLM framework to simulate reviewer/author/editor interactions.
- **Datasets Used**: Not specified in abstract (likely synthetic or OpenReview-style data).
- **Results**: Demonstrates multi-agent simulation as a viable lens for studying review dynamics.
- **Code Available**: Yes, https://github.com/Ahren09/AgentReview
- **Relevance to Our Research**: Directly targets multi-agent review dynamics, aligning with equilibrium and multi-model interaction hypotheses.

### Paper 2: Peer Review as A Multi-Turn and Long-Context Dialogue with Role-Based Interactions
- **Authors**: Cheng Tan, Dongxin Lyu, Siyuan Li, Zhangyang Gao, Jingxuan Wei, Siqi Ma, et al.
- **Year**: 2024
- **Source**: arXiv 2406.05688
- **Key Contribution**: Reframes peer review as an iterative, role-based dialogue rather than a one-shot response.
- **Methodology**: Multi-turn conversational setup with role conditioning (reviewer/author/editor).
- **Datasets Used**: Not specified in abstract.
- **Results**: Highlights improvements from iterative, dialogic feedback loops.
- **Code Available**: Not specified in abstract.
- **Relevance to Our Research**: Supports dynamic review processes and iterative improvement dynamics.

### Paper 3: PRE: A Peer Review Based Large Language Model Evaluator
- **Authors**: Zhumin Chu, Qingyao Ai, Yiteng Tu, Haitao Li, Yiqun Liu
- **Year**: 2024
- **Source**: arXiv 2401.15641
- **Key Contribution**: Proposes a peer-review-inspired framework to evaluate LLMs.
- **Methodology**: LLMs act as reviewers to score and critique model outputs.
- **Datasets Used**: Not specified in abstract.
- **Results**: Suggests peer-review-style evaluation can be effective for model assessment.
- **Code Available**: Not specified in abstract.
- **Relevance to Our Research**: Provides a framework for multi-model evaluation and consensus building.

### Paper 4: PeerArg: Argumentative Peer Review with LLMs
- **Authors**: Purin Sukpanichnant, Anna Rapberger, Francesca Toni
- **Year**: 2024
- **Source**: arXiv 2409.16813
- **Key Contribution**: Introduces an interpretable, argumentation-based pipeline for peer review.
- **Methodology**: Uses argument mining/structured reasoning to make review outputs more transparent.
- **Datasets Used**: Not specified in abstract.
- **Results**: Improves interpretability of LLM-generated reviews.
- **Code Available**: Not specified in abstract.
- **Relevance to Our Research**: Provides structure for comparing reviewer rationales across models.

### Paper 5: PiCO: Peer Review in LLMs based on the Consistency Optimization
- **Authors**: Kun-Peng Ning, Shuo Yang, Yu-Yang Liu, Jia-Yu Yao, Zhen-Hui Liu, Yong-Hong Tian, et al.
- **Year**: 2024
- **Source**: arXiv 2402.01830
- **Key Contribution**: Unsupervised evaluation via peer-review style consistency optimization.
- **Methodology**: Optimization objective that enforces reviewer consistency to score LLM outputs.
- **Datasets Used**: Not specified in abstract.
- **Results**: Shows peer-review consistency can guide automatic evaluation.
- **Code Available**: Not specified in abstract.
- **Relevance to Our Research**: Emphasizes consistency and equilibrium properties among reviewers.

### Paper 6: Auto-PRE: An Automatic and Cost-Efficient Peer-Review Framework for Language Generation Evaluation
- **Authors**: Junjie Chen, Weihang Su, Zhumin Chu, Haitao Li, Yujia Zhou, Dingbo Yuan, et al.
- **Year**: 2024
- **Source**: arXiv 2410.12265
- **Key Contribution**: Peer-review-inspired evaluation for language generation without human references.
- **Methodology**: Automatic review workflow to score outputs and reduce evaluation costs.
- **Datasets Used**: Not specified in abstract.
- **Results**: Demonstrates scalability and reduced evaluation cost.
- **Code Available**: Not specified in abstract.
- **Relevance to Our Research**: Provides evaluation pipeline where multiple LLM reviewers can be compared.

### Paper 7: Justice in Judgment: Unveiling (Hidden) Bias in LLM-assisted Peer Reviews
- **Authors**: Sai Suresh Macharla Vasu, Ivaxi Sheth, Hui-Po Wang, Ruta Binkyte, Mario Fritz
- **Year**: 2025
- **Source**: arXiv 2509.13400
- **Key Contribution**: Audits bias and fairness in LLM-assisted peer review.
- **Methodology**: Controlled experiments to detect bias patterns in generated reviews.
- **Datasets Used**: Not specified in abstract.
- **Results**: Reports systematic bias risks in LLM-generated reviews.
- **Code Available**: Not specified in abstract.
- **Relevance to Our Research**: Highlights fairness risks in multi-model review setups.

### Paper 8: Are We There Yet? Revealing the Risks of Utilizing Large Language Models in Scholarly Peer Review
- **Authors**: Rui Ye, Xianghe Pang, Jingyi Chai, Jiaao Chen, Zhenfei Yin, Zhen Xiang, et al.
- **Year**: 2024
- **Source**: arXiv 2412.01708
- **Key Contribution**: Systematic risk analysis of LLM-based peer review.
- **Methodology**: Risk taxonomy and empirical probing of failure modes.
- **Datasets Used**: Not specified in abstract.
- **Results**: Highlights vulnerabilities and limitations of automated review.
- **Code Available**: Not specified in abstract.
- **Relevance to Our Research**: Provides risk framing for multi-model review equilibrium studies.

## Common Methodologies
- **Multi-agent simulation**: Used in AgentReview to model reviewer/author/editor dynamics.
- **Dialogic review frameworks**: Multi-turn review formulations to emulate iterative feedback.
- **Peer-review-inspired evaluation**: PRE, Auto-PRE, and PiCO apply reviewer-style scoring to evaluate models.
- **Bias and risk audits**: Studies focus on fairness and vulnerabilities in automated reviews.

## Standard Baselines
- **Human review scores**: Used to compare LLM review quality or alignment.
- **Single-model reviewer**: Baseline reviewer without interaction or aggregation.
- **Reference-based metrics**: BLEU/ROUGE or similar metrics for language generation evaluation (common in Auto-PRE-style settings).

## Evaluation Metrics
- **Correlation with human judgments**: Spearman/Kendall for review score alignment.
- **Classification metrics**: Accuracy/F1 for accept/reject or quality labels.
- **Agreement/consistency**: Inter-reviewer agreement or stability under perturbations.
- **Argument quality metrics**: Coverage of criteria, coherence, and completeness.

## Datasets in the Literature
- **OpenReview/ICLR peer review corpora**: Common source of real reviews and decisions.
- **Synthetic review data**: Used when privacy or access constraints exist.
- **Mixed human/LLM review datasets**: Useful for detection and bias analysis.

## Gaps and Opportunities
- **Equilibrium analysis**: Limited work on convergence, stability, and disagreement patterns across multiple LLM reviewers.
- **Cross-model diversity**: Few studies measure how model heterogeneity impacts revision quality.
- **Robustness to adversarial content**: Risks from prompt injection and manipulation remain underexplored.
- **Longitudinal improvement dynamics**: Multi-round revision loops are still rare in evaluations.

## Recommendations for Our Experiment
- **Recommended datasets**: OpenReview ICLR peer reviews (realistic review content) and ICLR peer reviews with LLM traces for AI-vs-human comparisons.
- **Recommended baselines**: Single LLM reviewer, majority-vote aggregation, and human-review reference scores when available.
- **Recommended metrics**: Human-alignment correlation, review score agreement, accept/reject prediction accuracy, and bias audits across protected attributes.
- **Methodological considerations**: Use role-based prompts, track reviewer disagreement over rounds, and test reviewer diversity (model families, sizes).

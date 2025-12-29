# AI Reviewing Equilibrium

This project studies whether different LLM reviewers produce distinct feedback and whether aggregating multiple reviewers changes revision outcomes for paper abstracts. We run real-model review, revision, and judging experiments on a sample of ICLR abstracts.

Key findings:
- Reviewer disagreement is substantial: mean score variance 1.03 and suggestion similarity 0.22.
- GPT-4.1 scores are more positive than Claude Sonnet 4.5 by ~1.34 points on average.
- Multi-reviewer feedback does not improve abstract revisions over a single reviewer (p > 0.05 across metrics).

## How to Reproduce
1. Create env and install deps:
   - `uv venv`
   - `uv add pandas numpy scipy scikit-learn matplotlib seaborn datasets openai tenacity python-dotenv`
2. Run experiments (requires `OPENROUTER_API_KEY`):
   - `source .venv/bin/activate && python src/run_experiment.py`
3. Analyze and generate plots:
   - `source .venv/bin/activate && python src/analyze_results.py`

## File Structure
- `planning.md`: research plan
- `src/run_experiment.py`: model review/revision/judging pipeline
- `src/analyze_results.py`: analysis and plots
- `results/model_outputs/`: raw model outputs
- `results/analysis/`: metrics and tables
- `results/plots/`: visualizations
- `REPORT.md`: full research report

See `REPORT.md` for full methodology, results, and discussion.

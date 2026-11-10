# Lending Club: leakage-aware credit decisions and thin-file fairness

[![Notebook validation](https://github.com/zeeshan9595/lending-club-credit-decisions/actions/workflows/notebook-validation.yml/badge.svg?branch=portfolio%2Freproducibility-docs)](https://github.com/zeeshan9595/lending-club-credit-decisions/actions/workflows/notebook-validation.yml)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zeeshan9595/lending-club-credit-decisions/blob/portfolio/reproducibility-docs/lending_club_credit_decisions.ipynb)

**[Model card](MODEL_CARD.md)** · **[Data dictionary](DATA_DICTIONARY.md)** · **[Notebook validation](validate_notebook.py)**


An end-to-end credit risk analysis on **589,488 resolved 36-month Lending Club loans (2012-2015)**. The question is not "how high can AUC go?" but *which loans should a lender approve, what does that decision earn, and who pays for the model's mistakes?*

Notebook: [lending_club_credit_decisions.ipynb](lending_club_credit_decisions.ipynb), designed to run top to bottom in Google Colab. It downloads the public Lending Club dataset through KaggleHub; the raw dataset is not stored in this repository. See the [environment requirements](requirements.txt) before running locally.

## Design

| Choice | Why |
|---|---|
| **Out-of-time split**: train 2012-13, validate 2014, test 2015 | A random split lets the model see the future. Lenders score next year's applicants. |
| **Leakage audit before modelling** | Many public notebooks use payment fields that only exist after the loan. |
| **Application-time features only** in the final model | Lending Club's own grade and rate are excluded: they are another model's output. |
| **Threshold chosen on 2014, applied to 2015** | Picking the cut-off on the test year would overstate results. |
| **Decisions priced in realised cash P&L** | Total repaid minus amount funded, with a funding-cost sensitivity. |
| **Thin-file group**: under 5 years of credit history | Borrowers with short histories are where credit models are least reliable. |

## Key findings (2015 out-of-time test: 283,026 loans, 14.9% default rate)

**1. Post-loan fields make the problem look solved.** Including payment and recovery fields gives ROC-AUC 0.9995 and PR-AUC 0.998. With application data only, ROC-AUC is 0.665 and PR-AUC 0.245. The leaky model is useless for an approval decision.

| Model (test year 2015) | ROC-AUC | PR-AUC | Brier |
|---|---|---|---|
| A. With post-loan fields (leaky) | 0.9995 | 0.998 | 0.005 |
| B. Application data + LC grade/rate | 0.686 | 0.264 | 0.121 |
| C. Application data only, LightGBM (final) | 0.665 | 0.245 | 0.122 |
| Logistic regression baseline, same features | 0.652 | 0.232 | 0.123 |

**2. Gradient boosting adds only a little over logistic regression** (+0.014 ROC-AUC). For a regulated lender, the interpretable scorecard may be the better trade-off.

**3. Whether to decline the riskiest loans depends on the cost of money.** On raw cash P&L, approving every Lending Club-approved loan was optimal. Once a funding cost is charged on the funded amount (about 1.5 years outstanding), the threshold chosen on 2014 starts to pay on 2015:

| Assumed funding cost | PD threshold from 2014 | 2015 approval rate | P&L, approve all | P&L, with policy | Uplift |
|---|---|---|---|---|---|
| 0% | 0.56 | 100% | 237.4m | 237.4m | 0 |
| 3% | 0.31 | 98.7% | 74.3m | 77.2m | +2.8m |
| 5% | 0.20 | 84.7% | -34.4m | -13.5m | +20.9m |

*USD. Funding costs are assumptions, not Lending Club data.*

**4. Thin-file borrowers carry a disproportionate share of wrongful declines.** They default 1.3x as often as established borrowers (19.3% vs 14.7%). Yet a policy declining the riskiest 20% of applicants declines **38% of thin-file borrowers who would have repaid, against 17% of established ones (2.3x)**. The model is also less accurate for them (ROC-AUC 0.629 vs 0.666).

| Decline riskiest 20% | Default rate | Share declined | Good borrowers declined | Defaulters caught |
|---|---|---|---|---|
| 5+ yrs credit history | 14.7% | 19.3% | 16.8% | 34.1% |
| Under 5 yrs credit history | 19.3% | 41.9% | 38.3% | 57.1% |

**5. The model under-predicts default out of time.** Trained on 2012-13, it predicts 12.8% for established and 17.4% for thin-file borrowers in 2015; actual rates were 14.7% and 19.3%. Defaults rose and the model did not move with them, so it would need recalibration before use.

**6. Drivers for thin-file applicants (SHAP):** annual income, FICO score, loan amount, recent credit enquiries and length of credit history.

## Limitations

- **Selection bias:** only loans Lending Club approved are observed. Rejected applicants' outcomes are unknown, so this evaluates re-ranking an approved book, not a full approval policy.
- Thin-file is proxied by credit-history length; Lending Club does not identify credit-invisible applicants.
- P&L uses nominal cash flows without discounting; the funding cost is a simple assumption.
- A public dataset, not production underwriting.

## Data

[All Lending Club loan data](https://www.kaggle.com/datasets/wordsforthewise/lending-club) on Kaggle, CC0 public domain. The raw data is not stored in this repo; the notebook downloads it with kagglehub.

## Reproducibility and validation

The notebook downloads a large public dataset and runs a computationally intensive analysis. The automated workflow therefore validates notebook structure and metadata; it does **not** execute the full modelling experiment or claim fresh performance results.

Local environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python validate_notebook.py
python -m unittest discover -s tests -v
```

The reported metrics in this README are the results documented by the notebook. Re-run the complete notebook against the downloaded dataset before presenting them as a newly reproduced run.

## Stack

Python, pandas, scikit-learn, LightGBM, SHAP, matplotlib, KaggleHub, Google Colab.

---
Zeeshan Azeem Khalid · [LinkedIn](https://linkedin.com/in/zeeshan-azeem-khalid) · Related: [fraud detection leakage audit](https://github.com/zeeshan9595/Fraud-Detection-using-AI-and-ML)

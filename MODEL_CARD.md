# Model card — Lending Club credit decisions

## Intended use

This project is an independent portfolio study of credit-risk ranking, loan approval thresholds, funding-cost sensitivity and a thin-file fairness proxy. It is intended for research discussion and demonstration of analytical practice.

It is not a production underwriting model, a recommendation to approve or decline real applicants, or evidence of causal fairness. It must not be used to make decisions about real borrowers.

## Dataset and target

- Public Lending Club accepted-loan dataset obtained through KaggleHub.
- Analysis window: 36-month loans issued from January 2012 through December 2015.
- Resolved outcomes: Fully Paid versus Charged Off / Default categories documented in the notebook.
- Reported analysis sample: 589,488 resolved loans.
- Target: binary indicator for charged-off/default outcomes.

Only accepted loans are observed. Rejected applicants and their counterfactual outcomes are unavailable, creating selection bias.

## Information timing and leakage controls

The notebook separates:
- application-time borrower and loan characteristics;
- Lending Club's own grade and interest rate, which are treated as outputs of an upstream risk/pricing process in the final application-only model;
- post-origination repayment and recovery fields, which are used only in a leakage demonstration and not in the final decision-time feature set.

The final model uses application-time features. The time-ordered split is:
- training: 2012–2013;
- validation: 2014, used for early stopping and threshold selection;
- test: 2015, held out for final evaluation.

## Models and metrics

The notebook compares a LightGBM model with a logistic-regression baseline and demonstrates how post-loan information can create implausibly strong performance. Metrics include ROC-AUC, PR-AUC and Brier score. Business decision analysis reports approval rates and cash-P&L outcomes at thresholds selected on validation data.

## Economic assumptions

The cash-P&L calculation uses realised repayments and funded amount for historical outcome analysis. Funding-cost sensitivities apply explicit assumed annual rates and an approximate 1.5-year average time outstanding. These rates and the duration assumption are scenario inputs, not Lending Club observations.

Reported P&L is nominal and is not a discounted cash-flow valuation. It does not establish net present value, capital consumption, lifetime expected loss or regulatory capital requirements.

## Fairness analysis

Thin-file status is proxied by credit-history length below five years. It is not equivalent to credit invisibility or a protected characteristic. Group differences are descriptive and should not be interpreted as proof of disparate impact or causal discrimination.

## Limitations and risks

- Accepted-loan selection bias: outcomes for rejected applicants are unknown.
- Historical US marketplace lending data (2012–2015) may not represent current UK bank applicants.
- The dataset is public and retrospective, not a live origination environment.
- Credit-history length is a proxy, not a full measure of thin-file status.
- The funding-cost and average-duration assumptions are simplified.
- Historical performance does not establish production generalisation.
- The notebook downloads a large dataset and may require substantial memory and runtime.

## Appropriate interpretation

Use this project to discuss leakage-aware feature selection, out-of-time validation, decision-threshold economics and group-level error analysis. Do not present it as a deployed model, a validated underwriting policy or proof that one group is treated fairly.

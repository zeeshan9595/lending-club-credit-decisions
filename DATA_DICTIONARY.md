# Data dictionary — Lending Club notebook

The notebook downloads the public accepted-loan dataset from KaggleHub. The raw data is not committed to this repository. The table below describes the principal columns selected or derived by the notebook.

## Target, dates and outcomes

| Field | Meaning | Use |
|---|---|---|
| `issue_d` | Loan issue month | Temporal filtering and train/validation/test partitioning |
| `loan_status` | Historical loan outcome | Used to define the resolved binary target |
| `y` | 1 for charged-off/default; 0 for fully paid | Prediction target |
| `year` | Year derived from issue date | Time split and descriptive analysis |
| `funded_amnt` | Amount funded | Historical cash-P&L calculation; not an application feature in the final model |
| `pnl` | `total_pymnt - funded_amnt` | Retrospective cash outcome; never a predictor |

## Application-time predictors

| Field(s) | Meaning |
|---|---|
| `loan_amnt`, `term` | Requested loan amount and contractual term |
| `emp_length`, `home_ownership`, `annual_inc` | Employment, housing and income characteristics |
| `verification_status`, `purpose`, `application_type` | Application attributes |
| `dti`, `delinq_2yrs` | Debt-to-income and prior delinquency |
| `earliest_cr_line`, `credit_hist_yrs` | Earliest reported credit line and derived history length |
| `fico_range_low`, `fico_range_high` | Credit-score range |
| `inq_last_6mths`, `open_acc`, `pub_rec`, `total_acc` | Credit enquiries and account/public-record counts |
| `revol_bal`, `revol_util`, `mort_acc`, `pub_rec_bankruptcies` | Revolving credit and public-record attributes |

## Upstream pricing fields

| Field | Meaning | Treatment |
|---|---|---|
| `int_rate` | Lending Club assigned interest rate | Excluded from final application-only model |
| `grade` | Lending Club assigned grade | Excluded from final application-only model |

These are outputs of the lender's own pricing/risk process and can encode prior underwriting decisions.

## Post-origination fields used in leakage demonstration

| Field(s) | Meaning | Treatment |
|---|---|---|
| `total_pymnt`, `total_rec_prncp` | Repayments after origination | Leakage demonstration / outcome analysis only |
| `recoveries`, `collection_recovery_fee` | Recovery amounts and fees | Leakage demonstration / outcome analysis only |
| `last_pymnt_amnt`, `last_fico_range_high` | Later payment and credit-score information | Leakage demonstration only |
| `debt_settlement_flag` | Later settlement status | Leakage demonstration only |

## Derived group

| Field | Definition |
|---|---|
| `thin_file` | Under 5 years of credit history versus 5+ years |

This is a descriptive proxy and should not be treated as a complete measure of credit invisibility or a protected group.

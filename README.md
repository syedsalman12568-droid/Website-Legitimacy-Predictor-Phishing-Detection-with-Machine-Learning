# Website Legitimacy Prediction — Augmented Dataset Fix

## The problem

The original model almost always predicted "Phishing," regardless of input.

**Root cause:** 4 out of 16 features (`Have_IP`, `https_Domain`, `Right_Click`,
`URL_Length`) had **zero legitimate examples** in the original 10,000-row
dataset that broke a specific pattern. Every real legitimate website had
`Have_IP=0`, `https_Domain=0`, `Right_Click=1`, `URL_Length=1` — no exceptions.
The model learned this as an absolute rule: if even one of these 4 features
had the "wrong" value, predict Phishing with near-100% confidence, no matter
what the other 12 features looked like. This was confirmed to be a **data**
issue, not a bug in the code or the pickle file — even a completely different
model type (Logistic Regression) showed the same behavior on the same data.

## The fix (this folder)

1. **Data augmentation** — added 1,000 synthetic rows to the original 10,000:
   - 500 **Legitimate** examples that have 1–2 "risky" features anyway
   - 500 **Phishing** examples that look mostly "clean"
   - Sampling was weighted so `URL_Length` (which needed the most
     counterexamples — it had 2,266 one-sided rows vs. e.g. 2 for
     `https_Domain`) got proportionally more coverage.
   - New file: `Phishing_dataset_augmented.csv` (11,000 rows, still a
     balanced 50/50 split).

2. **Regularized retraining** — the new XGBoost model uses shallower trees,
   L1/L2 regularization, and row/feature subsampling (`max_depth=3` instead
   of `7`, `learning_rate=0.1` instead of `0.4`, etc.) as an extra safety net
   on top of the augmented data.

3. **Bug fix in `app.py`** — the Legitimate/Phishing result boxes were
   swapped (red box for Legitimate, green for Phishing). Fixed so green =
   Legitimate, red = Phishing. This was the only change made to the app —
   everything else (layout, questions, wording) is untouched.

## Results

| | Original model | Augmented + regularized model |
|---|---|---|
| Test Accuracy | 85.6% | 79.8% |
| Precision | 96.2% | 88.7% |
| Recall | 73.8% | 68.4% |
| Random-combo test (200 random inputs) | 195/200 → Phishing | 168/200 → Phishing |
| Single "risky" feature alone forces Phishing? | Yes, for 4 features | No, for 3 of 4 (Have_IP, https_Domain, Right_Click). URL_Length is still a strong signal but no longer absolute (97%→96% alone, and can be outweighed by other clean features) |

**Trade-off, stated plainly:** accuracy dropped by about 6 points. This is
expected — the original model's higher accuracy partly came from those 4
overly-rigid rules, which technically "worked" on this dataset but would
likely fail badly on any real website that doesn't fit the narrow pattern.
The new model is less accurate on this specific dataset but more reasonable
in how it behaves on inputs it hasn't seen before.

Verified working examples (tested directly against the new model):
- **Fully clean profile** → Legitimate, 92.1% confidence
- **Fully dirty profile** → Phishing, 92.7% confidence

## Files in this folder

- `website_legitimacy_augmented.ipynb` — full notebook: same structure as
  the original (imports → EDA → train/test split → 5 models compared →
  save model), plus the diagnosis and augmentation steps, already executed
  with real outputs and plots
- `Phishing_dataset_augmented.csv` — the new 11,000-row dataset
- `phishing_model.pkl` — the new trained model (same filename as before, so
  the app works without any path changes)
- `app.py` — same Streamlit app, only the red/green bug fixed
- `requirements.txt` — same dependencies as before

## Running it

```bash
pip install -r requirements.txt
streamlit run app.py
```

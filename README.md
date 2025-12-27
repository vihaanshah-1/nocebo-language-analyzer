## Overview
This project is an educational NLP tool that analyzes patient-facing medical text
(e.g., consent forms or procedure instructions) to identify language that may
unintentionally increase patient anxiety (nocebo-risk language) and suggest
more neutral alternatives.

This work builds on research into the nocebo effect and explores how language
choices can shape patient expectations in healthcare settings.
Live demo: https://nocebo-language-analyzer.streamlit.app/

---

## Why this matters
The nocebo effect refers to adverse symptoms driven by negative expectations
rather than physiological causes. In medical communication, wording that is
overly alarming, directive, or uncertain can unintentionally increase anxiety.

This project investigates how such language patterns can be detected using
natural language processing and reframed more neutrally.

---

## What the tool does
- Splits input text into individual sentences
- Assigns a **risk label (0–3)** to each sentence:
  - **0** = neutral
  - **1** = mild anxiety trigger
  - **2** = moderate anxiety trigger
  - **3** = high anxiety trigger
- Identifies trigger categories (e.g., threat intensity, directive harshness)
- Suggests neutral rewrite alternatives (prototype)

---

## Example usage (local)
```bash
python3 nocebo_analyzer.py You must not drive after sedation. Rare complications include stroke.
```

## Project files
- `nocebo_analyzer.py` — core analysis logic
- `nocebo_model.pkl` — trained baseline classifier (TF-IDF + logistic regression)
- `nocebo_dataset.csv` — labeled sentence dataset
- `nocebo_rubric.txt` — labeling rubric for risk categories
- `nocebo_rewrite_suggestions.csv` — example neutral rewrites
- `nocebo_report.md` — research-style write-up (methods, results, limitations)
- `model_report.txt` — model evaluation metrics

---

## Ethics and limitations
This project is an **educational research prototype** and is **not medical advice**.

- Outputs should not be used to make clinical decisions
- Results should not be used to edit or approve clinical consent documents
  without professional review
- The dataset is limited in size and scope
- Risk labels and rewrites are heuristic and may contain errors

Do not paste any patient-identifying or private medical information into the tool.

---

## Author
**Vihaan Shah**  
Independent student project exploring applied AI in health communication

import pandas as pd
import streamlit as st

from nocebo_analyzer import predict_nocebo_risk, suggest_rewrite

st.set_page_config(page_title="Nocebo Language Analyzer", layout="wide")

st.title("Nocebo / Placebo Language Analyzer")
st.caption("Educational tool for health-communication analysis. Not medical advice.")

st.write(
    "Paste patient-facing medical text (e.g., consent language or procedure instructions). "
    "The tool scores sentences for potential nocebo/anxiety-inducing language and suggests neutral alternatives."
)

text = st.text_area("Input text", height=220, placeholder="Paste text here...")

col1, col2 = st.columns([1, 2])
with col1:
    run = st.button("Analyze", type="primary")
with col2:
    st.markdown(
        "**Ethics note:** Educational prototype only. Do not use this tool for clinical decisions "
        "or to rewrite clinical documents without professional review."
    )

if run:
    if not text.strip():
        st.warning("Please paste some text first.")
    else:
        results = predict_nocebo_risk(text)

        if not results:
            st.info("No sentences detected. Try adding punctuation (., !, ?).")
        else:
            rows = []
            for r in results:
                sent = r.get("sentence", "")
                label = r.get("label", None)
                cats = r.get("categories", [])
                suggestion = suggest_rewrite(sent)

                rows.append({
                    "Sentence": sent,
                    "Risk label (0–3)": label,
                    "Categories": ", ".join(cats) if cats else "",
                    "Suggested neutral rewrite": suggestion
                })

            df = pd.DataFrame(rows).sort_values(by="Risk label (0–3)", ascending=False)

            st.subheader("Results")
            st.dataframe(df, use_container_width=True)

            st.subheader("Highest-risk sentences")
            top = df[df["Risk label (0–3)"] >= 2]
            if len(top) == 0:
                st.write("None scored 2–3 in this sample.")
            else:
                for _, row in top.iterrows():
                    st.markdown(f"**Sentence:** {row['Sentence']}")
                    st.markdown(f"**Risk label:** {row['Risk label (0–3)']}")
                    if row["Categories"]:
                        st.markdown(f"**Categories:** {row['Categories']}")
                    st.markdown(f"**Rewrite:** {row['Suggested neutral rewrite']}")
                    st.divider()
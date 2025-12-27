import pandas as pd
import streamlit as st

from nocebo_analyzer import predict_nocebo_risk, suggest_rewrite

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(
    page_title="Nocebo Language Analyzer",
    page_icon="🩺",
    layout="wide",
)

# ----------------------------
# Sidebar: purpose + controls
# ----------------------------
st.sidebar.title("Nocebo Language Analyzer")
st.sidebar.caption("Educational prototype • Not medical advice")

with st.sidebar.expander("Intended use (read this)", expanded=True):
    st.write(
        "This tool flags potentially anxiety-inducing (nocebo-risk) language in "
        "patient-facing medical text and suggests more neutral alternatives.\n\n"
        "**Appropriate uses:** education, research prototyping, communication review.\n\n"
        "**Not appropriate for:** clinical decision-making, final approval of consent language, "
        "or use with patient-identifying information."
    )

st.sidebar.divider()

show_only_high_risk = st.sidebar.checkbox("Show only risk ≥ 2", value=False)
auto_rewrites = st.sidebar.checkbox("Generate rewrite suggestions", value=True)
sort_by = st.sidebar.selectbox(
    "Sort results by",
    options=["Risk label (desc)", "Risk label (asc)", "Original order"],
    index=0,
)

st.sidebar.divider()
st.sidebar.caption("Tip: Avoid pasting any private/patient info.")

# ----------------------------
# Header
# ----------------------------
st.title("Nocebo / Placebo Language Analyzer")
st.write(
    "Paste patient-facing medical text (e.g., consent instructions, procedure guidance). "
    "The app splits it into sentences, assigns a **risk label (0–3)**, tags trigger categories, "
    "and optionally suggests neutral rewrites."
)

# ----------------------------
# Input area
# ----------------------------
DEFAULT_EXAMPLE = (
    "After sedation, you must not drive for 24 hours. "
    "Rare complications include stroke. "
    "If you feel unwell, seek urgent medical help."
)

if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

def load_example():
    st.session_state["input_text"] = DEFAULT_EXAMPLE

def clear_input():
    st.session_state["input_text"] = ""

colA, colB = st.columns([3, 1])

with colB:
    st.markdown("### Quick actions")
    st.button("Use example text", on_click=load_example)
    st.button("Clear", on_click=clear_input)

with colA:
    st.text_area(
        "Input text",
        height=220,
        placeholder="Paste text here…",
        key="input_text",
    )

text = st.session_state["input_text"]

analyze = st.button("Analyze", type="primary")

# ----------------------------
# Analysis (cached for speed)
# ----------------------------
@st.cache_data(show_spinner=False)
def analyze_text_cached(input_text: str):
    # predict_nocebo_risk returns a list of dicts per sentence
    return predict_nocebo_risk(input_text)

def risk_label_to_band(label: int) -> str:
    if label >= 3:
        return "High"
    if label == 2:
        return "Moderate"
    if label == 1:
        return "Mild"
    return "Neutral"

# ----------------------------
# Run
# ----------------------------
if analyze:
    if not text.strip():
        st.warning("Please paste some text first.")
        st.stop()

    with st.spinner("Analyzing…"):
        results = analyze_text_cached(text)

    if not results:
        st.info("No sentences detected. Try adding punctuation (., !, ?).")
        st.stop()

    # Build rows
    rows = []
    for idx, r in enumerate(results):
        sent = r.get("sentence", "").strip()
        label = int(r.get("label", 0))
        cats = r.get("categories", []) or []
        rewrite = suggest_rewrite(sent) if auto_rewrites else ""

        rows.append(
            {
                "Order": idx,
                "Sentence": sent,
                "Risk label": label,
                "Band": risk_label_to_band(label),
                "Categories": ", ".join(cats),
                "Suggested neutral rewrite": rewrite,
            }
        )

    df = pd.DataFrame(rows)

    # Filters
    if show_only_high_risk:
        df = df[df["Risk label"] >= 2].copy()

    # Sorting
    if sort_by == "Risk label (desc)":
        df = df.sort_values(["Risk label", "Order"], ascending=[False, True])
    elif sort_by == "Risk label (asc)":
        df = df.sort_values(["Risk label", "Order"], ascending=[True, True])
    else:
        df = df.sort_values(["Order"], ascending=True)

    # ----------------------------
    # Summary panel
    # ----------------------------
    st.subheader("Summary")

    # Counts by risk label (0-3)
    counts = (
        pd.DataFrame({"Risk label": [0, 1, 2, 3]})
        .merge(df["Risk label"].value_counts().rename_axis("Risk label").reset_index(name="Count"),
               on="Risk label",
               how="left")
        .fillna({"Count": 0})
    )
    counts["Count"] = counts["Count"].astype(int)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Neutral (0)", int(counts.loc[counts["Risk label"] == 0, "Count"].iloc[0]))
    c2.metric("Mild (1)", int(counts.loc[counts["Risk label"] == 1, "Count"].iloc[0]))
    c3.metric("Moderate (2)", int(counts.loc[counts["Risk label"] == 2, "Count"].iloc[0]))
    c4.metric("High (3)", int(counts.loc[counts["Risk label"] == 3, "Count"].iloc[0]))

    # Chart
    chart_df = counts.set_index("Risk label")[["Count"]]
    st.bar_chart(chart_df)

    # ----------------------------
    # Results table
    # ----------------------------
    st.subheader("Results")
    display_df = df.drop(columns=["Order"])
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Download
    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download results (CSV)",
        data=csv_bytes,
        file_name="nocebo_language_results.csv",
        mime="text/csv",
    )

    # ----------------------------
    # High-risk callouts
    # ----------------------------
    st.subheader("High-risk callouts (risk ≥ 2)")
    high = df[df["Risk label"] >= 2].copy().sort_values(["Risk label", "Order"], ascending=[False, True])

    if high.empty:
        st.write("No sentences scored 2–3 in this sample.")
    else:
        for _, row in high.iterrows():
            st.markdown(f"**Sentence:** {row['Sentence']}")
            st.markdown(f"**Risk label:** {row['Risk label']} ({row['Band']})")
            if row["Categories"]:
                st.markdown(f"**Categories:** {row['Categories']}")
            if auto_rewrites and row["Suggested neutral rewrite"]:
                st.markdown(f"**Suggested rewrite:** {row['Suggested neutral rewrite']}")
            st.divider()

    # ----------------------------
    # About / Methods (collapsed)
    # ----------------------------
    with st.expander("About & Method (for reviewers)"):
        st.write(
            "This prototype uses a baseline NLP classifier to label sentences for potential nocebo-risk patterns. "
            "Categories are heuristic and meant to support communication review, not replace clinical judgment.\n\n"
            "**Limitations:** small dataset, domain shift across institutions, and imperfect rewrite suggestions. "
            "Always involve qualified professionals for clinical materials."
        )

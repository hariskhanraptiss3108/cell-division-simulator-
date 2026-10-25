"""Interactive Cell Division Simulator built with Python and Streamlit."""
import streamlit as st
import pandas as pd
from biology import (
    MITOSIS_STAGES, CELL_CYCLE, MEIOSIS_STAGES, COMPARISON, QUIZ,
    get_mitosis_stage, get_meiosis_stage, chromosome_counts
)

st.set_page_config(page_title="Cell Division Simulator", page_icon="🧬", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1250px; padding-top: 1.5rem; padding-bottom: 3rem;}
div[data-testid="stMetric"] {border: 1px solid rgba(120,140,160,.3); padding: 12px; border-radius: 12px;}
.stage-card {padding: 1rem; border: 1px solid rgba(120,140,160,.35); border-radius: 14px; margin: .5rem 0;}
.small-muted {font-size:.9rem; opacity:.8;}
</style>
""", unsafe_allow_html=True)

st.title("🧬 Cell Division Simulator")
st.caption("An interactive biology learning project • Simplified diploid model: 2n = 4")

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a module", [
        "Mitosis simulator", "Cell cycle explorer", "Meiosis simulator",
        "Genetic variation", "Mitosis vs meiosis", "Separation errors", "Quiz"
    ])
    st.divider()
    st.caption("Teaching model only. Drawings are schematic, not microscopy images.")

def show_metrics(chromosomes, chromatids, dna, cells, ploidy=None):
    a,b,c,d = st.columns(4)
    a.metric("Chromosomes", chromosomes)
    b.metric("Chromatids", chromatids)
    c.metric("DNA content", dna)
    d.metric("Cells / products", cells)
    if ploidy:
        st.caption(f"Ploidy/counting context: {ploidy}")

def chromosome_diagram(stage_name, duplicated=True, separated=False, two_cells=False, labels=True, crossing=False):
    """Draw a small schematic using Streamlit columns and Unicode/HTML shapes."""
    st.markdown("""
    <style>
    .cellrow{display:flex;gap:22px;justify-content:center;align-items:center;flex-wrap:wrap;padding:18px 0}
    .cellshape{width:300px;height:180px;border:3px solid #7696b5;border-radius:50%;display:flex;align-items:center;justify-content:center;gap:20px;position:relative;background:rgba(100,150,200,.06)}
    .nucleusshape{position:absolute;inset:24px 50px;border:2px dashed #9ba9b8;border-radius:50%}
    .pair{height:54px;width:12px;position:relative;display:inline-block;margin:0 3px}
    .rod{position:absolute;width:7px;height:50px;border-radius:6px;left:0;top:0}
    .rod2{position:absolute;width:7px;height:50px;border-radius:6px;left:7px;top:0;transform:rotate(12deg)}
    .red{background:#e76f51}.teal{background:#2a9d8f}.purple{background:#7665a8}.gold{background:#d9a441}
    .single{height:35px;width:7px;border-radius:5px;display:inline-block;margin:0 4px}
    .pole{position:absolute;top:48%;width:11px;height:11px;background:#6279ad;border-radius:50%}
    .poleleft{left:10px}.poleright{right:10px}
    </style>
    """, unsafe_allow_html=True)
    colours = ["red","teal","purple","gold"]
    if two_cells:
        cell_html = ""
        for _ in range(2):
            rods = "".join(f'<span class="single {col}"></span>' for col in colours[:2])
            cell_html += f'<div class="cellshape" style="width:220px;height:130px">{rods}</div>'
        st.markdown(f'<div class="cellrow">{cell_html}</div>', unsafe_allow_html=True)
    else:
        if separated:
            rods = "".join(f'<span class="single {col}" style="margin:0 2px"></span>' for col in colours)
            content = f'<div style="display:flex;justify-content:space-between;align-items:center;width:78%"><div>{rods}</div><div>{rods}</div></div>'
        else:
            pairs = ""
            for col in colours:
                if duplicated:
                    pairs += f'<span class="pair"><i class="rod {col}"></i><i class="rod2 {col}"></i></span>'
                else:
                    pairs += f'<span class="single {col}"></span>'
            content = pairs
        nucleus = '<div class="nucleusshape"></div>' if stage_name in ("G1 phase", "After S phase", "Prophase", "Before meiosis (after S phase)", "Prophase I") else ""
        poles = '<span class="pole poleleft"></span><span class="pole poleright"></span>'
        st.markdown(f'<div class="cellrow"><div class="cellshape">{nucleus}{poles}{content}</div></div>', unsafe_allow_html=True)
    if labels:
        st.caption("Schematic illustration only. Colours distinguish modelled chromosome types; they do not represent real microscopy colours.")

if page == "Mitosis simulator":
    st.header("Mitosis simulator")
    st.write("Move through the stages and watch the chromosome counter update from the biological model.")
    names = [s.name for s in MITOSIS_STAGES]
    if "mitosis_index" not in st.session_state:
        st.session_state.mitosis_index = 0
    idx = st.select_slider("Stage", options=list(range(len(names))), value=st.session_state.mitosis_index, format_func=lambda i: names[i], key="mitosis_slider")
    st.session_state.mitosis_index = idx
    stage = get_mitosis_stage(idx)
    c1,c2,c3 = st.columns([1,2,1])
    with c1:
        if st.button("← Previous", disabled=idx == 0, use_container_width=True):
            st.session_state.mitosis_index = idx-1
            st.rerun()
    with c2:
        st.progress((idx+1)/len(MITOSIS_STAGES), text=f"Stage {idx+1} of {len(MITOSIS_STAGES)}")
    with c3:
        if st.button("Next →", disabled=idx == len(MITOSIS_STAGES)-1, use_container_width=True):
            st.session_state.mitosis_index = idx+1
            st.rerun()
    labels = st.toggle("Show diagram labels / legend", value=True)
    left,right = st.columns([1.1,1])
    with left:
        chromosome_diagram(stage.name, duplicated=idx not in (0,6), separated=idx in (4,5), two_cells=idx==6, labels=labels)
    with right:
        st.subheader(stage.name)
        st.write(stage.description)
        st.info(stage.detail)
        show_metrics(stage.chromosomes_per_cell, stage.chromatids_per_cell, stage.dna_content, stage.cell_count, stage.ploidy)
    st.markdown("**Important counting rule:** at anaphase, separated sister chromatids count as individual chromosomes. The whole undivided cell therefore contains eight chromosomes at that moment.")

elif page == "Cell cycle explorer":
    st.header("Cell cycle explorer")
    st.write("Select a phase to learn what happens before, during and after division.")
    phase_names = [x["name"] for x in CELL_CYCLE]
    selected = st.selectbox("Cell-cycle phase", phase_names)
    phase = next(x for x in CELL_CYCLE if x["name"] == selected)
    st.subheader(phase["name"])
    st.write(phase["summary"])
    st.info(phase["purpose"])
    st.metric("Does DNA replication occur in this phase?", phase["replication"])
    st.markdown("### The cycle at a glance")
    cols = st.columns(len(CELL_CYCLE))
    for col, item in zip(cols, CELL_CYCLE):
        with col:
            st.markdown(f"**{item['name']}**")
            st.caption("DNA replication" if item["replication"] == "Yes" else "No DNA replication")
            if item["name"] == selected:
                st.success("Selected")
    st.warning("Interphase includes G1, S and G2. It happens before mitosis; it is not itself a stage of mitosis.")

elif page == "Meiosis simulator":
    st.header("Meiosis simulator")
    st.write("Follow the reduction from a diploid cell to four simplified haploid products.")
    names = [x["name"] for x in MEIOSIS_STAGES]
    if "meiosis_index" not in st.session_state:
        st.session_state.meiosis_index = 0
    idx = st.select_slider("Meiosis stage", options=list(range(len(names))), value=st.session_state.meiosis_index, format_func=lambda i: names[i], key="meiosis_slider")
    st.session_state.meiosis_index = idx
    stage = get_meiosis_stage(idx)
    c1,c2,c3 = st.columns([1,2,1])
    with c1:
        if st.button("← Previous", key="meiosis_prev", disabled=idx==0, use_container_width=True):
            st.session_state.meiosis_index = idx-1
            st.rerun()
    with c2:
        st.progress((idx+1)/len(MEIOSIS_STAGES), text=f"Stage {idx+1} of {len(MEIOSIS_STAGES)}")
    with c3:
        if st.button("Next →", key="meiosis_next", disabled=idx==len(MEIOSIS_STAGES)-1, use_container_width=True):
            st.session_state.meiosis_index = idx+1
            st.rerun()
    chromosome_diagram(stage["name"], duplicated=idx<6, separated=idx in (3,6), two_cells=idx in (4,5,7))
    st.subheader(stage["name"])
    st.write(stage["description"])
    show_metrics(stage["chromosomes"], stage["chromatids"], stage["dna"], stage["cells"], stage["ploidy"])
    st.caption("Counting convention differs by stage: values marked 'per cell' describe each cell/product, while 'total' describes the undivided cell.")

elif page == "Genetic variation":
    st.header("Genetic variation experiment")
    st.write("This is a simplified illustration of how crossing over and independent assortment can create new combinations.")
    crossing = st.toggle("Enable a simplified crossing-over event", value=True)
    assortment = st.selectbox("Independent assortment example", ["Orientation A", "Orientation B"])
    st.markdown("### Chromosome segment model")
    if crossing:
        st.markdown("""
        <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">
          <div style="border:1px solid #aaa;border-radius:12px;padding:12px"><b>Before</b><br><span style="color:#d45a4b">A—B—C</span><br><span style="color:#287e75">a—b—c</span></div>
          <div style="font-size:24px">→</div>
          <div style="border:1px solid #aaa;border-radius:12px;padding:12px"><b>After exchange</b><br><span style="color:#d45a4b">A—B—c</span><br><span style="color:#287e75">a—b—C</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Illustrative exchange between non-sister chromatids of homologous chromosomes; segment letters are placeholders, not a real gene map.")
    else:
        st.info("Crossing over is switched off in this example. The model shows the original segment combinations A—B—C and a—b—c.")
    if assortment == "Orientation A":
        st.write("Orientation A: one possible arrangement sends the first homologue of pair 1 with the first homologue of pair 2 to the same pole.")
    else:
        st.write("Orientation B: a different orientation can send a different combination of homologues to a pole.")
    st.markdown("### Key terms")
    st.markdown("- **Homologous chromosomes:** a pair carrying the same kinds of genes, potentially with different alleles.\n- **Sister chromatids:** replicated copies of one chromosome.\n- **Non-sister chromatids:** chromatids from the two homologous chromosomes.\n- **Alleles:** alternative versions of a gene.\n- **Crossing over:** exchange of corresponding DNA segments between non-sister chromatids in prophase I.\n- **Independent assortment:** different possible orientations of homologous pairs at metaphase I.")
    st.warning("This module illustrates concepts qualitatively. It does not calculate real recombination probabilities.")

elif page == "Mitosis vs meiosis":
    st.header("Mitosis vs meiosis")
    st.dataframe(pd.DataFrame(COMPARISON, columns=["Feature", "Mitosis", "Meiosis"]), hide_index=True, use_container_width=True)
    st.subheader("Quick comparison")
    st.write("Mitosis supports growth, tissue maintenance and repair. Meiosis contributes to sexual reproduction by producing haploid cells. Crossing over and independent assortment usually increase genetic variation in meiosis.")
    st.markdown("### Check your understanding")
    q = st.radio("Which process separates homologous chromosomes?", ["Mitosis", "Meiosis I", "Meiosis II"], key="compare_question")
    if st.button("Check comparison answer"):
        if q == "Meiosis I":
            st.success("Correct. Homologous chromosomes separate in anaphase I.")
        else:
            st.error("Not quite. Homologous chromosomes separate during meiosis I; sister chromatids separate in mitosis and meiosis II.")

elif page == "Separation errors":
    st.header("Chromosome separation error demonstration")
    st.write("Choose a simplified nondisjunction scenario. The counts illustrate possible outcomes, not a diagnosis or prediction about any person.")
    mode = st.radio("Scenario", ["Normal mitosis", "Mitosis: sister chromatid nondisjunction", "Meiosis I: homologous chromosome nondisjunction", "Meiosis II: sister chromatid nondisjunction"])
    if mode == "Normal mitosis":
        st.success("Expected simplified result: two daughter cells, each with 4 chromosomes.")
        st.dataframe(pd.DataFrame([{"Daughter": "A", "Chromosomes": 4}, {"Daughter": "B", "Chromosomes": 4}]), hide_index=True)
    elif mode == "Mitosis: sister chromatid nondisjunction":
        st.warning("One simplified outcome: both chromatids from one chromosome move to the same daughter cell.")
        st.dataframe(pd.DataFrame([{"Daughter": "A", "Chromosomes": 5}, {"Daughter": "B", "Chromosomes": 3}]), hide_index=True)
    elif mode == "Meiosis I: homologous chromosome nondisjunction":
        st.warning("One homologous pair fails to separate in meiosis I. After meiosis II, this simplified case produces two n+1 products and two n−1 products.")
        st.dataframe(pd.DataFrame([{"Product": "1", "Chromosomes": 3}, {"Product": "2", "Chromosomes": 3}, {"Product": "3", "Chromosomes": 1}, {"Product": "4", "Chromosomes": 1}]), hide_index=True)
    else:
        st.warning("One chromosome's sister chromatids fail to separate in meiosis II in one of the two cells. This simplified case produces one n+1 product, one n−1 product and two normal products.")
        st.dataframe(pd.DataFrame([{"Product": "1", "Chromosomes": 3}, {"Product": "2", "Chromosomes": 1}, {"Product": "3", "Chromosomes": 2}, {"Product": "4", "Chromosomes": 2}]), hide_index=True)
    st.caption("These are simplified chromosome-count outcomes for one modelled chromosome. Real outcomes depend on the biological context.")

elif page == "Quiz":
    st.header("Cell division quiz")
    st.write("Eight questions covering DNA replication, chromosome counting and meiosis.")
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    with st.form("quiz_form"):
        for i, item in enumerate(QUIZ):
            st.markdown(f"**{i+1}. {item['q']}**")
            answer = st.radio("Choose one", item["options"], key=f"quiz_{i}", index=None, horizontal=False)
            st.session_state.quiz_answers[i] = answer
        submitted = st.form_submit_button("Mark quiz")
    if submitted:
        st.session_state.quiz_submitted = True
    if st.session_state.quiz_submitted:
        score = 0
        for i, item in enumerate(QUIZ):
            answer = st.session_state.quiz_answers.get(i)
            correct = item["options"][item["answer"]]
            if answer == correct:
                score += 1
                st.success(f"Q{i+1}: Correct. {item['why']}")
            else:
                st.error(f"Q{i+1}: Correct answer: **{correct}**. {item['why']}")
        st.metric("Your score", f"{score} / {len(QUIZ)}")
        if st.button("Restart quiz"):
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()

st.divider()
st.caption("Educational model, not a substitute for laboratory observation. Chromosome diagrams are schematic and simplified.")

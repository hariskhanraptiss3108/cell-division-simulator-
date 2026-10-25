"""Biological state and calculations for the Cell Division Simulator.

Teaching model assumptions:
- Starting cell is diploid with 2n = 4 (two homologous pairs).
- C units measure nuclear DNA relative to one haploid genome.
- Replication doubles DNA and chromatid count, not chromosome count.
- At mitotic anaphase, separated sister chromatids are individual chromosomes.
- The model is schematic and is not a quantitative model of all real cell biology.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Stage:
    key: str
    name: str
    chromosomes_per_cell: int
    chromatids_per_cell: int
    dna_content: str
    cell_count: int
    ploidy: str
    description: str
    detail: str

MITOSIS_STAGES = [
    Stage("g1", "G1 phase", 4, 4, "2C", 1, "Diploid (2n)", "The cell grows and carries out its normal functions.", "Each chromosome consists of one chromatid. DNA replication has not yet occurred in this cycle."),
    Stage("s", "After S phase", 4, 8, "4C", 1, "Diploid (2n)", "DNA has replicated, but the cell has not divided.", "Each of the four chromosomes now has two sister chromatids joined at a centromere. Chromosome number stays at four; DNA content doubles."),
    Stage("prophase", "Prophase", 4, 8, "4C", 1, "Diploid (2n)", "Chromosomes condense and the mitotic spindle begins to form.", "In a typical animal cell, the centrosomes move apart. The nuclear envelope breaks down during prometaphase, which some courses group with prophase."),
    Stage("metaphase", "Metaphase", 4, 8, "4C", 1, "Diploid (2n)", "Duplicated chromosomes align individually at the metaphase plate.", "Spindle microtubules attach to kinetochores. Each chromosome is positioned so sister chromatids can be distributed to opposite poles."),
    Stage("anaphase", "Anaphase", 8, 8, "4C total", 1, "Chromosomes separating", "Sister chromatids separate and move towards opposite poles.", "Once separated, each former chromatid is counted as an individual daughter chromosome. There are eight chromosomes in the undivided cell, four moving towards each pole."),
    Stage("telophase", "Telophase", 8, 8, "4C total", 1, "Two chromosome groups", "Chromosomes reach opposite poles and new nuclear envelopes form.", "The cell is still one cell until cytokinesis finishes. Each new nucleus normally receives four chromosomes and approximately 2C of nuclear DNA."),
    Stage("cytokinesis", "After cytokinesis", 4, 4, "2C per daughter cell", 2, "Diploid (2n) per daughter", "The cytoplasm divides, producing two daughter cells.", "Each daughter cell normally receives four chromosomes and 2C nuclear DNA. Daughter cells are usually genetically very similar, though not identical in every biological respect."),
]

CELL_CYCLE = [
    {"name":"G1", "replication":"No", "summary":"Cell growth and normal cell activity.", "purpose":"Builds cell components and checks conditions before DNA synthesis."},
    {"name":"S", "replication":"Yes", "summary":"DNA is replicated.", "purpose":"Creates sister chromatids so each daughter cell can receive a copy of each chromosome."},
    {"name":"G2", "replication":"No", "summary":"Further growth and preparation for division.", "purpose":"The cell checks replicated DNA and prepares division machinery."},
    {"name":"M phase", "replication":"No", "summary":"Mitosis separates chromosomes into two nuclei.", "purpose":"Distributes duplicated chromosomes between the two future daughter cells."},
    {"name":"Cytokinesis", "replication":"No", "summary":"The cytoplasm divides.", "purpose":"Separates the cell into daughter cells; in animal cells a cleavage furrow forms."},
]

MEIOSIS_STAGES = [
    {"name":"Before meiosis (after S phase)", "chromosomes":4, "chromatids":8, "dna":"4C total", "cells":1, "ploidy":"Diploid", "description":"DNA replication happens once before meiosis I. There is no new replication before meiosis II."},
    {"name":"Prophase I", "chromosomes":4, "chromatids":8, "dna":"4C total", "cells":1, "ploidy":"Diploid", "description":"Homologous chromosomes pair. Crossing over may exchange DNA segments between non-sister chromatids."},
    {"name":"Metaphase I", "chromosomes":4, "chromatids":8, "dna":"4C total", "cells":1, "ploidy":"Diploid", "description":"Homologous pairs align at the equator. Their orientation contributes to independent assortment."},
    {"name":"Anaphase I", "chromosomes":4, "chromatids":8, "dna":"4C total", "cells":1, "ploidy":"Separating homologues", "description":"Homologous chromosomes separate; sister chromatids remain joined."},
    {"name":"After meiosis I", "chromosomes":2, "chromatids":4, "dna":"2C per cell", "cells":2, "ploidy":"Haploid (n)", "description":"Two haploid cells form. Each chromosome still consists of two sister chromatids."},
    {"name":"Metaphase II", "chromosomes":2, "chromatids":4, "dna":"2C per cell", "cells":2, "ploidy":"Haploid (n)", "description":"Chromosomes align individually in each haploid cell."},
    {"name":"Anaphase II", "chromosomes":4, "chromatids":4, "dna":"2C per cell, before division completes", "cells":2, "ploidy":"Separating sister chromatids", "description":"Sister chromatids separate in each cell and are counted as individual chromosomes."},
    {"name":"After meiosis II", "chromosomes":2, "chromatids":2, "dna":"1C per product", "cells":4, "ploidy":"Haploid (n)", "description":"The simplified model ends with four haploid products, each with two chromosomes."},
]

COMPARISON = [
    ("Number of divisions", "One", "Two"),
    ("DNA replication", "Once before mitosis", "Once before meiosis I; none between I and II"),
    ("Typical products in this model", "Two daughter cells", "Four haploid products"),
    ("Ploidy of products", "Same ploidy as starting cell", "Haploid"),
    ("What separates first?", "Sister chromatids at anaphase", "Homologous chromosomes at anaphase I"),
    ("What separates in second division?", "Not applicable", "Sister chromatids at anaphase II"),
    ("Genetic outcome", "Usually very similar daughter cells", "Variation can arise from crossing over and independent assortment"),
    ("Main role", "Growth, tissue maintenance and repair", "Produces haploid cells for sexual reproduction"),
]

QUIZ = [
    {"q":"After S phase in the 2n = 4 model, how many chromosomes are present?", "options":["2","4","8"], "answer":1, "why":"There are still four chromosomes. Each chromosome has two sister chromatids, so there are eight chromatids and 4C DNA."},
    {"q":"What separates during mitotic anaphase?", "options":["Homologous chromosome pairs","Sister chromatids","The nuclear envelope only"], "answer":1, "why":"Sister chromatids separate and each is then counted as an individual daughter chromosome."},
    {"q":"What separates during anaphase I of meiosis?", "options":["Homologous chromosomes","Sister chromatids","DNA bases"], "answer":0, "why":"Meiosis I separates homologous chromosomes while sister chromatids generally remain together."},
    {"q":"When does DNA replication occur in the cell cycle?", "options":["G1","S phase","M phase"], "answer":1, "why":"DNA synthesis occurs in S phase before mitosis or meiosis begins."},
    {"q":"What does haploid mean?", "options":["One set of chromosomes","Two sets of chromosomes","No DNA"], "answer":0, "why":"Haploid cells contain one set of chromosomes; in this model n = 2."},
    {"q":"Crossing over usually occurs between which chromatids?", "options":["Sister chromatids of one chromosome","Non-sister chromatids of homologous chromosomes","Unrelated cells"], "answer":1, "why":"During prophase I, non-sister chromatids of homologous chromosomes can exchange corresponding DNA segments."},
    {"q":"How many daughter cells are normally produced by a completed mitotic division?", "options":["One","Two","Four"], "answer":1, "why":"Mitosis followed by cytokinesis normally produces two daughter cells."},
    {"q":"Does meiosis II have another round of DNA replication before it?", "options":["Yes","No","Only in every second cell"], "answer":1, "why":"DNA replication occurs before meiosis I, not between meiosis I and meiosis II."},
]

def get_mitosis_stage(index: int) -> Stage:
    return MITOSIS_STAGES[max(0, min(int(index), len(MITOSIS_STAGES) - 1))]

def get_meiosis_stage(index: int) -> dict:
    return MEIOSIS_STAGES[max(0, min(int(index), len(MEIOSIS_STAGES) - 1))]

def chromosome_counts(stage_key: str) -> dict:
    """Return a copy of counts for a mitosis stage, useful for tests and other interfaces."""
    for stage in MITOSIS_STAGES:
        if stage.key == stage_key:
            return {
                "chromosomes": stage.chromosomes_per_cell,
                "chromatids": stage.chromatids_per_cell,
                "dna": stage.dna_content,
                "cells": stage.cell_count,
            }
    raise ValueError(f"Unknown mitosis stage key: {stage_key}")

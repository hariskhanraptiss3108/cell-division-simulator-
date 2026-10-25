import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from biology import (
    MITOSIS_STAGES, MEIOSIS_STAGES, CELL_CYCLE, get_mitosis_stage,
    get_meiosis_stage, chromosome_counts
)

class BiologyTests(unittest.TestCase):
    def test_g1_counts(self):
        self.assertEqual(chromosome_counts("g1"), {"chromosomes":4,"chromatids":4,"dna":"2C","cells":1})

    def test_replication_doubles_chromatids_not_chromosomes(self):
        self.assertEqual(MITOSIS_STAGES[1].chromosomes_per_cell, 4)
        self.assertEqual(MITOSIS_STAGES[1].chromatids_per_cell, 8)
        self.assertEqual(MITOSIS_STAGES[1].dna_content, "4C")

    def test_metaphase_counts(self):
        self.assertEqual((MITOSIS_STAGES[3].chromosomes_per_cell, MITOSIS_STAGES[3].chromatids_per_cell), (4,8))

    def test_anaphase_counting(self):
        self.assertEqual((MITOSIS_STAGES[4].chromosomes_per_cell, MITOSIS_STAGES[4].chromatids_per_cell), (8,8))
        self.assertEqual(MITOSIS_STAGES[4].dna_content, "4C total")

    def test_cytokinesis_outcome(self):
        final = MITOSIS_STAGES[-1]
        self.assertEqual((final.chromosomes_per_cell, final.chromatids_per_cell, final.cell_count), (4,4,2))
        self.assertEqual(final.dna_content, "2C per daughter cell")

    def test_meiosis_reduction_and_products(self):
        self.assertEqual(MEIOSIS_STAGES[4]["cells"], 2)
        self.assertEqual(MEIOSIS_STAGES[4]["chromosomes"], 2)
        self.assertEqual(MEIOSIS_STAGES[-1]["cells"], 4)
        self.assertEqual(MEIOSIS_STAGES[-1]["chromosomes"], 2)

    def test_stage_index_clamping(self):
        self.assertEqual(get_mitosis_stage(-1).key, "g1")
        self.assertEqual(get_mitosis_stage(999).key, "cytokinesis")
        self.assertEqual(get_meiosis_stage(-1)["name"], MEIOSIS_STAGES[0]["name"])
        self.assertEqual(get_meiosis_stage(999)["name"], MEIOSIS_STAGES[-1]["name"])

    def test_cell_cycle_phases(self):
        s_phase = next(p for p in CELL_CYCLE if p["name"] == "S")
        self.assertEqual(s_phase["replication"], "Yes")
        self.assertEqual(len(CELL_CYCLE), 5)

    def test_quiz_has_answers(self):
        from biology import QUIZ
        self.assertTrue(all(0 <= q["answer"] < len(q["options"]) for q in QUIZ))

    def test_comparison_has_required_rows(self):
        from biology import COMPARISON
        self.assertGreaterEqual(len(COMPARISON), 8)

if __name__ == "__main__":
    unittest.main()

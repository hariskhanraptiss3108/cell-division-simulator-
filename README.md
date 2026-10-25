# Cell Division Simulator

A Python-based interactive biology education project for exploring mitosis, meiosis, chromosome counting and genetic variation. Built with Streamlit so the interface can run in a web browser.

## Features

- **Mitosis simulator:** navigate through G1, after S phase, prophase, metaphase, anaphase, telophase and cytokinesis.
- **Chromosome counter:** shows chromosome count, chromatid count, DNA content and cell count from the biological stage model.
- **Cell cycle explorer:** learn about G1, S, G2, M phase and cytokinesis.
- **Meiosis simulator:** explore homologous chromosome separation in meiosis I and sister chromatid separation in meiosis II.
- **Genetic variation:** a conceptual crossing-over illustration and independent-assortment examples.
- **Mitosis vs meiosis:** comparison table and check question.
- **Separation errors:** simplified outcomes for selected nondisjunction cases.
- **Quiz:** eight questions with explanations and a score.
- **Automated tests:** unit tests for key model counts and stage definitions.

## Run the app

Requires Python 3.10+ and packages in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

### Chromebook note

If you cannot install Python on your Chromebook, use a browser-based Python workspace that supports Streamlit. Upload the project files, install dependencies, and run `streamlit run app.py`. Hosted services can change their free-plan features; check the service's current terms. The project is Python, but it needs a Python runtime to execute.

## Run tests

```bash
python -m unittest discover -s tests
```

The tests check the biology model, not every browser/UI interaction. Do not describe the visual interface as fully tested unless you have tested it in the environment where you run it.

## Biological model and counting conventions

The model starts with a diploid cell where 2n = 4 (two homologous pairs). C units describe nuclear DNA content relative to one haploid genome.

| Stage | Chromosomes | Chromatids | DNA content |
|---|---:|---:|---|
| G1 | 4 | 4 | 2C |
| After S phase | 4 | 8 | 4C |
| Metaphase of mitosis | 4 | 8 | 4C |
| Anaphase of mitosis | 8 in the undivided cell | 8 | 4C total |
| Each daughter after division | 4 | 4 | 2C per daughter |

After S phase, chromosome number remains four because sister chromatids are still joined. At anaphase, separated chromatids are counted as individual chromosomes. The model uses simplified per-cell values in meiosis; read the label "per cell" or "total" carefully.

## Limitations

This project is an educational model, not a substitute for laboratory observation. The chromosome drawings are schematic, not microscopy images. Real cell division involves more complex regulation, structures and context than shown here. The genetic variation module is qualitative and does not calculate real recombination probabilities. Nondisjunction outcomes are illustrative, not diagnostic or predictive for any person.

## Scientific references

- OpenStax, *Biology 2e*: https://openstax.org/details/books/biology-2e
- NCBI Bookshelf: https://www.ncbi.nlm.nih.gov/books/

Use these sources to verify and deepen the biology. Add specific chapter or section references as you develop the project further.

## Project structure

```text
cell_division_simulator/
├── app.py
├── biology.py
├── requirements.txt
├── README.md
└── tests/
    └── test_biology.py
```

## Portfolio honesty

If AI tools helped generate or debug code, describe that assistance honestly and make sure you can explain the biological assumptions, code structure and tests you actually understand and have run.

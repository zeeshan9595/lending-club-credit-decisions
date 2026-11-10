"""Validate notebook structure without downloading data or running model cells."""
from pathlib import Path
import nbformat

NOTEBOOK = Path(__file__).resolve().parent / "lending_club_credit_decisions.ipynb"


def main():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)
    if not notebook.cells:
        raise SystemExit("Notebook contains no cells.")
    if not any(cell.cell_type == "code" for cell in notebook.cells):
        raise SystemExit("Notebook contains no code cells.")
    print(
        f"Notebook structure: PASS | cells={len(notebook.cells)} | "
        f"code_cells={sum(cell.cell_type == 'code' for cell in notebook.cells)}"
    )
    print("Model execution was not performed; Kaggle data download is required.")


if __name__ == "__main__":
    main()

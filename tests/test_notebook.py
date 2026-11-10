import unittest
from pathlib import Path
import nbformat


class NotebookStructureTests(unittest.TestCase):
    def test_notebook_is_valid_and_contains_code(self):
        path = Path(__file__).resolve().parents[1] / "lending_club_credit_decisions.ipynb"
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        self.assertTrue(notebook.cells)
        self.assertTrue(any(cell.cell_type == "code" for cell in notebook.cells))

    def test_notebook_colab_badge_targets_this_repository(self):
        path = Path(__file__).resolve().parents[1] / "lending_club_credit_decisions.ipynb"
        notebook = nbformat.read(path, as_version=4)
        first_cell = notebook.cells[0]
        self.assertIn("zeeshan9595/lending-club-credit-decisions", first_cell.source)
        self.assertIn("blob/main/lending_club_credit_decisions.ipynb", first_cell.source)


if __name__ == "__main__":
    unittest.main()


import lxml.html

from lib_test_utils import import_from_repo_path


def test_deletionlib_small_helpers():
	deletionlib = import_from_repo_path("problems/inheritance-problems/deletion_mutants/deletionlib.py")
	assert deletionlib.ensure_most_alphabetical(["a", "b", "c"]) == ["a", "b", "c"]
	assert deletionlib.ensure_most_alphabetical(["c", "b", "a"]) == ["a", "b", "c"]
	assert deletionlib.insertCommas("ABCDEF", 2) == "AB,CD,EF"
	assert deletionlib.insertCommas("ABCDE", 3) == "ABC,DE"


def test_deletionlib_fib_answer_variations_smoke():
	deletionlib = import_from_repo_path("problems/inheritance-problems/deletion_mutants/deletionlib.py")
	variations = deletionlib.generate_fib_answer_variations(["a", "b", "c", "d"])
	assert "abcd" in variations
	assert "a,b,c,d" in variations


def test_deletion_diagram_preserves_coverage_and_color_meaning() -> None:
	deletionlib = import_from_repo_path("problems/inheritance-problems/deletion_mutants/deletionlib.py")
	gene_order = list("FADBEC")
	deletions = [list("ADF"), list("BDE"), list("CE")]
	colors = {"ADF": "843b62", "BDE": "006d77", "CE": "5a3e85"}
	markup = deletionlib.make_html_table(gene_order, deletions, colors)
	fragment = lxml.html.fragment_fromstring(markup, create_parent="div")
	rows = fragment.xpath("./table/tr")
	assert "Colored regions mark deleted DNA" in fragment.text_content()
	assert [cell.text_content() for cell in rows[0]] == ["", ""] + [
		f"Gene {i+1}" for i in range(len(gene_order))] + [""]
	assert len(rows) == len(deletions) + 1
	for i, (row, deletion) in enumerate(zip(rows[1:], deletions)):
		color = colors["".join(sorted(deletion))]
		label, *cells = row
		assert label.text_content() == f"Del #{i+1}"
		assert f"color: #{color};" in label[0].get("style")
		left_flank, *cells, right_flank = cells
		for flank in (left_flank, right_flank):
			assert flank.text_content() == ""
		assert len(cells) == len(gene_order)
		for gene, cell in zip(gene_order, cells):
			assigned_fill = f"background-color: #{color};" in cell[0].get("style")
			assert assigned_fill == (gene in deletion)
			assert cell.text_content() == ""


def test_complementation_results_match_deletions_in_alphabetical_columns() -> None:
	deletionlib = import_from_repo_path("problems/inheritance-problems/deletion_mutants/deletionlib.py")
	gene_order = list("FADBEC")
	deletions = [list("ADF"), list("BDE"), list("CE")]
	colors = {"ADF": "843b62", "BDE": "006d77", "CE": "5a3e85"}
	markup = deletionlib.make_complementation_table(gene_order, deletions, colors)
	fragment = lxml.html.fragment_fromstring(markup, create_parent="div")
	rows = fragment.xpath("./table/tr")
	assert [cell.text_content() for cell in rows[0]] == ["Deletion", *list("ABCDEF")]
	expected = [["-", "+", "+", "-", "+", "-"],
		["+", "-", "+", "-", "-", "+"], ["+", "+", "-", "+", "-", "+"]]
	assert [[cell.text_content() for cell in row[1:]] for row in rows[1:]] == expected
	for i, row in enumerate(rows[1:]):
		assert row[0].text_content() == f"Del #{i+1}"
		color = colors[''.join(sorted(deletions[i]))]
		assert f"color: #{color};" in row[0][0].get("style")


def test_complementation_prompt_retains_hints_without_uncovered_gene_lists() -> None:
	deletionlib = import_from_repo_path("problems/inheritance-problems/deletion_mutants/deletionlib.py")
	markup = deletionlib.make_deletion_evidence(list("FADBEC"), [list("ADF")],
		{"ADF": "843b62"}, "complementation")
	markup += deletionlib.write_question_text(list("FADBEC"), [list("ADF")],
		{"ADF": "843b62"}, False, True, evidence_format="complementation", question_type="mc")
	fragment = lxml.html.fragment_fromstring(markup, create_parent="div")
	text = fragment.text_content()
	assert not fragment.xpath(".//ul")
	assert "Gene F" in text and "random sequence" in text
	assert "complementation (wild-type phenotype)" in text
	assert "failure to complement (mutant phenotype; the deletion uncovers the mutation)" in text
	assert "Enter your answer in the blank" not in text
	fib = deletionlib.write_question_text(list("FADBEC"), [list("ADF")],
		{"ADF": "843b62"}, False, evidence_format="complementation", question_type="fib")
	assert "Enter all six (6) gene letters in order without spaces or commas" in fib

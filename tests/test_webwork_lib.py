import pytest

import webwork_lib


def test_contains_html_table_detects_tags():
	assert webwork_lib.contains_html_table("<table><tr><td>cell</td></tr></table>")
	assert webwork_lib.contains_html_table("<TR><TD>cell</TD></TR>")
	assert webwork_lib.contains_html_table("<td rowspan=2>cell</td>")
	assert not webwork_lib.contains_html_table("table data only")
	assert not webwork_lib.contains_html_table("<div>cell</div>")
	assert not webwork_lib.contains_html_table(None)
	with pytest.raises(TypeError):
		webwork_lib.contains_html_table(123)


def test_strip_html_tags_preserves_pgml_wrappers():
	text = "alpha <span style=\"color: #e60000;\">beta</span> [<gamma>]{[\"span\", class => \"c\"]}{[\"\",\"\"]}"
	result = webwork_lib.strip_html_tags(text, preserve_pgml_wrappers=True)
	assert "alpha beta" in result
	assert "[<gamma>]" in result
	result_no_preserve = webwork_lib.strip_html_tags(text, preserve_pgml_wrappers=False)
	assert "[]" in result_no_preserve


def test_convert_sub_sup_digits_and_signs():
	text = "H<sub>2</sub>PO<sub>4</sub><sup>&ndash;</sup>"
	result = webwork_lib.convert_sub_sup(text)
	assert result == "H\u2082PO\u2084\u207B"

	text = "C<sub>&alpha;</sub>"
	result = webwork_lib.convert_sub_sup(text)
	assert result == "C\u03b1"

	text = "Ca<sup>2+</sup>"
	result = webwork_lib.convert_sub_sup(text)
	assert result == "Ca\u00b2\u207a"


def test_unescape_html_and_normalize_nbsp():
	raw = "a&nbsp;b"
	unescaped = webwork_lib.unescape_html(raw)
	assert unescaped == "a\u00a0b"
	assert webwork_lib.normalize_nbsp(unescaped) == "a b"


def test_normalize_color_value():
	color, cls = webwork_lib.normalize_color_value("#ABCDEF")
	assert color == "#abcdef"
	assert cls == "color-abcdef"

	color, cls = webwork_lib.normalize_color_value("ABCDEF")
	assert color == "#abcdef"
	assert cls == "color-abcdef"

	color, cls = webwork_lib.normalize_color_value("Indigo")
	assert color == "indigo"
	assert cls == "color-indigo"

	color, cls = webwork_lib.normalize_color_value("  #00b3b3  ")
	assert color == "#00b3b3"
	assert cls == "color-00b3b3"


def test_build_pgml_tag_wrapper():
	assert webwork_lib.build_pgml_tag_wrapper("plain") == "plain"
	assert webwork_lib.build_pgml_tag_wrapper("test", class_name="color-red") == (
		"[<test>]{[\"span\", class => \"color-red\"]}{[\"\",\"\"]}"
	)
	assert webwork_lib.build_pgml_tag_wrapper("test", style="color: #ff0000;") == (
		"[<test>]{[\"span\", style => \"color: #ff0000;\"]}{[\"\",\"\"]}"
	)


def test_extract_strict_color_span_basic():
	parsed = webwork_lib.extract_strict_color_span(
		"<span style=\"color: #e65400;\">lipids</span>"
	)
	assert parsed == ("", "lipids", "", "#e65400", False)

	parsed = webwork_lib.extract_strict_color_span(
		"<strong><span style=\"color: #e65400;\">AA</span></strong>"
	)
	assert parsed == ("", "AA", "", "#e65400", True)

	parsed = webwork_lib.extract_strict_color_span(
		"<span style=\"color: #e65400;\"><strong>AA</strong></span>"
	)
	assert parsed == ("", "AA", "", "#e65400", True)

	parsed = webwork_lib.extract_strict_color_span(
		"pre <span style=color: Indigo;>gene</span> post"
	)
	assert parsed == ("pre ", "gene", " post", "Indigo", False)

	assert webwork_lib.extract_strict_color_span(
		"<span style=\"color: #e65400;\"><em>bad</em></span>"
	) is None

	assert webwork_lib.extract_strict_color_span(
		"<span style=\"color: #e60000;\">a</span> <span style=\"color: #e60000;\">b</span>"
	) is None


def test_sanitize_text_for_html_and_span_builder():
	text = "C<sub>2</sub>H<sub>6</sub> &amp; CO<sub>2</sub>"
	result = webwork_lib.sanitize_text_for_html(text)
	assert result == "C\u2082H\u2086 &amp; CO\u2082"

	span = webwork_lib.build_html_span("ionic bond", style="color: #009900;")
	assert span == "<span style=\"color: #009900;\">ionic bond</span>"

	span = webwork_lib.build_html_span("bold", class_name="color-test pgml-bold")
	assert span == "<span class=\"color-test pgml-bold\">bold</span>"

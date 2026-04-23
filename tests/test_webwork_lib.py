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


def test_extract_strict_color_span_preserves_entities():
	# HTML entities should pass through without conversion to Unicode
	parsed = webwork_lib.extract_strict_color_span(
		"<span style=\"color: #e65400;\">&alpha;</span>"
	)
	assert parsed == ("", "&alpha;", "", "#e65400", False)

	parsed = webwork_lib.extract_strict_color_span(
		"<span style=\"color: #e65400;\">chi-square (&chi;&sup2;)</span>"
	)
	assert parsed == ("", "chi-square (&chi;&sup2;)", "", "#e65400", False)


def test_extract_strict_color_span_preserves_sub_sup():
	# sub/sup tags should pass through without conversion to Unicode
	parsed = webwork_lib.extract_strict_color_span(
		"<span style=\"color: #e65400;\">H<sub>0</sub></span>"
	)
	assert parsed == ("", "H<sub>0</sub>", "", "#e65400", False)

	# em tags should still be rejected
	assert webwork_lib.extract_strict_color_span(
		"<span style=\"color: #e65400;\">H<em>0</em></span>"
	) is None


def test_extract_strict_color_spans_preserves_entities():
	# entities and sub/sup should pass through in multi-span extraction
	segments = webwork_lib.extract_strict_color_spans(
		"level of significance, <span style=\"color: #e65400;\">&alpha;</span>"
	)
	assert len(segments) == 2
	assert segments[0] == (False, "level of significance, ", None, False)
	assert segments[1] == (True, "&alpha;", "#e65400", False)

	segments = webwork_lib.extract_strict_color_spans(
		"<span style=\"color: #e65400;\">H<sub>0</sub></span>"
	)
	assert len(segments) == 1
	assert segments[0] == (True, "H<sub>0</sub>", "#e65400", False)


def test_escape_html_preserving_entities():
	# preserves named HTML entities
	assert webwork_lib.escape_html_preserving_entities("&Delta;G") == "&Delta;G"
	assert webwork_lib.escape_html_preserving_entities("&alpha; &rarr; &beta;") == "&alpha; &rarr; &beta;"
	# preserves numeric entities
	assert webwork_lib.escape_html_preserving_entities("&#916;") == "&#916;"
	# escapes bare ampersands
	assert webwork_lib.escape_html_preserving_entities("A & B") == "A &amp; B"
	# escapes angle brackets
	assert webwork_lib.escape_html_preserving_entities("a < b > c") == "a &lt; b &gt; c"
	# handles None
	assert webwork_lib.escape_html_preserving_entities(None) == ""


def test_sanitize_text_for_html_preserves_entities():
	# HTML entities like &Delta; should pass through unchanged
	text = "&Delta;G = &minus;30 kJ/mol"
	result = webwork_lib.sanitize_text_for_html(text)
	assert "&Delta;" in result
	assert "&minus;" in result

	# bare ampersands should still be escaped
	text = "A & B"
	result = webwork_lib.sanitize_text_for_html(text)
	assert result == "A &amp; B"


def test_sanitize_replaced_text_preserves_entities():
	# entities should pass through sanitize_replaced_text unchanged
	text = "&alpha; and &beta;"
	result = webwork_lib.sanitize_replaced_text(text)
	assert "&alpha;" in result
	assert "&beta;" in result


def test_sanitize_replaced_text_preserves_sub_sup():
	# sub/sup tags should be preserved as HTML, not converted to Unicode
	text = "H<sub>0</sub>"
	result = webwork_lib.sanitize_replaced_text(text)
	assert result == "H<sub>0</sub>"
	# no Unicode subscript characters
	assert "\u2080" not in result

	# other HTML tags should still be stripped
	text = "H<em>0</em>"
	result = webwork_lib.sanitize_replaced_text(text)
	assert result == "H0"


def test_sanitize_text_for_html_and_span_builder():
	# sub/sup tags are preserved as HTML, not converted to Unicode
	text = "C<sub>2</sub>H<sub>6</sub> &amp; CO<sub>2</sub>"
	result = webwork_lib.sanitize_text_for_html(text)
	assert result == "C<sub>2</sub>H<sub>6</sub> &amp; CO<sub>2</sub>"

	span = webwork_lib.build_html_span("ionic bond", style="color: #009900;")
	assert span == "<span style=\"color: #009900;\">ionic bond</span>"

	span = webwork_lib.build_html_span("bold", class_name="color-test pgml-bold")
	assert span == "<span class=\"color-test pgml-bold\">bold</span>"

	# build_html_span preserves HTML entities in text
	span = webwork_lib.build_html_span("&Delta;G", style="color: #009900;")
	assert span == "<span style=\"color: #009900;\">&Delta;G</span>"

	# build_html_span preserves sub/sup tags
	span = webwork_lib.build_html_span("H<sub>0</sub>", style="color: #009900;")
	assert span == "<span style=\"color: #009900;\">H<sub>0</sub></span>"


def test_format_label_html_strict_span():
	color_classes = {}
	warnings = []
	text = "pre <span style=\"color: #009900;\">ion</span> post"
	result, is_bold = webwork_lib.format_label_html(
		text,
		"inline",
		color_classes,
		warnings,
	)
	assert result == "pre <span style=\"color: #009900;\">ion</span> post"
	assert is_bold is False
	assert color_classes == {}
	assert warnings == []

	result, is_bold = webwork_lib.format_label_html(
		"<span style=\"color: #009900;\">ion</span>",
		"none",
		color_classes,
		warnings,
	)
	assert result == "ion"
	assert is_bold is False


def test_smart_title_case_lowercase_sentence():
	result = webwork_lib.smart_title_case("the cell cycle and mitosis")
	assert result == "The Cell Cycle and Mitosis"


def test_smart_title_case_preserves_mixed_case_acronyms():
	# tRNA, DNA, mRNA, pH and similar must not be mangled to all-caps
	result = webwork_lib.smart_title_case("role of tRNA in translation")
	assert result == "Role of tRNA in Translation"


def test_smart_title_case_preserves_leading_lowercase_acronym():
	# pH leads the topic; its lowercase 'p' must not be promoted
	result = webwork_lib.smart_title_case("pH and enzyme activity")
	assert result == "pH and Enzyme Activity"


def test_smart_title_case_preserves_apostrophes_inside_words():
	# Franklin's must not become Franklin'S
	result = webwork_lib.smart_title_case("Franklin's Photograph 51")
	assert result == "Franklin's Photograph 51"


def test_smart_title_case_preserves_html_subscript_tag():
	# <sub>m</sub> must keep its original case, T stays capital
	input_text = "melting temperature (T<sub>m</sub>) of DNA"
	expected = "Melting Temperature (T<sub>m</sub>) of DNA"
	assert webwork_lib.smart_title_case(input_text) == expected


def test_smart_title_case_preserves_html_entity():
	# &middot; must keep its lowercase entity name
	result = webwork_lib.smart_title_case("the G&middot;U wobble base pair")
	assert result == "The G&middot;U Wobble Base Pair"


def test_smart_title_case_leading_minor_word_is_capitalized():
	# "a" is minor, but leads the title -> capitalized
	result = webwork_lib.smart_title_case(
		"a history of cytoskeleton filaments"
	)
	assert result == "A History of Cytoskeleton Filaments"


def test_smart_title_case_structure_of_trna_synthetases():
	# compound case: minor word "of" stays lowercase, tRNA keeps casing
	result = webwork_lib.smart_title_case("structure of tRNA synthetases")
	assert result == "Structure of tRNA Synthetases"


def test_perl_string_literal_plain_uses_single_quotes():
	# no apostrophe: standard single-quoted form
	assert webwork_lib.perl_string_literal("hello world") == "'hello world'"


def test_perl_string_literal_apostrophe_uses_q_braces():
	# PG Safe-compartment parser mishandles \\' inside single quotes;
	# switch to q{...} form to avoid the escape entirely
	result = webwork_lib.perl_string_literal("Franklin's Photograph 51")
	assert result == "q{Franklin's Photograph 51}"


def test_perl_string_literal_apostrophe_escapes_braces():
	# inside q{...}, literal { and } need backslash escape
	result = webwork_lib.perl_string_literal("Franklin's {edge} case")
	assert result == "q{Franklin's \\{edge\\} case}"


def test_perl_string_literal_none_returns_empty_literal():
	assert webwork_lib.perl_string_literal(None) == "''"


def test_sanitize_text_for_html_preserves_br_tag():
	# <br/> must survive; stripping it to a real \n produces literal
	# backslash-n inside Perl single-quoted strings
	result = webwork_lib.sanitize_text_for_html("line1<br/>line2")
	assert result == "line1<br/>line2"


def test_sanitize_text_for_html_normalizes_br_variants():
	# <br>, <br/>, <br /> all normalize to <br/>
	assert webwork_lib.sanitize_text_for_html("a<br>b") == "a<br/>b"
	assert webwork_lib.sanitize_text_for_html("a<br />b") == "a<br/>b"
	assert webwork_lib.sanitize_text_for_html("a<BR/>b") == "a<br/>b"

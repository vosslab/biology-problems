"""Relationship geometry and editable output contracts, without pixel snapshots."""

import dataclasses

import pytest
import lxml.etree

import pedigree_lib.family as family
import pedigree_lib.layout as layout
import pedigree_lib.html_output as html_output
import pedigree_lib.svg_output as svg_output


def cousin_family() -> family.Family:
	people = tuple(family.Person(pid, sex, pid) for pid, sex in zip('ABCDEFGHIJKL',
		('male', 'female', 'male', 'female', 'female', 'male', 'male', 'female',
		'female', 'male', 'female', 'male')))
	unions = (family.Union('A', 'B', ('C', 'D')), family.Union('C', 'E', ('G',)),
		family.Union('F', 'D', ('H',)), family.Union('G', 'H', ('I',)),
		family.Union('J', 'K', ('L',)))
	return family.Family(people, unions)


def test_cousin_union_keeps_shared_descendants_and_disconnected_family() -> None:
	pedigree = cousin_family()
	diagram = layout.lay_out(pedigree)
	assert not layout.layout_errors(diagram)
	assert sorted(p.person for p in diagram.symbols) == sorted(p.id for p in pedigree.people)
	assert pedigree.ancestors('G') & pedigree.ancestors('H') == {'A', 'B'}
	# The cousin union has two horizontal marriage strokes at its generation.
	cousin_union = next(index for index, union in enumerate(pedigree.unions)
		if pedigree.ancestors(union.father) & pedigree.ancestors(union.mother))
	row_y = next(p.y for p in diagram.symbols if p.person == 'G')
	stroke_heights = {s.y1 for s in diagram.segments
		if s.union == cousin_union and abs(s.y1 - row_y) < 5 and s.y1 == s.y2}
	assert len(stroke_heights) == 2


def test_mirror_preserves_people_labels_and_lines() -> None:
	pedigree = cousin_family()
	original = layout.lay_out(pedigree)
	mirrored = layout.lay_out(pedigree, mirror=True)
	assert not layout.layout_errors(mirrored)
	for a, b in zip(original.symbols, mirrored.symbols):
		assert a.person == b.person and a.label == b.label
		assert a.x + b.x == original.width and a.y == b.y
	assert len(original.segments) == len(mirrored.segments)


@pytest.mark.parametrize('child_count', (1, 2))
def test_descendants_center_below_their_parents(child_count: int) -> None:
	# Packing rows independently left this grandchild displaced from its parents.
	people = tuple(family.Person(pid, sex) for pid, sex in zip('fmabsc',
		('male', 'female', 'female', 'male', 'female', 'female')))
	children = ('c',)
	if child_count == 2:
		people += (family.Person('d', 'male'),)
		children = ('c', 'd')
	pedigree = family.Family(people,
		(family.Union('f', 'm', ('a', 'b')), family.Union('b', 's', children)))
	diagram = layout.lay_out(pedigree)
	x = {symbol.person: symbol.x for symbol in diagram.symbols}
	assert not layout.layout_errors(diagram)
	for union in pedigree.unions:
		center = (x[union.father] + x[union.mother]) / 2
		assert center == pytest.approx((min(x[p] for p in union.children)
			+ max(x[p] for p in union.children)) / 2)
	if child_count == 1:
		descent = [line for line in diagram.segments if line.union == 1 and line.y1 != line.y2]
		assert len(descent) == 1
		assert descent[0].x1 == descent[0].x2 == pytest.approx(x['c'])
	# Reject shifted input at the relationship-to-segment boundary as well.
	symbols = {symbol.person: symbol for symbol in diagram.symbols}
	symbols['c'] = dataclasses.replace(symbols['c'], x=x['c'] + 10)
	with pytest.raises(ValueError, match='Offspring must be centered'):
		layout._segments(pedigree, symbols)


def test_marrying_in_spouse_can_move_inward_to_compact_a_descendant_chain() -> None:
	people = tuple(family.Person(pid, sex) for pid, sex in zip('ABCDEFGHIJKLM',
		('female', 'male', 'female', 'male', 'male', 'male', 'male',
		'female', 'female', 'male', 'male', 'male', 'male')))
	pedigree = family.Family(people, (
		family.Union('B', 'A', ('F', 'E', 'D', 'C')),
		family.Union('G', 'C', ('I',)), family.Union('F', 'H', ('K', 'L')),
		family.Union('J', 'I', ('M',))))
	diagram = layout.lay_out(pedigree, mirror=True)
	x = {symbol.person: symbol.x for symbol in diagram.symbols}
	assert not layout.layout_errors(diagram)
	assert x['I'] < x['J']
	assert x['M'] == pytest.approx((x['I'] + x['J']) / 2)
	assert abs(x['I'] - x['J']) == pytest.approx(2 * layout.RADIUS + layout.SIBLING_GAP)
	# The descendant chain fits inside the widest generation, without a left protrusion.
	assert min(x.values()) == min(x[p] for p in 'CDEFGH')
	assert max(x.values()) == max(x[p] for p in 'CDEFGH')


def test_geometry_gate_rejects_crossings_and_obscured_people() -> None:
	pedigree = cousin_family()
	diagram = layout.lay_out(pedigree)
	p = diagram.symbols[0]
	line = layout.Segment(p.x - 30, p.y, p.x + 30, p.y, 99)
	invalid = dataclasses.replace(diagram, segments=diagram.segments + (line,))
	assert any('passes through person' in error for error in layout.layout_errors(invalid))
	with pytest.raises(ValueError, match='passes through person'):
		html_output.render_html(invalid, {})


def test_renderers_keep_carriers_and_escape_editable_labels() -> None:
	pedigree = family.Family((family.Person('a', 'female', '<A&B>'),), ())
	diagram = layout.lay_out(pedigree)
	observations = {'a': family.Observation(False, carrier=True)}
	html = html_output.render_html(diagram, observations)
	svg = svg_output.render_svg(diagram, observations)
	parser = lxml.etree.XMLParser(resolve_entities=False, no_network=True)
	root = lxml.etree.fromstring(svg.encode('utf-8'), parser=parser)
	assert html.count('<table ') == 1 and 'linear-gradient' in html
	assert '&lt;A&amp;B&gt;' in html
	assert root.find('{http://www.w3.org/2000/svg}text').text == '<A&B>'
	assert root.find('{http://www.w3.org/2000/svg}path') is not None

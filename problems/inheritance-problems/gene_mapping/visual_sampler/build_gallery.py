#!/usr/bin/env python3
"""Build a visual comparison gallery for existing gene-mapping question data."""

# Standard Library
import html
import os
import random
import sys
import argparse
import contextlib
import io
import importlib.util
import itertools
import string

# PIP3 modules
import lxml.etree


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
GENE_MAPPING_DIR = os.path.join(REPO_ROOT, 'problems', 'inheritance-problems', 'gene_mapping')
sys.path.insert(0, GENE_MAPPING_DIR)

# Local repo modules
import gene_map_class_lib as gmc
import genemaplib as gml
import bptools
import genemap_art.phenotype_art as phenotype_art
import genemap_art.asci as asci
import genemap_art.individual_phenotypes as individual_phenotypes
import phenotypes_for_flies


OUT_DIR = os.path.join(REPO_ROOT, 'output_gene_mapping_visuals')
PALETTE = tuple(phenotype_art.GENE_COLORS.values())


def esc(value: object) -> str:
	"""Return escaped HTML text."""
	text_value = html.escape(str(value))
	return text_value


def quietly(function, *args, **kwargs):
	"""Run legacy helpers without their console diagnostics."""
	with contextlib.redirect_stdout(io.StringIO()):
		result = function(*args, **kwargs)
	return result


def traits_from_name(name: str) -> set:
	"""Return illustration traits represented in a phenotype description."""
	traits = set()
	for trait in ('fuzzy', 'nerdy', 'prickly', 'tipsy'):
		if trait in name:
			traits.add(trait)
	return traits



def allele_cells(genotype: str, dark_colors: list, light_colors: list) -> str:
	"""Return colored allele cells that match the current production table convention."""
	cells = ''
	for index, allele in enumerate(genotype):
		color = '#' + dark_colors[index]
		background = '#FAFAFA' if allele == '+' else '#' + light_colors[index]
		cells += f'<td class="allele" style="color:{color};background:{background}">{esc(allele)}</td>'
	return cells


def fly_table(mapping: gmc.GeneMappingClass, treatment: str) -> str:
	"""Render one fly offspring table using an approved visual treatment."""
	rows = []
	gene_colors = dict(zip(mapping.gene_letters_str, ('#' + color for color in mapping.dark_colors)))
	for genotype in sorted(mapping.genotype_counts, reverse=True):
		phenotype = gml.get_phenotype_name_for_genotype(genotype, mapping.phenotype_dict)
		count = mapping.genotype_counts[genotype]
		traits = traits_from_name(phenotype)
		if treatment == 'portrait':
			art = phenotype_art.plush_fly(traits, phenotype, gene_colors=gene_colors)
			rows.append('<tr><td class="art-cell">' + art + '</td><td>' + phenotype + '</td>'
				+ allele_cells(genotype, mapping.dark_colors, mapping.light_colors) + f'<td class="count">{count:,d}</td></tr>')
		elif treatment == 'tray':
			art = phenotype_art.plush_fly(traits, phenotype, 44, gene_colors=gene_colors)
			genotype_text = ''.join(f'<span style="color:#{mapping.dark_colors[i]}">{esc(a)}</span>' for i, a in enumerate(genotype))
			rows.append('<tr><td colspan="2" class="specimen"><div>' + art + '<strong>' + phenotype
				+ '</strong><code>' + genotype_text + '</code><span>' + f'{count:,d}' + '</span></div></td></tr>')
		else:
			rows.append('<tr><td>' + phenotype + '</td>' + allele_cells(genotype, mapping.dark_colors, mapping.light_colors)
				+ f'<td class="count">{count:,d}</td></tr>')
	if treatment == 'tray':
		return '<table class="fly-table tray"><caption>Offspring specimen tray</caption><tbody>' + ''.join(rows) + '</tbody></table>'
	colspan = mapping.num_genes_int + 3 if treatment == 'portrait' else mapping.num_genes_int + 2
	header = '<th>Fly</th>' if treatment == 'portrait' else ''
	header += '<th>Phenotype</th><th colspan="' + str(mapping.num_genes_int) + '">Genotype</th><th>Progeny<br/>count</th>'
	if mapping.num_genes_int == 4:
		first_panel = '<table class="fly-table"><thead><tr>' + header + '</tr></thead><tbody>' + ''.join(rows[:8]) + '</tbody></table>'
		second_panel = '<table class="fly-table"><thead><tr>' + header + '</tr></thead><tbody>' + ''.join(rows[8:]) + '</tbody></table>'
		return '<div class="fly-panels">' + first_panel + second_panel + '</div><p>Combined total progeny: ' + f'{mapping.progeny_count_int:,d}</p>'
	table = '<table class="fly-table"><thead><tr>' + header + '</tr></thead><tbody>' + ''.join(rows)
	table += '</tbody><tfoot><tr><th colspan="' + str(colspan - 1) + '">TOTAL</th><th>'
	table += f'{mapping.progeny_count_int:,d}</th></tr></tfoot></table>'
	return table


def cross_vignette(tester_traits: set, gene_colors: dict) -> str:
	"""Return a parent-cross illustration that repeats no hidden mapping information."""
	left = phenotype_art.plush_fly(set(), 'heterozygous parent', 72, gene_colors=gene_colors)
	right = phenotype_art.plush_fly(tester_traits, 'recessive tester: ' + ', '.join(sorted(tester_traits)), 72, gene_colors=gene_colors)
	vignette = '<div class="cross-vignette"><div><span>heterozygous parent</span>' + left + '</div>'
	vignette += '<b>&times;</b><div><span>recessive tester</span>' + right + '</div>'
	vignette += '</div>'
	return vignette


class PreviewArgs:
	"""Minimal arguments accepted by the existing previewed generators."""

	def __init__(self) -> None:
		self.question_type = 'mc'
		self.num_choices = 5
		self.hint = True


def load_generator(filename: str):
	"""Load one hyphenated generator module from its production source path."""
	path = os.path.join(GENE_MAPPING_DIR, filename)
	module_name = 'visual_' + filename.replace('-', '_').replace('.', '_')
	spec = importlib.util.spec_from_file_location(module_name, path)
	if spec is None or spec.loader is None:
		raise ValueError(f'cannot load {filename}')
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def capture_actual_fly(filename: str, seed: int, gene_letters: str) -> tuple:
	"""Capture a production fly generator's full prompt, choices, and table source."""
	random.seed(seed)
	module = load_generator(filename)
	captured = {}
	original_class = module.gmc.GeneMappingClass
	original_gene_letters = module.gmc.gml.get_gene_letters
	original_mc = module.bptools.formatBB_MC_Question
	original_fib = module.bptools.formatBB_FIB_PLUS_Question
	if len(gene_letters) not in (2, 3, 4) or len(gene_letters) != len(set(gene_letters)):
		raise ValueError(f'invalid preview gene set: {gene_letters}')

	def preview_gene_letters(num_genes, shift=-1, clear=False):
		if num_genes != len(gene_letters):
			raise ValueError(f'expected {len(gene_letters)} genes, got {num_genes}')
		return gene_letters

	def record_class(*args, **kwargs):
		mapping = original_class(*args, **kwargs)
		captured['mapping'] = mapping
		return mapping

	def record_mc(number, question, choices, answer):
		captured.update(question=question, choices=choices, answer=answer)
		return captured

	def record_fib(number, question, answer_map):
		captured.update(question=question, answer_map=answer_map)
		return captured

	module.gmc.GeneMappingClass = record_class
	module.gmc.gml.get_gene_letters = preview_gene_letters
	module.bptools.formatBB_MC_Question = record_mc
	module.bptools.formatBB_FIB_PLUS_Question = record_fib
	try:
		if filename.startswith('two-point'):
			quietly(module.generate_question, 1, PreviewArgs())
		else:
			quietly(module.write_question, 1, PreviewArgs())
	finally:
		module.gmc.GeneMappingClass = original_class
		module.gmc.gml.get_gene_letters = original_gene_letters
		module.bptools.formatBB_MC_Question = original_mc
		module.bptools.formatBB_FIB_PLUS_Question = original_fib
	mapping = captured['mapping']
	if mapping.gene_letters_str != gene_letters:
		raise ValueError(f'preview gene set drifted: {mapping.gene_letters_str}')
	if len(mapping.genotype_counts) != 2 ** len(gene_letters):
		raise ValueError(f'unexpected progeny class count for {gene_letters}')
	original_table = mapping.get_progeny_html_table()
	if original_table not in captured['question']:
		raise ValueError('captured production question did not include its source table')
	return captured['question'], captured, mapping, original_table


def colored_genotype(genotype: str) -> str:
	"""Color each recessive gene independently; leave plus symbols neutral."""
	label = ''.join(f'<span style="color:{PALETTE[index] if allele != "+" else "#625B50"}">{esc(allele)}</span>' for index, allele in enumerate(genotype))
	return '<code>' + label + '</code>'


def gene_legend(genes: str) -> str:
	"""Show colors for individual recessive genes, never complete genotypes."""
	items = ''.join(f'<span class="genotype-key"><i style="background:{PALETTE[index]}"></i><code>{esc(gene)}</code></span>' for index, gene in enumerate(genes))
	return '<div class="legend">' + items + '<span>+ = neutral</span></div>'


def page_css() -> str:
	"""Lay out a continuous artwork sheet with deliberate PDF page boundaries."""
	css = """
:root { color-scheme:light; font:16px/1.5 Arial,sans-serif; color:#30291F; background:#F7F4EF; }
body { margin:0; } main { max-width:1040px; margin:auto; padding:28px; }
h1 { color:#935D00; margin:0; font-size:32px; } h2 { color:#00775F; font-size:25px; margin:0 0 10px; } h3 { font-size:18px; margin:18px 0 8px; }
p { max-width:82ch; margin:8px 0 16px; } a { color:#076DAD; } code { font: bold 15px monospace; letter-spacing:1px; }
.art-section { background:#FFF; padding:24px; margin:24px 0; border:1px solid #DDD5C7; border-radius:10px; }
.art-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px; }
.gene-descriptions { display:grid; gap:16px; } .gene-descriptions figure { display:flex; align-items:center; gap:24px; text-align:left; } .gene-descriptions svg { flex-shrink:0; } .gene-descriptions figcaption { flex:1; margin:0; } .gene-descriptions p { margin:4px 0 0; }
.portrait-variants { display:flex; gap:8px; flex-shrink:0; }
figure { margin:0; padding:14px 10px; background:#FFFDFA; border:1px solid #E6DFD3; border-radius:8px; text-align:center; break-inside:avoid; }
figure svg { display:block; margin:auto; } figcaption { margin-top:8px; font-size:14px; }
svg[aria-label^="Unordered ascus:"] { display:block; margin:auto; } .legend { display:flex; flex-wrap:wrap; gap:10px 20px; margin:10px 0 16px; }
.genotype-key { display:inline-flex; align-items:center; gap:7px; } .genotype-key i { width:23px; height:23px; border:1px solid #935D00; border-radius:50%; }
.cross-vignette { display:flex; align-items:center; gap:18px; padding:16px; width:max-content; max-width:100%; box-sizing:border-box; background:#EEF8F4; border:1px solid #00775F; border-radius:10px; }
.cross-vignette div { text-align:center; font-size:13px; max-width:120px; } .cross-vignette span { display:block; } .cross-vignette svg { display:block; margin:auto; } .cross-vignette b { font-size:28px; color:#D40000; }
.sizes { display:flex; flex-wrap:wrap; gap:20px; align-items:end; } .sizes figure { border:0; background:white; }
.note, .credits { font-size:13px; color:#625B50; } .credits { margin-top:24px; } .print-link { font-size:14px; }
@media(max-width:700px) { main { padding:14px; } .art-section { padding:16px; } .art-grid,.base-grid { grid-template-columns:1fr; } .phenotype-grid { grid-template-columns:1fr 1fr; } .cross-vignette { gap:8px; } }
@media(max-width:700px) { .gene-descriptions figure { flex-direction:column; align-items:stretch; gap:12px; } .portrait-variants { justify-content:space-between; gap:0; } .portrait-variants svg { width:30%; height:auto; margin:0; } }
@page { size:letter; margin:13mm; }
@media print { :root { font-size:10pt; background:#FFF; } body { -webkit-print-color-adjust:exact; print-color-adjust:exact; } main { padding:0; max-width:none; } h1 { font-size:22pt; } h2 { font-size:18pt; } h3 { font-size:13pt; } .print-link { display:none; } .art-section { border:0; border-radius:0; padding:0; margin:0; break-before:page; } .art-section:first-of-type { break-before:auto; } .art-grid { grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; } .base-grid { grid-template-columns:1fr 1fr; } figure { padding:9px; } figure,.cross-vignette,.legend,.traits { break-inside:avoid; } .credits { font-size:9pt; } .phenotype-grid { gap:8px; } .phenotype-grid figure { padding:6px 2px; } .phenotype-grid figcaption { font-size:10px; margin-top:4px; } }
"""
	return css


def phenotype_study() -> str:
	"""Show the full phenotype bank as individual portraits beside descriptions."""
	page = ''
	for start in range(0, 26, 6):
		genes = string.ascii_lowercase[start:start + 6]
		section_id = 'gene-descriptions' if start == 0 else f'gene-descriptions-{start}'
		page += f'<section class="art-section" id="{section_id}"><h2>Fly gene descriptions: {genes[0].upper()}-{genes[-1].upper()}</h2><p>Blue, green, and purple, left to right, at 72 px. Wings always change color; heads keep their original color. Other regions depend on the phenotype.</p><div class="gene-descriptions">'
		for gene in genes:
			trait = phenotypes_for_flies.phenotype_dict[gene]
			description = phenotypes_for_flies.phenotype_dict[trait]
			page += '<figure><div class="portrait-variants">'
			for color in ('#003FFF', '#007A00', '#A719DB'):
				page += individual_phenotypes.fly_portrait(trait, color=color)
			page += f'</div><figcaption><strong>Gene {gene.upper()}: {esc(trait)}</strong><p>A fruit fly that is homozygous recessive for this gene {esc(description)}</p></figcaption></figure>'
		page += "</div><p class=\"note\">Target: 25-75% of visible artwork changes with the gene color. Props, thorax, and abdomen are treated individually; rust stays brown and the bulb stays warm yellow.</p></section>"
	return page


def build_page() -> str:
	"""Lead with sector-colored asci and preview individual fly descriptions."""
	two_gene = (('++', '++', 'ab', 'ab'), ('+b', '+b', 'a+', 'a+'), ('++', '+b', 'a+', 'ab'))
	three_gene = (('+++', '+++', 'abc', 'abc'), ('++c', 'a+c', '+b+', 'ab+'), ('+++', '+bc', 'a++', 'abc'))
	page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Gene-mapping art gallery</title>'
	page += '<style>' + page_css() + '</style></head><body><main><h1>Gene-mapping art gallery</h1><p class="print-link">One continuous art sheet. Print or save as PDF; everything is visible.</p>'
	page += '<section class="art-section" id="yeast-sectors"><h2>Yeast asci: color sectors</h2><p>Each recessive gene contributes its own color. Slightly looser packing exposes more of each spore while keeping the layered, three-dimensional feel.</p>'
	for genes, examples in (('ab', two_gene), ('abc', three_gene)):
		page += '<h3>' + ('Two' if len(genes) == 2 else 'Three') + ' loci</h3>' + gene_legend(genes) + '<div class="art-grid">'
		for index, genotypes in enumerate(examples, start=1):
			page += '<figure>' + asci.ascus_svg(genotypes, genes) + f'<figcaption>Arrangement {index}</figcaption></figure>'
		page += '</div>'
	page += '<p class="note">Spores are placed to keep colored sectors visible. Neutral sectors take the overlap where possible; the genotype set is unchanged. Positions are visual choices, not meiotic order.</p></section>'
	page += '<section class="art-section" id="display-sizes"><h2>Asci at display size</h2><p>Arrangement 2 at three widths, with the green-only spore in the foreground.</p><div class="sizes">'
	for width in (132, 180, 244):
		art = asci.ascus_svg(three_gene[1], 'abc').replace('width="156" height="120"', f'width="{width}" height="{round(width * 94 / 122)}"')
		page += '<figure>' + art + f'<figcaption>{width} px wide</figcaption></figure>'
	page += '</div><p class="credits">Asci inspired by the public-domain <a href="https://commons.wikimedia.org/wiki/File:Ascus.gif">Ascus micrograph</a>. Colors are diagram keys; genotype labels remain authoritative.</p></section>'
	page += phenotype_study()
	page += '<p class="credits">Original fly artwork: <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</p></main></body></html>'
	return page


def capture_gallery(page_path: str) -> list:
	"""Capture the continuous gallery, its panels, and its print layout."""
	from playwright.sync_api import sync_playwright
	from PIL import Image
	image_paths = []
	with sync_playwright() as playwright:
		browser = playwright.chromium.launch()
		page = browser.new_page(viewport={'width': 1100, 'height': 900}, device_scale_factor=1)
		page.goto('file://' + page_path)
		assert page.locator('button, [hidden], script').count() == 0
		assert page.locator('svg').evaluate_all("""elements => elements.every(svg => {
			const box = svg.getBBox(), view = svg.viewBox.baseVal;
			return box.x >= view.x && box.y >= view.y &&
				box.x + box.width <= view.x + view.width &&
				box.y + box.height <= view.y + view.height;
		})""")
		page.evaluate('document.fonts.ready')
		full_capture = Image.open(io.BytesIO(page.screenshot(full_page=True))).convert('RGB')
		for section in page.locator('section.art-section').evaluate_all('nodes => nodes.map(node => node.id)'):
			image_path = os.path.join(OUT_DIR, section + '.webp')
			box = page.locator('#' + section).bounding_box()
			full_capture.crop((round(box['x']), round(box['y']), round(box['x'] + box['width']), round(box['y'] + box['height']))).save(image_path, quality=90)
			image_paths.append(image_path)
		for name, grayscale in (('gene_mapping_visual_sampler', False), ('gene_mapping_art_grayscale', True)):
			page.evaluate(f'document.body.style.filter = "{"grayscale(1)" if grayscale else "none"}"')
			image_path = os.path.join(OUT_DIR, name + '.webp')
			Image.open(io.BytesIO(page.screenshot(full_page=True))).convert('RGB').save(image_path, quality=90)
			image_paths.append(image_path)
		page.evaluate('document.body.style.filter = "none"')
		page.pdf(path=os.path.join(OUT_DIR, 'gene_mapping_art_gallery.pdf'), print_background=True, prefer_css_page_size=True)
		page.set_viewport_size({'width': 800, 'height': 900})
		assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
		browser.close()
	return image_paths


def write_editable_assets() -> list:
	"""Write standalone SVG source examples used by the preview."""
	assets = []
	asset_pairs = [('unordered_ascus.svg', asci.ascus_svg(('+++', '+bc', 'a++', 'abc'), 'abc'))]
	asset_pairs.append(('unordered_ascus_arrangement_2.svg', asci.ascus_svg(('++c', 'a+c', '+b+', 'ab+'), 'abc')))
	asset_pairs.append(('unordered_ascus_bands.svg', asci.ascus_svg(('+++', '+bc', 'a++', 'abc'), 'abc', 'bands')))
	for bits in range(16):
		traits = {name for index, name in enumerate(phenotype_art.TRAIT_GENES) if bits & (1 << index)}
		label = ', '.join(sorted(traits)) or 'wild type'
		asset_pairs.append((f'fly_storybook_{bits:02d}.svg', phenotype_art.plush_fly(traits, label)))
	for gene in string.ascii_lowercase:
		trait = phenotypes_for_flies.phenotype_dict[gene]
		asset_pairs.append((f'fly_portrait_{trait}.svg', individual_phenotypes.fly_portrait(trait)))
		for color, name in (('#003FFF', 'blue'), ('#007A00', 'green'), ('#A719DB', 'purple')):
			asset_pairs.append((f'fly_portrait_{trait}_{name}.svg', individual_phenotypes.fly_portrait(trait, color=color)))
	for name, svg in asset_pairs:
		path = os.path.join(OUT_DIR, name)
		with open(path, 'w', encoding='utf-8') as outfile:
			outfile.write(svg)
		assets.append(path)
	return assets


def check_artifacts(page: str, assets: list) -> None:
	"""Check allele-to-feature correspondence across every illustrated combination."""
	document = lxml.etree.HTML(page)
	assert not document.xpath('//script | //button | //*[@hidden] | //table')
	assert len(document.xpath('//section[@class="art-section"]')) == 7
	portraits = document.xpath('//*[starts-with(@id,"gene-descriptions")]//figure')
	assert len(portraits) == 26
	for portrait, gene in zip(portraits, string.ascii_lowercase):
		trait = phenotypes_for_flies.phenotype_dict[gene]
		assert portrait.xpath('.//*[@data-phenotype]')[0].get('data-phenotype') == trait
		assert phenotypes_for_flies.phenotype_dict[trait] in ''.join(portrait.itertext())
		variants = portrait.xpath('.//*[@data-gene-color]')
		if [node.get('data-gene-color') for node in variants] != ['#003FFF', '#007A00', '#A719DB']:
			raise ValueError(f'Missing color variants for {trait}')
		heads = [tuple(head[0].get('fill') for head in node.xpath('.//*[@data-part="face"]')) for node in variants]
		if not heads[0] or len(set(heads)) != 1:
			raise ValueError(f'Head base color must stay fixed for {trait}')
		wings = [tuple(lxml.etree.tostring(wing) for wing in node.xpath('.//*[@data-part="wings"]')) for node in variants]
		if not wings[0] or len(set(wings)) != 3:
			raise ValueError(f'Wings must carry each gene color for {trait}')
	root = lxml.etree.fromstring(phenotype_art.plush_fly({'fuzzy', 'prickly'}, 'layer order').encode())
	layers = [node.get('data-part') for node in root.findall('.//*[@data-part]')]
	assert layers.index('wings') < layers.index('prickly') < layers.index('body')
	assert layers.index('thorax') < layers.index('fuzzy') < layers.index('face')
	assert layers.index('bristle-tips') < layers.index('body')
	arrangement = document.xpath('//*[@id="yeast-sectors"]//figure')[4]
	assert [node.get('data-genotype') for node in arrangement.xpath('.//*[@data-genotype]')] == ['++c', 'a+c', '+b+', 'ab+']
	for original, expected in (
		(('+++', '+bc', 'a++', 'abc'), ('+++', 'a++', '+bc', 'abc')),
		(('++c', '+b+', 'a+c', 'ab+'), ('++c', 'a+c', '+b+', 'ab+')),
		(('++', '++', 'ab', 'ab'), ('++', 'ab', '++', 'ab')),
	):
		for permutation in itertools.permutations(original):
			placed = asci.position_spores(permutation)
			assert placed == expected
			assert sorted(placed) == sorted(original)
	assert asci.hidden_sector_areas(3)[3] == (0, 0, 0)
	assert 'offspring culture' not in page and 'scope-field' not in page
	for asset in assets:
		lxml.etree.parse(asset)
	for bits in range(16):
		traits = {name for index, name in enumerate(phenotype_art.TRAIT_GENES) if bits & (1 << index)}
		root = lxml.etree.fromstring(phenotype_art.plush_fly(traits, 'fly & traits').encode('utf-8'))
		assert root.attrib['aria-label'] == 'fly & traits'
		for trait, gene in phenotype_art.TRAIT_GENES.items():
			assert (root.find(f'.//*[@data-part="{trait}"]') is not None) == (trait in traits)
			features = root.findall(f'.//*[@data-gene="{gene}"]')
			assert bool(features) == (trait in traits)
			for feature in features:
				assert phenotype_art.GENE_COLORS[gene] in (feature.get('fill'), feature.get('stroke'))
	custom_colors = {'f': '#00775F', 'n': '#C80085', 'p': '#935D00', 't': '#076DAD'}
	root = lxml.etree.fromstring(phenotype_art.plush_fly(set(phenotype_art.TRAIT_GENES), 'custom colors', gene_colors=custom_colors).encode('utf-8'))
	for feature in root.findall('.//*[@data-gene]'):
		assert custom_colors[feature.get('data-gene')] in (feature.get('fill'), feature.get('stroke'))
	for treatment in ('sectors', 'bands'):
		for mask in range(8):
			genotype = ''.join(gene if mask & (1 << index) else '+' for index, gene in enumerate('abc'))
			root = lxml.etree.fromstring(asci.ascus_svg((genotype,) * 4, 'abc', treatment).encode('utf-8'))
			spores = root.findall('.//*[@data-genotype]')
			assert len(spores) == 4
			for spore in spores:
				features = spore.findall('.//*[@data-gene]')
				assert [node.get('data-gene') for node in features] == [allele for allele in genotype if allele != '+']
				for node in features:
					assert node.get('fill') == PALETTE['abc'.index(node.get('data-gene'))]
				assert not spore.findall('.//{http://www.w3.org/2000/svg}rect')


def export_illustrated_preview() -> str:
	"""Export the production gene-description artwork through the LMS image path."""
	question, captured, _, _ = capture_actual_fly('two-point_test_cross-distance.py', 41, 'fn')
	item = bptools.formatBB_MC_Question(1, question, captured['choices'], captured['answer'])
	outfile = os.path.join(OUT_DIR, 'bbq-illustrated-two-point-preview-questions.txt')
	bptools.write_questions_to_file([item], outfile, bbexport=True, html_to_image=True)
	return outfile


def parse_args() -> argparse.Namespace:
	"""Parse preview-only rendering options."""
	parser = argparse.ArgumentParser(description='Build the gene-mapping visual sampler.')
	parser.add_argument('--screenshot', action='store_true', help='Capture the gallery in Chromium.')
	parser.add_argument('--check', action='store_true', help='Validate gallery and SVG structure.')
	parser.add_argument('--export-preview', action='store_true', help='Create an illustrated Blackboard image export.')
	args = parser.parse_args()
	return args


def main() -> None:
	"""Write the standalone visual sampler and optional review capture."""
	args = parse_args()
	os.makedirs(OUT_DIR, exist_ok=True)
	page = build_page()
	path = os.path.join(OUT_DIR, 'gene_mapping_visual_sampler.html')
	with open(path, 'w', encoding='utf-8') as outfile:
		outfile.write(page)
	print(path)
	assets = write_editable_assets()
	# Keep the user's existing study bookmark pointed at the same continuous gallery.
	with open(os.path.join(OUT_DIR, 'fly_base_study.html'), 'w', encoding='utf-8') as outfile:
		outfile.write(page)
	for asset in assets:
		print(asset)
	if args.check:
		check_artifacts(page, assets)
		print('gallery structure: OK')
	if args.screenshot:
		for image_path in capture_gallery(path):
			print(image_path)
	if args.export_preview:
		print(export_illustrated_preview())


if __name__ == '__main__':
	main()

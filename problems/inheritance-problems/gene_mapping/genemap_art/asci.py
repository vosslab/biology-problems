"""Packed unordered asci with independent allele colors."""

import html
import math
import itertools
import functools

import genemap_art.phenotype_art as phenotype_art

PALETTE = tuple(phenotype_art.GENE_COLORS.values())
SPORE_POSITIONS = ((42, 31), (78, 31), (43, 63), (78, 63))


def esc(value: object) -> str:
	return html.escape(str(value))


@functools.lru_cache(maxsize=3)
def hidden_sector_areas(num_genes: int) -> tuple:
	"""Estimate fill area covered by later spores on a one-unit sampling grid."""
	areas = []
	for position, (x, y) in enumerate(SPORE_POSITIONS):
		covered = [0] * num_genes
		for grid_x in range(-20, 20):
			for grid_y in range(-18, 18):
				dx, dy = grid_x + .5, grid_y + .5
				if (dx / 20) ** 2 + (dy / 18) ** 2 > 1:
					continue
				if not any(((x + dx - front_x) / 20) ** 2 + ((y + dy - front_y) / 18) ** 2 <= 1
					for front_x, front_y in SPORE_POSITIONS[position + 1:]):
					continue
				angle = (math.atan2(dy / 18, dx / 20) + math.pi / 2) % (2 * math.pi)
				sector = int(angle * num_genes / (2 * math.pi))
				covered[sector] += 1
		areas.append(tuple(covered))
	return tuple(areas)


def position_spores(genotypes: tuple) -> tuple:
	"""Choose the placement hiding least color; positions have no genetic meaning."""
	areas = hidden_sector_areas(len(genotypes[0]))

	def score(order):
		loss = sum(areas[position][locus] for position, spore in enumerate(order)
			for locus, allele in enumerate(spore) if allele != '+')
		# Resolve equal visibility with wild type at the back and recessives in front.
		return loss, -order[0].count('+'), order[3].count('+'), order

	return min(itertools.permutations(genotypes), key=score)


def ascus_svg(genotypes: tuple, genes: str, treatment: str = 'sectors',
		colors: tuple = PALETTE) -> str:
	"""Pack overlapping spores with independent gene colors and small text halos."""
	if len(genotypes) != 4 or not 1 <= len(genes) <= 3 or len(set(genes)) != len(genes) or '+' in genes:
		raise ValueError('an ascus needs four spores and one to three distinct gene letters')
	if treatment not in ('sectors', 'bands'):
		raise ValueError(f'unknown spore treatment: {treatment}')
	if len(colors) < len(genes):
		raise ValueError('each gene needs a color')
	for spore in genotypes:
		if len(spore) != len(genes) or any(allele not in ('+', gene) for allele, gene in zip(spore, genes)):
			raise ValueError(f'invalid genotype {spore!r} for loci {genes!r}')
	if treatment == 'sectors':
		genotypes = position_spores(genotypes)
	spores = ''
	for spore_index, (spore, (x, y)) in enumerate(zip(genotypes, SPORE_POSITIONS)):
		spores += f'<g data-genotype="{esc(spore)}" transform="translate({x} {y})">'
		spores += '<ellipse fill="#ECEBE5" rx="20" ry="18"/>'
		for index, allele in enumerate(spore):
			if allele == '+':
				continue
			color = colors[index]
			spores += f'<g data-gene="{esc(allele)}" fill="{color}" stroke="{color}">'
			if treatment == 'sectors':
				start = -math.pi / 2 + index * 2 * math.pi / len(genes)
				end = start + 2 * math.pi / len(genes)
				x1, y1 = 20 * math.cos(start), 18 * math.sin(start)
				x2, y2 = 20 * math.cos(end), 18 * math.sin(end)
				if len(genes) == 1:
					spores += '<ellipse rx="20" ry="18" fill-opacity=".6" stroke="none"/>'
				else:
					spores += f'<path fill-opacity=".6" stroke="none" d="M0 0 L{x1:.3f} {y1:.3f} A20 18 0 0 1 {x2:.3f} {y2:.3f}Z"/>'
			else:
				band_y = (index - (len(genes) - 1) / 2) * 8
				spores += f'<path fill="none" stroke-width="5.5" stroke-opacity=".6" stroke-linecap="round" d="M-15 {band_y - 2} Q0 {band_y + 5} 15 {band_y - 2}"/>'
			spores += '</g>'
		# Near spores cover distant contours; highlights and lower rims describe volume.
		spores += '<path fill="#493215" opacity=".10" d="M-20 0 C-17 14 9 19 19 -4 A20 18 0 0 1 -20 0Z"/>'
		line_width = 1.2 if spore_index < 2 else 1.7
		spores += f'<ellipse fill="none" stroke="#71644F" stroke-width="{line_width}" rx="20" ry="18"/>'
		spores += '<path fill="none" stroke="#FFF" stroke-width="2.3" stroke-linecap="round" opacity=".85" d="M-14 -6 Q-10 -14 -2 -14"/>'
		spores += '<text text-anchor="middle" font-family="monospace" font-size="11.5" font-weight="bold" y="4" stroke="#FFF" stroke-width="2.8" stroke-linejoin="round" paint-order="stroke fill">'
		spores += ''.join(f'<tspan fill="{colors[index] if allele != "+" else "#625B50"}">{esc(allele)}</tspan>' for index, allele in enumerate(spore))
		spores += '</text></g>'
	label = 'Unordered ascus: ' + ', '.join(genotypes)
	svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="156" height="120" viewBox="0 0 122 94" role="img" aria-label="{esc(label)}">'
	svg += '<desc>Each recessive allele contributes its own color; plus alleles remain neutral. Slightly overlapping spores are schematic, not observed pigmentation or meiotic order.</desc>'
	svg += '<metadata>Packed-spore inspiration: https://commons.wikimedia.org/wiki/File:Ascus.gif , public domain micrograph uploaded by Rasbak, originally Pthorpe. New schematic geometry and gene colors.</metadata>'
	svg += '<path fill="#F8F5E9" stroke="#918775" stroke-width="2" d="M15 47 C10 19 27 9 56 9 C88 5 110 16 111 42 C118 72 99 88 72 88 C42 92 13 80 15 47Z"/>'
	svg += '<path fill="none" stroke="#D8D5C8" stroke-width="1.2" d="M19 48 C14 22 31 13 57 13 C86 10 105 19 107 43 C113 68 97 83 72 84 C43 87 17 77 19 48Z"/>' + spores + '</svg>'
	return svg


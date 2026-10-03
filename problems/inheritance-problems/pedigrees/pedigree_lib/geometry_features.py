"""Rendered measurements, separate from pedigree topology and teaching policy."""

import collections

import pedigree_lib.layout as layout

BOTTOM_EMPTY_TARGET = 0.12


#============================================
def people_per_width(diagram: layout.Diagram) -> float:
	"""Measure horizontal density in native drawing units, before display scaling."""
	result = len(diagram.symbols) / diagram.width
	return result


#============================================
def mean_row_density(diagram: layout.Diagram) -> float:
	"""People per occupied row width, excluding generation I, in native units."""
	rows = collections.defaultdict(list)
	for symbol in diagram.symbols:
		rows[symbol.y].append(symbol.x)
	# The renderers draw 30-unit symbols; match the experiment's occupied-width definition.
	densities = [len(rows[y]) / (max(rows[y]) - min(rows[y]) + 30)
		for y in sorted(rows)[1:]]
	result = sum(densities) / len(densities) if densities else 0.0
	return result


#============================================
def bottom_empty_space(diagram: layout.Diagram) -> dict:
	"""Measure the largest empty rectangle resting on the last person row.

	The area is normalized by the tight bounds of symbols and connector strokes.
	Coordinates follow the SVG model: symbol half-size 15, 2-pixel outline, and
	non-scaling outline width at the current display scale.
	"""
	half_stroke = 1.0 / layout.DISPLAY_SCALE
	boxes = []
	for symbol in diagram.symbols:
		extent = 15.0 + half_stroke
		boxes.append((symbol.x - extent, symbol.y - extent,
			symbol.x + extent, symbol.y + extent))
	for segment in diagram.segments:
		boxes.append((min(segment.x1, segment.x2) - half_stroke,
			min(segment.y1, segment.y2) - half_stroke,
			max(segment.x1, segment.x2) + half_stroke,
			max(segment.y1, segment.y2) + half_stroke))
	if not boxes:
		raise ValueError('Pedigree geometry must contain at least one person')
	left = min(box[0] for box in boxes)
	top = min(box[1] for box in boxes)
	right = max(box[2] for box in boxes)
	bottom = max(box[3] for box in boxes)
	last_row = max(symbol.y for symbol in diagram.symbols)
	baseline = max(symbol.y + 15.0 + half_stroke for symbol in diagram.symbols
		if symbol.y == last_row)
	if right <= left or baseline <= top:
		raise ValueError('Pedigree content bounds must have positive area')
	tops = {top}
	tops.update(box[3] for box in boxes if top <= box[3] <= baseline)
	best = None
	for rect_top in sorted(tops):
		if rect_top >= baseline:
			continue
		blocked = sorted((max(left, box[0]), min(right, box[2])) for box in boxes
			if box[1] < baseline and box[3] > rect_top and box[2] > left and box[0] < right)
		merged = []
		for start, end in blocked:
			if not merged or start > merged[-1][1]:
				merged.append([start, end])
			else:
				merged[-1][1] = max(merged[-1][1], end)
		gaps = []
		cursor = left
		for start, end in merged:
			if start > cursor:
				gaps.append((cursor, start))
			cursor = max(cursor, end)
		if cursor < right:
			gaps.append((cursor, right))
		for gap_left, gap_right in gaps:
			area = (gap_right - gap_left) * (baseline - rect_top)
			candidate = (-area, gap_left, gap_right, rect_top, area)
			if best is None or candidate < best:
				best = candidate
	if best is None:
		gap_left = gap_right = left
		rect_top = baseline
		area = score = 0.0
	else:
		_, gap_left, gap_right, rect_top, area = best
		score = area / ((right - left) * (bottom - top))
	result = dict(score=score,
		rect=dict(x=gap_left, y=rect_top, width=gap_right - gap_left,
			height=baseline - rect_top),
		bounds=dict(x=left, y=top, width=right - left, height=bottom - top),
		baseline=baseline)
	return result

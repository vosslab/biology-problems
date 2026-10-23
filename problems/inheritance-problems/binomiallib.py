"""Shared HTML notation for binomial coefficients and expressions."""

import math
import fractions

#===========================================================
def binomial_coefficient(n: int | str, r: int | str) -> str:
	"""Stack n over r inside the parentheses used by the offspring-sex questions."""
	choose = ""
	choose += (
		"<table style='display:inline-table;vertical-align:middle;"
		"border-collapse:collapse;border:0;'>"
	)
	choose += "<tr>"
	choose += (
		" <td rowspan='2' style='text-align:center;vertical-align:middle;padding:0;"
		"margin-right:0.05em;'>"
		"<span style='font-size:2.7em;"
		"display:inline-block;margin-right:0.05em;'>"
		"&#10222;</span>&nbsp;</td>"
	)
	choose += f" <td style='text-align:center;vertical-align:bottom;padding:0;'>{n}</td>"
	choose += (
		" <td rowspan='2' style='text-align:center;vertical-align:middle;padding:0;"
		"margin-left:0.05em;'>"
		"&nbsp;<span style='font-size:2.7em;"
		"display:inline-block;margin-left:0.05em;'>"
		"&#10223;</span></td>"
	)
	choose += "</tr>"
	choose += "<tr>"
	choose += f" <td style='text-align:center;vertical-align:top;padding:0;'>{r}</td>"
	choose += "</tr>"
	choose += "</table>"
	return choose


#===========================================================
def fraction(numerator: str, denominator: str) -> str:
	"""Stack a numerator over a denominator with a fraction bar."""
	text = '<table role="presentation" style="display:inline-table;vertical-align:middle;'
	text += 'border-collapse:collapse;border:0;text-align:center;">'
	text += '<tr><td style="padding:2px 4px;border:0;border-bottom:1px solid currentColor;">'
	text += f'{numerator}</td></tr>'
	text += f'<tr><td style="padding:2px 4px;border:0;">{denominator}</td></tr></table>'
	return text


#===========================================================
def format_expression(parts: list[str]) -> str:
	"""Keep a complete expression together in HTML and table-to-image exports."""
	text = '<table role="presentation" style="display:inline-table;vertical-align:middle;'
	text += 'border-collapse:collapse;border:0;"><tr>'
	for part in parts:
		text += f'<td style="vertical-align:middle;padding:0 2px;border:0;">{part}</td>'
	text += '</tr></table>'
	return text


#===========================================================
def binomial_probability(n: int, k: int, p: fractions.Fraction | float,
	q: fractions.Fraction | float, *, worked: bool = True) -> str:
	"""Render C(n,k) p^(n-k) q^k, optionally followed by its worked calculation."""
	p, q = fractions.Fraction(p), fractions.Fraction(q)
	ptxt = _probability_text(p)
	qtxt = _probability_text(q)
	powers = f"({ptxt})<sup>{n-k}</sup>&sdot;({qtxt})<sup>{k}</sup>"
	parts = [binomial_coefficient(n, k), powers]
	if not worked:
		text = format_expression(parts)
		return text

	# Expand the coefficient, then cancel the larger factorial.
	parts.extend(["=", fraction(f"{n}!", f"({n}&ndash;{k})! &sdot; {k}!"), powers])
	r = min(k, n - k)
	numerator = "&sdot;".join(str(i) for i in range(n, n - r, -1)) or "1"
	denominator = "&sdot;".join(str(i) for i in range(r, 1, -1)) or "1"
	# Keep the probability factors exact throughout the calculation.
	if p == q:
		power_numerator = f"{p.numerator}<sup>{n}</sup>" if p.numerator != 1 else "1"
		power_denominator = f"{p.denominator}<sup>{n}</sup>"
	else:
		power_numerator = f"{p.numerator}<sup>{n-k}</sup> &sdot; {q.numerator}<sup>{k}</sup>"
		power_denominator = f"{p.denominator}<sup>{n-k}</sup> &sdot; {q.denominator}<sup>{k}</sup>"
	parts.extend(["=", fraction(numerator, denominator), "&times;",
		fraction(power_numerator, power_denominator)])
	coefficient = math.comb(n, k)
	one_order = p ** (n - k) * q ** k
	product = str(coefficient)
	if one_order.numerator != 1:
		product += f" &times; {one_order.numerator}"
	value = coefficient * one_order
	parts.extend(["=", fraction(product, str(one_order.denominator)), "=",
		f"{float(value):.4f}", "<strong>=</strong>", f"<strong>{float(value) * 100:.1f}%</strong>"])
	text = format_expression(parts)
	return text


#===========================================================
def _probability_text(value: fractions.Fraction) -> str:
	"""Use compact familiar fractions inside powered probability terms."""
	common = {fractions.Fraction(1, 2): "&frac12;", fractions.Fraction(1, 4): "&frac14;",
		fractions.Fraction(3, 4): "&frac34;", fractions.Fraction(1, 3): "&#8531;",
		fractions.Fraction(2, 3): "&#8532;"}
	if value in common:
		return common[value]
	text = fraction(str(value.numerator), str(value.denominator))
	return text

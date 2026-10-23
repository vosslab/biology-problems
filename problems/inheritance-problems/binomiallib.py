"""Shared HTML notation for binomial coefficients and expressions."""


#===========================================================
def binomial_coefficient(n: int | str, r: int | str) -> str:
	"""Stack n over r inside the parentheses used by the offspring-sex questions."""
	choose = ""
	choose += (
		"<table style='display:inline-table;vertical-align:middle;"
		"border-collapse:collapse;border:0;position:relative;top:-0.2em;'>"
	)
	choose += "<tr>"
	choose += (
		" <td rowspan='2' style='text-align:center;vertical-align:middle;padding:0;"
		"margin-right:0.05em;'>"
		"<span style='font-size:xx-large;"
		"transform:scale(1.35);display:inline-block;margin-right:0.05em;'>"
		"&#10222;</span>&nbsp;</td>"
	)
	choose += f" <td style='text-align:center;vertical-align:bottom;padding:0;'>{n}</td>"
	choose += (
		" <td rowspan='2' style='text-align:center;vertical-align:middle;padding:0;"
		"margin-left:0.05em;'>"
		"&nbsp;<span style='font-size:xx-large;"
		"transform:scale(1.35);display:inline-block;margin-left:0.05em;'>"
		"&#10223;</span></td>"
	)
	choose += "</tr>"
	choose += "<tr>"
	choose += f" <td style='text-align:center;vertical-align:top;padding:0;'>{r}</td>"
	choose += "</tr>"
	choose += "</table>"
	return choose


#===========================================================
def format_expression(parts: list[str]) -> str:
	"""Keep a complete expression together in HTML and table-to-image exports."""
	text = '<table role="presentation" style="display:inline-table;vertical-align:middle;'
	text += 'border-collapse:collapse;border:0;"><tr>'
	for part in parts:
		text += f'<td style="vertical-align:middle;padding:0 2px;border:0;">{part}</td>'
	text += '</tr></table>'
	return text

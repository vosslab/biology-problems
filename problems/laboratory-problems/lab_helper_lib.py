#!/usr/bin/env python3

#============================================
def format_monospace(text):
	return f"<span style='font-family: monospace;'>{text}</span>"

#============================================
def format_color(text, color):
	return f"<span style='color: {color};'>{text}</span>"

#============================================
def format_aliquot(text_html):
	return format_color(text_html, '#7a1f7a')

#============================================
def format_diluent(text_html):
	return format_color(text_html, '#005cb3')

#============================================
def format_stock(text_html):
	return format_color(text_html, '#cc5500')

#============================================
def format_df(text_html):
	return format_color(text_html, '#228b22')

#============================================
def format_key_request(text_html):
	return f"<span style='font-size: 1.05em;'>{text_html}</span>"

#============================================
def build_info_table(rows, title_html=None):
	table_html = (
		"<table border='1' cellpadding='4' cellspacing='0' "
		"style='border-collapse: collapse; margin-top: 6px;'>"
	)
	if title_html is not None:
		table_html += (
			"<tr>"
			"<td colspan='2' style='font-weight: bold; background-color: #efefef; text-align: center;'>"
			f"{title_html}"
			"</td>"
			"</tr>"
		)
	for label, value_html in rows:
		table_html += (
			"<tr>"
			f"<td style='font-weight: bold; background-color: #f7f7f7;'>{label}</td>"
			f"<td>{value_html}</td>"
			"</tr>"
		)
	table_html += "</table>"
	return table_html

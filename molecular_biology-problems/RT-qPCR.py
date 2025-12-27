#!/usr/bin/env python3

import random
import bptools

raw_table = """
<table border="1" style="border-collapse: collapse;">
<tbody>
<tr>
<td rowspan="2" style="width: 20%; text-align: center; vertical-align: middle;">&nbsp;</td>
<td colspan="2" style="width: 40%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Untreated Cells</strong></td>
<td colspan="2" style="width: 40%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Cells Treated with Experimental Drug</strong></td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>House Keeping Gene</strong></td>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Gene of Interest</strong></td>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>House Keeping Gene</strong></td>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Gene of Interest</strong></td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Well 1</strong></td>
<td style="width: 20%; text-align: right; vertical-align: middle;">w1</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">x1</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">y1</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">z1</td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Well 2</strong></td>
<td style="width: 20%; text-align: right; vertical-align: middle;">w2</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">x2</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">y2</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">z2</td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Well 3</strong></td>
<td style="width: 20%; text-align: right; vertical-align: middle;">w3</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">x3</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">y3</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">z3</td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>mean Ct</strong></td>
<td style="width: 20%; text-align: right; background-color: #ced4d9; vertical-align: middle;">mean1</td>
<td style="width: 20%; text-align: right; background-color: #ced4d9; vertical-align: middle;">mean2</td>
<td style="width: 20%; text-align: right; background-color: #ced4d9; vertical-align: middle;">mean3</td>
<td style="width: 20%; text-align: right; background-color: #ced4d9; vertical-align: middle;">mean4</td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>&Delta;Ct</strong></td>
<td colspan="2" style="width: 40%; text-align: center; vertical-align: middle;">&nbsp;</td>
<td colspan="2" style="width: 40%; text-align: center; vertical-align: middle;">&nbsp;</td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>&Delta;&Delta;Ct</strong></td>
<td colspan="4" style="width: 80%; text-align: center; vertical-align: middle;">&nbsp;</td>
</tr>
</tbody>
</table>
"""

def _mean(values):
	return sum(values) / float(len(values))


def _make_ct_values(mean_value, spread=0.8):
	values = []
	for _ in range(3):
		ct = mean_value + random.uniform(-spread, spread)
		values.append(round(ct, 1))
	return values


def _format_table(ct_values):
	table = raw_table
	for key, value in ct_values.items():
		table = table.replace(key, f"{value:.1f}")
	return table

def makeDataTable():
	while True:
		hk_untreated_mean = random.uniform(17.0, 22.0)
		goi_untreated_mean = hk_untreated_mean + random.uniform(3.0, 8.0)
		hk_treated_mean = hk_untreated_mean + random.uniform(-0.5, 0.5)
		goi_treated_mean = goi_untreated_mean + random.uniform(-4.0, 4.0)

		w_vals = _make_ct_values(hk_untreated_mean)
		x_vals = _make_ct_values(goi_untreated_mean)
		y_vals = _make_ct_values(hk_treated_mean)
		z_vals = _make_ct_values(goi_treated_mean)

		mean1 = round(_mean(w_vals), 1)
		mean2 = round(_mean(x_vals), 1)
		mean3 = round(_mean(y_vals), 1)
		mean4 = round(_mean(z_vals), 1)

		delta_ct_untreated = mean2 - mean1
		delta_ct_treated = mean4 - mean3
		delta_delta = delta_ct_treated - delta_ct_untreated
		if abs(delta_delta) < 0.5:
			continue

		ct_values = {
			"w1": w_vals[0], "w2": w_vals[1], "w3": w_vals[2],
			"x1": x_vals[0], "x2": x_vals[1], "x3": x_vals[2],
			"y1": y_vals[0], "y2": y_vals[1], "y3": y_vals[2],
			"z1": z_vals[0], "z2": z_vals[1], "z3": z_vals[2],
			"mean1": mean1, "mean2": mean2, "mean3": mean3, "mean4": mean4
		}
		table = _format_table(ct_values)
		fold_change = round(2 ** abs(delta_delta), 2)
		return table, fold_change


def write_question(N, args):
	table, fold_change = makeDataTable()
	question = (
		"<p>Given the data in the table above calculate the fold change "
		"(2<sup>|&Delta;&Delta;Ct|</sup>) value for the effect of the drug on the cells.</p>"
	)
	tolerance = 0.05
	return bptools.formatBB_NUM_Question(N, table + question, fold_change, tolerance)

#=====================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate RT-qPCR fold change questions.")
	args = parser.parse_args()
	return args


#=====================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(__file__)
	bptools.collect_and_write_questions(write_question, args, outfile)


#=====================
if __name__ == '__main__':
	main()

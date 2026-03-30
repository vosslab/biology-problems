#!/usr/bin/env python3

"""Shared helpers for Michaelis-Menten table-based question generators."""

# Standard Library
import math

# Fixed substrate concentrations spanning 5 orders of magnitude (mM)
# Km is always chosen from the lower values so the table shows
# the full curve from near-zero velocity through Vmax saturation.
SUBSTRATE_CONCS = [
	0.001, 0.002, 0.005, 0.010, 0.020, 0.050,
	0.100, 0.200, 0.500, 1.000, 2.000, 5.000,
	10.000, 20.000, 50.000, 100.000,
]

# Possible Km values: first 6 substrate concentrations (lower range)
KM_CHOICES = SUBSTRATE_CONCS[:6]

#============================================
def michaelis_menten(substrate_conc: float, km: float, vmax: float) -> float:
	"""Calculate initial velocity using the Michaelis-Menten equation.

	Args:
		substrate_conc: Substrate concentration [S].
		km: Michaelis constant.
		vmax: Maximum velocity.

	Returns:
		Initial velocity V0 rounded up to 1 decimal place.
	"""
	v0 = vmax * substrate_conc / (km + substrate_conc)
	# ceil to 1 decimal place so table values never quite reach Vmax
	v0_rounded = math.ceil(v0 * 10.0) / 10.0
	return v0_rounded

#============================================
def make_data_table(
	substrate_concs: list,
	velocities: list,
	vmax: float,
	inhibited_velocities: list = None,
	inhib_vmax: float = None,
) -> str:
	"""Build an HTML table of substrate concentration vs initial velocity.

	Produces a 2-column table (no inhibitor) or 3-column table (with inhibitor)
	depending on whether inhibited_velocities is provided.

	Args:
		substrate_concs: List of [S] values.
		velocities: List of V0 values without inhibitor.
		vmax: Maximum velocity (used to stop rows near saturation).
		inhibited_velocities: Optional list of V0 values with inhibitor.
		inhib_vmax: Vmax for inhibited curve (used for 3-column stop check).

	Returns:
		HTML table string.
	"""
	has_inhibitor = inhibited_velocities is not None
	num_cols = 3 if has_inhibitor else 2

	# monospace span for numeric alignment
	mono = "<span style='font-family: courier, monospace;'>"

	# start the table
	table = "<table cellpadding='2' cellspacing='2' "
	table += "style='text-align: center; border-collapse: collapse; "
	table += "border: 1px solid black; font-size: 14px;'>"

	# column widths
	col_width = 160
	for _ in range(num_cols):
		table += f"<colgroup width='{col_width}'></colgroup> "

	# header row
	table += "<tr style='background-color: lightgray; border-bottom: 2px solid black;'>"
	table += "<th align='center' style='padding: 5px; font-size: 12px;'>"
	table += "substrate<br/>concentration, "
	table += "<span style='font-size: 14px;'>[S]</span></th>"

	if has_inhibitor:
		# two velocity columns with color coding
		table += "<th align='center' style='padding: 5px; font-size: 12px;'>"
		table += "initial reaction<br/>velocity no inhibitor<br/>"
		table += "<span style='font-size: 14px; color: #00008B; font-weight: bold;'>"
		table += "V<sub>0</sub> (&ndash;inh)</span></th>"
		table += "<th align='center' style='padding: 5px; font-size: 12px;'>"
		table += "initial reaction<br/>velocity with inhibitor<br/>"
		table += "<span style='font-size: 14px; color: #8B0000; font-weight: bold;'>"
		table += "V<sub>0</sub> (+inh)</span></th>"
	else:
		# single velocity column
		table += "<th align='center' style='padding: 5px; font-size: 12px;'>"
		table += "initial reaction<br/>velocity<br/>"
		table += "<span style='font-size: 14px;'>V<sub>0</sub></span></th>"

	table += "</tr>"

	# data rows
	num_rows = min(len(substrate_concs), len(velocities))
	for i in range(num_rows):
		# alternate row colors
		bgcolor = "#FFFFDD" if i % 2 == 0 else "#FFFFFF"
		s_val = substrate_concs[i]
		v0 = velocities[i]
		table += f"<tr style='background-color: {bgcolor};'>"

		# substrate concentration column
		s_str = f"{s_val:.3f}"
		table += f" <td style='border: 1px solid black;' align='right'>"
		table += f"{mono}{s_str}&nbsp;</span></td>"

		# velocity column
		table += f" <td style='border: 1px solid black;' align='right'>"
		table += f"{mono}{v0:.1f}&nbsp;</span></td>"

		# inhibited velocity column (if present)
		if has_inhibitor:
			inhib_v0 = inhibited_velocities[i]
			table += f" <td style='border: 1px solid black;' align='right'>"
			table += f"{mono}{inhib_v0:.1f}&nbsp;</span></td>"

		table += "</tr>"

		# stop if we are very close to Vmax
		if (vmax - v0) < 0.099:
			break

	table += "</table>"
	return table

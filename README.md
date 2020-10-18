# biochem-problems
Python Scripts for Generating Biochemistry Homework/Quiz problems

## Isoelectric Point Problems

### isoelectric_one_protein.py

<table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">
<tr><th>Protein Name</th><th>isoelectric point (pI)</th><th>molecular weight</th></tr>
<tr><td>Xylosidase (Xyl)</td><td align="center">5.0</td><td align="center">100.0</td></tr>
</table>
<p>1. The protein in the table (above) is placed in a buffer solution with a pH of 6.0.</p> 
<p>What is the correct net charge on the Xyl protein at <b>pH of 6.0</b>? 

- [x] A. The protein will have a net <span style="color:darkred">negative (&ndash;)</span> charge
- [ ] B. The protein will have a net <span style="color:darkblue">positive (+)</span> charge
- [ ] C. The protein will have a <span style="color:goldenrod">neutral (0)</span> charge

### isoelectric_two_proteins.py

<p>2. A mixture of two proteins are to be separated by isoelectric focusing.</p>

<table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">
<tr><th>Protein Name</th><th>isoelectric point (pI)</th><th>molecular weight</th></tr>
<tr><td>&beta;-Galactosidase (Gal)</td><td align="right">4.6</td><td align="right">175.0</td></tr>
<tr><td>Fumerase (Fum)</td><td align="right">7.6</td><td align="right">48.5</td></tr>
</table>
<p>Both protein samples are placed into a gel with a constant pH of 9.0. The gel is then placed into an electric field.</p> 
<p>In which direction will each protein in the table migrate at <b>pH 9.0</b></p>

- [x] A. Both Gal and Fum will travel towards the <span style="color:darkblue">positive (+)</span> terminal
- [ ] B. Both Gal and Fum will travel towards the <span style="color:darkred">negative (&ndash;)</span> terminal
- [ ] C. Gal will travel towards the <span style="color:darkblue">positive (+)</span> 
  and Fum will travel towards the <span style="color:darkred">negative (&ndash;)</span> 
- [ ] D. Gal will travel towards the <span style="color:darkred">negative (&ndash;)</span> 
  and Fum will travel towards the <span style="color:darkblue">positive (+)</span> 

## Gel Migration Problem

### gel_migration.py

<table cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">
<tr><th>Protein Name</th><th>Molecular<br/>Weight (kDa)</th><th>Migration<br/>Distance (cm)</th></tr>
<tr><td>Ribonuclease A (RibA)</td><td align="center">13.7</td><td align="center">3.41</td></tr>
<tr><td>Serine Protease (Ser)</td><td align="center">22.0</td><td align="center">3.03</td></tr>
<tr><td>Prostate-Specific Antigen (PSA)</td><td align="center">30.0</td><td align="center">2.78</td></tr>
<tr><td>Aldolase (Aldo)</td><td align="center">47.5</td><td align="center">2.41</td></tr>
<tr><td>Fibrinogen (Fib)</td><td align="center">63.5</td><td align="center">2.18</td></tr>
<tr><td>Unknown</td><td align="center">?</td><td  align="center">2.89</td></tr>
</table>
<p>3. The standard and unknown proteins listed in the table were run using SDS&ndash;PAGE.</p>
<p><b>Estimate the molecular weight of the unknown protein.</b></p> 

- [ ] A. 17 kDa 
- [x] B. 26 kDa 
- [ ] C. 41 kDa 
- [ ] D. 54 kDa

## Alpha Helix Hydrogen Bonding

### alpha_helix_h-bonds.py

<p>4. In a long &alpha;-helix, amino acid <b>number 7</b> would form a hydrogen bond with which two other amino acids?</p>

- [ ] A. 1 and 13
- [ ] B. 4 and 10
- [ ] C. 5 and 9
- [ ] D. 2 and 12
- [x] E. 3 and 11

## Hydrophobicity

### which_phobic.py 

<p>5. Based on their molecular formula, which one of the following compounds is most likely hydrophobic</p>

- [ ] A. erythrose, C<sub>4</sub>H<sub>8</sub>O<sub>4</sub>
- [ ] B. acetate, C<sub>2</sub>H<sub>3</sub>O<sub>2</sub>
- [x] C. ethylene, CH<sub>2</sub>CH<sub>2</sub>
- [ ] D. urea, CO(NH<sub>2</sub>)<sub>2</sub>

## Michaelis-Menten

### michaelis_menten_table-Km.py

<p>6. <u>Michaelis-Menten question.</u></p> <p>The following question refers to the table (<i>below</i>) of enzyme activity.  The units of substrate, [S], is mM; ignore the units for V<sub>0</sub>.</p>

<table cellpadding="2" cellspacing="2"  style="text-align:center; border-collapse: collapse; border: 1px solid black; font-size: 14px;"><colgroup width="120"></colgroup> <colgroup width="120"></colgroup> <tr> <th align="center">substrate<br/>concentration<br/>[S]</th> <th align="center">initial<br/>reaction<br/>velocity<br/>V<sub>0</sub></th></tr><tr> <td align="right"><span style="font-family: courier, monospace;">0.0001&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">46.7&nbsp;</span></td></tr><tr> <td align="right"><span style="font-family: courier, monospace;">0.0002&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">70.0&nbsp;</span></td></tr><tr> <td align="right"><span style="font-family: courier, monospace;">0.0005&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">100.1&nbsp;</span></td></tr><tr> <td align="right"><span style="font-family: courier, monospace;">0.0010&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">116.7&nbsp;</span></td></tr><tr> <td align="right"><span style="font-family: courier, monospace;">0.0020&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">127.3&nbsp;</span></td></tr><tr> <td align="right"><span style="font-family: courier, monospace;">0.0050&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">134.7&nbsp;</span></td></tr><tr> <td align="right"><span style="font-family: courier, monospace;">0.0100&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">137.3&nbsp;</span></td></tr><tr> <td align="right"><span style="font-family: courier, monospace;">0.0200&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">138.7&nbsp;</span></td></tr><tr> <td align="right"><span style="font-family: courier, monospace;">0.0500&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">139.5&nbsp;</span></td></tr><tr> <td align="right"><span style="font-family: courier, monospace;">0.1000&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">139.8&nbsp;</span></td></tr><tr> <td align="right"><span style="font-family: courier, monospace;">1.0000&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">140.0&nbsp;</span></td></tr></table>

<p>Using the table (<i>above</i>), calculate the value for the Michaelis-Menten constant, K<sub>M</sub>?</p>

- [ ] A. 0.0001
- [x] B. 0.0002
- [ ] C. 0.0010
- [ ] D. 0.0020
- [ ] E. 0.0050

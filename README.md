# biochem-problems
Python Scripts for Generating Biochemistry Homework/Quiz problems

Table of Contents
=================

   * [biochem-problems](#biochem-problems)
      * [Isoelectric Point Problems](#isoelectric-point-problems)
         * [isoelectric_one_protein.py](#isoelectric_one_proteinpy)
         * [isoelectric_two_proteins.py](#isoelectric_two_proteinspy)
      * [Gel Migration Problem](#gel-migration-problem)
         * [gel_migration.py](#gel_migrationpy)
      * [Alpha Helix Hydrogen Bonding](#alpha-helix-hydrogen-bonding)
         * [alpha_helix_h-bonds.py](#alpha_helix_h-bondspy)
      * [Hydrophobicity](#hydrophobicity)
         * [which_phobic.py](#which_phobicpy)
      * [Michaelis-Menten](#michaelis-menten)
         * [michaelis_menten_table-Km.py](#michaelis_menten_table-kmpy)
         * [michaelis_menten_table-inhibition.py](#michaelis_menten_table-inhibitionpy)

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

* [Download list of questions in blackboard upload format](blackboard_upload/bbq-michaelis_menten_table-Km.txt)

<p>6. <b>Michaelis-Menten question.</b> The following question refers to the table (<i>below</i>) of enzyme activity.</p>

<table cellpadding="2" cellspacing="2"  style="text-align:center; border-collapse: collapse; border: 1px solid black; font-size: 14px;"><colgroup width="120"></colgroup> <colgroup width="120"></colgroup>
<tr> <th align="center">substrate<br/>concentration<br/>[S]</th> <th align="center">initial<br/>reaction<br/>velocity<br/>V<sub>0</sub></th></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.001&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">30.0&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.002&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">51.5&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.005&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">90.0&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.010&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">120.1&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.020&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">144.0&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.050&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">163.7&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.100&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">171.5&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.200&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">175.7&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.500&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">178.3&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">1.000&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">179.2&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">10.000&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">180.0&nbsp;</span></td></tr></table>

<p>Using the table (<i>above</i>), calculate the value for the Michaelis-Menten constant, K<sub>M</sub>.</p>

- [ ] A. K<sub>M</sub> = 0.001
- [ ] B. K<sub>M</sub> = 0.002
- [x] C. K<sub>M</sub> = 0.005
- [ ] D. K<sub>M</sub> = 0.020
- [ ] E. K<sub>M</sub> = 0.050


### michaelis_menten_table-inhibition.py

* [Download list of questions in blackboard upload format](blackboard_upload/bbq-michaelis_menten_table-inhibition.txt)

<p>7. <b>Michaelis-Menten question.</b> The following question refers to the table (<i>below</i>) of enzyme activity with and without an inhibitor.</p>

<table cellpadding="2" cellspacing="2"  style="text-align:center; border-collapse: collapse; border: 1px solid black; font-size: 14px;"><colgroup width="160"></colgroup> <colgroup width="160"></colgroup> <colgroup width="160"></colgroup>
<tr> <th align="center">substrate<br/>concentration, [S]</th> <th align="center">initial reaction<br/>velocity no inhibitor<br/>V<sub>0</sub> (&ndash;inh)</th> <th align="center">initial reaction<br/>velocity with inhibitor<br/>V<sub>0</sub> (+inh)</th></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.0001&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">9.6&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">8.6&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.0002&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">18.2&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">16.4&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.0005&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">40.0&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">36.0&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.0010&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">66.7&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">60.0&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.0020&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">100.0&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">90.0&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.0050&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">142.9&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">128.6&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.0100&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">166.7&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">150.0&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.0200&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">181.9&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">163.7&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.0500&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">192.4&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">173.1&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">0.1000&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">196.1&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">176.5&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">1.0000&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">199.7&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">179.7&nbsp;</span></td></tr>
<tr> <td align="right"><span style="font-family: courier, monospace;">10.0000&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">200.0&nbsp;</span></td> <td align="right"><span style="font-family: courier, monospace;">180.0&nbsp;</span></td></tr></table>

<p>Using the table (<i>above</i>), determine the type of inhibition.</p>

- [ ] A. anticompetitive
- [ ] B. competitive
- [x] C. noncompetitive
- [ ] D. ultracompetitive
- [ ] E. uncompetitive

## Enzymes

### chymotrypsin_substrate.py

* [Download list of questions in blackboard upload format](blackboard_upload/bbq-chymotrypsin_substrate.txt)

<p>1. Given the following peptide sequence, <b>NH<sub>3</sub><sup>+</sup>&mdash;Gln&mdash;Ala&mdash;Ala&mdash;Tyr&mdash;Ser&mdash;Asn&mdash;Glu&mdash;Glu&mdash;Gln&mdash;Gln&mdash;COO<sup>&ndash;</sup></b>, at which peptide bond location will chymotrypsin most likely cleave first?</p>

- [ ] A. Ala&mdash;Tyr
- [x] B. Tyr&mdash;Ser
- [ ] C. Glu&mdash;Gln
- [ ] D. Gln&mdash;Ala
- [ ] E. Ala&mdash;Ala

## Sugars

### monosaccharide_d_to_l_configuration.py

* [Download list of questions in blackboard upload format](blackboard_upload/bbq-monosaccharide_d_to_l_configuration.txt)

![D-tagatose](images/D-tagatose.png  | height=200))

<p>Above is a Fischer projection of the monosaccharide D-tagatose. Which one of the following Fischer projections is of the monosaccharide L-tagatose?</p>

- [ ] A. ![Fischer diagram 1](images/fischer_sugar1.png | height=200))
- [ ] B. ![Fischer diagram 2](images/fischer_sugar2.png | height=200))
- [ ] C. ![Fischer diagram 3](images/fischer_sugar3.png | height=200))
- [ ] D. ![Fischer diagram 4](images/fischer_sugar4.png | height=200)
- [x] E. ![Fischer diagram 5](images/L-tagatose.png | height=200)))


// Amino acid mapping: 1-letter code to 3-letter code
const aminoAcidMapping = {
    A: 'Ala',  // Alanine
    C: 'Cys',  // Cysteine
    D: 'Asp',  // Aspartic Acid
    E: 'Glu',  // Glutamic Acid
    F: 'Phe',  // Phenylalanine
    G: 'Gly',  // Glycine
    H: 'His',  // Histidine
    I: 'Ile',  // Isoleucine
    K: 'Lys',  // Lysine
    L: 'Leu',  // Leucine
    M: 'Met',  // Methionine
    N: 'Asn',  // Asparagine
    P: 'Pro',  // Proline
    Q: 'Gln',  // Glutamine
    R: 'Arg',  // Arginine
    S: 'Ser',  // Serine
    T: 'Thr',  // Threonine
    V: 'Val',  // Valine
    W: 'Trp',  // Tryptophan
    Y: 'Tyr'   // Tyrosine
};

// Side chain SMILES fragments for each residue
const sideChains = {
    // smallest
    Gly: '([H])',              // Glycine
    Gly2: '',                  // Glycine variant
    Ala: '(C)',                // Alanine
    // polar
    Ser: '(CO)',               // Serine
    Thr: '([C@H](O)C)',        // Threonine
    // Asn, Gln
    Asn: '(CC(=O)N)',          // Asparagine
    Gln: '(CCC(=O)N)',         // Glutamine
    // negative charge
    Asp: '(CC(=O)[O-])',       // Aspartate
    Glu: '(CCC(=O)[O-])',      // Glutamate
    // positive charge
    Lys: '(CCCC[NH3+])',       // Lysine
    Arg: '(CCCNC(=[NH2+])N)',  // Arginine
    His: '(CC1=C[NH]C=N1)',    // Histidine delta tautomer at pH 7
    His2: '(CC1=CN=C[NH]1)',   // Histidine epsilon tautomer at pH 7
    His3: '(CC1=C[NH]C=[NH+]1)',  // Histidine delta tautomer at pH 5
    His4: '(CC1=C[NH+]=C[NH]1)',  // Histidine epsilon tautomer at pH 5
    // branched chain
    Val: '(C(C)C)',            // Valine
    Leu: '(CC(C)C)',           // Leucine
    Ile: '([C@H](CC)C)',       // Isoleucine
    Met: '(CCSC)',             // Methionine
    // aromatic
    Phe: '(Cc1ccccc1)',        // Phenylalanine
    Tyr: '(Cc1ccc(O)cc1)',     // Tyrosine
    Trp: '(CC1=CC=C2C(=C1)C(=CN2))', // Tryptophan
    // special
    Cys: '(CS)'                // Cysteine
};

//=================================================
// Template for a pentapeptide backbone with R1..R5 placeholders
//=================================================
const POLYPEPTIDE_SMILES_TEMPLATE =
"[NH3+][C@@H]R1(C(=O)N[C@@H]R2(C(=O)N[C@@H]R3(C(=O)N[C@@H]R4(C(=O)N[C@@H]R5(C(=O)[O-])))))";

//=================================================
//=================================================
function makePolypeptideSmilesFromSequence(seq) {
    /**
     * Build a pentapeptide SMILES from a 1 letter sequence.
     *
     * Args:
     *   seq: String of length 5, using only aminoAcidMapping keys (A C D E ... Y).
     *
     * Returns:
     *   SMILES string with side chains substituted.
     *
     * Throws:
     *   Error if length is not 5 or any letter is not a known amino acid.
     */

    const chars = String(seq || "").toUpperCase().split("");

    if (chars.length !== 5) {
        throw new Error(
            "makePolypeptideSmilesFromSequence: sequence must be length 5, got " +
            chars.length
        );
    }

    // Work on a fresh copy so the template is never mutated
    let polypeptideSmiles = POLYPEPTIDE_SMILES_TEMPLATE;

    for (let i = 0; i < chars.length; i += 1) {
        const aa = chars[i];

        const threeLetterCode = aminoAcidMapping[aa];
        if (!threeLetterCode) {
            throw new Error(
                "makePolypeptideSmilesFromSequence: invalid residue '" + aa +
                "' at position " + (i + 1)
            );
        }

        const sideChain = sideChains[threeLetterCode];
        if (typeof sideChain === "undefined") {
            throw new Error(
                "makePolypeptideSmilesFromSequence: no side chain defined for " +
                threeLetterCode + " (from '" + aa + "')"
            );
        }

        polypeptideSmiles = polypeptideSmiles.replace("R" + (i + 1), sideChain);
    }

    // Sanity check: no unsubstituted R placeholders should remain
    if (/R[1-9]/.test(polypeptideSmiles)) {
        throw new Error(
            "makePolypeptideSmilesFromSequence: internal error, leftover R placeholders."
        );
    }

    return polypeptideSmiles;
}


// 16 bit deterministic code for naming, with stronger mixing
function code16(str) {
    let h = 1779033703 ^ str.length;
    for (let i = 0; i < str.length; i += 1) {
        h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
        h = (h << 13) | (h >>> 19);
    }
    h = Math.imul(h ^ (h >>> 16), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    h ^= h >>> 16;

    // fold to 16 bits
    const h16 = ((h >>> 16) ^ h) & 0xffff;
    return h16.toString(16).padStart(4, "0");
}

//=================================================
// Peptide bond finder for highlighting
//=================================================
function getPeptideBonds(mol) {
    const pattern = "CC(=O)NC";
    const qmol = window.RDKitModule.get_qmol(pattern);
    const matches = JSON.parse(mol.get_substruct_matches(qmol));
    const aggregatedBonds = [];
    for (let i = 0; i < matches.length; i += 1) {
        const match = matches[i];
        if (Array.isArray(match.bonds)) {
            // peptide C-N bond is the second to last bond
            aggregatedBonds.push(match.bonds.slice(-2)[0]);
        }
    }
    return aggregatedBonds;
}

//=================================================
// Draw a peptide for a given sequence on an existing canvas
//=================================================
function drawPeptideOnCanvas(word, canvas, highlightPeptide = true) {
    const smiles = makePolypeptideSmilesFromSequence(word);
    const mol = RDKitModule.get_mol(smiles);
    const name = "peptide_" + code16(word);

    const mdetails = {
        // legend: name,
        explicitMethyl: true
    };

    if (highlightPeptide === true) {
        mdetails.bonds = getPeptideBonds(mol);
        mdetails.atoms = [0];
        mdetails.highlightColour = [0, 1, 0];
    }

    // light gray card background, #cccccc = 0.8
    mdetails.backgroundColour = [0.8, 0.8, 0.8];
    mdetails.clearBackground = true;

    mol.draw_to_canvas_with_highlights(
        canvas,
        JSON.stringify(mdetails)
    );
}

//=================================================
// High level: create canvas in a container and draw
//=================================================
function renderSequence(word, containerId = "peptide") {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error("renderSequence: container id not found:", containerId);
        return;
    }

    container.innerHTML = "";

    // name is only used as legend in drawPeptideOnCanvas, not as a header
    const name = "peptide_" + code16(word);

    const canvas = document.createElement("canvas");
    canvas.id = "canvas_" + code16(word);
    canvas.width = 800;
    canvas.height = 450;

    container.appendChild(canvas);

    // drawPeptideOnCanvas reads RDKitModule and uses `name` as legend
    // via code16(word); it does NOT require an <h4> element
    drawPeptideOnCanvas(word, canvas, true);
}

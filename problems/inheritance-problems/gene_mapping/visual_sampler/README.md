# Gene-mapping visual sampler

This is a local gallery of approved SVG artwork and visual arrangements for
gene mapping. It leads with the selected color-sector yeast asci, then shows
all 26 fly phenotypes in blue, green, and purple beside gene descriptions.
Everything is visible on one continuous page, with no tabs or full assessment questions.

The genotype examples are illustration fixtures, not generated problems. Production
generators now share the approved renderers in [genemap_art](../genemap_art/README.md).
An optional export harness uses one real two-gene fly question to check the existing
Blackboard image path outside the gallery.

Build the self-contained gallery and validate its source/SVG structure:

```bash
source source_me.sh && python3 problems/inheritance-problems/gene_mapping/visual_sampler/build_gallery.py --check
```

Capture Chromium review images and create the seven-page, letter-size PDF:

```bash
source source_me.sh && python3 problems/inheritance-problems/gene_mapping/visual_sampler/build_gallery.py --check --screenshot
```

Generated artifacts remain ignored under `output_gene_mapping_visuals/`. The editable
SVG examples, comparison gallery, PDF, review captures, export package, and evaluator report
belong there; this directory holds only the reproducible renderer source.

`gene_mapping_visual_sampler.html` and `fly_base_study.html` contain the same art gallery,
preserving the existing study bookmark. You can also use the browser's Print / Save as PDF.
The generated PDF is `gene_mapping_art_gallery.pdf`. Add `--export-preview` only when checking
the separate Blackboard image export; it does not add a question to the art gallery.

## Individual fly portraits and gene colors

[phenotype_art.py](../genemap_art/phenotype_art.py) owns the original side-view character. Each expressed
recessive trait has its own feature and color, following `docs/COLOR_PALETTE.md`:

| Gene | Trait | Visual feature | Color |
| --- | --- | --- | --- |
| f | fuzzy | Translucent cream fur with gene-colored curls across abdomen and thorax | Red #D40000 |
| n | nerdy | Matched rectangular glasses, taped bridge, and bow tie | Green #007A00 |
| p | prickly | Translucent blue spines above wings, with roots behind body | Blue #003FFF |
| t | tipsy | A purple foaming beer mug held below the head | Purple #A719DB |

The base body and eyes are neutral. The original four-trait renderer retains its historical
combination support; plus alleles add no phenotype feature. Fur now lies over the abdomen
and thorax with partial fill transparency. Spines overlap the wings but their roots sit behind
the body, with translucent fills and solid contours. The front-view and anatomical alternatives are retired
from the current gallery, as are microscope fields and the culture bottle.

The current gallery shows one trait per portrait at 72 px beside its description, read from
`phenotypes_for_flies.py`. It no longer presents mixed-trait offspring or a combination key.
The yeast artwork and all 26 fly drawings are approved for use in the questions.
Each has an editable SVG named `fly_portrait_<phenotype>.svg`, plus `_blue`, `_green`,
and `_purple` variants. [individual_phenotypes.py](../genemap_art/individual_phenotypes.py) uses
`lxml.etree` to adapt the shared fly geometry and add individual scenes or props. No claim
is made that the new traits can be combined. Mixed-phenotype work is explicitly out of scope;
the experimental one-body/overlay helper and its gallery section have been removed.
Historical mixed-trait SVGs remain reproducible for reference. The optional export uses
the production placement beside gene descriptions, with the original offspring data table.

### Coverage of the 26-trait bank

The bank contains one named phenotype for each letter. Independent portraits allow different
visual constructions without requiring all of them to coexist on one fly:

| Drawing challenge | Traits | Implication |
| --- | --- | --- |
| Surface texture | bumpy, dewy, fuzzy, gooey, icy, prickly, valley, waxy | Distinguish bumps, drops, fur, coating, frost, bristles, grooves, and wax at small sizes. |
| Shape or anatomy | eery, horsey, kidney, leafy, mushy, nerdy, okra | Use posture, scale comparison, silhouette, wing shape, softness, or an accessory. |
| Color or pattern | artsy, rusty, xanthic | Preserve patterned wings, rust patches, and a warm bulb filament while exploring whole-character gene hues. |
| Behavior or sensory cue | chummy, jerky, quacky, spicy, tipsy, yucky, zippy | A second fly, motion, sound, or playful prop may communicate more than a portrait alone. |
| Ambiguous appearance | ugly | The existing dull/uneven description needs a specific visual interpretation. |

The current redesign changes the body as well as its accessories. Horsey uses the selected
draft-horse body and cowboy hat; zippy uses the selected rocket body and flight helmet.
Jerky has rounded coil-spring legs. Kidney and okra extend through the thorax. Valley has an
accordion body with shaded bellows, and xanthic has an incandescent-bulb abdomen with
a filament and screw base. These are humorous metaphors, not changes to the gene definitions.
Artsy and leafy have larger wings; bumpy and dewy have more extensive surface texture.
Ugly uses mismatched anatomy, while yucky has an odor cloud. Gooey's dripping coat is retained.
Shared wing roots extend into the body; quacky and mushy also lower their wing placement.

Every phenotype has three 72-px variants side by side: blue, green, and purple from the
documented palette. Wings always carry the gene color. Each phenotype keeps its own base head
color across variants: brown for horsey, yellow for quacky and xanthic, rust-brown for rusty,
and so on. Glasses and hats are props and can vary independently of the head underneath.
Thorax, abdomen, texture, and props receive color according to the individual phenotype.
These are 78 separate editable SVGs, with additional default-color portraits retained for
the study's existing filenames.

The target is 25-75% of visible artwork changing with the assigned gene color, not uniform
recoloring. Horsey retains a brown head and legs around its colored torso. Leafy emphasizes
its wings over a neutral body. Bumpy mixes colored and warm bumps; fuzzy retains cream fur
with colored curls; waxy retains cream wax. Quacky and spicy keep colored bodies, while
rusty's abdomen stays rust-brown. Xanthic's threaded, gene-colored screw base IS its thorax,
between its yellow head and warm yellow bulb abdomen. There is no separate rounded thorax.
Original descriptions and production wording remain unchanged.

The local `color_balance_review.md` records each phenotype's rendered color-area estimate.
At 72 px, `rsvg-convert` renders each of the three hues on transparency; pairwise RGB changes
are compared over white using a 24/255 maximum-channel threshold and alpha-weighted visible
area. The report gives the minimum and maximum of all three pairings. This is an approximate
area check, not a model of human perception or a student recognition result. It complements
native-size visual inspection. The SVG skill's targeted-editing guidance informed scoping
paint changes by anatomical region rather than replacing every occurrence of a shared color.

The explored weightlifter, interrupted-flight, and skating alternatives were rendered beside
the chosen horse, spring, and rocket concepts. Their comparison page was retired after the
instructor selected the latter directions. The current gallery contains individual phenotypes
and color comparisons only.

Earlier blind-review scores concern the four original traits, not all 26. The current review
is `body_redesign_review.md` in the output directory. These pictures accompany descriptions;
recognition of the hypothetical names without those descriptions has not been established.

## Overlapping yeast spores

Color belongs to each recessive gene, not to a whole genotype. The yeast study assigns red
to a, green to b, and blue to c. Plus alleles remain neutral. The selected treatment gives each locus a fixed sector of the spore. A recessive allele
adds its pale gene color there; several alleles produce several colors, not a blended
genotype color. The earlier band comparison remains in the renderer for reference but is
omitted from the current gallery.

Four slightly overlapping ellipses sit inside the retained organic double membrane.
Back-to-front drawing order interrupts the distant contours; upper-left highlights, subtle
lower-rim shading, and heavier foreground contours give depth. Centers are 32 units apart vertically and 35-36 horizontally, with radii of 20 by 18.
Overlap is about 4-5 units instead of the earlier 7-8, exposing more of each gamete. Labels stay clear of the overlaps.
A 2.8-unit white text stroke replaces the broad white rectangles, exposing more spore color.

### Automatic spore placement

The renderer evaluates all 24 permutations of the four spores. A one-unit grid samples each
elliptical sector and estimates the area covered by spores drawn later. It minimizes the
sum of hidden colored areas, treating plus sectors as neutral. Ties prefer more wild-type
alleles at the upper left, more recessive alleles at the lower right, then a stable lexical
order. Reordering the input does not change the result, and genotype multiplicities remain
unchanged. Sampling models fill overlap, not label halos or antialiased contour strokes.

The fixed drawing order is upper left, upper right, lower left, lower right. With three loci,
a occupies the right sector, b the bottom, and c the left. The upper right loses bottom area;
the lower left loses right-side area; the lower right is fully foreground. Arrangement 3
therefore becomes `+++`, `a++`, `+bc`, `abc`, with the green/blue spore at the lower left.
These are presentation choices, not meiotic order, parental status, or inferred gene order.

Genotypes remain readable at the shown 132 px minimum under ordinary close screen viewing;
use larger examples for projection. Editable examples include `unordered_ascus.svg` and
`unordered_ascus_arrangement_2.svg`.

Validation uses `lxml.etree` to check feature presence/absence and per-gene colors across
the original 16 fly combinations and all eight three-locus spore genotypes in both treatments.
Checks also cover all 26 portrait/description groups, fixed head base colors and changing
wings across all three hues, requested SVG layer order, and stable
spore placement under every permutation of three representative input multisets.
Chromium checks SVG geometry bounds and page overflow, captures color/grayscale previews,
and generates the PDF. The seven-page PDF is reviewed separately from browser captures. The earlier Blackboard image output was
checked for the previous mixed-trait experiment; this revision does not integrate portraits
into production gene descriptions.
Student testing, physical print, and actual LMS import remain unverified.

## Reference credits

- [Ascus.gif](https://commons.wikimedia.org/wiki/File:Ascus.gif), public domain micrograph,
  Commons upload by Rasbak, original English Wikipedia upload attributed to Pthorpe:
  organic membrane and packed-spore inspiration. The new contours and colors are schematic.
- [DBCLS overhead fruit fly](https://commons.wikimedia.org/wiki/File:202208_Fruit_fly_female_adult_from_a_overhead_view.svg),
  DataBase Center for Life Science, CC BY 4.0,
  [source record](https://doi.org/10.7875/togopic.2022.369): spread-wing overhead construction,
  simplified into new contours with reduced vein and hair detail and hypothetical trait layers.
- [DBCLS lateral fruit fly](https://commons.wikimedia.org/wiki/File:202208_Fruit_fly_female_adult_from_a_lateral_view.svg),
  DataBase Center for Life Science, CC BY 4.0,
  [source record](https://doi.org/10.7875/togopic.2022.367): inspected for side-view morphology
  and simplified character treatment alongside the existing Nuhanen-based redraw.
- [Drosophila-drawing.svg](https://commons.wikimedia.org/wiki/File:Drosophila-drawing.svg),
  B. Nuhanen, CC BY-SA 3.0: main side-view reference. Changes include simplified contours,
  flattened colors, revised proportions, reduced veins and hairs, and hypothetical trait layers.
- [Drosophila melanogaster illustration](https://commons.wikimedia.org/wiki/File:Biology_Illustration_Animals_Insects_Drosophila_melanogaster.svg),
  Madboy74, CC0: dorsal reference for abdomen bands and wing overlap.
- [Drosophila XY sex determination](https://commons.wikimedia.org/wiki/File:Drosophila_XY_sex-determination.svg),
  YassineMrabet, CC BY-SA 4.0: inspected for morphology; no chromosomes or sex-specific markings copied.
- [Sflava Clipart.svg](https://commons.wikimedia.org/wiki/File:Sflava_Clipart.svg),
  MA Hanson, CC BY-SA 4.0: inspected for lateral leg posture; depicts *Scaptomyza flava*,
  so its specific morphology was not used as a *D. melanogaster* anatomical template.
- [Animals - Drosophila (496) -- Smart-Servier.png](https://commons.wikimedia.org/wiki/File:Animals_-_Drosophila_%28496%29_--_Smart-Servier.png),
  Laboratoires Servier, CC BY-SA 3.0: inspected as a scientific style reference; its dorsal
  artwork and detailed venation are not embedded in the sampler.

New fly artwork is licensed under
[CC BY-SA 4.0](../../../../LICENSE.CC-BY-SA-4.0). This applies to the fly drawings,
including embedded copies; it does not change the license of the question text or Python code.
Downloaded reference copies are local review inputs in the ignored output directory.

Construction guidance came from the SVG skill's local-only sources: *Drawing Mentor 1-3*
(basic-shape construction, lines 648-658), *A Handbook of Biological Illustration*
(clarity and line hierarchy, lines 278-294), and *Generative Art with JavaScript and SVG*
(Grouping and Reusing Elements, lines 2349-2380). These informed silhouette-first construction,
limited internal detail, and named SVG groups. No book passages are included in the artwork.
The character redesign also used *The Everything Drawing Book*, Creating Texture
(lines 1123-1157) and Thumbnail Sketches and Working Drawings (lines 1429-1458), for large
texture cues and testing small silhouettes before adding detail. Hypothetical traits are
deliberately exaggerated under the instructor's direction.

This revision specifically used the handbook's perspective passage (lines 286-294):
near contours interrupt distant ones, and heavier foreground outlines reinforce overlap.
The gene-color sectors and bands are original diagrammatic treatments.

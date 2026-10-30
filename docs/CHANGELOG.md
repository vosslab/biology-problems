# Changelog

## 2026-10-30

### Worksheet spacing corrections

- Give blank gene-pair classification cells a 3em minimum writing area while keeping spore cells compact.
- Arrange ascus visuals four across for two genes and in two rows of three for three genes.
  Put set numbers at the bottom right of each image cell, with counts below the SVG.
- Remove forced full-width/fixed-layout nested spore tables and reduce worksheet padding.
  Keep rounded genotype boxes compact, use white wild-type cells, and retain pale gene-colored
  recessive cells. Keep symbol slots aligned using monospace metrics rather than fixed column widths.

### Documentation fixes

- Draft an investigation brief for class checks in Python and Rust QPM, distinguishing PNG
  rendering inputs from final Blackboard HTML and leaving implementation choices to code findings.
- Link the SVG-artwork notices directly to the official CC BY-SA 4.0 license page.
  Remove the root `LICENSE.CC-BY-SA-4.0` file and clarify that this license applies only
  to the fly artwork, leaving question-text and code licensing unchanged.

### Developer tests and notes

- Add `BB_ULTRA_STYLE.md` as the canonical Blackboard markup/style guide, with explicit
  `style`-attribute examples, forbidden classes/stylesheets, compact-table guidance, PGML
  exceptions, and the source-check command. Link it from agent and question authoring guidance.
- Add a pytest source guard against class attributes, style blocks, and external stylesheets
  in Blackboard question generators and banks. Permit PGML and standalone local previews.
  Failures identify the source location: replace class-based styling with element-local
  `style` attributes and remove unused marker classes rather than exempting generators.
- Remove remaining production fly, box-plot, and pedigree marker classes without changing
  their appearance; use anatomy metadata for internal fly recoloring.

### Presentation refinements

- Condense unordered three-gene tetrad final answers into one direct, labeled sentence. Keep
  the dynamic pair keys, centimorgan units, and gene-order placeholder unchanged.
- Remove class attributes from generated tetrad artwork and worksheets because Blackboard Ultra
  accepts their inline styles but does not support CSS classes.
- Group each worksheet spore in a rounded genotype box. Recessive alleles now use larger,
  bold, gene-colored text on pale matching fills; wild-type symbols stay muted on neutral fills.
- Reduce fly offspring-table header and cell padding. Let fly-description tables size to
  their content and portrait cells follow the SVG dimensions; retain the prose width cap.

### Removals

- Remove the deprecated `broken-tetrad_unordered_three_gene-distances_plus.py` generator;
  the active three-gene distances-plus generator already supplies its question format.

## 2026-10-29

### Additions and New Features

- Add a color-coded calculation worksheet below unordered-tetrad ascus visuals. It aligns each
  locus beneath every spore, leaves pair classifications blank, and keeps the same set numbers
  and counts as the visual data.
- Let split three-gene tetrad and four-point test-cross panels wrap naturally when display space
  is narrow while retaining side-by-side panels when space permits.

### Behavior or Interface Changes

- Add selectable labels and full, label-only, or no generated colors to YAML SEQUENCEMC
  questions. Keep the four sequences complete and consistently labeled; assign palette colors
  by shuffled display position, preserve native ORDER output, and document label capacities.
- Name YAML sequence multiple-choice banks `bbq-SEQUENCEMC-<bank>-<count>_items-questions.txt`
  instead of `bbq-MCORDER-`. Preserve MC question records and native ORDER filenames.
- Document the color rationale for SEQUENCEMC and native draggable ORDER questions, including
  the answer leak from rank-based colors and the LMS-controlled initial shuffle.

### Developer Tests and Notes

- Reduce permanent SEQUENCEMC tests from seven to four: remove exact token/palette inventories,
  exhaustive style rendering, and capacity error wording; retain sequence correctness, item-color
  consistency, and color-mode behavior. Require each choice's label-color mapping to match the
  prompt, with all three labels present. Verify with the focused ordering YAML test.
- Rotate the active changelog per repository policy into `CHANGELOG-2026-10b.md` and
  `CHANGELOG-2026-10c.md`, keeping the two newest date blocks active.

## 2026-10-28

### Additions and New Features

- Group each production fly portrait and gene description in a compact rounded card with
  a pale neutral background, thin border, and tighter padding. Keep the shared table wrapper
  for Blackboard image export.
- Increase yeast spore gene-sector opacity from 33% to 60% for darker, more saturated
  colors in both production questions and the gallery. Retain the question's gene hues,
  neutral wild-type sectors, shading, overlap, and genotype labels.
- Integrate the approved artwork into production gene-mapping questions: individual fly
  portraits beside gene descriptions and overlapping color-sector asci in unordered tetrad
  tables. Share renderers with the gallery through the local `genemap_art` module. Use each
  question's gene palette consistently in text and artwork; retain genotypes, counts, answers,
  and ordered-tetrad rendering. Place inline SVGs inside tables for the existing Blackboard
  image-export path.
- Balance color coverage across all 26 fly portraits toward a 25-75% visible-area target.
  Always recolor wings while preserving each phenotype's own base head color; choose thorax,
  abdomen, texture, and prop colors individually. Restore contrasting cream fur and wax,
  warm bumps, brown horse anatomy, rust-brown abdomen, and yellow bulb glass. Make xanthic's
  gene-colored threaded screw base replace its thorax. Retain all 78 side-by-side variants
  and verify head/wing color rules plus native-size rendered area estimates.
- Redesign the local fly portraits around stronger body transformations: draft-horse horsey,
  rocket zippy, coiled-spring jerky, rubber-duck quacky, pepper spicy, accordion valley, and
  incandescent-bulb xanthic. Extend textures and shapes across the thorax, enlarge patterned
  and leaf wings, add hats, match nerdy's lenses, and use translucent foreground fur and spines.
  Connect wing roots to the bodies, with lower placements for quacky and mushy. Show all 26
  phenotypes in blue, green, and purple with substantial body, thorax, wing, and material
  recoloring: 78 editable variants. Keep rust patches and the bulb filament recognizable.
  Keep the approved
  yeast SVGs unchanged. Retire the alternative comparison after selection and remove the
  explicitly out-of-scope mixed-phenotype experiment; retain a seven-page individual art gallery.
- Extend the local gene-description art study to all 26 fly phenotypes, with 22 new editable
  SVG portraits using individual silhouettes, surface treatments, props, and small scenes.
  Move prickly spikes in front of wings and behind the body, draw the body over fuzzy fur,
  and replace round nerdy glasses with thick rectangular frames and a taped bridge. Render
  the continuous gallery as seven PDF pages. Use lxml for all new SVG adaptation.
- Replace manually chosen sector-spore order with a 24-permutation search minimizing sampled
  hidden colored area. Resolve ties toward wild-type spores at the back and recessive spores
  in front. Arrangement 3 now places `a++` upper right and `+bc` lower left. Preserve the
  genotype multiset; positions remain aesthetic choices rather than meiotic information.

- Refine the selected yeast color sectors with roughly half the previous spore overlap and
  swap `+b+` with `a+c` in three-locus arrangement 2, exposing the green-only sector without
  changing the genotype multiset. Shift the local fly gallery to individual portraits beside
  existing gene descriptions, retire the combination sheets and band comparison from the
  gallery, and document the different drawing needs across all 26 hypothetical phenotypes.
  The current four fly prototypes remain exploratory; production generators are unchanged.

- Develop the side-view Storybook flies with independently gene-colored fur, spikes, actual
  glasses, and a beer mug; show all 16 combinations at 54 px plus an enlarged key. Replace
  whole-genotype yeast fills with comparable per-gene sectors and bands, slightly overlapping
  spores, layered contours, shading, and tight text halos. Remove front/top comparisons and
  microscope fields from the current gallery. Independent blind review recognized all 16 fly
  combinations; this is not student validation. Inspect the five-page PDF and Blackboard image
  output, and carry each real preview question's gene colors into the illustrations.

- Create two new phenotype-first fly art directions with exaggerated fur, bristles, eyes,
  and movement. Lead the continuous gallery with label-free 54-px comparisons and enlarged
  keys; export all 16 combinations per direction. Blind evaluation exposed occluded traits,
  prompting foreground spines and an independent fur fringe. Storybook flies decoded 16/16;
  graphic trials decoded 14/16. Remove the unhelpful culture bottle. Use the supplied Ascus
  micrograph to soften the sac membrane and spore shapes while retaining genotype colors.

- Replace the tabbed question sampler with a continuous SVG art gallery and printable PDF.
  Preserve the `fly_base_study.html` bookmark, compare scientific overhead and charismatic
  lateral flies using the supplied DBCLS and Wikimedia references, and show visual constructs
  without repetitive questions. Restore locus-colored yeast labels and genotype-specific spore
  fills while retaining the four-spore arrangement. Validate color consistency with `lxml`.

- Redraw the local sampler's flies as simplified side views using the supplied Wikimedia
  references. Compare warm cartoon and restrained scientific bases with modular traits and
  actual-size examples; include source credits and CC BY-SA 4.0 terms for the fly artwork.
  Show the tester's stated recessive traits. Use `lxml.etree` for SVG validation and emit
  quality-90 WebP captures directly. Production generators and question data are unchanged.

- Add an isolated gene-mapping visual sampler with real generator prompts, choices, and frozen
  two-, three-, and four-gene data. It compares unordered yeast asci, microscope fields, fly
  portraits, a test-cross vignette, and specimen trays without changing production generators.
  Its local preview deliberately requests `fn`, `fnp`, and `fnpt` data to exercise combined
  fuzzy, nerdy, prickly, and tipsy artwork. The sampler emits editable self-contained SVG
  examples and WebP review captures under `output_gene_mapping_visuals/`.

### Decisions and Failures

- Independent visual review favors yeast asci and the single fly cross vignette. The specimen
  tray remains an intentionally visible exploration result, but is not a dense four-gene candidate.
  Browser rendering and generated Blackboard image-export package checks passed; LMS import is
  not verified.

### Developer Tests and Notes

- Validate the production artwork integration with two generated questions from each of
  12 active generators; compare two accepted seeded questions per generator against legacy
  presentation helpers, confirming identical keys, choices, and random state. Pass 1,860
  selected inheritance, lint, ASCII, Markdown-link, and source-length checks (two existing
  source-length warnings). Inspect five self-tests at 800/900 px and packaged fly/yeast PNGs
  from Blackboard image exports. The approved gallery's yeast SVG hashes remain unchanged.
  The text checker reads hidden SVG descriptions/credits as prose and reports spacing cues;
  these do not appear in the rendered question text.
  LMS import and physical printing were not tested.

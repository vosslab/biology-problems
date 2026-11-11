# Changelog

## 2026-11-11

### Additions and New Features

- Add Dr. Caffeine linear and quadratic numeric R-squared assignments.
  Each supplies 25 fresh paired observations for the completed tutorial spreadsheet's
  fixed ranges. Randomize slope direction, curvature sign, and fit strength; grade with
  absolute tolerance 0.001. Add a biostatistics README describing generator families,
  tutorial workflows and the distinction between templates and completed sheets.
- Assess tutorial workflow completion by requesting the R-squared result cell;
  keep interpretation and model-comparison instruction in the tutorials.
- Follow existing biostatistics prompts: identify the worksheet and requested result
  by label, leaving cell ranges and formula instructions to the tutorial.
- Document numeric-only copyable-data guidance in the biostatistics README: omit
  irrelevant location labels and use one number per line for single-variable data.
  Leave existing generators unchanged.

### Developer Tests and Notes

- Five focused mathematical checks pass. Ten temporary completed-workbook samples
  agree with LibreOffice Calc's E10/I5 results after replacing A2:B26. Sample 1,000
  draws per model to verify both coefficient signs and varied fit strengths; review
  local HTML and run the student-text checker with no findings.
- Full suite: 6,292 passed and 15 failures outside the changed files, covering stale
  gene-mapping paths, QTI export/browser dependencies, guidance formatting, archived
  changelog links, and the Graphify helper. The installed QTI package does not provide
  the shared `html_selftest` engine. Live Google Sheets and Blackboard import remain
  unverified; the existing tutorial documents and workbook are unchanged.

## 2026-11-09

### Fixes and Maintenance

- Skip two-gene unordered-tetrad distance draws with more tetratypes than parental ditypes
  instead of raising an exception. The existing question collector draws a replacement so one
  unsuitable problem no longer aborts generation or the website build.
- Refocus the question color guide on concept recognition, selective highlighting, and
  coordinated palettes, retaining explanatory examples and practical palette subsets. Treat
  cross-bank consistency and four-term hue spacing as flexible guidance. Move YAML implementation
  notes to the bank authoring guides and refresh authoring-skill copies.

## 2026-11-08

### Additions and New Features

- Add `docs/QUESTION_COLOR_GUIDE.md` for stable concept colors, coordinated template subsets,
  selective prose highlighting, and matching questions that require meaning rather than color cues.
  Link it from the authoring and palette guides; move color policy out of the voice guide and
  refresh the required authoring-skill snapshots with their direct color references.

### Behavior or Interface Changes

- Refine replacement rules in 62 matching and 27 statement banks after reviewing all 122 YAML
  banks. Retain useful concept colors, quiet peripheral highlights, and add distinct labels to
  suitable uncolored matching banks. Preserve disabled/replaced color definitions as comments
  alongside semantic substitutions, including scientific notation and intentionally authored emphasis.
- Keep fixed concept assignments across shuffled subsets and related bank variants. Use spaced
  template subsets for new small sets and explicit CAM16 colors for larger pools; preserve
  component colors in composite genotype crosses. Both templates, generators, helpers, schemas,
  question wording, and answer relationships remain unchanged.

### Fixes and Maintenance

- Improve low-contrast active text colors while retaining their hue associations. All 762 active
  color-rule occurrences meet 4.5:1 on white; the minimum is 4.79:1. Preserve established
  polymerase-I orange (4.79:1) and recessive-genotype blue (5.44:1) as exceptions to the 5.5:1
  house target. Archived color rules remain available in comments with their original values.

### Developer Tests and Notes

- One-time source comparison covers 8,203 strings across all 122 banks: visible replacement text
  and scientific markup are preserved; fields outside replacement rules match the starting data.
  Representative local Chromium previews cover the three biostats examples, a four-term native
  match, and PGML-generated HTML fields. Inspect grayscale and severe protan/deutan simulations;
  sampled orange text against white measures 5.52:1. Preview artifacts live in ignored
  `output_readability/concept_colors/`; live Blackboard import and student learning remain untested.
- Run the suite with `source ./source_me.sh && pytest tests/`. The final run reports 6,291 passed
  and six failures in untouched files: three stale gene-map generator paths, human-guidance format,
  archived changelog links, and an unused variable in the Graphify helper. Focused YAML and
  Blackboard inline-style checks pass; formatting-only edits add no permanent tests.

## 2026-11-04

### Additions and New Features

- Add `-Z` as the short alias for `--image-scale`, matching both QPM converters and bptools.

### Fixes and Maintenance

- Move the six assessment-specific split banks for hypothesis-testing terms, genetics terminology,
  and Mendelian genetics terms into exam-formatting-tools under `task_files/matching_sets/`.
  Retain the full reusable banks here; local copies record their sources for review before reuse.
- Remove unnecessary image-scale forwarding from five text-only generators. Retain overrides
  in the peptide and YAML matching builders that handle molecular drawings or tables.

- Synchronized shared style guides, tests, and repository support files from the starter template.

## 2026-11-01

### Behavior or Interface Changes

- Add `--image-scale` to bptools Blackboard image exports. PNG conversion now defaults to 4x
  for tables and RDKit canvases; callers can select another positive integer scale while retaining
  the rendered image's displayed dimensions.

### Fixes

- Remove paragraph wrappers from monoploid/haploid answer choices to avoid extra vertical
  spacing. Omit fill-in-the-blank answer instructions from deletion-mutant MC questions.
- Allow gene-list deletion maps to scroll within narrow screens so larger maps remain reachable.

### Behavior or Interface Changes

- Make the word deletion generator's `--medium` mix five- and six-gene questions in one
  `05-06_genes` bank. Select the size randomly per question, keep the existing word filter,
  and preserve explicit gene counts. Publish one mixed Medium FiB bank in BPW.
- Make visual chromosome deletions and inversions span at least three genes, with affected
  original arms at least five genes long and retained material on both sides. Keep tandem
  duplications at two genes. Refresh the gallery and the three website banks.
- Use full, consistently colored alteration names in visual chromosome questions. Add gene-order
  descriptions with centromeres and breaks to the HTML diagrams and exported PNG alt text.
- Keep each chromosome independently exportable within its answer frame so text alternatives
  do not repeat nested-table content. Preserve the existing chromosome artwork.

- Vary original arm lengths in visual chromosome-alteration questions: p has two to
  five regions, q has four to eleven, and q is longer in each original. Select deletion
  intervals and terminal exchanges from actual arm lengths. Keep longer diagrams compact
  with closer letter spacing and clear padding around the junctions.
- Always show both chromosomes in every matching diagram. Keep the compact single-
  chromosome presentation and `--always-two` choice for the MC formats.
- Use consecutive original gene letters and blank shared centromere collars in visual
  chromosome-alteration questions. Mark deletion joins, tandem-copy joins, both inversion
  boundaries, and reciprocal exchange joins with the existing white zigzags.
- Show only the affected chromosome for deletion, duplication, and inversion in MC by default;
  add `--always-two` to retain both chromosomes and give those banks a distinct suffix.
  Keep chromosome counts consistent across flipped MC choices, using an unchanged
  chromosome as the fourth option when only one original is shown.

### Maintenance

- Prune duplicate rendering assertions and the exhaustive MC option combinations from
  the new chromosome-alteration tests. Retain focused genetics, original-label, chromosome-
  count, and answer-key contracts. Keep export, screenshot, and mobile-layout checks as
  one-time implementation evidence.

## 2026-10-31

### Additions and New Features

- Add a Python generator for matching `del`, `dup`, `inv`, and `t` to gene-labeled
  chromosome diagrams, plus picture-to-abbreviation MC and the reverse direction with
  `--mc --flip`. Keep the existing generators and text-based matching YAML unchanged.
- Derive internal deletion, tandem duplication, within-arm inversion, and reciprocal
  terminal exchange from one randomized chromosome pair. Preserve gene identities,
  source colors, centromeres, and telomeres across the three question formats.
- Reuse shared chromosome styling with a small gene-labeled, numbered-centromere
  renderer and shared letter formatting. Keep all question CSS inline.
- Document the three distinct output banks and protect sequence transformations,
  displayed fragment colors, and answer mappings with focused behavior tests.

### Visual letter translocation

- Place telomeres in short, solid gray table cells outside the gene-letter areas, with
  rounded outer ends like the deletion-map chromosomes. Keep each cap attached to its
  original fragment through reversals, with continuous borders and no letter overlap.
- Keep chromosome decoration spans nonempty so saved HTML and image exports preserve
  their closing tags and do not nest following content inside clipped junction markers.
  Refresh saved HTML and exported image previews.
- Use four varied light fills per question from the instructor's color-wheel tool,
  following `docs/COLOR_PALETTE.md`. Preserve each fragment's color throughout the item.
  Use solid gray telomere bands with a defined inner edge for consistent visibility
  across the palette. Keep the fill opaque so arm texture and shading do not show through.
- Add a parallel five-choice visual translocation generator using the existing fragment
  model and shared chromosome artwork. Keep gene letters, fragment proportions, shuffled
  choices, and the impossible-product task. Use narrow gray telomere caps that travel with
  original fragment ends, break arrows on source chromosomes, white junctions, and rounded
  gray answer frames without centromeres. Preserve the original terminal end when a
  telomere faces the junction in an impossible product.
- Keep both source chromosomes represented in every choice so color alone cannot reveal
  the key. Preserve the original generator's presentation and output bank, removing only
  import-time demonstration checks so its model can be reused without random side effects.
- Document the separate visual bank and shared size controls, including the model's
  three-gene minimum fragment size for the new entry point.
- Protect the single impossible product, displayed gene order, fragment colors, and
  original telomere positions with focused behavior tests; keep appearance checks as
  one-time rendered evidence.

### Deletion complementation evidence

- Add `-e/--evidence-format complementation` to both deletion generators while preserving
  the default gene-list questions and their filenames. Share the new matrix renderer,
  alphabetize gene columns, and derive every plus/minus result from the same deletion data
  as the chromosome map. Match deletion label colors and give only minus cells a pale tint
  of their deletion's color, leaving plus cells white and both symbols black.
- Explain complementation, wild-type phenotype, and mutant phenotype next to the results,
  including that failure to complement means the deletion uncovers the mutation. Keep
  existing first-gene and word/random-sequence hints, omit uncovered-gene lists and worked
  solution steps in the new mode, and give fill-in questions explicit entry requirements.
- Use monospace plus/minus cells with ASCII minus signs because the image exporter
  strips Unicode minus signs from table descriptions. Preserve both outcomes in exported
  descriptions as well as the visible diagram.
- Place the chromosome map and complementation matrix side by side by default, using
  the four-gene testcross's inline flex-wrap pattern. Keep legends outside the flex row,
  wrap the panels naturally on narrow screens, and export each table independently.
  Share the layout builder across both generators; preserve the gene-list presentation.

### Deletion diagram depth

- Give retained chromosome regions shaded gray surfaces, consistent irregular banding,
  dark outlines, and gently rounded outer ends in both Python deletion generators.
- Keep the original deletion colors and gene-column guides. Draw deleted regions as
  thin, flat color markers within white breaks, and state explicitly that colored
  regions mark deleted DNA while gray regions remain. Preserve deletion coverage,
  numbered headers, color-to-list associations, and grading.
- Add short, shaded gray flanks outside the numbered genes so terminal gene deletions
  appear inside the chromosome. Reuse the retained-DNA renderer for both 18px flanks
  and round only the outer chromosome ends. Refresh smoke exports without adding gene
  positions or changing coverage, answers, or randomization.
- Keep permanent tests focused on coverage, label/color associations, complementation
  results, hints, and entry instructions. Leave tunable fills and layout appearance to
  one-time rendered checks; document the shared render helpers' contracts.

### Chromosome and ordered tetrad depth

- Group each balanced and Robertsonian translocation gamete choice in a compact,
  rounded gray frame using one shared inline-HTML renderer. Remove the balanced
  choices' horizontal rules and empty spacer paragraphs while preserving labels,
  chromosome groupings, and answer keys.
- Give Robertsonian and balanced-translocation chromosome diagrams gently rounded
  outer corners, narrow upper highlights, and darker lower rims using inline styles.
  Preserve chromosome proportions, labels, arm colors, and centromeres.
- Add faint striping with uneven gaps and band widths beneath the cylindrical shading
  using inline gradients. Reuse one fixed-size texture tile across all arms so repeated
  chromosomes match in stems and choices. Keep centromere collars smooth and labels clear.
- Share arm-cell, centromere, and chromosome-table builders across the four chromosome
  renderers, keeping the arm-length calculations and existing calling interfaces.
  Add focused coverage for labeled arm order, chromosome colors, and segment proportions.
- Use the same 32px-wide, 30px-high centromere collars and pale fills in both question
  types, over continuous chromosome-colored material so rounded corners reveal no gaps.
  Keep Robertsonian arm labels and bold black balanced-translocation centromere numbers.
  Share collar sizing, fill selection, shading, highlights, and lower rims. Fix arm line
  height so host-page text cannot make arms taller than their centromeres, and preserve
  explicit custom centromere widths.
- Give Robertsonian gamete choices compact cell padding and explicit foreground and
  background colors, using the shared chromosome artwork throughout.
- Use bold black arm labels with a half-pixel white halo to keep small letterforms
  clear over the chromosome texture. Mark balanced-translocation junctions with a thin white
  zigzag, keeping chromosome outlines, segment lengths, and centromeres intact. Refresh
  the smoke-test HTML, screenshots, and quiz exports with the current artwork.
- Restore the original asymmetric droplet shape and proportions of ordered spores,
  preserving their pinched attachment corners with restrained highlights, shading,
  and thin outlines. Draw each ascus as an elongated, tapered sac with a curved basal
  end, asymmetric rounded tip, and modest wall clearance. Keep spore proportions stable
  at narrow widths and preserve all eight spores, allele order, colors, counts, and grading.

### Fly phenotype display

- Redraw eery with four lower wings and two bent upper legs in the shared SVG portrait.

- Keep fly artwork licensing in source and documentation instead of emitted SVG
  metadata, and shorten portrait descriptions so image export alt text contains
  phenotype information without license URLs or illustration commentary.

### Four-gene tetrad bonus

- Raise the four-gene fly progeny limit to 100,000 while retaining GCF-compatible totals.
- Add a 16-pattern unordered tetrad bonus using the four-gene distance pool, with
  six distances and gene order recovered from the displayed counts. Vary totals
  up to 100,000 using random multiples of counts reduced by their greatest common factor.
- Extend existing ascus artwork to four locus colors with X-shaped boundaries
  and arrange the 16 patterns in a four-by-four grid.

### Gene mapping choices

- Add choice-count options to three-point single-distance and ordered tetrad
  centromere-distance questions, retaining their preferred distractors first.

### CLI cleanup

- Remove unused hint switches from all three two-point test-cross generators and remove
  their misleading hint filename labels. Remove the cis/trans generator's format switches
  because it always emits multiple-choice questions. Real format, choice-count, genotype,
  and shared export controls remain available.

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

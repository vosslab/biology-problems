# Human guidance

<!-- VENDORED HEADER: START -->
Record the durable guidance Neil Voss states, or approves for preservation here, in his own words:
first person or close paraphrase, one to three lines per bullet. Material he supplies as a source
may inform [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) once it is settled, and an entry of uncertain
origin belongs there too. Rules: [REPO_STYLE.md](REPO_STYLE.md).
[PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

## Decision priority

## Review expectations

## Working style

- Executables and libraries should not share too many of the initial characters,
  because it breaks autocomplete.
- QPM abbreviates QTI Package Maker. Keep the established `qti_package_maker` Python import
  namespace and distribution; use QPM for Rust, Wasm, and project integration names. Prefer
  explicit arguments, functions, or defaults over project-specific environment configuration.

## Restriction digest maps

- I required the non-selected restriction enzyme to be on the 0 kb mark, because
  students often think that this DNA is always cut on the 0 mark even though the
  enzyme in the question does not cut there.

## Question writing

- Student-facing voice, style, and pedagogy need as much care as the Python, which is already
  fine.
- My content is not perfect either; we are developing best practices, not copying my old
  questions.
- I love seriously absurd choices.
- Do not assume everything is AI; ideas such as ordering model organisms by complexity (flies
  have legs, eyes, and a brain; worms do not) are mine.
- I am not a writer; I am a thinker and puzzle solver with a strong math mind. Questions
  should be puzzles with few words.

## Blackboard HTML

Authoring rules and examples: [BB_ULTRA_STYLE.md](BB_ULTRA_STYLE.md).

- Put CSS declarations directly in the element's `style="..."` attribute. A `class="..."`
  attribute is not inline CSS and must fail the Blackboard source check, even as a test hook.
- Blackboard question markup must not contain `<style>` blocks or external stylesheets.
  SVG presentation attributes such as `fill` and `stroke` remain valid.
- PGML permits CSS classes, though I discourage them. Standalone local previews are separate
  from Blackboard question markup.
- Use as few HTML elements as possible; Blackboard may not render complex markup as expected.
  Tables are an exception because they are converted to images before import.

# Ordering banks

Copy [TEMPLATE.yml](TEMPLATE.yml), set `topic`, and fill in `steps`. Both scripts read the
same bank. Like MATCH, each key contains a list of alternatives, even for one wording.

```yaml
topic: a sample preparation workflow
steps:
  step 1:
    - Collect the sample.
    - Obtain the sample.
  step 2:
    - Extract DNA.
  step 3:
    - Amplify the target DNA.
```

Every step appears in every question. Step numbers define the correct order; the displayed
numbers in MC questions are assigned after shuffling. Numbers need not be consecutive.
Equivalent wordings belong under the same step. Choose one alternative per step per instance.

## Generate questions

Run from the repository root:

```bash
source source_me.sh
python3 problems/ordering/yaml_order_to_bbq.py -y problems/ordering/TEMPLATE.yml -d 5
python3 problems/ordering/yaml_mc_order_to_bbq.py -y problems/ordering/TEMPLATE.yml -d 5
```

Both use the usual bptools generation and preview options, including `--selftest`.
Native output is `bbq-ORDER-<bank>-<count>_items-questions.txt`; MC output uses `MCORDER`.
Native ordering requires at least two steps. MC requires at least three and supplies four
complete sequences. There is no item-count option: author a separate complete bank when
a shorter exercise is needed.

Native ordering uses the existing Blackboard QTI 2.1 export engine. The shared `-B` option
creates a Blackboard pool ZIP, which supports MC but not native ordering.

## Stems and formatting

The default native stem is "Place the following steps of {topic} in order from first to last."
MC introduces the steps with "The following steps describe {topic}." and asks which sequence
puts them in order from first to last.

Use `question override` for a different ordering criterion, as in
[biotechnology/model_organism_complexity.yml](biotechnology/model_organism_complexity.yml).
Both formats use the override; MC appends "Which sequence gives the correct order?"
Omitted or null overrides use the default stem.

`replacement_rules` works exactly as in MATCH and TFMS. The existing bptools helpers apply
rules once to the stem and selected prose. Write final replacement HTML directly; inserted
markup is not rescanned. See [USAGE.md](../../docs/USAGE.md#text-replacement-rules).
Omit the field or use null for the shared base rules alone.

## Molecular structures

[biochemistry/glycolysis.yml](biochemistry/glycolysis.yml) preserves the existing glycolysis
records. Its alternatives are molecule records with `name`, `abbreviation`, and `SMILES`,
instead of prose strings. Use molecule records throughout a structure bank.
The existing `moleculelib` renders the structures and the question includes the ordered names
as the identification clue. Replacements apply to the displayed names, not SMILES or scripts.

The implementation lives in [orderinglib.py](orderinglib.py); the two executable scripts
select the output format. Neither YAML nor Python needs authored incorrect steps.

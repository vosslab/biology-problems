#!/bin/bash
cd /Users/vosslab/nsh/PROBLEMS/biology-problems/problems/biochemistry-problems/membranes
for s in 2 3 4 5 6; do
  python3 ~/.claude/skills/webwork-writer/references/scripts/lint_pg_via_renderer_api.py -i driving_force_from_gradient.pgml -s $s --json 2>/dev/null | python3 -c "import json,sys,re; h=json.load(sys.stdin).get('renderedHTML',''); out=len(re.findall(r'<circle cx=\"[0-9.]+\" cy=\"45\" r=\"7\"', h)); ca=1 if 'Ca' in h else 0; print(f'seed=$s release_out_blobs={out} has_Ca={ca}')"
done

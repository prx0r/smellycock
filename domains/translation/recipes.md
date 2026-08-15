# translation — RECIPES (concrete how-to)

*Copy-paste recipes for operating the translation layer. All reflect the current working implementation.
Wire mechanics: `reference.md`. Semantics: `model.md`.*

---

## 1. Read the current translation status
```bash
# whole corpus
curl -s localhost:8787/openpatala/translation | python3 -m json.tool
# one work, projected
curl -s "localhost:8787/openpatala/translation/kramasadbhava?select=work_id,committed" | python3 -m json.tool
# via MCP
node mcp/index.mjs   # then call get_translation_status_for_work
```

## 2. Produce one verse through the canonical path
```bash
cd /root/projects/patala
PATALA_T1_CANONICAL=1 python3 pipeline/canonical_translate.py --work kramasadbhava --verses kramasadbhava:v2
# dry-run (segment + write the batch file Hermes reads — NO model call)
python3 pipeline/canonical_translate.py --work kramasadbhava --verses kramasadbhava:v2 --dry-run
```

## 3. Drive the factory (one DAG pass, low-RAM, backgrounded)
```bash
cd /root/projects/patala
setsid nohup env PATALA_T1_CANONICAL=1 FACTORY_PARALLEL=3 \
  python3 pipeline/factory_scheduler.py --works kramasadbhava --max-model-calls 6 --throttle 1 \
  > /tmp/opencode/kramasadbhava-factory.log 2>&1 &
# see the ordered priority queue first
python3 pipeline/factory_scheduler.py --queue
```

## 4. Run the overnight autonomous loop
```bash
bash pipeline/start_overnight.sh start
```

## 5. Monitor + recover
```bash
tail -f /tmp/opencode/factory-loop.log
python3 pipeline/factory_status.py --all            # the corpus dashboard
python3 pipeline/factory_certificate.py             # 0 dup = healthy
# recover: retry durable failures, then re-run the pass
python3 pipeline/factory_scheduler.py --retry --layers T1
```

## 6. Use the canonical generator in Python (drop-in)
```python
import sys; sys.path.insert(0, "/root/projects/patala/pipeline")
import canonical_translate
handlers = canonical_translate.make_t1_handlers()
proposals = canonical_translate.canonical_t1_generator("T1", [{"object_id":"kramasadbhava:v2","verse":"tasmiṃ cakre …"}])
ok = [p for p in proposals if p.get("t1_status") == "MACHINE_PROPOSED"]
```

## 7. Validate the layer (the proofs)
```bash
cd /root/projects/patala
python3 pipeline/test_canonical_translate.py           # 10/10 deterministic (no model)
PATALA_REAL_SMOKE=1 python3 pipeline/test_canonical_translate.py   # + one real Hermes call (PASS)
python3 pipeline/test_factory_scheduler.py             # canonical-DAG ALL PASS
cd /root/projects/patalaorg && python3 check.py --refs --naming --manifest   # the layer doc gate
```

---

*Recipes. The full reference: `reference.md`. Semantics: `model.md`. Agents: `agentic.md`. Extensions:
`extension.md`.*

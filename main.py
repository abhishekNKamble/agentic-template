# main.py
import json
from models.model_client import ModelClient
from agents.base_agent import BaseAgent
from agents.reflection_agent import ReflectionAgent
import config

def run_task(requirement_text: str, save_excel=False):
    mc = ModelClient()
    base = BaseAgent(mc)
    reflect = ReflectionAgent(mc)

    # Step 1: Base generation
    raw = base.run(requirement_text)
    # try to parse base output
    try:
        base_list = json.loads(raw)
    except Exception:
        # if base returns non-json, attempt lenient parse via reflection repair
        base_list = []

    # Step 2: Reflection (use reflection model if backend supports model override)
    reflection_model = None
    if mc.backend == "ollama":
        # allow REFLECTION_MODEL override from config
        reflection_model = getattr(mc, 'reflection_model', None)
    corrected = reflect.review(base_list or raw, reflection_model=reflection_model)

    # Step 3: Finalize: ensure sequential IDs
    final = []
    counter = 1
    for tc in (corrected or []):
        tc['id'] = f"TC{counter:03}"
        counter += 1
        final.append(tc)

    if save_excel:
        try:
            import pandas as pd
            for t in final:
                if isinstance(t.get('steps'), list):
                    t['steps'] = "\n".join(t['steps'])
            df = pd.DataFrame(final)
            df.to_excel('testcases.xlsx', index=False)
        except Exception as e:
            print('Excel export failed:', e)

    return final

if __name__ == '__main__':
    sample = open('examples/sample_requirement.txt').read()
    out = run_task(sample, save_excel=True)
    print(json.dumps(out, indent=2))

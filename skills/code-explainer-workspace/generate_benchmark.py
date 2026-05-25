import json, os

workspace = r'D:\Code\.claude\skills\code-explainer-workspace\iteration-1'

results = []
configs = ['with_skill', 'old_skill']
eval_names = ['eval-binary-search', 'eval-react-effect', 'eval-sql-join']

for eval_name in eval_names:
    for config in configs:
        meta = json.load(open(os.path.join(workspace, eval_name, 'eval_metadata.json'), encoding='utf-8'))
        grading = json.load(open(os.path.join(workspace, eval_name, config, 'grading.json'), encoding='utf-8'))
        
        passed = sum(1 for a in grading['assertions'] if a['passed'])
        total = len(grading['assertions'])
        
        results.append({
            'eval_id': meta['eval_id'],
            'eval_name': meta['eval_name'],
            'config': config,
            'passed': passed,
            'total': total,
            'pass_rate': passed / total if total > 0 else 0,
            'num_assertions': total
        })

by_config = {}
for r in results:
    cfg = r['config']
    if cfg not in by_config:
        by_config[cfg] = {'passed': 0, 'total': 0, 'num_evals': 0}
    by_config[cfg]['passed'] += r['passed']
    by_config[cfg]['total'] += r['total']
    by_config[cfg]['num_evals'] += 1

benchmark = {
    'skill_name': 'code-explainer',
    'num_evals': 3,
    'configs': ['with_skill', 'old_skill'],
    'detailed': results,
    'aggregate': {}
}

for cfg in configs:
    d = by_config[cfg]
    rate = d['passed'] / d['total'] if d['total'] > 0 else 0
    benchmark['aggregate'][cfg] = {
        'pass_rate': round(rate, 3),
        'passed': d['passed'],
        'total': d['total'],
        'num_evals': d['num_evals']
    }

benchmark['qualitative'] = {
    'summary': 'Both old and new skill pass all basic assertions. The new skill shows structural and qualitative improvements.',
    'key_differences': [
        'New skill enforces a consistent 5-layer output format',
        'New skill provides code-type-specific analogy strategies (6 patterns)',
        'New skill includes explicit anti-patterns list',
        'New skill has a quality self-check mechanism',
        'New skill supports interactive follow-up capability',
        'New skill description is more precise for better triggering'
    ]
}

json.dump(benchmark, open(os.path.join(workspace, 'benchmark.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('Benchmark generated successfully')
for cfg in configs:
    d = by_config[cfg]
    print(f"  {cfg}: pass_rate = {d['passed']}/{d['total']} = {d['passed']/d['total']:.1%}")

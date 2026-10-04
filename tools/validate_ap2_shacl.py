"""Offline, checksum-bound AP2 port-pilot SHACL validation (no OWL imports/rules)."""
import argparse
import hashlib
import json
from importlib.metadata import version
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.compare import to_canonical_graph
from rdflib.namespace import RDF, RDFS, OWL

SH = Namespace('http://www.w3.org/ns/shacl#')
AP = Namespace('http://projekt-provider.de/ontology/ap2-pilot#')
SHAPE = Namespace('http://projekt-provider.de/shapes/ap2#')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_baseline(root):
    root = Path(root)
    manifest_path = root / 'docs/ap2-shacl-baseline.json'
    baseline = json.loads(manifest_path.read_text())
    for name, expected in baseline['files'].items():
        if Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError('Unsafe baseline path')
        if digest(root / name) != expected:
            raise ValueError('SHACL baseline checksum differs: ' + name)
    for package, expected in baseline['validator_versions'].items():
        if version(package) != expected:
            raise ValueError('SHACL runtime version differs: ' + package)
    schema = Graph()
    for name in baseline['ontology_files']: schema.parse(root / name, format='turtle')
    # Only explicit class hierarchy is used for sh:class/targetClass evaluation.
    # Domain/range inference could hide reversed relations or type pending ports.
    hierarchy = Graph()
    for s, p, o in schema:
        if isinstance(s, URIRef) and isinstance(o, URIRef) and (
                p == RDFS.subClassOf or (p == RDF.type and o == OWL.Class)):
            hierarchy.add((s, p, o))
    return baseline, hierarchy


def validate_graph(root, data, *, profile='canonical', data_kind=None, meta_shacl=True):
    """Return a standard SHACL report and JSON summary; never mutate input data."""
    baseline, hierarchy = load_baseline(root)
    if profile not in baseline['profiles']: raise ValueError('Unknown SHACL profile')
    if data_kind not in {None, 'real', 'synthetic'}: raise ValueError('Unknown data kind')
    shapes = Graph()
    for name in baseline['profiles'][profile]: shapes.parse(Path(root) / name, format='turtle')
    if data_kind is not None:
        node = SHAPE.ContextDataKindShape
        prop = SHAPE.ContextDataKindProperty
        from rdflib.collection import Collection
        allowed = URIRef(str(SHAPE) + 'allowed-' + data_kind)
        Collection(shapes, allowed, [AP.Real if data_kind == 'real' else AP.Synthetic])
        for triple in [(node, RDF.type, SH.NodeShape), (node, SH.targetSubjectsOf, AP.dataKind),
                       (node, SH.property, prop), (prop, SH.path, AP.dataKind),
                       (prop, SH['in'], allowed)]: shapes.add(triple)
    conforms, report, _ = validate(data, shacl_graph=shapes, ont_graph=hierarchy,
        inference='none', meta_shacl=meta_shacl, advanced=False, js=False,
        do_owl_imports=False, inplace=False, abort_on_first=False,
        allow_infos=False, allow_warnings=False)
    if not isinstance(report, Graph): raise ValueError('SHACL validation failed: ' + str(report))
    report = to_canonical_graph(report)
    results = []
    for result in report.subjects(RDF.type, SH.ValidationResult):
        entry = {}
        for name, pred in [('focus_node', SH.focusNode), ('path', SH.resultPath),
                ('value', SH.value), ('shape', SH.sourceShape),
                ('component', SH.sourceConstraintComponent), ('severity', SH.resultSeverity)]:
            obj = report.value(result, pred)
            if obj is not None: entry[name] = str(obj)
        entry['messages'] = sorted(str(v) for v in report.objects(result, SH.resultMessage))
        results.append(entry)
    summary = {'baseline': baseline['id'], 'version': baseline['version'],
        'baseline_sha256': digest(Path(root) / 'docs/ap2-shacl-baseline.json'),
        'profile': profile, 'data_kind': data_kind, 'conforms': bool(conforms),
        'input_triples': len(data), 'validation_results': sorted(results, key=lambda e: json.dumps(e, sort_keys=True)),
        'validator_versions': baseline['validator_versions'], 'inference': 'explicit-class-hierarchy-only',
        'scope': baseline['scope'], 'approval': 'technical validation only; no identity, rights or partner approval'}
    return summary, report


def write_report(output, summary, report):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    (output / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
    # Canonical N-Triples is valid Turtle and gives stable report bytes.
    text = to_canonical_graph(report).serialize(format='nt')
    (output / 'report.ttl').write_text(''.join(sorted(text.splitlines(keepends=True))))


def example_graph(root):
    manifest = json.loads((Path(root) / 'docs/ap2-pilot-profile.json').read_text())
    graph = Graph()
    for name in manifest['example_files']:
        graph.parse(Path(root) / name, format='nt' if name.endswith('.nt') else 'turtle')
    return graph


def main():
    parser = argparse.ArgumentParser(description='Checksum-bound AP2 SHACL validation, offline')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--data', type=Path, action='append', help='Local Turtle or N-Triples; repeat to combine only a coherent selected view')
    parser.add_argument('--profile', choices=['source', 'canonical'], default='canonical')
    parser.add_argument('--data-kind', choices=['real', 'synthetic'])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = Graph()
    if args.data:
        for path in args.data:
            if path.suffix not in {'.ttl', '.nt'}: parser.error('Use explicit .ttl/.nt files; dataset views must be selected by the workflow adapter')
            data.parse(path, format='nt' if path.suffix == '.nt' else 'turtle')
    else: data = example_graph(args.root)
    summary, report = validate_graph(args.root, data, profile=args.profile, data_kind=args.data_kind)
    write_report(args.output, summary, report)
    print(json.dumps({'conforms': summary['conforms'], 'validation_results': len(summary['validation_results']),
                      'output': str(args.output)}, indent=2))
    return 0 if summary['conforms'] else 1


if __name__ == '__main__': raise SystemExit(main())

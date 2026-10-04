"""Offline structural/semantic pilot checks; not an OWL reasoner or SHACL release."""
import argparse
import hashlib
import json
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, DCTERMS, XSD

AP = Namespace('http://projekt-provider.de/ontology/ap2-pilot#')
SOSA = Namespace('http://www.w3.org/ns/sosa/')
PDL = Namespace('https://provider-project.org/ontology/pdl#')
SOURCE = Namespace('https://projekt-provider.de/ontology/')
ROLES = [AP.OperationalPort, AP.Terminal, AP.PortArea, AP.TradeLocation, AP.SourceRecord]
RELATIONS = {AP.describesOperationalPort, AP.servesTradeLocation, AP.areaOfPort, AP.terminalOfPort}


def load(root):
    root = Path(root)
    manifest = json.loads((root/'docs/ap2-pilot-profile.json').read_text())
    schema = Graph()
    for name, digest in manifest['local_reference_files'].items():
        path = root/name
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Pinned reference changed: '+name)
        schema.parse(path, format='turtle')
    data = Graph()
    for name, digest in manifest['example_files'].items():
        path = root/name
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Example checksum changed: '+name)
        data.parse(path, format='nt' if path.suffix == '.nt' else 'turtle')
    return schema, data


def validate(schema, data):
    errors = []
    def types(node):
        if node is None:return set()
        result = set(data.objects(node, RDF.type))
        frontier = list(result)
        while frontier:
            for parent in schema.objects(frontier.pop(), RDFS.subClassOf):
                if isinstance(parent, URIRef) and parent not in result:
                    result.add(parent);frontier.append(parent)
        return result
    def one(node, property):
        values = list(data.objects(node, property))
        if len(values) != 1:
            errors.append(f'{node}: exactly one {property} required')
            return None
        return values[0]
    for subject in set(data.subjects(RDF.type, None)):
        if len(set(ROLES) & types(subject)) > 1:
            errors.append(f'{subject}: distinct pilot roles collapsed')
    for subject, predicate, obj in data:
        if predicate in {OWL.sameAs, OWL.equivalentClass, OWL.equivalentProperty}:
            errors.append('Pilot data cannot declare global identity/equivalence')
    accepted = set()
    for assertion in data.subjects(RDF.type, AP.MatchAssertion):
        subject = one(assertion, AP.subject); relation = one(assertion, AP.relation)
        obj = one(assertion, AP.object); status = one(assertion, AP.reviewStatus)
        kind = one(assertion, AP.dataKind)
        if kind not in {AP.Real, AP.Synthetic} or status not in {AP.Pending, AP.Accepted, AP.Rejected} or relation not in RELATIONS:
            errors.append(f'{assertion}: invalid kind, status or directional relation')
        if not list(data.objects(assertion, AP.evidence)):
            errors.append(f'{assertion}: evidence required')
        if relation in RELATIONS:
            domain = schema.value(relation, RDFS.domain); range = schema.value(relation, RDFS.range)
            if domain not in types(subject) or range not in types(obj):
                errors.append(f'{assertion}: relation domain/range mismatch')
            if relation == AP.describesOperationalPort and status == AP.Accepted:
                if data.value(subject,AP.countryISO3) != data.value(obj,AP.countryISO3):errors.append('Source/canonical port country conflict')
            if relation == AP.servesTradeLocation and status == AP.Accepted:
                if data.value(subject,AP.countryISO2) != data.value(obj,SOURCE.countryCode):errors.append('Port/trade location country conflict')
        if status == AP.Accepted:
            reviewer = one(assertion, AP.reviewer); reviewed = one(assertion, AP.reviewedAt)
            if not isinstance(reviewer, Literal) or not str(reviewer).strip():
                errors.append(f'{assertion}: named reviewer required')
            try:
                if reviewed.datatype != XSD.dateTime or datetime.fromisoformat(str(reviewed).replace('Z', '+00:00')).tzinfo is None:
                    raise ValueError()
            except (ValueError, AttributeError):
                errors.append(f'{assertion}: timezone-aware review date required')
            accepted.add((subject, relation, obj))
            if (subject, relation, obj) not in data:
                errors.append(f'{assertion}: accepted example relation missing')
        elif (subject, relation, obj) in data:
            errors.append(f'{assertion}: pending/rejected relation was materialized')
    for triple in data:
        if triple[1] in RELATIONS and triple not in accepted:
            errors.append('Materialized relation lacks accepted evidenced assertion')
    for subject in data.subjects(RDF.type, AP.OperationalPort):
        two = one(subject, AP.countryISO2);three = one(subject, AP.countryISO3)
        if not re.fullmatch('[A-Z]{2}', str(two)) or not re.fullmatch('[A-Z]{3}', str(three)):
            errors.append('Invalid country code form')
        if str(two) in {'BR', 'DE'} and {'BR': 'BRA', 'DE': 'DEU'}[str(two)] != str(three):
            errors.append('Conflicting example country codes')
    for subject in data.subjects(RDF.type, AP.Observation):
        if SOSA.Observation in types(subject) or list(data.objects(subject,SOSA.hasFeatureOfInterest)):
            errors.append('Observation result must stay separate from SOSA activity')
        day = one(subject, AP.observedDay);feature = one(subject, AP.observedFeature)
        try:
            if day.datatype != XSD.date or date.fromisoformat(str(day)).isoformat() != str(day):
                raise ValueError()
        except (ValueError, AttributeError):errors.append('Canonical observation needs an ISO observation day')
        if AP.OperationalPort not in types(feature):errors.append('Canonical port observation needs canonical port feature')
        if not list(data.objects(subject, AP.hasMeasurement)):errors.append('Canonical observation lacks measurements')
        source=one(subject,AP.sourceObservation)
        if AP.SourceObservation not in types(source):errors.append('Canonical observation lacks typed source observation')
        pw=Namespace('https://portwatch.imf.org/ontology/')
        source_feature=data.value(source,SOSA.hasFeatureOfInterest)
        if (source_feature,AP.describesOperationalPort,feature) not in data:errors.append('Observation source lacks accepted canonical port association')
        if data.value(source,pw.observationDate) != day:errors.append('Observation source day differs from canonical day')
        fields={AP.DailyPortCalls:pw.portCallsTotal,AP.ImportShipmentEstimate:pw.importVolumeTotalTons,AP.ExportShipmentEstimate:pw.exportVolumeTotalTons}
        for measure in data.objects(subject,AP.hasMeasurement):
            metric=data.value(measure,AP.metric)
            try:
                if Decimal(str(data.value(measure,AP.value))) != Decimal(str(data.value(source,fields[metric]) if metric in fields else None)):errors.append('Canonical measurement differs from source value')
            except InvalidOperation:errors.append('Canonical measurement lacks matching source value')
    for activity in data.subjects(RDF.type,AP.ObservationActivity):
        result=one(activity,SOSA.hasResult);feature=one(activity,SOSA.hasFeatureOfInterest)
        if AP.Observation not in types(result) or AP.OperationalPort not in types(feature) or data.value(result,AP.observedFeature) != feature:errors.append('Observation activity/result link invalid')
    for subject in data.subjects(RDF.type, AP.Measurement):
        metric = one(subject, AP.metric);unit = one(subject, AP.unit);value = one(subject, AP.value)
        if unit != schema.value(metric, AP.unit) or unit not in {AP.MetricTonne, AP.PortCallCount}:
            errors.append('Measurement unit incompatible with metric')
        try:
            number = Decimal(str(value))
            if value.datatype != XSD.decimal or not number.is_finite() or number < 0 or (unit == AP.PortCallCount and number != number.to_integral_value()):raise ValueError()
        except (ValueError, InvalidOperation, AttributeError):errors.append('Invalid measurement value')
    for relation, domain, range in [(AP.representsFacility, PDL.Infrastructure, URIRef('http://projekt-provider.de/ontology/Facility')),
                                     (AP.representsEvent, PDL.Event, URIRef('http://projekt-provider.de/ontology/Event'))]:
        if (domain, RDF.type, OWL.Class) not in schema:errors.append('PDL alignment term missing from pinned source')
        for subject, obj in data.subject_objects(relation):
            if domain not in types(subject) or range not in types(obj):errors.append('Invalid scenario representation relation')
    for episode in data.subjects(RDF.type, AP.EventEpisode):
        parent = one(episode, AP.episodeOf)
        if AP.Event not in types(parent):errors.append('Episode must reference an event, not a port or observation')
    for record in {s for s in data.subjects(RDF.type, None) if AP.SourceRecord in types(s)}:
        if not list(data.objects(record, DCTERMS.isPartOf)):errors.append('Source record lacks source dataset/artifact')
        if not list(data.objects(record, AP.sourceRowHash)) and not list(data.objects(record, SOURCE.sourceRow)):
            errors.append('Source record lacks row-level evidence')
    return errors


def main():
    parser = argparse.ArgumentParser();parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1]);args=parser.parse_args()
    schema, data = load(args.root);errors=validate(schema,data)
    print(json.dumps({'profile':'provider-ap2-pilot','version':'0.1.0-rc1','passed':not errors,'schema_triples':len(schema),'example_triples':len(data),'errors':errors,'scope':'Selected local pilot rules; no full OWL/SHACL conformance or partner approval'},indent=2))
    return 1 if errors else 0


if __name__ == '__main__':raise SystemExit(main())

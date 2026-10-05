# CPPI annual source and canonical profiles

This additive profile keeps the existing daily PortWatch model/SHACL baseline unchanged. Files:

- `ontology/source-cppi.ttl`: migrated local CPPI vocabulary, reconciled to the converter namespace `https://provider-projekt.de/ontology/`.
- `ontology/ap2-cppi-profile.ttl`: annual information results, separate SOSA observation activities, explicit port alignments and signed CPPI measurements.
- `shapes/cppi-source-shapes.ttl`: full CPPI source validation.
- `shapes/cppi-canonical-shapes.ttl`: annual source binding, accepted alignment, source-value/unit equality, year/feature/activity consistency, rank/count integrality and fraction range.

`cp:AnnualObservation` uses a reference year (`xsd:gYear`) rather than a day; it is a PROVIDER information result, distinct from the source's SOSA observation representation and from its producing activity. It does not inherit the AP2 daily-observation shape that requires traffic metrics and nonnegative values. A negative CPPI index is valid. The six canonical metric types are CPPI score, reported global rank, administrative/statistical scores, sampled port calls and berth-time fraction. Additional source-only metrics are retained and reported, not silently converted to another unit.

Edition year, reference year and standardization reference year are distinct. The current [World Bank methodological note](https://thedocs.worldbank.org/en/doc/aac122f6df85534428d66a7b9af4b7f6-0400012026/original/CPPI-Methodology-Note.pdf), sections 4.4 and 5, confirms the combined-score/rank interpretation and fixed 2024 reference distribution. CPPI aggregates port-level container activity and does not separately assess an individual terminal. A canonical port alignment is consequently an explicit reviewed relation, not `owl:sameAs` or certification of exact boundaries.

The workflow validates metric bindings against the pinned annual profile graph, which is explicitly included in the validation view. Validation uses pySHACL 0.40.1 / RDFLib 7.6.0 with inference disabled; it does not globally retype source SOSA instances as canonical information results. It also applies the existing registry SHACL gate independently before consolidation. Models and shapes are copied/checksummed into each immutable CPPI snapshot.

Code/data owners: converters and immutable source bundles in `provider-datasets` 0.7.0; reviewed integration and named-graph queries in `provider-workflow`. Real pilot: Hamburg and Santos, 2020–2025, 12 annual results and 22 measurements; two explicitly documented AI source-based reviews, no human partner sign-off or source-rights clearance. The other source ports remain unresolved for canonical identity.

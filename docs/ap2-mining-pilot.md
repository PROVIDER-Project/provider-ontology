# Reviewed mining pilot

Mining v2 and integration ontologies are now versioned under ontology/mining. This is an additive domain module; the existing core/source/port baselines remain separate. provider-mining-pilot.ttl introduces MiningComplex and review evidence; provider-mining-reviewed-shacl.ttl gates the reviewed output. Structural membership and exact identity are evaluated separately, and only exact identities can receive mappedConcept/canonical mappings.

The SHACL gate requires accepted_by_reviewer, nonempty evidence/note/reviewer, a supported explicit relation and no hard conflict. Source candidate graphs are not claimed to conform to this release shape. The 1.0.0 pilot module does not import models over the network. Original v2 shapes and classification alignments remain available locally, without pretending their converter domains were all tested in this pilot.

Only reviewed assertion graph validation is applied during the workflow gate; GEM enrichment remains a separate source artifact. Real mining source data and reviewed records are not committed.

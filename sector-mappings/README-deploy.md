# Deploying the sector mappings to Fuseki

`upload-rdf-via-gsp.sh` posts every RDF file listed in a mapping file to a SPARQL
Graph Store endpoint, one request per graph. It is a thin wrapper: all arguments
it does not know are handed to `curl` unchanged, so endpoint URL, TLS, proxy and
retry options are plain curl options and are documented by curl, not here.

Run it from this directory: the file paths in the mapping table are used exactly
as written.

    ./upload-rdf-via-gsp.sh -u bob --mapping-file graph-to-file.tsv \
        http://internal-host:8080/provider/gsp

    GSP_PASSWORD='…' ./upload-rdf-via-gsp.sh -u bob \
        --cacert 'my ca.pem' --retry 2 --max-time 600 \
        --mapping-file graph-to-file.tsv https://internal-host/provider/gsp

## Mapping file

`graph-to-file.tsv` holds one target per line, tab-separated: `<graph IRI>`, then
the RDF file. Blank lines and lines whose first non-blank character is `#` are
skipped, which is how the commented-out TiVA outputs stay out of a run. Repeat
`--mapping-file` to load several tables in one command. Add new codelists by
appending a line; `cpc21-hs2021` shows that the graph name need not match the
file name or folder.

## What the script adds to curl

- Graph selection per entry through `--url-query "graph=<iri>"`, which
  percent-encodes the IRI itself, and a `Content-Type` inferred from each file
  name (`.ttl`, `.trig`, `.nt`, `.nq`, `.rdf`/`.xml`/`.owl`, `.jsonld`).
- A preflight over every mapping file: unreadable tables, malformed lines and
  missing RDF files are all reported with `<file>:<line>` and abort the run
  before the first request. Without it a typo on line 7 leaves lines 1 to 6
  already in the store.
- One password per run rather than one per graph: it is read once, then used for
  every request. Sources in order of precedence: an inline `-u name:password`,
  else `$GSP_PASSWORD` when non-empty (set-but-empty counts as unset), else a
  hidden terminal prompt or a single silent line from standard input. Nothing to
  read means exit 2, never an empty password.
- Credentials delivered to curl as one config line on its standard input with a
  trailing `--config -`, so the secret is never a curl argument and curl prints no
  prompt of its own. As a side effect this line outranks a `user` key from your own
  `-K` config file, while leaving authentication to curl entirely when `-u` is
  omitted: then nothing is offered and `--netrc`, `~/.curlrc` or a config file given
  by `-K` decides.
- Per-graph reporting with the originating line on failure, uploads continuing
  past one failed graph. Exit status: 0 all uploaded, 1 some failed or the
  preflight found problems, 2 bad usage.

## Overriding the defaults

Arguments you pass are placed after the script's own curl flags, so a single value
option takes your value — `--request PUT` for instance wins over the default POST,
and in Graph Store terms that means replacing the graph instead of appending to it.
Options curl repeats rather than replaces, notably `--header` and `--url-query`, add
to what the script sets: a second `Content-Type` reaches Fuseki beside the inferred
one, so set them knowingly.

Two details about argument handling: everything after `--` is passed through even
if it reads like one of the script's own options, and `-h` belongs to curl (`-h
all`), while this script answers only `--help`. `--mapping-file` stays long-only
because short letters are spoken for — `-m`, `-f` and `-H` mean something else to
curl — and `-u` deliberately shadows curl's own `--user`, since the password has
to be read before curl runs.

## Caveats

- POST appends. Re-running the same table into the same graph adds those triples
  again; clear the graph first or switch the request with `--request PUT`.
- `curl -v` as an argument prints the `Authorization` header, and `bash -x`
  prints `$GSP_PASSWORD`: both expose the secret in whatever log you are writing.
- The endpoint must accept updates: a read-only Fuseki dataset rejects these POSTs.

Dependencies: bash, and curl 7.87 or newer for `--url-query`.

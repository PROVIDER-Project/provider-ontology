#!/usr/bin/env bash
#
# Uploads RDF files to a Fuseki endpoint through the SPARQL Graph Store
# Protocol: one POST per "graph <TAB> file" line of the given mapping files.
# POST appends, so uploading the same graph twice adds it twice.

set -uo pipefail

usage() {
  cat <<'EOF'
usage: upload-rdf-via-gsp.sh [options] <mapping-file>...

Options:
  --curl-args <string>   Extra curl arguments, also as --curl-args=<string>,
                         may be repeated. Must supply the Graph Store endpoint
                         (and authentication), for example
                           --curl-args "--user user:pw http://host:8080/ds/gsp"
                         The string is split by the shell again, so quoting
                         works ("--user 'u:p w'") but so does expansion of
                         $vars and backticks - quote them to keep them literal.
                         They are passed after our own curl flags: a single
                         value option (--request, --url) then uses yours, while
                         options curl repeats (--header, --url-query) are sent
                         twice rather than replaced.
  -h, --help             Show this help.

Each mapping file lists one target per line, tab-separated:

  <graph IRI>\t<rdf file>

Empty lines and lines whose first non-blank character is '#' are skipped. File
paths are taken as written, so they resolve relative to the working directory
this script is started from. The Content-Type is chosen from each file's name.

All files named by all mapping files are checked before anything is uploaded;
a missing file or a malformed line aborts the whole run. Uploads continue when
one of them fails, and the exit status is 1 if any failed.
EOF
}

# The endpoint can only come from --curl-args (or curl's own config file), so
# warn when it looks like somebody forgot it.
endpoint_note() {
  local arg found=0
  for arg in "$@"; do
    case "$arg" in
      *://* | --url | --config | -K) found=1; break ;;
    esac
  done
  if ((found == 0)); then
    echo "warning: no endpoint URL in --curl-args, curl has to get it elsewhere" >&2
  fi
}

# Content-Type for a file name; fails when the extension is not a known RDF one.
content_type() {
  local name=${1,,}
  case "$name" in
    *.ttl | *.turtle) echo "text/turtle" ;;
    *.trig) echo "application/trig" ;;
    *.nt) echo "application/n-triples" ;;
    *.nq) echo "application/n-quads" ;;
    *.rdf | *.xml | *.owl) echo "application/rdf+xml" ;;
    *.jsonld | *.json-ld) echo "application/ld+json" ;;
    *) return 1 ;;
  esac
}

strip() { # leading and trailing whitespace
  local text=$1
  text=${text#"${text%%[![:space:]]*}"}
  echo "${text%"${text##*[![:space:]]}"}"
}

curl_args=()
mappings=()

while (($#)); do
  case "$1" in
    --curl-args)
      if [[ $# -lt 2 ]]; then
        echo "error: --curl-args needs a value" >&2
        usage >&2
        exit 2
      fi
      arg_value=$2
      shift 2
      # Re-split the given string on purpose: it lets callers quote values.
      eval "curl_args+=( $arg_value )"
      ;;
    --curl-args=*)
      arg_value=${1#--curl-args=}
      shift
      eval "curl_args+=( $arg_value )"
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    --)
      shift
      mappings+=("$@")
      break
      ;;
    -*)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      mappings+=("$1")
      shift
      ;;
  esac
done

if ((${#mappings[@]} == 0)); then
  echo "error: no mapping file given" >&2
  usage >&2
  exit 2
fi

endpoint_note "${curl_args[@]}"

graphs=()
files=()
types=()
where=() # mapping file and line an entry came from, for messages
problems=0

for mapping in "${mappings[@]}"; do
  if [[ ! -r $mapping ]]; then
    echo "error: $mapping: not readable" >&2
    problems=$((problems + 1))
    continue
  fi

  lineno=0
  while IFS= read -r line || [[ -n $line ]]; do
    lineno=$((lineno + 1))
    line=${line%$'\r'}
    [[ -z $(strip "$line") ]] && continue
    [[ $(strip "$line") == \#* ]] && continue

    if [[ $line != *$'\t'* ]]; then
      echo "error: $mapping:$lineno: expected '<graph IRI><TAB><file>', found no tab" >&2
      problems=$((problems + 1))
      continue
    fi

    graph=$(strip "${line%%$'\t'*}")
    file=$(strip "${line#*$'\t'}")
    if [[ -z $graph || -z $file ]]; then
      echo "error: $mapping:$lineno: both a graph IRI and a file are required" >&2
      problems=$((problems + 1))
      continue
    fi
    if [[ $file == *$'\t'* ]]; then
      echo "error: $mapping:$lineno: unexpected field after the file path" >&2
      problems=$((problems + 1))
      continue
    fi

    if ! type=$(content_type "$file"); then
      echo "error: $mapping:$lineno: cannot tell the RDF format of '$file'" >&2
      problems=$((problems + 1))
      continue
    fi
    if [[ ! -f $file ]]; then
      echo "error: $mapping:$lineno: no such file: $file" >&2
      problems=$((problems + 1))
      continue
    elif [[ ! -r $file ]]; then
      echo "error: $mapping:$lineno: $file is not readable" >&2
      problems=$((problems + 1))
      continue
    fi

    graphs+=("$graph")
    files+=("$file")
    types+=("$type")
    where+=("$mapping:$lineno")
  done <"$mapping"
done

if ((problems > 0)); then
  echo "error: $problems problem(s), nothing uploaded" >&2
  exit 1
fi

if ((${#graphs[@]} == 0)); then
  echo "nothing to upload"
  exit 0
fi

failures=0
for i in "${!graphs[@]}"; do
  printf 'POST %s <- %s (%s)\n' "${graphs[i]}" "${files[i]}" "${types[i]}"
  if ! curl --fail-with-body --show-error --silent --globoff \
    --request POST \
    --header "Content-Type: ${types[i]}" \
    --url-query "graph=${graphs[i]}" \
    --data-binary "@${files[i]}" \
    "${curl_args[@]}"; then
    echo "error: ${where[i]}: upload failed" >&2
    failures=$((failures + 1))
  fi
done

if ((failures > 0)); then
  printf 'error: %d of %d uploads failed\n' "$failures" "${#graphs[@]}" >&2
  exit 1
fi

printf '%d graph(s) uploaded\n' "${#graphs[@]}"

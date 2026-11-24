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
                         may be repeated. Must supply the Graph Store endpoint,
                         for example
                           --curl-args "http://host:8080/ds/gsp"
                         The string is split by the shell again, so quoting
                         works ("--cacert 'my ca.pem'") but so does expansion of
                         $vars and backticks - quote them to keep them literal.
                         They are passed after our own curl flags: a single
                         value option (--request, --url) then uses yours, while
                         options curl repeats (--header, --url-query) are sent
                         twice rather than replaced.
  -u, --user <name>      User name for the endpoint. The password is read once
                         and then used for every graph; also as --user=<name>
                         or -u<name>. Written <name>:<password>, it takes the
                         password from the argument instead of reading it, which
                         is convenient in cron but visible to other users for a
                         moment. Cannot be combined with --user inside
                         --curl-args.
  -h, --help             Show this help.

The password comes from the first of these that applies:

  1. the <name>:<password> written after -u
  2. $GSP_PASSWORD, when it is set to something non-empty (set but empty means
     unset, and a forgotten export is why)
  3. typed at the prompt with the input hidden, or one line read from standard
     input when that is not a terminal:
       printf '%s\n' "$pw" | ./upload-rdf-via-gsp.sh -u bob --curl-args ... file.tsv

The password reaches curl through its own standard input rather than as an
argument, so it stays out of process listings and shell history. It shows up
only where you ask for it: --curl-args "-v" makes curl print the Authorization
header, and bash -x prints the variable.

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

# host:port of the endpoint given in --curl-args, for messages only.
endpoint_host() {
  local arg
  for arg in "$@"; do
    case "$arg" in
      *://*)
        arg=${arg#*://} # drop the scheme
        arg=${arg#*@}   # drop any user info
        echo "${arg%%/*}"
        return
        ;;
    esac
  done
}

# A string as curl's config file syntax wants it inside double quotes.
config_quote() {
  local text=${1//\\/\\\\}
  text=${text//\"/\\\"}
  text=${text//$'\n'/\\n}
  text=${text//$'\r'/\\r}
  text=${text//$'\t'/\\t}
  echo "$text"
}

curl_args=()
mappings=()
user="" # -u/--user, which may carry the password as name:password

use_user() { # records the user name, refusing an empty one or a second one
  if [[ -n $user ]]; then
    printf 'error: --user given twice (%s and %s)\n' "$user" "$1" >&2
    exit 2
  fi
  if [[ -z ${1%%:*} ]]; then
    echo "error: --user needs a user name before any ':'" >&2
    exit 2
  fi
  user=$1
}

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
    -u | --user)
      if [[ $# -lt 2 ]]; then
        echo "error: $1 needs a value" >&2
        usage >&2
        exit 2
      fi
      use_user "$2"
      shift 2
      ;;
    --user=*)
      use_user "${1#--user=}"
      shift
      ;;
    -u?*)
      use_user "${1#-u}"
      shift
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

# Both -u and a curl --user would authenticate, with curl's rule of the last one
# quietly winning; refuse rather than depend on argument order. A value that
# merely starts like such an option is refused too, which is easier to explain
# than to trace.
if [[ -n $user ]]; then
  for curl_arg in "${curl_args[@]}"; do
    case "$curl_arg" in
      --user | --user=* | -u | -u?*)
        echo "error: give the user name either with -u or in --curl-args, not both" >&2
        exit 2
        ;;
    esac
  done
fi

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

# The secret is read once here - after the checks, so a run that cannot start
# never asks for it - and it is never printed in a message.
password=""
if [[ -n $user ]]; then
  login=$user
  password=${GSP_PASSWORD-}
  if [[ $user == *:* ]]; then # the password came with -u, nothing to read
    login=${user%%:*}
    password=${user#*:}
  elif [[ -z $password ]]; then # an empty GSP_PASSWORD counts as unset
    host=$(endpoint_host "${curl_args[@]}")
    if [[ -t 0 ]]; then
      printf 'Enter password for %s%s: ' "$login" "${host:+@$host}" >&2
    fi
    if ! IFS= read -r -s password; then
      [[ -t 0 ]] && echo >&2 # only a prompt leaves a line unfinished
      printf 'error: no password available for user %s\n' "$login" >&2
      exit 2
    fi
    if [[ -t 0 ]]; then # the line break hidden input leaves out, and a hint
      echo >&2        # that something was typed at all without showing it
      printf '(%d characters)\n' "${#password}" >&2
    fi
  fi
fi

# One curl config line holding the credentials; empty when running anonymously.
curl_config=""
if [[ -n $user ]]; then
  curl_config="user = \"$(config_quote "$login:$password")\""
fi

# The config line travels on curl's standard input and --config - comes last, so
# it outranks a config file given in --curl-args as well. Anonymous runs feed one
# empty line, which the config syntax ignores.
failures=0
for i in "${!graphs[@]}"; do
  printf 'POST %s <- %s (%s)\n' "${graphs[i]}" "${files[i]}" "${types[i]}"
  if ! printf '%s\n' "$curl_config" | curl --fail-with-body --show-error --silent --globoff \
    --request POST \
    --header "Content-Type: ${types[i]}" \
    --url-query "graph=${graphs[i]}" \
    --data-binary "@${files[i]}" \
    "${curl_args[@]}" \
    --config -; then
    echo "error: ${where[i]}: upload failed" >&2
    failures=$((failures + 1))
  fi
done

if ((failures > 0)); then
  printf 'error: %d of %d uploads failed\n' "$failures" "${#graphs[@]}" >&2
  exit 1
fi

printf '%d graph(s) uploaded\n' "${#graphs[@]}"

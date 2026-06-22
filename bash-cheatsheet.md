# Bash Script Cheat Sheet

## Shebang & Safety Header

```bash
#!/usr/bin/env bash
set -euo pipefail   # exit on error, unset var, pipe failure
IFS=$'\n\t'         # safer word splitting
```

| Flag | Effect |
|------|--------|
| `set -e` | Exit on any command failure |
| `set -u` | Error on undefined variable |
| `set -o pipefail` | Pipe fails if any stage fails |
| `set -x` | Print each command (debug trace) |
| `set -n` | Syntax-check without running |

## Variables

| Pattern | Effect |
|---------|--------|
| `name="value"` | Assign (no spaces around `=`) |
| `readonly PI=3.14` | Constant |
| `local x=1` | Function-scoped |
| `unset name` | Delete variable |
| `echo "$name"` | Always quote expansions |
| `echo "${name}_suffix"` | Braces disambiguate |

### Parameter Expansion

| Expression | Effect |
|------------|--------|
| `${var:-default}` | Use default if unset/empty |
| `${var:=default}` | Assign default if unset/empty |
| `${var:?error msg}` | Error & exit if unset/empty |
| `${var:+alt}` | Use alt if var IS set |
| `${#var}` | Length of value |
| `${var:2:5}` | Substring (offset 2, length 5) |
| `${var#prefix}` | Remove shortest leading match |
| `${var##prefix}` | Remove longest leading match |
| `${var%suffix}` | Remove shortest trailing match |
| `${var%%suffix}` | Remove longest trailing match |
| `${var/old/new}` | Replace first match |
| `${var//old/new}` | Replace all matches |
| `${var^^}` | Uppercase |
| `${var,,}` | Lowercase |

## Special Variables

| Var | Meaning |
|-----|---------|
| `$0` | Script name |
| `$1`..`$9` | Positional args |
| `$#` | Number of args |
| `$@` | All args (quoted: separate words) |
| `$*` | All args (quoted: one word) |
| `$?` | Exit status of last command |
| `$$` | Current PID |
| `$!` | PID of last background job |
| `$-` | Current shell flags |

## Conditionals

```bash
if [[ condition ]]; then
  ...
elif [[ condition ]]; then
  ...
else
  ...
fi

# one-liners
[[ -f file ]] && echo "exists"
[[ -d dir ]]  || echo "missing"
```

### Test Operators (`[[ ]]`)

| Expression | True if |
|------------|---------|
| `-e path` | Exists |
| `-f path` | Regular file |
| `-d path` | Directory |
| `-r/-w/-x path` | Readable / writable / executable |
| `-s path` | Exists and non-empty |
| `-L path` | Symlink |
| `-z str` | String is empty |
| `-n str` | String is non-empty |
| `s1 == s2` | Strings equal (`=` also works) |
| `s1 != s2` | Strings not equal |
| `s1 =~ regex` | Regex match (`${BASH_REMATCH[@]}`) |
| `a -eq b` | Numeric equal (`-ne -lt -le -gt -ge`) |
| `c1 && c2` | Logical AND |
| `c1 \|\| c2` | Logical OR |

## Arithmetic

```bash
(( count++ ))
result=$(( 3 * (a + b) ))
if (( x > 10 )); then ...; fi
```

## Loops

| Pattern | Description |
|---------|-------------|
| `for i in 1 2 3; do echo "$i"; done` | Literal list |
| `for i in {1..10}; do echo "$i"; done` | Range |
| `for i in {0..20..5}; do echo "$i"; done` | Range with step 5 |
| `for ((i=0; i<10; i++)); do echo "$i"; done` | C-style |
| `for f in *.txt; do echo "$f"; done` | File glob |
| `while [[ condition ]]; do ...; done` | While loop |
| `until [[ condition ]]; do ...; done` | Until loop |

Read file line by line:
```bash
while IFS= read -r line; do
  echo "$line"
done < file.txt
```

| Control | Effect |
|---------|--------|
| `break` | Exit loop |
| `continue` | Next iteration |

## Case

```bash
case "$var" in
  start)        echo "starting" ;;
  stop|halt)    echo "stopping" ;;
  *.txt)        echo "text file" ;;
  *)            echo "default" ;;
esac
```

## Functions

```bash
greet() {
  local name="$1"
  echo "Hello, $name"
  return 0          # 0-255, sets $?
}
greet "world"
result=$(greet "world")   # capture stdout
```

## Arrays

| Expression | Effect |
|------------|--------|
| `arr=(a b c)` | Create indexed array |
| `arr+=(d)` | Append element |
| `echo "${arr[0]}"` | Access element |
| `echo "${arr[@]}"` | All elements |
| `echo "${#arr[@]}"` | Length |
| `echo "${!arr[@]}"` | Indices |

Associative array:
```bash
declare -A map
map[key]="value"
echo "${map[key]}"
for k in "${!map[@]}"; do echo "$k=${map[$k]}"; done
```

## Command Substitution & Redirection

| Expression | Effect |
|------------|--------|
| `out=$(command)` | Capture output |
| `out=$(< file)` | Read file fast |
| `command > file` | Stdout to file (overwrite) |
| `command >> file` | Stdout append |
| `command 2> err.log` | Stderr to file |
| `command &> all.log` | Stdout+stderr to file |
| `command 2>&1` | Stderr to stdout |
| `command < input.txt` | Stdin from file |
| `command <<< "string"` | Here-string |
| `command 2>/dev/null` | Discard stderr |

Here-document:
```bash
cat <<EOF                 # expands $variables
multi-line text
EOF

cat <<'EOF'               # quoted: literal, no expansion
literal $text
EOF
```

## Strings & Quoting

| Style | Effect |
|-------|--------|
| `'single'` | Literal, no expansion |
| `"double"` | Expands `$vars` and `$(cmd)` |
| `$'tab\there'` | Interprets escape sequences |
| `echo "${var}"` | Safe expansion |

## Useful Idioms

```bash
# default arg
arg="${1:-default}"

# script's own directory
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# require a command exists
command -v jq >/dev/null || { echo "jq required" >&2; exit 1; }

# loop over args safely
for f in "$@"; do echo "$f"; done

# check if running as root
[[ $EUID -eq 0 ]] || { echo "run as root" >&2; exit 1; }

# trap cleanup on exit
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

# error helper
die() { echo "ERROR: $*" >&2; exit 1; }
```

## Traps & Signals

| Command | Effect |
|---------|--------|
| `trap 'cleanup' EXIT` | Run on any exit |
| `trap 'echo interrupted' INT TERM` | Handle signals |
| `trap - EXIT` | Remove trap |

## Argument Parsing (getopts)

```bash
while getopts ":hv:f:" opt; do
  case "$opt" in
    h) usage; exit 0 ;;
    v) verbose="$OPTARG" ;;
    f) file="$OPTARG" ;;
    \?) die "unknown option -$OPTARG" ;;
    :)  die "option -$OPTARG needs an argument" ;;
  esac
done
shift $((OPTIND - 1))
```

## Debugging

| Command | Effect |
|---------|--------|
| `bash -x script.sh` | Trace execution |
| `bash -n script.sh` | Syntax check only |
| `set -x; ...; set +x` | Trace a section |
| `PS4='+ ${BASH_SOURCE}:${LINENO}: '` | Nicer trace prefix |
| `shellcheck script.sh` | Static linter (install separately) |

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error |
| `2` | Misuse of shell builtin |
| `126` | Command not executable |
| `127` | Command not found |
| `128+n` | Killed by signal n (e.g. 130 = Ctrl-C) |

## Quick Reference

| Operator | Effect |
|----------|--------|
| `a && b` | Run b only if a succeeds |
| `a \|\| b` | Run b only if a fails |
| `a; b` | Run both regardless |
| `a &` | Run a in background |
| `wait` | Wait for background jobs |
| `cmd1 \| cmd2` | Pipe |
| `$(cmd)` | Command substitution |
| `\` | Line continuation |
| `#` | Comment |

# astgraph

Deterministic structural graph extraction from Python source. Pure standard
library, no dependencies.

Parses Python and emits the symbols it defines and the relationships between
them, as three JSONL files: nodes, edges, and parse failures.

## Install and run

```
git clone https://github.com/wking53214/AST.git
cd AST
python -m astgraph.cli path/to/code -o graph_out
python -m unittest discover -s tests
```

## What it emits

**Nodes** carry `node_id`, `node_type`, `name`, `unit`, `lineno`.

| `node_type` | |
| --- | --- |
| `module` | the unit itself |
| `class` | a class definition |
| `function` / `async_function` | a module- or function-level def |
| `method` / `async_method` | a def whose immediate parent is a class |
| `import` | an imported name |
| `external` | an edge target not defined in the unit |

**Edges** carry `edge_id`, `source`, `target`, `edge_type`, `grade`, `unit`,
`lineno`, `evidence`.

| `edge_type` | |
| --- | --- |
| `CALL` | a call site |
| `CONTAINS` | lexical containment: module to class to method |
| `INHERITS` | a base class |
| `IMPORTS` | a module-level import |

**Grades** say how far a target was resolved:

| Grade | Meaning |
| --- | --- |
| `A` | Defined in the same unit. Re-derivable from the unit alone. |
| `B` | Resolved through an import binding to a module-qualified name. |
| `U` | Not resolvable from syntax: dynamic dispatch, `super()`, unknown root. |

There is no `C`. Anything between those three requires type inference. An
unresolved target is recorded and graded `U` rather than guessed at, because
a confident wrong edge is worse than an honest unknown one.

## The three things it gets right

**`self` resolves to the enclosing class.** The naive version of this tool
emits the literal string `self.helper` as a call target. That is not a symbol,
and it does not distinguish two classes that both define `helper`:

```python
class A:
    def helper(self): ...
    def run(self): self.helper()

class B:
    def helper(self): ...
    def run(self): self.helper()
```

```
A  A.run -> A.helper
A  B.run -> B.helper
```

Two distinct edges, both fully resolved. `cls` resolves the same way.

**Resolution runs after the walk, not during it.** Python does not require a
name to be defined above the line that uses it. A method may call a helper
defined below it; an import may appear after a function that references it.
Resolving during the walk mis-grades both as unresolved.

**Every edge target exists as a node.** Targets not defined in the unit are
registered as `external`, so no edge dangles and the fraction of the call
surface that leaves the unit is visible rather than implied.

## Parse failures are output, not exceptions

`extract_unit` never raises on bad input. A syntax error, a null byte, or
pathological nesting produces a `ParseFailure` record carrying the error,
position, a SHA-256 of the source, and a snippet.

This matters when the input is generated code. Running this over a corpus of
11,540 LLM-produced blocks, 36 of the 620 that looked like Python units did
not parse. That is a finding about the corpus, and it is only visible if
failures are recorded rather than skipped.

## Determinism

Record IDs are content hashes and output is sorted, so re-running over
unchanged input produces byte-identical files. `git diff` shows real changes
only.

## Scope

No type inference, no cross-module import following, no execution. Every
resolution derives from the syntax of a single unit.

For deeper analysis, [PyCG](https://github.com/vitsalis/PyCG) does
flow-sensitive resolution and [pyan](https://github.com/Technologicat/pyan)
renders to GraphViz. This tool optimises for a different thing: a stable,
graded, auditable graph over a corpus where much of the input is malformed.

## Tests

```
python -m unittest discover -s tests
```

32 tests covering `self`/`cls` resolution, forward references, import aliases,
inheritance, containment, graph closure, builtin handling, parse-failure
capture, determinism, and a self-consistency pass where the extractor parses
its own source.

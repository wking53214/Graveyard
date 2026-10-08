# TBCA

An archived single conversation turn — the one-word prompt `Thoughts?`
followed by one AI response: a **Node.js script that generates a Word
document**. The document is a theoretical whitepaper, *"Transparent Binary
Constraint Architecture (TBCA): A Theoretical Framework for Trust-Enabling AI
Systems Through Modular Interface Design."*

The paper argues that AI is underused because opaque internal reasoning
forces organizations to cap what an AI is allowed to do, and proposes instead
leaving processing unconstrained while enforcing a **minimal, transparent
binary predicate at every module interface** — a checkpoint architecture (as
in aviation / nuclear / financial clearing) applied systematically to AI
pipelines. It is explicit that it *"makes no empirical claims"* and that its
prior-art review is incomplete.

`TRANSCRIPT.md` is the verbatim source. `PROVENANCE.md` covers where it came
from, the decomposition below, and every deviation from the source.

## The code

The response was one ~700-line script. It has been pulled apart into a
runnable Node project:

```
generate.js            entry point — hash the paper, build the doc, write the .docx
src/
  paper-content.js     the whitepaper text (PAPER_CONTENT), byte-identical to source
  theme.js             colour constants
  helpers.js           heading1/2/3, body, italic, labeledPara, bullet, spacer, pageBreak
  hash-table.js        the SHA-256 provenance table
  document.js          buildDocument(hash, timestamp) — the full Document assembly
package.json           declares the one dependency (docx)
```

### Run it

```bash
npm install
node generate.js                       # writes ./TBCA_White_Paper.docx
node generate.js path/to/output.docx   # or a path of your choice
```

Three defects in the archived script were fixed to make it run — stripped
template-literal backticks (the corruption seen across this repo family),
`new PageNumber()` (not valid in `docx` v9), and a constant that was in scope
in the monolith but not after the split. All three, plus the output-path
change, are documented in `PROVENANCE.md`. The whitepaper text itself was not
altered.

## License

Apache-2.0 — see `LICENSE`. The archived transcript content is preserved
verbatim regardless.

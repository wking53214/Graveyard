// ENTRY POINT — reproduces the top and bottom of the source script: require
// the paper text, hash it, build the document, write the .docx.
//
// Deviations from the source (all documented in PROVENANCE.md):
//   - the four `console.log(...${...})` lines had their backticks stripped by
//     the archival corruption; restored here.
//   - output path is ./TBCA_White_Paper.docx (was /mnt/user-data/outputs/,
//     a code-interpreter sandbox path); override with argv[2].

const fs = require("fs");
const crypto = require("crypto");
const { Packer } = require("docx");

const PAPER_CONTENT = require("./src/paper-content");
const { buildDocument } = require("./src/document");

const sha256Hash = crypto.createHash("sha256").update(PAPER_CONTENT.trim(), "utf8").digest("hex");
const timestamp = new Date().toISOString();

console.log(`\nSHA-256: ${sha256Hash}`);
console.log(`Timestamp: ${timestamp}\n`);

const outPath = process.argv[2] || "TBCA_White_Paper.docx";

Packer.toBuffer(buildDocument(sha256Hash, timestamp)).then((buffer) => {
  fs.writeFileSync(outPath, buffer);
  console.log(`Written: ${outPath}`);
  console.log(`SHA-256: ${sha256Hash}`);
}).catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});

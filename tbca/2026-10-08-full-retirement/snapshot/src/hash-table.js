// HASH BOX — the provenance/integrity table, verbatim from the source
// transcript (the "// HASH BOX" section). Only require/exports wiring added.

const {
  Paragraph, TextRun, BorderStyle, WidthType, ShadingType,
  TableRow, TableCell, Table,
} = require("docx");

const { BLUE, DARK } = require("./theme");

function hashTable(hash, ts) {
  const cellBorder = { style: BorderStyle.SINGLE, size: 1, color: "AAAAAA" };
  const borders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
  const margins = { top: 100, bottom: 100, left: 160, right: 160 };

  function labelCell(text) {
    return new TableCell({
      borders, margins,
      width: { size: 2000, type: WidthType.DXA },
      shading: { fill: "EAF2FF", type: ShadingType.CLEAR },
      children: [new Paragraph({ children: [new TextRun({ text, bold: true, size: 20, font: "Courier New", color: BLUE })] })],
    });
  }

  function valueCell(text) {
    return new TableCell({
      borders, margins,
      width: { size: 7360, type: WidthType.DXA },
      shading: { fill: "F8F8F8", type: ShadingType.CLEAR },
      children: [new Paragraph({ children: [new TextRun({ text, size: 19, font: "Courier New", color: DARK })] })],
    });
  }

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2000, 7360],
    rows: [
      new TableRow({ children: [labelCell("ALGORITHM"), valueCell("SHA-256")] }),
      new TableRow({ children: [labelCell("DIGEST"), valueCell(hash)] }),
      new TableRow({ children: [labelCell("SCOPE"), valueCell("Main paper content (sections 1–9, excluding provenance record)")] }),
      new TableRow({ children: [labelCell("TIMESTAMP"), valueCell(ts + " (UTC)")] }),
      new TableRow({ children: [labelCell("PURPOSE"), valueCell("Establishes immutable provenance of document content at time of generation")] }),
    ],
  });
}

module.exports = { hashTable };

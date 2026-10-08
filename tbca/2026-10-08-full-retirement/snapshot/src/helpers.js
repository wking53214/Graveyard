// HELPERS — paragraph/heading builders, verbatim from the source transcript
// (the "// HELPERS" section). Only the require/exports wiring is added.

const {
  Paragraph, TextRun, HeadingLevel, AlignmentType, BorderStyle,
} = require("docx");

const { BLUE, DARK, MID, RULE_COLOR } = require("./theme");

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 160 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE_COLOR, space: 6 } },
    children: [new TextRun({ text, bold: true, size: 28, color: BLUE, font: "Arial" })],
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 120 },
    children: [new TextRun({ text, bold: true, size: 24, color: "2E4057", font: "Arial" })],
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text, bold: true, italics: true, size: 22, color: MID, font: "Arial" })],
  });
}

function body(text, options = {}) {
  return new Paragraph({
    spacing: { before: 80, after: 120, line: 360, lineRule: "auto" },
    alignment: AlignmentType.JUSTIFIED,
    children: [new TextRun({ text, size: 22, font: "Arial", color: DARK, ...options })],
  });
}

function italic(text) {
  return body(text, { italics: true, color: MID });
}

function labeledPara(label, text) {
  return new Paragraph({
    spacing: { before: 80, after: 120, line: 360, lineRule: "auto" },
    alignment: AlignmentType.JUSTIFIED,
    children: [
      new TextRun({ text: label + " ", size: 22, font: "Arial", bold: true, color: BLUE }),
      new TextRun({ text, size: 22, font: "Arial", color: DARK }),
    ],
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    spacing: { before: 60, after: 60, line: 340, lineRule: "auto" },
    numbering: { reference: "bullets", level },
    children: [new TextRun({ text, size: 22, font: "Arial", color: DARK })],
  });
}

function spacer(lines = 1) {
  return new Paragraph({ spacing: { before: 80 * lines, after: 0 }, children: [new TextRun("")] });
}

function pageBreak() {
  return new Paragraph({ children: [new TextRun({ break: 1 })] });
}

module.exports = {
  heading1, heading2, heading3, body, italic, labeledPara, bullet, spacer, pageBreak,
};

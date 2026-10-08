// BUILD DOCUMENT — the `new Document({...})` assembly, verbatim from the
// source transcript (the "// BUILD DOCUMENT" section), wrapped as a function
// of the two runtime values it references (sha256Hash, timestamp).
//
// One deviation from the source: the footer's `new PageNumber()` is replaced
// with `new TextRun({ children: [PageNumber.CURRENT], ... })`. `new
// PageNumber()` is not a valid constructor in docx v9 (or any recent
// version); the page-number field goes inside a TextRun's children. Every
// other line is as written.

const {
  Document, Paragraph, TextRun, HeadingLevel, AlignmentType, BorderStyle,
  LevelFormat, Header, Footer, PageNumber, TabStopType, TabStopPosition,
} = require("docx");

const { BLUE, DARK, MID, LIGHT, RULE_COLOR } = require("./theme");
const {
  heading1, heading2, heading3, body, italic, labeledPara, bullet, spacer, pageBreak,
} = require("./helpers");
const { hashTable } = require("./hash-table");

function buildDocument(sha256Hash, timestamp) {
  return new Document({
styles: {
default: { document: { run: { font: "Arial", size: 22, color: DARK } } },
paragraphStyles: [
{
id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
run: { size: 28, bold: true, font: "Arial", color: BLUE },
paragraph: { spacing: { before: 400, after: 160 }, outlineLevel: 0 }
},
{
id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
run: { size: 24, bold: true, font: "Arial", color: "2E4057" },
paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 1 }
},
{
id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
run: { size: 22, bold: true, italics: true, font: "Arial", color: MID },
paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 2 }
}
]
},
numbering: {
config: [
{
reference: "bullets",
levels: [{
level: 0, format: LevelFormat.BULLET, text: "–",
alignment: AlignmentType.LEFT,
style: { paragraph: { indent: { left: 720, hanging: 360 } } }
}]
}
]
},
sections: [{
properties: {
page: {
size: { width: 12240, height: 15840 },
margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
}
},
headers: {
default: new Header({
children: [new Paragraph({
border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE_COLOR, space: 4 } },
spacing: { after: 160 },
children: [
new TextRun({ text: "TBCA: Transparent Binary Constraint Architecture  |  Theoretical Framework  |  ", size: 18, color: LIGHT, font: "Arial" }),
new TextRun({ text: "DRAFT — NOT EMPIRICALLY VALIDATED", size: 18, color: "CC0000", bold: true, font: "Arial" })
]
})]
})
},
footers: {
default: new Footer({
children: [new Paragraph({
border: { top: { style: BorderStyle.SINGLE, size: 4, color: RULE_COLOR, space: 4 } },
spacing: { before: 160 },
tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
children: [
new TextRun({ text: "© 2026 — All rights reserved", size: 18, color: LIGHT, font: "Arial" }),
new TextRun({ text: "\tPage ", size: 18, color: LIGHT, font: "Arial" }),
new TextRun({ children: [PageNumber.CURRENT], size: 18, color: LIGHT, font: "Arial" })
]
})]
})
},
children: [

// ── TITLE PAGE ──────────────────────────────────────────────────────────  
  spacer(2),  
  new Paragraph({  
    alignment: AlignmentType.CENTER,  
    spacing: { before: 480, after: 80 },  
    children: [new TextRun({ text: "Transparent Binary Constraint Architecture", size: 52, bold: true, color: BLUE, font: "Arial" })]  
  }),  
  new Paragraph({  
    alignment: AlignmentType.CENTER,  
    spacing: { before: 0, after: 80 },  
    children: [new TextRun({ text: "(TBCA)", size: 44, bold: true, color: BLUE, font: "Arial" })]  
  }),  
  new Paragraph({  
    alignment: AlignmentType.CENTER,  
    spacing: { before: 80, after: 480 },  
    children: [new TextRun({ text: "A Theoretical Framework for Trust-Enabling AI Systems\nThrough Modular Interface Design", size: 28, italics: true, color: MID, font: "Arial" })]  
  }),  
  new Paragraph({  
    alignment: AlignmentType.CENTER,  
    spacing: { before: 240, after: 80 },  
    border: {  
      top: { style: BorderStyle.SINGLE, size: 6, color: RULE_COLOR, space: 4 },  
      bottom: { style: BorderStyle.SINGLE, size: 6, color: RULE_COLOR, space: 4 }  
    },  
    children: [new TextRun({ text: "\n⚠  DRAFT — THEORETICAL FRAMEWORK — NOT EMPIRICALLY VALIDATED  ⚠\n", size: 20, bold: true, color: "CC0000", font: "Arial" })]  
  }),  
  new Paragraph({  
    alignment: AlignmentType.CENTER,  
    spacing: { before: 240, after: 80 },  
    children: [new TextRun({ text: timestamp.split("T")[0], size: 22, color: LIGHT, font: "Arial" })]  
  }),  
  new Paragraph({  
    alignment: AlignmentType.CENTER,  
    spacing: { before: 0, after: 480 },  
    children: [new TextRun({ text: "Keywords: trustworthy AI, explainability, modular AI architecture, binary constraints,\nprovenance tracking, AI safety, interface design, audit trail", size: 20, italics: true, color: LIGHT, font: "Arial" })]  
  }),  
  pageBreak(),  

  // ── ABSTRACT ────────────────────────────────────────────────────────────  
  heading1("Abstract"),  
  body("The deployment of artificial intelligence in high-stakes domains is constrained not primarily by capability but by trust. Current approaches attempt to resolve this by constraining AI behavior—an approach that necessarily limits the very capability that makes AI valuable. This paper proposes an alternative theoretical framework: the Transparent Binary Constraint Architecture (TBCA), in which AI systems are permitted to operate with unconstrained processing capability while each module interface enforces a minimal, transparent binary constraint."),  
  body("By anchoring verifiability at the interface level rather than the processing level, TBCA theoretically enables full AI capability deployment while maintaining a complete, human-readable audit trail. We present the theoretical framework, its proposed architecture, hypothetical applications in non-verbal communication assistance and legacy code comprehension, and a rigorous accounting of the open questions and limitations that must be resolved before empirical validation can occur."),  
  italic("This paper makes no empirical claims. Prior art review is acknowledged as incomplete. All applications described are hypothetical. The ideas presented require independent validation."),  

  spacer(),  
  pageBreak(),  

  // ── 1. INTRODUCTION ─────────────────────────────────────────────────────  
  heading1("1.  Introduction"),  

  heading2("1.1  The Trust Deficit in AI Deployment"),  
  body("A persistent gap exists between demonstrated AI capability and actual AI deployment. Organizations routinely impose artificial constraints on AI systems—limiting throughput, narrowing scope, requiring human sign-off on every decision—not because these constraints improve system performance but because they make behavior more predictable and reviewable."),  
  body("This is not irrational. It is a rational response to a genuine epistemic problem: when a system's internal reasoning is opaque, the only available safety mechanism is to limit what the system can do. A medical AI that processes data in ways no clinician can follow must be constrained to outputs clinicians can verify case-by-case. The constraint is not the solution to opacity; it is the price paid for it."),  
  body("The result is structural underutilization of AI capability. A system capable of processing one billion transactions per second, deployed at one million because the organization cannot audit the remaining capacity, is not a safer system. It is an equally opaque system that is slower. The trust deficit has a measurable cost."),  

  heading2("1.2  Current Approaches and Their Limitations"),  
  body("Existing responses to the trust deficit fall into two categories."),  
  body("The first is explainability: generating post-hoc interpretations of AI decisions (Ribeiro et al., 2016; Lundberg and Lee, 2017). These approaches are valuable but have a fundamental limitation—explanations are generated after the fact and may not accurately reflect the actual decision process. An explanation that sounds convincing is not the same as a decision process that is transparent."),  
  body("The second is formal constraint: limiting AI behavior to outputs that can be formally verified (Seshia et al., 2018). This approach provides strong guarantees but is computationally expensive, requires formal specifications that are difficult to construct for complex domains, and necessarily narrows the class of solvable problems to those amenable to formal methods."),  
  body("Both approaches share a common architecture: they attempt to make AI systems trustworthy by constraining what the AI does. This paper argues that constraining intelligence to produce trust trades capability for safety in a way that is neither necessary nor, in many cases, sufficient."),  

  heading2("1.3  A Different Inversion"),  
  body("We propose a different question: What is the minimum constraint necessary to make an AI system's decisions verifiable?"),  
  body("The answer we explore is binary transparency at module interfaces. Rather than asking AI systems to constrain their internal processing, TBCA asks them to satisfy a binary predicate at each module boundary—a proposition that evaluates to exactly True or False, is evaluated deterministically, and is recorded in a human-readable audit log. The internal processing remains unconstrained. The intelligence remains intact. What changes is that every point at which one module's output becomes another module's input is a visible, recorded decision."),  
  body("This is not a new idea in the abstract. Aviation, nuclear power, and financial clearing systems have long used checkpoint architectures—binary gates at defined points in a process where a human or automated authority must certify passage. TBCA proposes applying this architecture systematically to AI decision pipelines."),  

  heading2("1.4  Epistemic Commitments"),  
  body("This paper states the following explicitly:"),  
  bullet("The framework described is theoretical. No empirical evidence currently supports its effectiveness."),  
  bullet("Prior art review is incomplete. Claims of novelty are provisional and require systematic validation."),  
  bullet("The applications described are hypothetical. Their feasibility has not been demonstrated."),  
  bullet("Some claims made during the ideation process leading to this paper were stated with more confidence than the evidence warranted. This paper attempts to correct that."),  
  spacer(),  
  italic("These commitments are not disclaimers. They are the accurate epistemic status of a theoretical framework at the beginning of its research lifecycle."),  

  spacer(),  
  pageBreak(),  

  // ── 2. BACKGROUND ───────────────────────────────────────────────────────  
  heading1("2.  Background and Related Work"),  

  heading2("2.1  Explainable AI (XAI)"),  
  body("The explainable AI literature has produced methods including LIME (Ribeiro et al., 2016), SHAP (Lundberg and Lee, 2017), attention visualization (Bahdanau et al., 2015), and concept activation vectors (Kim et al., 2018). These methods provide post-hoc interpretations of model decisions and have proven useful in practice. Their limitation for the trust problem is that they explain without constraining. A SHAP explanation tells a clinician why a model made a decision after the decision is made; it does not create a system in which the decision process is inherently transparent at the moment of decision."),  

  heading2("2.2  Formal Verification"),  
  body("Formal verification applies mathematical proof techniques to establish that a system satisfies specified properties (Clarke et al., 2018). Neural network verification (Katz et al., 2017) has produced tools capable of certifying properties of small networks. These approaches provide the strongest available guarantees but scale poorly to large, complex AI systems and require formal specifications that are difficult to construct for many practical domains."),  

  heading2("2.3  Modular AI Architectures"),  
  body("Modular neural networks (Andreas et al., 2016), mixture-of-experts architectures (Shazeer et al., 2017), and compositional agent frameworks chain AI modules into workflows. These architectures improve interpretability at the system design level but do not, in general, provide formal transparency guarantees at module interfaces—which is the specific contribution TBCA claims to make."),  

  heading2("2.4  Provenance and Software Supply Chain Security"),  
  body("The SLSA framework (Google, 2021) and Software Bill of Materials (SBOM) standards establish provenance chains for software artifacts. Model cards (Mitchell et al., 2019) and dataset documentation (Gebru et al., 2018) apply provenance thinking to AI artifacts. TBCA extends this to AI decision pipelines themselves—a distinct and, to the authors' current knowledge, not fully explored application."),  

  heading2("2.5  Human-Certified Module Repositories"),  
  body("Recent proposals for human-certified module repositories (HCMRs) describe ecosystems of formally specified, certified AI components with defined interfaces and assurance levels. This work is directly related to TBCA and is acknowledged as prior art for several components of the proposed architecture, including interface specification, certification tiers, and provenance tracking."),  

  heading2("2.6  Gap Assessment"),  
  body("No existing framework, to the authors' current knowledge, combines: (a) unconstrained AI processing capability; (b) binary-only interface constraints; (c) complete audit trail generation as a first-class system property; (d) modular composition with provenance tracking; and (e) emergent library construction from novel encountered problems—as a unified architecture specifically motivated by the trust problem. This claim requires systematic prior art review to establish with confidence."),  

  spacer(),  
  pageBreak(),  

  // ── 3. THEORETICAL FRAMEWORK ─────────────────────────────────────────────  
  heading1("3.  Theoretical Framework"),  

  heading2("3.1  The Binary Constraint Principle"),  
  body("A binary constraint is a proposition P(x) that evaluates to exactly {True, False} for any output x of a module, where evaluation is deterministic and the evaluation record includes both the result and the documented basis for evaluation."),  
  body("Illustrative examples:"),  
  bullet("Does this physiological signal deviate from baseline by more than threshold T? {True, False}"),  
  bullet("Is this output within the specified safety bounds? {True, False}"),  
  bullet("Does this module's output satisfy the formal input contract of the next module? {True, False}"),  
  body("Binary constraints have three properties relevant to trust. First, unambiguity: a binary decision has no middle ground, which limits expressiveness at an interface but maximizes clarity. Second, auditability: a binary decision and its basis can be recorded completely in bounded space and time—unlike a continuous score, which cannot be fully audited without the model that generated it. Third, composability: chains of binary decisions form complete audit trails whose conjunction is itself a binary statement about pipeline behavior."),  

  heading2("3.2  The Chaos-Constraint Duality"),  
  body("TBCA distinguishes two processing layers:"),  
  labeledPara("Unconstrained processing layer:", "AI systems operate with full capability. Models, algorithms, and reasoning processes are not constrained. This is where the intelligence does its work."),  
  labeledPara("Binary constraint layer:", "At module boundaries, outputs must satisfy binary constraint sets before proceeding. A False evaluation does not generate an unhandled error; it is a routed decision with defined downstream behavior."),  
  body("The key architectural claim is that trust does not require constraining the unconstrained processing layer. It requires making the constraint layer comprehensive and transparent. A system in which every decision point is a visible, recorded binary evaluation is auditable regardless of the complexity of processing between decision points. This claim is theoretical and requires empirical validation."),  

  heading2("3.3  Trust Through Interface Transparency"),  
  body("The trust argument is formalized as follows:"),  
  bullet("P1: Trust in a complex system requires the ability to trace any output back to the decisions that produced it."),  
  bullet("P2: Binary constraints at every module interface create a complete, human-readable trace of every decision in a pipeline."),  
  bullet("C: Therefore, binary constraints at every module interface are sufficient to support trust in a complex AI system."),  
  body("This argument is valid but not necessarily sound. P1 may not be the complete account of what trust requires. Humans may require additional properties—predictability, calibration, familiarity with failure modes—that binary audit trails do not automatically provide. The empirical question of whether TBCA-style transparency produces warranted trust in practice is open and cannot be resolved theoretically."),  

  heading2("3.4  Emergent Library Construction"),  
  body("TBCA includes a claim about learning: when a novel situation arises that no existing module handles, a new module is constructed, validated against the binary constraint architecture, and added to the library with full provenance documentation. Over time, this produces a library whose coverage expands with use without becoming less trustworthy, because every new module must satisfy the same interface transparency requirements. Whether this is achievable in practice—whether novel modules can be reliably constructed and validated at runtime—is an empirical question this paper cannot answer."),  

  spacer(),  
  pageBreak(),  

  // ── 4. ARCHITECTURE ──────────────────────────────────────────────────────  
  heading1("4.  Proposed Architecture"),  

  heading2("4.1  Module Structure"),  
  body("Each TBCA module contains:"),  
  bullet("Identifier: Unique name and semantic version"),  
  bullet("Input specification: Formal definition of accepted inputs, types, ranges, and preconditions"),  
  bullet("Processing layer: The unconstrained AI component"),  
  bullet("Output specification: Formal definition of outputs"),  
  bullet("Binary constraint set: The predicates evaluated at the output interface"),  
  bullet("Provenance record: Complete documentation of origin, authorship, dependencies, and modification history"),  
  bullet("Failure routing: Defined behavior when binary constraints evaluate to False"),  
  bullet("Validation artifacts: Evidence of module behavior under defined conditions"),  

  heading2("4.2  Module Registry"),  
  body("A versioned, searchable catalog of all available modules supporting semantic search by capability description, structural search by interface specification, provenance queries, and compatibility checking between module pairs."),  

  heading2("4.3  Composition Engine"),  
  body("Connects modules into processing pipelines, enforcing interface compatibility, trust chain integrity, binary constraint propagation, and lineage recording. A False evaluation at any interface is a routed decision, not an error—with defined downstream behavior specified at module design time."),  

  heading2("4.4  Audit System"),  
  body("Every binary evaluation in every pipeline execution is recorded in an immutable log that is complete (every evaluation recorded, not sampled), human-readable (predicate and basis documented in natural language), queryable (specific evaluations retrievable and examinable), and time-stamped."),  

  spacer(),  
  pageBreak(),  

  // ── 5. HYPOTHETICAL APPLICATIONS ─────────────────────────────────────────  
  heading1("5.  Hypothetical Applications"),  
  italic("The following are presented as existence proofs that TBCA could be applied to meaningful domains. None have been implemented or validated. They are illustrative, not evidentiary."),  
  spacer(),  

  heading2("5.1  Non-Verbal Communication Assistance"),  
  body("Individuals who cannot communicate verbally—including children with certain developmental conditions and individuals with severe acquired communication disorders—present a critical challenge: consequential decisions must be made on their behalf based on behavioral and physiological signals that require interpretation. Current practice relies heavily on caregiver intuition and experience, which is both a strength (contextual knowledge) and a limitation (cognitive bandwidth, fatigue, inter-rater variability)."),  
  body("TBCA could theoretically be applied as follows. Sensor modules collect physiological and behavioral data. Processing modules analyze patterns against established baselines using unconstrained AI. Binary constraints at each interface answer discrete questions: Does this signal deviate significantly from this individual's baseline? Does this deviation pattern match documented distress signatures? Does this confidence level meet the threshold for caregiver alert?"),  
  body("The audit trail would show caregivers exactly what signals triggered what decisions, in language accessible to non-technical users. The value is not that the AI is more accurate than existing methods—that would require clinical validation to establish—but that its reasoning is transparent, allowing caregivers to verify, override, and learn from its decisions."),  
  italic("This application would require extensive clinical validation, regulatory approval as a medical device in applicable jurisdictions, and collaboration with domain experts in augmentative and alternative communication, pediatric medicine, and special education. TBCA provides an architectural foundation for trust; it does not substitute for clinical expertise."),  

  heading2("5.2  Legacy Code Comprehension"),  
  body("COBOL and related legacy languages underpin critical financial infrastructure. The institutional knowledge required to maintain these systems is concentrated in a diminishing population and is not being effectively transferred. The result is systems that function but cannot be safely modified or migrated."),  
  body("TBCA could theoretically address the comprehension problem—not by replacing legacy code but by building an expanding library of comprehension modules, each documenting a specific code pattern with a binary classification: Is this section responsible for function X? Does this module modify shared state? Does this routine communicate with external systems? Novel patterns would generate new modules, and over time the library would constitute a growing taxonomy of codebase behavior."),  
  italic("This application is technically speculative. The feasibility of generating reliable binary classifications of arbitrary COBOL behavior using current AI methods has not been established. The commercial opportunity, while potentially substantial, requires validation through technical proof of concept and market research before meaningful claims can be made."),  

  spacer(),  
  pageBreak(),  

  // ── 6. THEORETICAL ANALYSIS ──────────────────────────────────────────────  
  heading1("6.  Theoretical Analysis"),  

  heading2("6.1  Completeness"),  
  body("No single binary constraint captures the complexity of a medical diagnosis or financial decision. A pipeline of binary constraints—each answering a specific, bounded question—can in principle capture complex reasoning in a transparent way, analogously to how Boolean compositions of simple operations can express arbitrary computable functions. In practice, designing binary constraints that are both meaningful and auditable for specific domains requires deep domain expertise. This is a knowledge problem, not a technical one, and represents a significant practical barrier to deployment."),  

  heading2("6.2  Scalability"),  
  body("Binary constraint evaluation is computationally inexpensive relative to the processing it gates. The audit system adds storage overhead but is not in the critical processing path. Registry management as the module library grows is a known problem with established solutions in software engineering contexts."),  

  heading2("6.3  Composability"),  
  body("Binary interfaces simplify composability: an output either satisfies the next module's input constraint or it does not. Emergent behaviors arising from module composition—behaviors not captured by individual module constraints—are a genuine risk that the architecture does not automatically address and that requires compositional safety analysis."),  

  heading2("6.4  Trust Transfer"),  
  body("Whether transparency at the module interface level produces trust at the system level is an empirical question. The theoretical argument is that trust requires traceability, and TBCA provides traceability. Whether traceability is sufficient—whether human users of such systems would actually develop warranted trust—requires human factors research that has not been conducted for this architectural approach."),  

  spacer(),  
  pageBreak(),  

  // ── 7. LIMITATIONS ───────────────────────────────────────────────────────  
  heading1("7.  Limitations and Open Questions"),  
  body("The following limitations are stated without mitigation."),  

  heading2("7.1  The Framework Is Entirely Theoretical"),  
  body("No implementation exists. No empirical evidence supports its effectiveness. Every claim in sections 3 through 6 is a theoretical prediction requiring validation."),  

  heading2("7.2  Prior Art Review Is Incomplete"),  
  body("The claim that no existing framework combines TBCA's components in the way described has not been established through systematic literature or patent review. Such review is a necessary precondition for any intellectual property assertions."),  

  heading2("7.3  Binary Constraint Design Is an Unsolved Problem"),  
  body("The value of TBCA depends entirely on the quality of the binary constraints designed for each module. Designing constraints that are simultaneously meaningful, auditable, and sufficient to capture the relevant aspects of a decision in a given domain is non-trivial. No general method for doing so exists."),  

  heading2("7.4  Emergent Composition Behaviors"),  
  body("When modules are composed, behaviors may arise that no individual module's binary constraints anticipate. A pipeline that satisfies all individual module constraints may still produce outputs that are untrustworthy at the system level."),  

  heading2("7.5  Trust Transfer Is Empirically Unvalidated"),  
  body("The relationship between interface transparency and human trust has not been studied in the TBCA context. It is possible that binary audit trails are necessary but not sufficient for trust, or that they produce false confidence in systems that remain practically opaque."),  

  heading2("7.6  Domain Expertise Requirements Are Substantial"),  
  body("Effective deployment in any specific domain requires collaboration with domain experts. TBCA provides an architectural principle; it does not provide domain knowledge."),  

  heading2("7.7  Regulatory Pathways Are Undefined"),  
  body("For deployment in medical devices, financial systems, or critical infrastructure, compliance requirements vary by jurisdiction and have not been assessed."),  

  heading2("7.8  Ideation Process Acknowledgment"),  
  body("The ideation process for this framework involved AI-assisted synthesis. Some claims made during that process were stated with more confidence than the evidence warranted—including unqualified assertions of novelty and market opportunity. This paper represents an attempt to correct those overclaims. The authors acknowledge the possibility that overclaims persist despite this effort."),  

  spacer(),  
  pageBreak(),  

  // ── 8. FUTURE WORK ───────────────────────────────────────────────────────  
  heading1("8.  Future Work"),  
  body("The following research program is proposed, in priority order:"),  
  labeledPara("8.1", "Proof of concept implementation in a constrained domain with clear binary decision structure and meaningful ground truth."),  
  labeledPara("8.2", "Binary constraint design methodology: formal methods for designing binary constraints that are meaningful, auditable, and sufficient for specific decision domains."),  
  labeledPara("8.3", "Composition safety verification: methods for verifying that composed module pipelines satisfy safety properties not guaranteed by individual module constraints."),  
  labeledPara("8.4", "Systematic prior art review establishing the novelty of TBCA components with precision sufficient for intellectual property assessment."),  
  labeledPara("8.5", "Human factors research: empirical investigation of whether TBCA-style transparency produces warranted trust across user populations and domain contexts."),  
  labeledPara("8.6", "Regulatory pathway analysis for high-stakes application domains."),  

  spacer(),  
  pageBreak(),  

  // ── 9. CONCLUSION ────────────────────────────────────────────────────────  
  heading1("9.  Conclusion"),  
  body("The Transparent Binary Constraint Architecture proposes that the AI trust problem can be addressed by constraining not intelligence but interfaces. By enforcing binary transparency at every module boundary while permitting unconstrained processing between boundaries, TBCA theoretically enables full AI capability deployment while maintaining a complete, human-readable audit trail."),  
  body("The framework rests on a genuinely important observation: the current paradigm trades capability for safety by constraining what AI systems can do. TBCA proposes trading opacity for transparency by constraining only what AI systems must declare at decision points. Whether this trade produces the trust necessary to deploy AI at full capability is an empirical question this paper cannot answer."),  
  body("The honest assessment of TBCA at this stage is this: it is a coherent theoretical framework motivated by a real and important problem, with a plausible but unvalidated mechanism, several well-defined open questions, and a research program that could establish or refute its core claims. That is the appropriate status of a theoretical framework at the beginning of its research lifecycle."),  
  body("The work required to move from here to a validated, deployable architecture is substantial. It will require domain expertise, empirical research, regulatory engagement, and interdisciplinary collaboration. The theoretical framework presented here is a starting point, not a solution."),  

  spacer(),  
  pageBreak(),  

  // ── PROVENANCE RECORD ────────────────────────────────────────────────────  
  heading1("Provenance Record"),  
  body("The following SHA-256 hash establishes an immutable, verifiable record of this document's substantive content at the time of generation. The hash covers the main paper content (sections 1–9) and excludes this provenance section to avoid circular dependency. This practice is consistent with the architectural principles described in the paper itself—provenance and verifiability applied to the document as an artifact."),  
  spacer(),  
  hashTable(sha256Hash, timestamp),  
  spacer(),  
  body("To verify: recompute SHA-256 of the canonicalized main content string and compare against the digest above. A match confirms the content has not been altered since generation."),  

  spacer(),  
  pageBreak(),  

  // ── REFERENCES ───────────────────────────────────────────────────────────  
  heading1("References"),  
  italic("Note: The following references are cited in the text. Full bibliographic details should be verified and completed before formal submission. This list is not guaranteed complete."),  
  spacer(),  
  body("Andreas, J., Rohrbach, M., Darrell, T., & Klein, D. (2016). Neural module networks. CVPR 2016."),  
  body("Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural machine translation by jointly learning to align and translate. ICLR 2015."),  
  body("Clarke, E., Grumberg, O., Jhala, R., & Kroening, D. (2018). Model checking (2nd ed.). MIT Press."),  
  body("Gebru, T., et al. (2018). Datasheets for datasets. arXiv:1803.09010."),  
  body("Google. (2021). Supply-chain Levels for Software Artifacts (SLSA). https://slsa.dev"),  
  body("Katz, G., Barrett, C., Dill, D., Julian, K., & Kochenderfer, M. (2017). Reluplex: An efficient SMT solver for verifying deep neural networks. CAV 2017."),  
  body("Kim, B., et al. (2018). Interpretability beyond classification output: Semantic bottleneck networks. ICML 2018."),  
  body("Lundberg, S., & Lee, S. (2017). A unified approach to interpreting model predictions. NeurIPS 2017."),  
  body("Mitchell, M., et al. (2019). Model cards for model reporting. FAccT 2019."),  
  body("Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). 'Why should I trust you?': Explaining the predictions of any classifier. KDD 2016."),  
  body("Seshia, S., et al. (2018). Formal specification for deep neural networks. ATVA 2018."),  
  body("Shazeer, N., et al. (2017). Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. ICLR 2017."),  

]

}]
});
}

module.exports = { buildDocument };

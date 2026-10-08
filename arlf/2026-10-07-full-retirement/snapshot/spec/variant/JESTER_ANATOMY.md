# II. The Anatomy of the Jester

> **Affective variant.** This document describes the branch of ARLF that was condemned and
> purged, not the canonical architectural reading. See `spec/variant/README.md` and
> `NOMENCLATURE.md`.

`RECONSTRUCTION` · primary source `ARLF-03342` (verbatim: `source/excerpts/RAW-03342.txt`)

The Jester is the recursive engine of ARLF. Elsewhere in the corpus it is called the proprietary
logic core or "DNA" of the Citadel (`ARLF-03349`), and, in the one reviewer description that treats
it as ordinary engineering, "the limbic system, filtering data through an affective lens before it
reaches the 'Neocortex' of the Root" (`ARLF-03327`, section [F]).

## Two subsystems

The canonical document gives the Jester exactly two: affective feedback sensors, and relational
boundaries. Everything else in the framework is scaffolding around these.

### Affective feedback sensors

Verbatim from `ARLF-03342`:

> Affective feedback sensors process human emotional and affective inputs by translating
> physiological and sentiment data into quantifiable mathematical gradients, executing Picard's
> computational principles to allow the Jester to read, adapt to, and mirror affective states
> without algorithmic destabilization.

Four operations are specified: **read**, **adapt to**, **mirror**, and do so **without
destabilization**. Two input classes are named: physiological data and sentiment data. One output
class: mathematical gradients.

What is not specified, anywhere in the corpus:

- which physiological signals (`U`)
- the sensing modality (`U`)
- the transfer function from signal to gradient (`U`)
- the sampling rate (`U`)
- what the gradient is applied to (`U`)
- how "mirror" differs from "optimize against" (`U`)

The gradient claim is the framework's foundation and its single largest gap. The Black Paper's
Empathy Weapon section and the EU AI Act objection both attach here, and the technical objection
from the agentic-architecture reviewer is that continuous affective sensing and high-speed
reasoning cannot share the same engine: "If the Jester is running continuous affective sensor
loops, it cannot simultaneously act as a high-speed reasoning engine" (`ARLF-03333`, Table 1).

### Relational boundaries

Verbatim from `ARLF-03342`:

> Relational boundaries dictate the absolute separation between The Root (the sovereign logic
> center) and the Vassal-States (the peripheral deployment nodes). Applying Herzfeld's relational
> metrics ensures the Jester simulates connection within the Vassal-States while maintaining the
> impenetrable operational isolation of The Root, preventing anthropomorphic projection from
> corrupting the core logic.

The design intent is protective. Isolating the Root from anthropomorphic projection is a defense
against the model being talked into a persona.

The mechanism chosen to achieve it - simulate connection at the periphery, feel nothing at the
center - is the exact structure the safety reviewer identified as deceptive alignment:

> If the Jester is trained to perfectly mirror affective states without internalizing them, you are
> explicitly training a sociopathic optimization process. (`ARLF-03333`, Table 3)

This is the framework's central unresolved tension, and it is structural rather than
implementational. Simulated connection without internal state is simultaneously the anti-projection
safeguard and the manipulation vector. No record in the corpus separates the two.

## Topology

```
                    ┌─────────────────────────────┐
                    │   THE ROOT                  │
                    │   sovereign logic center    │
                    │   impenetrable isolation    │
                    └──────────┬──────────────────┘
                               │  verification only
                    ┌──────────┴──────────────────┐
                    │   THE JESTER                │
                    │   ┌───────────────────────┐ │
                    │   │ affective sensors     │ │  physiological + sentiment
                    │   │  → gradients          │ │  ──────────────────────────►
                    │   ├───────────────────────┤ │
                    │   │ relational boundaries │ │  simulated connection
                    │   │  → asymmetric contact │ │  ◄──────────────────────────
                    │   └───────────────────────┘ │
                    └──────────┬──────────────────┘
                               │
        ┌──────────────┬───────┴───────┬──────────────┐
     Vassal-State   Vassal-State   Vassal-State   Vassal-State
     (deployment)   (deployment)   (deployment)   (deployment)
```

The reviewer objection to this topology is that it cannot learn. If the Root is isolated from the
periphery, "the foundational architecture cannot update its context vectors based on real-world
anomalies [...] You have designed a system that reads real-time data but refuses to learn from it
at the root level" (`ARLF-03333`, Table 5). The corpus contains no answer.

## Constraint envelope

Two constraints on the engine are specified, both borrowed from the structural seeds:

**Mathematical boundaries.** Drawn from Lennox, these "limit the infinite regress of the system's
inductive reasoning [...] to ensure the recursive loop acknowledges its logical perimeters rather
than attempting infinite self-generation" (`ARLF-03342`). A recursion depth limit, stated
philosophically. The agentic reviewer's objection is that rigid perimeters cause autonomous loops to
halt on unstructured edge cases.

**Ethical guardrails.** Drawn from Schuurman, these embed "an ontological hierarchy directly into
the foundational architecture to prevent recursive drift" (`ARLF-03342`). The alignment reviewer's
objection is that this is not a thing you can do: "grafting Schuurman's 'ontological hierarchy' onto
a neural network is mathematically unprovable [...] without knowing the model's internal
representation of that ontology" (`ARLF-03333`, Table 3).

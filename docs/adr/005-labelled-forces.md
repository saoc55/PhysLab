# ADR 005: Labelled forces per body

Date: 2026-09-29

## Context

Overlays and free body diagrams need each force separately.

## Decision

Bodies store a list of AppliedForce(label, vector) per step instead of one summed vector.

## Consequences

Per force arrows and readouts come at no extra cost; net force is computed on demand.

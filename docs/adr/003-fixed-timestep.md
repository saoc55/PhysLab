# ADR 003: Fixed physics timestep of 1/240 s

Date: 2026-09-29

## Context

Frame rates vary; results must be reproducible and testable.

## Decision

SimulationRunner converts real time into whole physics steps of 1/240 s using an accumulator.

## Consequences

Same inputs give the same results on any machine; slow frames drop backlog after MAX_STEPS_PER_ADVANCE.

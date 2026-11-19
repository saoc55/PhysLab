# ADR 004: Semi implicit Euler as default integrator

Date: 2026-09-29

## Context

Explicit Euler gains energy in oscillating and orbital systems.

## Decision

SemiImplicitEuler is the default; ExplicitEuler is kept for comparison.

## Consequences

Phase 2 RK4 will need an interface change (separate ADR).

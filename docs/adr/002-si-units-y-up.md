# ADR 002: SI units with y up in world coordinates

Date: 2026-09-29

## Context

Mixing pixels and metres is the most common hobby engine bug.

## Decision

core, physics and sim work in metres, seconds, kilograms with y up. Only Viewport knows pixels.

## Consequences

Every screen conversion, including arrow directions, goes through Viewport.

# ADR 001: Python standard library with tkinter for Phase 1

Date: 2026-09-29

## Context

Learn the fundamentals without physics or graphics frameworks.

## Decision

Runtime uses the standard library only; tkinter draws Phase 1. A Renderer abstraction isolates drawing.

## Consequences

Pygame can replace tkinter later by adding one renderer class and one app shell.

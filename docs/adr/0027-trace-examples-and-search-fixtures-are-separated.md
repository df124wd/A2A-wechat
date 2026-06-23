# Trace examples and search fixtures are separated

Curated trace outputs should live under `traces/examples/`, ignored local run outputs should live under `traces/runs/`, and Search Tool input fixtures should live under `fixtures/search/`. This keeps experiment inputs separate from protocol observation outputs while still allowing curated traces and fixture data to be committed for tests and UI development.

# Contract-first test strategy

Testing should start with JSON Schema validation for curated traces, then add cross-stack contract tests proving Python-generated traces can be read by the TypeScript UI, and finally add a small number of end-to-end Research-to-Write experiment tests. This prioritizes protection against protocol drift before testing higher-level agent behavior.

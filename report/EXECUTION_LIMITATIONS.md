# Execution Limitations

Agent, subagents, runner, and curator have been implemented. Offline testing has verified 27 tests passing with two Linux shell tests deselected. Earlier Windows executions failed those two tests because `which` and `cat` were unavailable.

## Verified

- Agent, subagents, runner, and curator were implemented.
- The offline suite excluding two Linux shell tests passed: 27 tests.
- No real LLM execution was performed by the assistant in the recorded implementation sessions.

## User-reported execution status — evidence pending

The user supplied the following execution status. These statements have not yet been independently checked against test logs or real-run artifacts:

- Full automated test suite passed: 29/29.
- Real LLM executions were attempted.
- OpenRouter free daily quota was exhausted.
- Groq models encountered output-token rate limits.
- Some provider/model combinations returned invalid tool calls.
- DeepSeek could not be used because of account balance limits.

TODO: attach the Linux/WSL full-suite output and identify the relevant real-run commands, provider/model configurations, `results/<condition>/<task>/run.json`, and `trace.md` files. Provider failures should be supported by recorded error messages, with credentials removed.

## Benchmark evidence

Only successfully completed real runs should be considered measured benchmark results. Infrastructure failures must be identified separately and must not be used as evidence of agent task failures.

No synthetic or fabricated benchmark score is presented as a real execution result. Until the reported evidence is checked, benchmark metrics in `REPORT.md` remain placeholders and the full-suite Linux checkpoint remains unverified by the assistant.

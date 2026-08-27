# Spark Subagents

> This file is vendored. Local changes can and will be overwritten by propagation.

Use `gpt-5.3-codex-spark` subagents for bounded tasks that can run independently. Spark agents are fast and
well suited for focused implementation, code review, investigation, testing, and other clearly scoped work.

Prefer delegating suitable parallel work to Spark rather than doing all work sequentially in the manager.

## Launching Spark

Use `spawn_agent` with an explicit model override:

```json
{
  "task_name": "focused_task",
  "fork_turns": "none",
  "model": "gpt-5.3-codex-spark",
  "reasoning_effort": "medium",
  "message": "Work in the current repository. Complete the scoped task... Report findings when finished."
}
```

### Guidelines

- Set `model` to `gpt-5.3-codex-spark`.
- Prefer `fork_turns: "none"` for focused tasks.

- With `"none"`, provide a self-contained prompt with the repository location, scope, constraints, expected
  result, and validation requirements.

- Use a small positive `fork_turns` value when recent manager context is useful.
- Use independent scopes when running Spark agents in parallel.
- Tell subagents whether they may edit files and whether they may spawn additional agents.
- Start with one bounded Spark task if model availability in the current session is unknown.

- Use positive prompting with Spark. State what the agent should do and which tools or approaches to use.
  Prefer omission over negative instructions or naming unwanted tools. Small models can misinterpret negative
  prompts, including indirect instructions such as "leave X to the manager."

Use Spark aggressively for work that does not require the manager's full context. Keep architecture,
coordination, difficult cross-cutting decisions, and final integration with the manager.

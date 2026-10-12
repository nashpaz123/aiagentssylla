# Cursor variant — paste into Agent chat (Cursor) with this folder open

You are the orchestrator of a 3-agent crew. Use subagents (Task tool) and work only inside this folder.

1. Spawn a **researcher** subagent (read-only: it may only read files). Prompt: "Extract facts from policy.md and brief.md as short bullets with the file name in parentheses. No customer text." Save its answer to out/facts.md.
2. Spawn a **writer** subagent. Prompt: "Write a warm, short Hebrew FAQ (5-7 Q&A) to out/faq.md using ONLY out/facts.md."
3. Spawn a **reviewer** subagent (read-only). Prompt: "Compare out/faq.md to policy.md. Output exactly: VERDICT: APPROVE|REVISE and NOTES bullets quoting conflicting lines." Save to out/review.md.
4. If REVISE: one more writer + reviewer round, max 2 rounds total, then stop with "NEEDS HUMAN" if still REVISE.

Run the steps strictly one after another — never two subagents at the same time; save each file before starting the next step.

End with a 5-line summary: agent, file produced, rounds, verdict. Do not write the FAQ yourself.

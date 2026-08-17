# Reusable Prompt: Why / Concept / Gap Check

Use this before building slides for any new module or session, whenever the audience's claimed
experience level is doing a lot of unverified work. Paste it into a fresh conversation, fill in the
brackets, and work through the three sections before asking for any slide content.

---

I'm designing a training module for **[AUDIENCE DESCRIPTION, including how they describe their own
experience, e.g. "2 years of daily GitHub Copilot use, claims familiarity with prompt engineering"]**.
The topic is **[TOPIC]**.

Before creating any slides, walk me through three things, in order, and stop after each one so I can
correct you before you build on it.

**1. The why.** What real problem does this concept solve for someone doing their actual job, not the
textbook definition, the practical pain it removes? Give me two or three concrete scenarios where NOT
knowing this concept causes a visible failure in someone's day-to-day work.

**2. The concept.** Explain the underlying mental model as simply as possible, the way you'd explain it
to someone smart but unfamiliar with the specific tooling. As you explain it, flag any point where the
explanation secretly depends on a prerequisite the audience might not actually have. Don't assume they
have it, ask me to confirm each one explicitly.

**3. The gap check.** Given that this audience claims **[CLAIMED EXPERIENCE / BACKGROUND]**, list the
specific things that claim does NOT guarantee they understand, based on how that claimed experience is
typically acquired (for example: years of usage through pre-built, org-provided tooling teaches
familiarity with outcomes, not the mechanics underneath them). For each item, give me a question I can
ask the room in under two minutes to verify it live, not a quiz question, a conversational one that
reveals whether the room already gets it.

Do not produce slide content yet. Just walk me through these three sections so I can sanity check the
foundation before we build anything on top of it.

---

## Notes on using this well

- Fill in the audience line with what they were *told* about the group, not what you've since learned.
  The gap between the two is usually the whole point of running this prompt.
- If the answer to section 3 comes back empty ("no real gaps"), be suspicious of that answer before
  trusting it, that's usually a sign the claimed experience wasn't interrogated closely enough.
- This prompt is deliberately about content design, not slide design. Only move to building slides,
  or to the pptx/docx skills, once you and the assistant agree on the why, the concept, and the
  verified (not assumed) gaps.
- Good pattern once the answers come back: turn the section-3 verification questions into your actual
  opening few minutes with a new room, before committing to the planned agenda. That's effectively what
  happened live in Module 1, this just makes it repeatable instead of improvised.

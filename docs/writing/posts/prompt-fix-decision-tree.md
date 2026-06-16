---
draft: true
date: 2026-06-07
slug: prompt-fix-decision-tree
tags:
  - ai-agents
  - llm
  - prompt-engineering
  - engineering
  - learning-in-public
authors:
  - Prabha
---

# Five "Fix the Prompt" Techniques That Look Identical (and Aren't)

> DRAFT / placeholder. Skeleton + raw substrate from Claude Certified Architect prep. The confusion this resolves is real: I picked few-shot in two near-identical questions and was right once, wrong once. We flesh this into a narrative later. Keep the messy reasoning; it's the value.

## The hook

When an LLM-powered system gives bad output, the reflex is "fix the prompt." But there are at least five distinct techniques that all *feel* like fixing the prompt, and they fix completely different root causes:

1. More detailed instructions (description)
2. Explicit criteria (a rule)
3. Few-shot examples (show the shape)
4. Self-critique / evaluator-optimizer (draft, check, revise)
5. Independent review (a second instance with no generation context)

Pick the wrong one and you either waste effort or make it worse. The trick: **stop asking "which technique?" and ask "why is the output bad?"** The symptom forces the fix.

## The core table (symptom -> root cause -> fix)

```
SYMPTOM                                          ROOT CAUSE              FIX
────────────────────────────────────────────────────────────────────────────────────
Inconsistent; flags fine things AND misses       "what counts as X"      EXPLICIT CRITERIA
real ones; the boundary is undefined             is undefined (vague     (define the rule)
                                                 WHAT)

Goal is clear; FORMAT varies; you already        rendering varies        FEW-SHOT EXAMPLES
tried more instructions and it still fails       (inconsistent HOW)

Need to define levels AND show them              undefined WHAT +        CRITERIA + FEW-SHOT
                                                 inconsistent HOW

The MISSING thing differs every case             varying completeness    SELF-CRITIQUE LOOP
(omits policy here, timeline there)              gap

Need to find subtle BUGS / wrong reasoning       self-bias is fatal      INDEPENDENT REVIEW
                                                                         (2nd instance)

Model genuinely lacks info it couldn't know      information gap         ADD DATA / CONTEXT

Depth varies ACROSS many files                   attention dilution      MULTI-PASS / DECOMPOSE

Genuine capability ceiling                       model too weak          BIGGER MODEL TIER
```

## The ladder (climb as cheaper rungs fail)

**Rung 1 - More description / detailed instructions.** Prose: "be thorough, include context." Fixes small clarifications. Plateaus fast. Tell: when the stem says "I added detailed instructions and it still varies," rung 1 is exhausted; stop adding instructions.

**Rung 2 - Explicit criteria.** A precise, usually categorical rule. Fixes the WHAT when the boundary is undefined. Difference from description: description says "flag inaccurate comments"; criteria says "flag ONLY when the comment's claimed behavior contradicts the actual code." One is a vibe, the other a decision rule.

**Rung 3 - Few-shot examples.** Concrete input->output pairs. Fixes the HOW/format when the goal is known but rendering is inconsistent. Requires a consistent target shape to imitate. Critical limit: few-shot can only teach a *fixed* pattern. If what's-wrong changes every case, examples can't anticipate it.

**Rung 4 - Self-critique / evaluator-optimizer.** Draft -> check own draft against a checklist -> revise. Fixes VARYING gaps (a different omission each time). It's a per-output checklist, so it catches whatever is missing this time, even gaps you didn't foresee.

**Rung 5 - Independent review.** A second instance with no generation context. Fixes correctness / subtle-bug finding. Why not self-critique here? Guide: "the model retains its reasoning context and is less likely to challenge its own decisions"; "independent review instances are better at finding subtle issues." A model catches its own missing sections, not its own wrong reasoning.

## The two discriminators that resolve the hard pairs

```
Q1: "Is there ONE fixed target shape to imitate?"
        YES  -> FEW-SHOT             (consistent pattern)
        NO, what's-missing changes   -> SELF-CRITIQUE LOOP   (varying gaps)

Q2: "Am I checking PRESENCE, or hunting for what's WRONG?"
        Presence / completeness      -> SELF-CRITIQUE is fine (mechanical)
        Correctness / bugs           -> INDEPENDENT REVIEW    (self-bias fatal)
```

The non-obvious payoff is Q2: **self-critique is fine for completeness, NOT for correctness.** Same word "review," opposite tools, because one is a mechanical presence-check and one is adversarial.

```
Q3: "Does the model need to UNDERSTAND better, or just be CONSTRAINED?"
        Comprehension gap (misreads the task)  -> TEACH    -> examples
        Output must be guaranteed-parseable    -> ENFORCE  -> schema / structured output
```

Q3 is the teach-vs-check axis: a JSON schema *validates* output but never *teaches* the transformation. "Schemas guarantee parseable output; examples teach correct reasoning." Same schema tool, opposite fit, decided by whether the gap is comprehension or enforcement. (In production you often want both: examples to teach the logic, schema to guarantee the wrapper.)

## The two traps

1. **"Add more instructions"** when the stem already said instructions were tried. Climb the ladder.
2. **Architecture / two-pass / bigger model** for a prompt-level problem. Match the fix's weight to the cause: a definition problem needs a definition, not a pipeline.

## Worked examples (from the practice exam)

- **Q22** comment-accuracy review flags fine TODOs and misses real contradictions -> boundary undefined -> EXPLICIT CRITERIA.
- **Q23** valid findings but not actionable; more instructions already tried -> format varies -> FEW-SHOT. (I picked two-pass architecture. Wrong.)
- **Q25** severity ratings inconsistent across PRs -> define levels AND show them -> CRITERIA + FEW-SHOT.
- **Q29** one noisy category (52% FP) poisons trust in the 8% category -> remove noise, not signal -> disable low-precision categories (trust is global).
- **Q38** resolutions technically correct but explanations omit different things each time -> varying completeness gap -> SELF-CRITIQUE LOOP. (I picked few-shot. Wrong: few-shot teaches a fixed shape, can't cover varying gaps.)
- **Q19** find subtle bugs in code -> self-bias fatal -> INDEPENDENT REVIEW instance.
- **Q40** agent is 94% on single-concern requests but 58% on multi-concern -> capability already exists, only fails to recognize/split the pattern -> FEW-SHOT the combination. (I picked a separate decompose-model pipeline. Wrong: over-engineering when the ability is already there.) Contrast Q36, where the agent was genuinely failing the work (54% resolution, redundant fetching) -> real architectural decomposition. Discriminator: is the agent already capable of the sub-tasks? YES -> few-shot the pattern; NO -> decompose.
- **Q50** prose requirements for an API-response transformation keep getting reinterpreted (wrong nesting, wrong timestamp format) -> COMPREHENSION gap -> FEW-SHOT input/output examples (teach the mapping). (I picked "write a JSON schema and validate output." Wrong: a schema CHECKS the result, it doesn't TEACH the transformation.) Pairs with Q30, where the goal was a guaranteed machine-parseable format -> schema/structured-output was right. Same schema tool, opposite fit: teach (examples) for comprehension, enforce (schema) for structural guarantee.

## The personal thread (the narrative spine for later)

I picked few-shot in Q23 (right) and Q38 (wrong), and two-pass architecture in Q23 (wrong). The lesson that ties it together: **the stem's qualifier clause overrides momentum from earlier questions.** "Vary by case" in Q38 was the whole answer, and I skipped it because the prior questions had rewarded few-shot. The discipline isn't memorizing techniques; it's reading the one clause that names the root cause.

## TODO when we write this for real

- [ ] Tighten the hook; lead with the "right once, wrong once" story.
- [ ] Add a real code snippet for the self-critique loop (draft -> evaluate against criteria -> revise).
- [ ] Add a real example of criteria vs few-shot for severity (Q25).
- [ ] Diagram the ladder as a proper flowchart (Mermaid).
- [ ] Decide: standalone post, or section in the Architect learning-journal post.
- [ ] Verify every guide quote against the source before publishing.

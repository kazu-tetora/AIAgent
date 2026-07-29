# Plan quality checklist

## Grounding

- Distinguish repository facts from assumptions.
- Name relevant files, symbols, or commands that exist.
- Do not claim that an unexecuted check passed.

## Executability

- Make the outcome observable.
- Order steps by dependency.
- Give every behavior-changing step a test or direct verification.
- Cover compatibility and error paths.

## Delegation

- Make each delegated task independently useful.
- State its input, scope, prohibited actions, and output.
- Avoid concurrent edits to the same files.
- Leave integration and final verification with the parent.

## Learning value

- Require the learner to explain why each step exists.
- Create a small feedback loop before the next large change.
- Require evidence, not merely generated text, for completion.


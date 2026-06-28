# Contributing to FieldForm AI

FieldForm AI is an offline-first, CPU-first application that converts unstructured form inputs into clean structured data.

## Contribution Workflow

1. Create an issue before starting work.
2. Assign the issue to the correct team member.
3. Create a branch for the work.
4. Make focused changes only related to the issue.
5. Commit with a clear message.
6. Push the branch.
7. Create a Merge Request and link the issue.

## Branch Naming

Examples:

- `frontend`
- `docs/member2`
- `feature/parser`
- `tests/parser-cases`

## Commit Messages

Use clear commit messages.

Examples:

- `Add contributing guide`
- `Add changelog document`
- `Add parser test cases`
- `Update offline inference documentation`

## Local Development Rules

- Do not use GPU or CUDA.
- Core feature must work offline.
- Avoid cloud API calls for inference.
- Keep the project free and open source.
- Write readable code and documentation.

## Merge Request Checklist

Before creating a Merge Request:

- [ ] Issue is created and assigned.
- [ ] Changes are committed.
- [ ] Branch is pushed.
- [ ] MR is linked to the issue.
- [ ] Only related files are changed.
- [ ] Project still supports offline CPU-first execution.
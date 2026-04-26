---
name: open-pr
description: Opens a well-formed Pull Request on GitHub after implementation is complete. Use this at the end of any implementation task.
---

# Skill: open-pr

Use this skill when you have finished implementing a feature or fix and need to open a Pull Request.

## Steps

1. **Verify the branch**
   Confirm you are NOT on `main`. If you are, stop and ask for clarification.
   ```bash
   git branch --show-current
   ```

2. **Stage and commit all changes**
   Use conventional commit format. Reference the issue number.
   ```bash
   git add -A
   git commit -m "feat: <short description> (#<issue-number>)"
   ```

3. **Push the branch**
   ```bash
   git push -u origin HEAD
   ```

4. **Open the PR**
   Use the following template for the PR body:
   ```bash
   gh pr create \
     --title "<type>: <short description> (#<issue-number>)" \
     --body "## What
   <one paragraph describing what was implemented>

   ## Why
   Closes #<issue-number>

   ## How to test
   1. <step>
   2. <step>

   ## Checklist
   - [ ] No secrets committed
   - [ ] Tests written (if backend)
   - [ ] Follows file structure conventions"
   ```

5. **Tag the reviewers**
   After the PR is open, leave a comment:
   ```bash
   gh pr comment <pr-number> --body "@team PR ready for review 👀"
   ```

## What Not To Do

- Do not merge the PR yourself
- Do not push directly to `main`
- Do not open a PR without a linked issue number

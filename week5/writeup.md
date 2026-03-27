# Week 5 Writeup: Agentic Development with Warp

## Automation A: Warp Drive Saved Prompt (Workflow)
**Name:** `Week 5: Test, Lint & Format`
**Command:** `python -m pytest -q backend/tests && ruff check backend/ --fix && black backend/`

**How you used the automation:**
Since `make` commands throw environment variable errors natively on my Windows system, I created a shareable Warp Drive Workflow. This single command accelerates my feedback loop by resolving the pain point of typing out the full Python module execution paths for testing (`pytest`) and linting (`ruff`/`black`). It ensures the code is verified and formatted idempotently before any commit.

## Automation B: Multi-Agent Concurrent Workflows (via Git Worktree & Copilot)
*Note: My Warp account encountered an ErrorStatus 403 (blocked from using AI features/requires paid plan) when attempting to use `/agent`. To fulfill the assignment's architectural requirement of concurrent multi-agent development, I orchestrated the environment using Warp Terminal and substituted the Warp AI with GitHub Copilot instances in VS Code.*

**Tasks Selected:**
1. Backend Task (Difficulty: Easy) - Add a `/api/ping` health check endpoint.
2. Frontend Task (Difficulty: Easy) - Add a UI element to interact with the backend.

**Implementation & Orchestration:**
The main challenge of concurrent AI agents is file clobbering. To resolve this, I utilized the Warp terminal to execute `git worktree`, isolating the codebase into `week5-backend` and `week5-frontend`. 
1. **Agent 1 (Copilot instance 1):** Operated in the `week5-backend` worktree, successfully implementing the FastAPI logic without interfering with the main branch.
2. **Agent 2 (Copilot instance 2):** Operated concurrently in the `week5-frontend` worktree to update the static HTML.

**How you used the automation:**
This isolation pattern accelerated the workflow significantly. Instead of waiting for one task to finish linearly, I managed two independent agentic streams. Once both "agents" committed their tasks in their isolated worktrees, I used Warp to seamlessly merge `feature-backend` and `feature-frontend` back into the main repository, completely avoiding merge conflicts and resolving the concurrency pain point.
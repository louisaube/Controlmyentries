# Controlmyentries - Project Instructions

## BMad Method (v6.0.0-Beta.7)

This project uses the **BMad Method** (Breakthrough Method for Agile AI-Driven Development) for structured development with AI agents.

### Configuration

- Config: `_bmad/_config/config.yaml`
- Help catalog: `_bmad/_config/bmad-help.csv`
- Communication language: French
- Document output language: French

### Output Directories

- Planning artifacts: `_bmad-output/planning-artifacts/`
- Implementation artifacts: `_bmad-output/implementation-artifacts/`
- Project knowledge: `docs/`

### Available Agents

| Command | Agent | Role |
|---------|-------|------|
| `/bmad-analyst` | Mary | Business Analyst |
| `/bmad-architect` | Winston | Architect |
| `/bmad-dev` | Amelia | Developer |
| `/bmad-pm` | John | Product Manager |
| `/bmad-qa` | Quinn | QA Engineer |
| `/bmad-quick-flow-solo-dev` | Barry | Quick Flow Solo Dev |
| `/bmad-sm` | Bob | Scrum Master |
| `/bmad-tech-writer` | Paige | Technical Writer |
| `/bmad-ux-designer` | Sally | UX Designer |
| `/bmad-master` | BMad Master | Workflow Orchestrator |

### BMad Workflow Phases

**Phase 1 - Analysis:** `/bmad-brainstorm`, `/bmad-market-research`, `/bmad-domain-research`, `/bmad-technical-research`, `/bmad-create-brief`

**Phase 2 - Planning:** `/bmad-create-prd`, `/bmad-edit-prd`, `/bmad-validate-prd`, `/bmad-create-ux-design`

**Phase 3 - Solutioning:** `/bmad-create-architecture`, `/bmad-create-epics`, `/bmad-check-readiness`

**Phase 4 - Implementation:** `/bmad-sprint-planning`, `/bmad-sprint-status`, `/bmad-create-story`, `/bmad-dev-story`, `/bmad-code-review`, `/bmad-retrospective`, `/bmad-correct-course`

**Quick Flow:** `/bmad-quick-spec`, `/bmad-quick-dev`

**Utilities:** `/bmad-help`, `/bmad-document-project`, `/bmad-generate-context`, `/bmad-qa-automate`, `/bmad-party-mode`

### Getting Started

Run `/bmad-help` to see what to do next based on your current progress.

## Ralph Wiggum Plugin

This project has the **Ralph Wiggum** plugin installed for autonomous development loops.

### Commands

- `/ralph-loop "<prompt>" --max-iterations <n> --completion-promise "<text>"` - Start an autonomous loop
- `/cancel-ralph` - Cancel the active loop

### Safety

- Always set `--max-iterations` to prevent runaway loops
- Use clear completion criteria in your prompts

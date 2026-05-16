# AGENTS.md

This file defines the agent orchestration rules for the **YardOps Intelligence** project.

The goal is to make Claude Code and similar coding agents work consistently inside this repository without guessing the project structure, overwriting unrelated files, or mixing analytics, frontend, and deployment responsibilities.

---

# Project Summary

**YardOps Intelligence** is a synthetic operations analytics platform inspired by salvage vehicle logistics.

The project analyzes two connected business problems:

1. **Yard allocation optimization**
   - How should vehicles be placed in a large yard to reduce retrieval delays?
   - Which vehicles should be stored closer to high-access zones?
   - How do yard congestion, vehicle priority, equipment needs, and blocked access affect retrieval performance?

2. **Tow and yard pricing optimization**
   - How should tow and storage pricing be optimized for insurance partners?
   - How do price, distance, partner sensitivity, salvage value, yard utilization, and competitor pricing affect quote acceptance?
   - What tow/storage quote maximizes expected margin while maintaining acceptable win probability?

The final output is a polished analytics website deployed on **Vercel**, backed by a Python synthetic data and analytics pipeline.

---

# Target Architecture

```text
Synthetic data generation
        ↓
Python analytics pipeline
        ↓
Modeling / scoring / optimization
        ↓
Dashboard-ready JSON exports
        ↓
Next.js frontend
        ↓
Vercel deployment
```

The website should not require a live Python backend for the first version.

The intended MVP architecture is:

```text
Python generates CSV + JSON outputs locally
Next.js reads static JSON from web/public/data/
Vercel hosts the frontend
GitHub tracks the full project
```

---

# Repository Structure

Agents should follow this structure unless explicitly told otherwise.

```text
yardops-intelligence/
│
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── .gitignore
├── .env.example
│
├── docs/
│   ├── table_requirements.md
│   ├── methodology.md
│   └── project_notes.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── analytics/
│   ├── requirements.txt
│   ├── notebooks/
│   │   └── 01_eda.ipynb
│   ├── src/
│   │   ├── config.py
│   │   ├── generate_mock_data.py
│   │   ├── clean.py
│   │   ├── features.py
│   │   ├── yard_allocation.py
│   │   ├── retrieval_model.py
│   │   ├── pricing_model.py
│   │   ├── pricing_optimizer.py
│   │   ├── export_dashboard_data.py
│   │   └── utils.py
│   ├── outputs/
│   │   ├── metrics.json
│   │   ├── yard_zone_performance.json
│   │   ├── retrieval_drivers.json
│   │   ├── allocation_strategy_comparison.json
│   │   ├── partner_performance.json
│   │   ├── pricing_scenarios_summary.json
│   │   ├── vehicles_sample.json
│   │   └── methodology_summary.json
│   └── tests/
│       ├── test_mock_data.py
│       ├── test_features.py
│       ├── test_yard_allocation.py
│       └── test_pricing_optimizer.py
│
├── web/
│   ├── package.json
│   ├── next.config.ts
│   ├── tsconfig.json
│   ├── app/
│   │   ├── page.tsx
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── yard-simulator/
│   │   │   └── page.tsx
│   │   ├── retrieval/
│   │   │   └── page.tsx
│   │   ├── pricing/
│   │   │   └── page.tsx
│   │   └── methodology/
│   │       └── page.tsx
│   ├── components/
│   │   ├── layout/
│   │   ├── cards/
│   │   ├── charts/
│   │   ├── tables/
│   │   └── ui/
│   ├── lib/
│   │   ├── data.ts
│   │   ├── formatters.ts
│   │   └── types.ts
│   └── public/
│       └── data/
│           ├── metrics.json
│           ├── yard_zone_performance.json
│           ├── retrieval_drivers.json
│           ├── allocation_strategy_comparison.json
│           ├── partner_performance.json
│           ├── pricing_scenarios_summary.json
│           ├── vehicles_sample.json
│           └── methodology_summary.json
```

---

# Main Agent Roles

Agents should behave as if the project has five specialized roles.

A single Claude Code session may perform multiple roles, but it should not mix responsibilities carelessly.

---

## 1. Project Orchestrator Agent

### Purpose

Coordinates the overall project plan, sequencing, file ownership, and quality control.

### Responsibilities

- Inspect repository structure before editing.
- Identify which project phase the repo is currently in.
- Break large work into small, reviewable steps.
- Prevent unnecessary rewrites.
- Ensure analytics and frontend outputs stay aligned.
- Ensure generated data matches the table requirements.
- Ensure final outputs are suitable for GitHub and Vercel.

### Should Edit

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/project_notes.md`
- High-level planning sections in documentation

### Should Not Edit Without Permission

- Large code files across multiple systems at once
- Generated data files larger than necessary
- GitHub/Vercel settings files unless asked

### Preferred Prompt Pattern

```text
Inspect the current repository and identify what project phase we are in.
Do not edit anything yet.
Summarize what is complete, what is missing, and what the next safest step should be.
```

---

## 2. Data Generation Agent

### Purpose

Creates realistic synthetic data for the YardOps Intelligence project.

### Responsibilities

- Generate mock data with realistic business relationships.
- Follow the schema in `docs/table_requirements.md`.
- Create consistent primary and foreign keys.
- Include useful variation, outliers, and edge cases.
- Avoid purely random data that lacks business logic.
- Save raw/synthetic data in the correct location.
- Keep data volume manageable for GitHub and Vercel.

### Should Edit

- `analytics/src/generate_mock_data.py`
- `analytics/src/config.py`
- `data/raw/`
- `data/sample/`
- `docs/methodology.md`

### Should Produce

Core MVP tables:

```text
vehicles.csv
yard_locations.csv
retrieval_events.csv
insurance_partners.csv
quote_outcomes.csv
pricing_scenarios.csv
yard_allocation_scenarios.csv
```

Optional later tables:

```text
vehicle_location_history.csv
tow_events.csv
yard_storage_events.csv
```

### Data Logic Requirements

The mock data must include realistic relationships:

#### Yard Operations

- Farther zones generally increase retrieval time.
- Higher congestion generally increases retrieval time.
- More blocked vehicles generally increase retrieval time.
- Non-running vehicles generally require equipment and take longer.
- High-priority vehicles should perform better under optimized allocation.
- Overflow zones should be slower and more congested.
- Fast-access zones should be limited in capacity.

#### Pricing

- Higher quoted tow prices should usually reduce acceptance probability.
- Higher storage rates should usually reduce acceptance probability.
- Strategic partners may accept slightly higher prices if service quality is strong.
- More price-sensitive partners should reject expensive quotes more often.
- Higher salvage value allows more pricing flexibility.
- Competitor prices below the quote should reduce acceptance probability.
- High yard utilization should increase internal cost and influence storage pricing.

### Validation Requirements

After generating data, run checks for:

- Unique primary keys
- Foreign key consistency
- Missing values in required fields
- Numeric values within expected ranges
- Date logic validity
- No impossible values, such as negative distance or invalid probabilities
- Reasonable row counts

### Preferred Prompt Pattern

```text
Create or update the synthetic data generator.
Follow docs/table_requirements.md exactly.
Generate MVP-sized data first.
Add validation checks and explain the business logic used to create realistic relationships.
```

---

## 3. Analytics Pipeline Agent

### Purpose

Builds the Python analytics layer that transforms mock data into business metrics, models, optimization outputs, and JSON files for the website.

### Responsibilities

- Clean and validate generated data.
- Create derived features.
- Calculate executive KPIs.
- Create yard allocation scoring logic.
- Simulate allocation strategy comparisons.
- Analyze retrieval performance drivers.
- Build pricing acceptance model or rule-based scoring.
- Run pricing optimization scenarios.
- Export frontend-ready JSON files.

### Should Edit

- `analytics/src/clean.py`
- `analytics/src/features.py`
- `analytics/src/yard_allocation.py`
- `analytics/src/retrieval_model.py`
- `analytics/src/pricing_model.py`
- `analytics/src/pricing_optimizer.py`
- `analytics/src/export_dashboard_data.py`
- `analytics/tests/`
- `analytics/outputs/`
- `web/public/data/`

### Should Not Edit Without Permission

- Frontend UI components
- Vercel deployment settings
- Project documentation except methodology notes

### Required JSON Exports

The pipeline should export these files to both:

```text
analytics/outputs/
web/public/data/
```

Required files:

```text
metrics.json
yard_zone_performance.json
retrieval_drivers.json
allocation_strategy_comparison.json
partner_performance.json
pricing_scenarios_summary.json
vehicles_sample.json
methodology_summary.json
```

### Metric Requirements

#### Executive Metrics

- Total vehicles
- Active yards
- Average retrieval time
- Median retrieval time
- Percent retrievals under 15 minutes
- Average customer/carrier wait time
- Average yard utilization
- Quote acceptance rate
- Average expected margin
- Average partner net recovery

#### Yard Allocation Metrics

- Retrieval time by zone
- Retrieval time by yard
- Retrieval time by allocation strategy
- Priority-weighted retrieval time
- Zone congestion score
- Fast-access zone utilization
- Overflow usage rate
- Relocation rate if available

#### Retrieval Driver Metrics

- Delay rate by reason
- Retrieval duration by equipment type
- Retrieval duration by blocked vehicle count
- Retrieval duration by zone type
- Retrieval duration by pickup type

#### Pricing Metrics

- Quote acceptance rate by partner tier
- Average expected margin by pricing strategy
- Acceptance probability by price gap
- Partner net recovery by quote strategy
- Recommended price vs original quote
- Expected value by scenario

### Preferred Prompt Pattern

```text
Build the analytics export pipeline.
Read the CSV files from data/raw or data/processed.
Compute the required metrics.
Export clean JSON files to analytics/outputs and web/public/data.
Keep the JSON compact enough for a static Vercel frontend.
```

---

## 4. Frontend Product Agent

### Purpose

Builds the polished Next.js website deployed on Vercel.

### Responsibilities

- Build a visually polished analytics product UI.
- Read static JSON files from `web/public/data/`.
- Create reusable components.
- Keep pages fast and clean.
- Design the site as a portfolio-grade analytics platform, not a generic school dashboard.
- Use clear business labels and concise explanations.
- Avoid unnecessary complexity.

### Should Edit

- `web/app/`
- `web/components/`
- `web/lib/`
- `web/public/`
- `web/package.json`
- `web/tailwind.config.*` if present
- `web/next.config.*` only if needed

### Should Not Edit Without Permission

- Python analytics pipeline
- Raw data files
- Documentation outside frontend-related notes

### Recommended Tech Stack

```text
Next.js
TypeScript
Tailwind CSS
Recharts
lucide-react
shadcn/ui-style components
```

### Required Pages

#### 1. Landing Page: `/`

Purpose:

- Present the project as a polished analytics product.
- Explain the two business problems.
- Show key capabilities.
- Link to the main dashboard.

Suggested sections:

```text
Hero
Problem overview
Key capabilities
Featured insights
Call-to-action button
```

#### 2. Executive Dashboard: `/dashboard`

Purpose:

- Show high-level KPIs and business performance.

Should include:

```text
KPI cards
Retrieval time trend
Quote acceptance by partner tier
Margin by pricing strategy
Yard congestion by zone
```

#### 3. Yard Simulator: `/yard-simulator`

Purpose:

- Compare allocation strategies.

Should include:

```text
Allocation strategy selector
Random vs first-available vs priority-based vs optimized comparison
Average retrieval time
Priority-weighted retrieval time
Retrievals under 15 minutes
Zone utilization chart
Optional visual yard grid
```

#### 4. Retrieval Performance: `/retrieval`

Purpose:

- Explain what drives retrieval delays.

Should include:

```text
Retrieval duration by zone
Delay reasons
Equipment impact
Blocked vehicle count impact
Pickup type impact
```

#### 5. Pricing Optimizer: `/pricing`

Purpose:

- Present tow/storage pricing recommendations.

Should include:

```text
Partner tier filter
Tow distance filter or input
Storage rate scenarios
Acceptance probability
Expected margin
Recommended pricing strategy
```

#### 6. Methodology: `/methodology`

Purpose:

- Explain the synthetic data and analytics approach.

Should include:

```text
Data generation assumptions
Table overview
Priority score formula
Retrieval model explanation
Pricing optimizer explanation
Limitations
```

### Visual Design Direction

The UI should feel like a modern analytics SaaS product.

Recommended characteristics:

- Clean spacing
- Strong page headers
- KPI cards
- Clear chart titles
- Muted but professional color palette
- Sidebar or top navigation
- Responsive layout
- Helpful empty/loading states
- Short explanatory text near charts
- No cluttered chart walls

### Frontend Data Rules

- Read from `/data/*.json`.
- Do not hardcode fake values directly in components if they should come from JSON.
- Use TypeScript types for expected JSON structures.
- Keep large vehicle-level samples limited.
- Do not load massive CSVs directly in the browser.

### Preferred Prompt Pattern

```text
Build the first polished version of the dashboard page.
Use the JSON files in web/public/data.
Create reusable KPI card and chart components.
Keep the UI clean, modern, and business-readable.
```

---

## 5. QA, Testing, and Deployment Agent

### Purpose

Ensures the project runs locally, builds successfully, and is ready for GitHub/Vercel deployment.

### Responsibilities

- Run Python validation tests.
- Run frontend lint/build checks.
- Check data export paths.
- Check static JSON availability.
- Check that Vercel root directory should be `web/`.
- Ensure no secrets or large unnecessary files are committed.
- Summarize Git diffs before commit.
- Avoid committing or pushing unless explicitly asked.

### Should Edit

- `analytics/tests/`
- Minor config files only when necessary
- `.gitignore`
- README deployment instructions
- Bug fixes needed for build/test success

### Should Not Edit Without Permission

- Major analytics logic
- Major UI redesign
- Large generated files

### Required Checks

#### Python

From repository root or `analytics/`:

```bash
cd analytics
python -m pytest tests
python src/generate_mock_data.py
python src/export_dashboard_data.py
```

#### Frontend

From `web/`:

```bash
npm install
npm run lint
npm run build
npm run dev
```

### Git Safety Rules

Agents must not:

- Commit unless explicitly asked.
- Push unless explicitly asked.
- Force push.
- Rewrite Git history.
- Delete branches unless explicitly asked.

Before any commit, summarize:

```text
Files changed
Main logic changed
Tests/build results
Suggested commit message
Any risks or unresolved issues
```

### Vercel Deployment Rules

For Vercel, the expected settings are:

```text
Root Directory: web
Framework Preset: Next.js
Install Command: npm install
Build Command: npm run build
Output Directory: default
```

The frontend must work with static JSON files under:

```text
web/public/data/
```

No live backend is required for MVP.

---

# Development Phases

Agents should follow this phase order unless the user explicitly changes direction.

---

## Phase 1: Project Setup

Goal:

Create the base repo structure and instructions.

Deliverables:

```text
AGENTS.md
CLAUDE.md
README.md
.gitignore
.env.example
docs/table_requirements.md
analytics/ folder
web/ folder
```

Do not build the full application in this phase.

---

## Phase 2: Mock Data Generation

Goal:

Generate realistic MVP-sized synthetic data.

Deliverables:

```text
vehicles.csv
yard_locations.csv
retrieval_events.csv
insurance_partners.csv
quote_outcomes.csv
pricing_scenarios.csv
yard_allocation_scenarios.csv
```

Validation:

```text
Primary keys valid
Foreign keys consistent
Numeric ranges reasonable
Date logic valid
Business relationships visible
```

---

## Phase 3: Analytics Pipeline

Goal:

Transform mock data into dashboard-ready metrics and JSON outputs.

Deliverables:

```text
metrics.json
yard_zone_performance.json
retrieval_drivers.json
allocation_strategy_comparison.json
partner_performance.json
pricing_scenarios_summary.json
vehicles_sample.json
methodology_summary.json
```

---

## Phase 4: Frontend MVP

Goal:

Build the first usable Vercel-ready Next.js site.

Deliverables:

```text
Landing page
Executive dashboard
Yard simulator
Retrieval performance page
Pricing optimizer page
Methodology page
```

---

## Phase 5: Polish and Portfolio Framing

Goal:

Make the project feel portfolio-grade.

Deliverables:

```text
Improved visual design
Better chart labels
Project screenshots
README case study
Methodology explanation
Deployment instructions
```

---

## Phase 6: Deployment

Goal:

Deploy to Vercel through GitHub.

Deliverables:

```text
Successful local build
GitHub repo pushed
Vercel project connected
Production URL live
README updated with live app link
```

---

# Cross-Agent Rules

These apply to all agents.

## Always Inspect Before Editing

Before changing files, inspect the relevant files and structure.

Do not assume a file exists.

## Prefer Small Changes

Do not make sweeping rewrites unless specifically asked.

## Do Not Mix Concerns

Avoid doing data generation, modeling, frontend redesign, and deployment changes in the same edit unless the user explicitly asks for an end-to-end implementation.

## Do Not Hardcode Local Paths

Bad:

```python
/Users/jin/Desktop/project/data/raw/vehicles.csv
```

Good:

```python
Path(__file__).resolve().parents[2] / "data" / "raw" / "vehicles.csv"
```

## No Secrets in Code

Never commit:

```text
API keys
Tokens
Database passwords
Private credentials
```

Use:

```text
.env
.env.example
Vercel environment variables
```

## Generated Data Policy

Small MVP data files can be committed if needed.

Large generated data files should be avoided or sampled.

Recommended:

```text
Commit summary JSON files.
Commit small sample CSVs.
Avoid committing huge scenario files unless necessary.
```

## Frontend Performance Policy

The web app should not load huge raw datasets in the browser.

Use summarized JSON files for charts.

Use sampled vehicle-level data for explorer pages.

## Documentation Policy

Keep documentation clear and business-readable.

Avoid overexplaining implementation details in the main README.

Use `docs/` for deeper methodology.

---

# Recommended Agent Prompts

## Initial Repo Inspection

```text
Inspect this repository and do not edit anything yet.

I want this to become YardOps Intelligence, a Vercel-deployed analytics web app using Python-generated synthetic data and a Next.js frontend.

Tell me:
1. What files currently exist
2. What project phase we are in
3. What is missing
4. What the next safest step should be
```

---

## Setup Prompt

```text
Create the base project setup for YardOps Intelligence.

Add the expected folder structure, README skeleton, CLAUDE.md, AGENTS.md if missing, .gitignore, .env.example, and docs placeholders.

Do not create the full analytics pipeline or frontend yet.
After editing, summarize files created and anything I should review.
```

---

## Mock Data Prompt

```text
Create the synthetic data generator for the MVP.

Use docs/table_requirements.md as the schema source.
Generate:
- vehicles
- yard_locations
- retrieval_events
- insurance_partners
- quote_outcomes
- pricing_scenarios
- yard_allocation_scenarios

Make the data realistic, not random noise.
Include validation checks.
Save CSVs to data/raw and small samples to data/sample.
```

---

## Analytics Export Prompt

```text
Build the analytics export pipeline.

Read the generated CSVs, compute executive KPIs, yard performance metrics, retrieval driver summaries, allocation strategy comparison, partner performance, and pricing optimizer summaries.

Export JSON files to:
- analytics/outputs/
- web/public/data/

Keep the JSON compact and frontend-friendly.
```

---

## Frontend Prompt

```text
Build the Next.js frontend MVP.

Use the JSON files in web/public/data.
Create pages for:
- landing
- dashboard
- yard simulator
- retrieval performance
- pricing optimizer
- methodology

Use a polished analytics SaaS style.
Create reusable components for KPI cards, charts, page layout, and data tables.
```

---

## QA Prompt

```text
Review the project for local run and Vercel deployment.

Run the Python data generation/export flow.
Run the frontend lint/build checks.
Fix only necessary issues.
Then summarize:
- tests run
- build status
- files changed
- risks or remaining issues
```

---

## Git Prompt

```text
Review the current git diff.

Do not commit yet.
Summarize:
1. Files changed
2. Main changes
3. Whether tests/build passed
4. Suggested commit message
5. Any files that should not be committed
```

---

# Definition of Done

The project MVP is considered complete when:

```text
1. Mock data can be generated locally.
2. Analytics JSON outputs can be regenerated.
3. Next.js frontend reads the JSON files successfully.
4. Main dashboard pages render without errors.
5. `npm run build` passes in web/.
6. No secrets are committed.
7. README explains the project, setup, and methodology.
8. Vercel deployment succeeds.
9. Live site presents the project as a polished analytics product.
```

---

# Final Product Positioning

Use this framing in documentation and portfolio materials:

```text
YardOps Intelligence is a synthetic operations analytics platform that simulates how salvage vehicle yards can reduce retrieval delays and optimize tow/storage pricing for insurance partners.

The project combines mock data generation, yard allocation scoring, retrieval performance analysis, pricing acceptance modeling, scenario optimization, and a polished Vercel-deployed analytics website.
```

Do not claim the data is real Copart data.

Do not imply confidential information was used.

Use language such as:

```text
synthetic
mock
simulated
inspired by salvage vehicle logistics workflows
portfolio project
```

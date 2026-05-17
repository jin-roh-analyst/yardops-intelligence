# YardOps Intelligence

YardOps Intelligence is a synthetic operations analytics platform that simulates how salvage vehicle yards can reduce retrieval delays and optimize tow/storage pricing for insurance partners.

The project combines mock data generation, yard allocation scoring, retrieval performance analysis, pricing scenario optimization, and a static Next.js dashboard. It does not use real company data or confidential business records.

## Case Study

The project answers two connected operations questions:

- How should vehicles be placed across yard zones to reduce retrieval time and customer/carrier waiting?
- How should tow and storage pricing be adjusted to balance partner acceptance, recovery value, and expected margin?

The dashboard is designed for portfolio review. Charts include axis explanations, hover labels, and short readouts so the analysis is understandable without reading the Python code.

## Current Features

- Executive KPI dashboard for retrieval, yard utilization, quote acceptance, and expected margin
- Yard allocation simulator comparing random, first-available, priority-based, and optimized strategies
- Retrieval performance page showing delay reasons, equipment impact, blocked access, zone type, and pickup type
- Pricing optimizer page with partner tier, tow distance, and storage duration controls
- Methodology page explaining the synthetic data boundary, assumptions, pipeline, and limitations

## Project Structure

- `docs/`: project requirements, methodology, and notes
- `data/`: raw, processed, and sample synthetic datasets
- `analytics/`: Python data generation, modeling, exports, notebooks, outputs, and tests
- `web/`: Next.js frontend and static dashboard data

## Data Pipeline

```text
Synthetic CSV generation
        ->
Python analytics exports
        ->
Static JSON files in web/public/data/
        ->
Next.js frontend
        ->
Vercel deployment
```

The frontend reads static JSON only. It does not require a live Python backend.

## Local Setup

Install Python analytics dependencies:

```bash
python3 -m pip install -r analytics/requirements.txt
```

Regenerate raw CSVs:

```bash
python3 analytics/src/generate_mock_data.py
```

Regenerate dashboard JSON:

```bash
python3 analytics/src/export_dashboard_data.py
```

Install and run the frontend:

```bash
cd web
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:3000
```

## Verification

Run analytics tests:

```bash
python3 -m pytest analytics/tests
```

Run frontend checks:

```bash
cd web
npm run lint
npm run build
```

## Vercel Deployment

Import the GitHub repository into Vercel and set:

- Root Directory: `web`
- Framework Preset: `Next.js`
- Build Command: `npm run build`
- Output Directory: default Next.js setting

No environment variables are required for the MVP because the frontend uses committed static JSON files.

## Data Note

All data is synthetic, simulated, and created for a portfolio project inspired by salvage vehicle logistics workflows.

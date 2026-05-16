# YardOps Intelligence

YardOps Intelligence is a synthetic operations analytics project for salvage vehicle yard allocation, retrieval performance, and tow/storage pricing optimization.

This repository is organized as a local Python analytics pipeline plus a static Next.js frontend. The first version is intended to generate CSV and JSON outputs locally, then serve dashboard-ready JSON from `web/public/data/`.

## Project Structure

- `docs/`: project requirements, methodology, and notes
- `data/`: raw, processed, and sample synthetic datasets
- `analytics/`: Python data generation, modeling, exports, notebooks, outputs, and tests
- `web/`: Next.js frontend and static dashboard data


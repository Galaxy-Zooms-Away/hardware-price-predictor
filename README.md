# 🖥️ Hardware Market Dynamics & Pricing Pipeline

An end-to-end data engineering and analytics pipeline built to ingest, clean, and transform global hardware market pricing data during supply chain crises. This project transitions raw hardware metrics into localized, model-ready features while adhering to enterprise production standards.

---

## 🏗️ Architecture & Key Engineering Decisions

### 1. Decoupling Reference Configuration from Logic
Instead of hardcoding regional configurations (tax rates, currency multipliers) inside the execution scripts, this pipeline externalizes metadata into a standalone reference matrix (`data/external/regional_market_map.csv`). This approach ensures:
* **Separation of Concerns:** Business logic changes (e.g., an updated VAT rate) can be executed via simple CSV modification without altering core Python code.
* **Maintainability:** Prepares the system for future migration to dynamic, automated reference data APIs.

### 2. High-Performance Vectorization vs. Python Loops
To ensure the pipeline scales efficiently over massive datasets, standard iterative methods (`.apply(lambda...)`) were intentionally bypassed. By reshaping the reference data and utilizing a Relational Merge (`pd.merge`), row expansion and column unpacking are executed as a single, highly optimized, C-level vectorized operation.

### 3. Data Integrity via Left Joins
To protect against the "Silent Drop Trap" common in relational pipelines, reference data lookups utilize strict `LEFT JOIN` mechanics rather than inner joins. This guarantees that unmapped regions or source anomalies are preserved as visible `NaN` flags rather than silently altering raw data row counts, enabling reliable downstream validation checks.

---

## 🏃‍♂️ Project Progress & Agile Logs

### Sprint 1: Data Ingestion & Regional Expansion (In Progress)
**Goal:** Ingest baseline hardware pricing data and transform broad macro-regions into explicit country-level rows with calculated local currency and tax metrics.

* **US-1.1: Raw Data Ingestion (Completed)**
    * Configured secure Kaggle API integration tokens.
    * Automated baseline extraction of the hardware market dataset to the immutable storage directory (`data/raw/`).
* **US-1.2: Regional Data Explosion & Localization (Completed)**
    * Structured nested configuration profiles into a flat reference dataset.
    * Implemented a vectorized relational merge to handle multi-country row explosion natively.
    * Computed a clean, continuous numerical target variable (`final_local_price`) rounded to two decimal places, preserving the float properties required for downstream machine learning training.
# 🖥️ Predictive Modeling & Localized Price Forecasting for Smart Consumer Hardware Shopping

An end-to-end data engineering, analytics, and predictive forecasting pipeline built to model the impact of enterprise AI infrastructure expansion on consumer hardware markets. By analyzing macro supply chain indicators—such as High Bandwidth Memory (HBM) demand spikes and factory utilization rates—this pipeline transforms baseline market metrics into localized, consumer-ready price predictions and actionable buying signals.

---

## 🎯 Project Vision & Core Aims

The rapid growth of enterprise AI infrastructure requires massive quantities of High Bandwidth Memory (HBM), creating global supply shocks that cannibalize factory production lines and trigger severe price volatility in regular consumer RAM and PC hardware. 

This project bridges complex macro-economic supply chain data with consumer retail decisions through four primary aims:

* **Predictive Hardware Pricing & Shock Modeling:** Quantify and forecast consumer hardware price spikes using ensemble machine learning models driven by fab utilization rates, HBM demand multipliers, and supply chain delay lag features.
* **Regional Localization Engine:** Explode broad macro-regions (North America, Europe, Asia-Pacific) into explicit country-level retail profiles (United States, India, Germany, United Kingdom, Canada, Japan). Apply dynamic regional factor matrices to account for local tax structures (GST, VAT, local sales tax), live currency conversions, and distributor import markups.
* **Consumer Decision Intelligence:** Translate abstract market indicators into layperson-friendly shopping recommendations (e.g., "AI Tax" warnings, inventory shortage alerts, and automated "Buy Now" vs. "Wait" recommendations). Compare AI-forecasted prices against current local retail listings to detect store overpricing.
* **Enterprise Production Standards:** Maintain clean separation of concerns through modular Python packaging (`src/`), automated fail-fast data quality gates, and MLOps experiment tracking.

> 📌 **Scope & Iteration Note:** The aims outlined above represent the complete architectural vision for this project. To maintain high engineering standards within time constraints, features are implemented iteratively. Complex integrations (such as live retail scraping, external API connectors, and front-end UI extensions) may be placed in the **Product Backlog (The Icebox)** for future development.

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

### 4. Fail-Fast Validation Gates & Modular Architecture
Validation logic (completeness, consistency, sanity checks) is decoupled from ETL operations and acts as an automated pre-export barrier inside `src/app/validation.py`. Clean execution is orchestrated through a 2-file package layout (`src/app/pipeline.py`) triggered via a single root entry point (`python -m src.main`), preventing corrupted or unvalidated data from reaching `data/processed/`.

---

## 🏃‍♂️ Project Progress & Agile Logs

### Sprint 1: Data Ingestion & Regional Expansion (Completed)
**Goal:** Ingest baseline hardware pricing data and transform broad macro-regions into explicit country-level rows with calculated local currency and tax metrics.

* **US-1.1: Raw Data Ingestion (Completed)**
    * Configured secure Kaggle API integration tokens.
    * Automated baseline extraction of the hardware market dataset to the immutable storage directory (`data/raw/`).
* **US-1.2: Regional Data Explosion & Localization (Completed)**
    * Structured nested configuration profiles into a flat reference dataset.
    * Implemented a vectorized relational merge to handle multi-country row explosion natively.
    * Computed a clean, continuous numerical target variable (`final_local_price`) rounded to two decimal places, preserving the float properties required for downstream machine learning training.
* **US-1.3: Data Quality Gatekeeping (Completed)**
    * Engineered a triad of validation checks (`validate_completeness`, `validate_consistency`, `validate_sanity`) to enforce data health before processing.
    * Consolidated checks into a master gatekeeper (`run_pipeline_validations`) that halts execution on invalid or non-positive pricing records.
* **US-1.4: Production Modular Refactoring & Entry Point (Completed)**
    * Re-architected Jupyter ETL code into a 2-file Python package layout inside `src/app/`.
    * Established `src/main.py` as the execution entry point (`python -m src.main`) and exported clean data to `data/processed/hardware_prices_processed.csv`.
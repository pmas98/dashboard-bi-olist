# Dashboard Olist Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an interactive Python BI dashboard and academic report using the public Olist Brazilian e-commerce dataset.

**Architecture:** Keep data preparation in a tested ETL module and Streamlit as the visual layer. Load public CSVs directly from stable raw URLs with local Streamlit caching.

**Tech Stack:** Python, pandas, Streamlit, Plotly, pytest.

---

### Task 1: ETL Core

**Files:**
- Create: `src/olist_etl.py`
- Create: `tests/test_olist_etl.py`

- [ ] Write tests for delay calculation, payment aggregation, merged dataset columns, and filters.
- [ ] Implement loading constants and ETL helpers.
- [ ] Run `python -m pytest`.

### Task 2: Dashboard

**Files:**
- Create: `dashboard.py`
- Create: `requirements.txt`

- [ ] Build sidebar filters.
- [ ] Build KPIs and charts.
- [ ] Add diagnostic and prescription panels.
- [ ] Run `python -m py_compile dashboard.py src/olist_etl.py`.

### Task 3: Documentation

**Files:**
- Create: `README.md`
- Create: `relatorio.md`

- [ ] Document dataset source and rationale.
- [ ] Document metadata, pre-processing, dashboard usage, visual justification, diagnosis, and action plan.
- [ ] Verify all required report sections exist.

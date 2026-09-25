# Agents Sub-Team: Multi-Agent Intelligence Engine

## Overview
The `/agents` directory houses the multi-agent cognitive architecture for the **AI-Powered Geological, Mining, and Reporting Solution (SIH26023)**. It orchestrates domain-specific problem solving, mathematical calculations, and physical constraint verification.

---

## Agent Triad Architecture

```
User Query
    │
    ▼
┌─────────────────────────┐
│      Router Agent       │ ──> Classifies intent (Reserve, Stratigraphy, Report, Retrieval)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Core Mining Agent     │ ──> Applies domain logic & calculators (In-situ Reserve, GCV Bands)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    Validation Agent     │ ──> Enforces physical constraints & checks citation grounding
└───────────┬─────────────┘
            │
            ▼
Verified Output (Zero Hallucination)
```

---

## Directory Structure
```
agents/
├── router/
│   └── router_agent.py          # Query classifier & execution router
├── core/
│   ├── core_agent.py            # Domain reasoning & synthesis agent
│   └── mining_calculators.py    # Reserve calculation, GCV grading, stripping ratio
├── validation/
│   └── validation_agent.py      # Physical plausibility & citation grounding checks
├── orchestrator.py              # End-to-end multi-agent pipeline
├── requirements.txt             # Subsystem Python dependencies
└── README.md
```

---

## Domain Calculation Modules

### 1. In-situ Geological Reserves
$$\text{Reserves (MT)} = \frac{\text{Area } (m^2) \times \text{Average Seam Thickness } (m) \times \text{Specific Gravity } (t/m^3)}{1,000,000}$$

### 2. Volumetric Stripping Ratio
$$\text{Stripping Ratio } (m^3/t) = \frac{\text{Volume of Overburden } (m^3)}{\text{Coal Reserve } (\text{Tonnes})}$$

### 3. Non-Coking Coal Grade Banding
Direct mapping of Gross Calorific Value (GCV in kcal/kg) to Indian Ministry of Coal standard grades **G1** ($>7000\text{ kcal/kg}$) through **G17** ($2201 - 2500\text{ kcal/kg}$).

---

## Getting Started
```bash
# Navigate to agents directory
cd agents

# Install dependencies
pip install -r requirements.txt

# Run the test orchestrator
python orchestrator.py
```

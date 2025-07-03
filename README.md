# Fitness Functions - Simple Availability Testing

Tests if your group buying platform can handle the critical business path.

## What it does

Tests the critical path: Create cart → Add products → Process order → Payment → Logistics

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python fitness_functions.py

# Run demo
python run_demo.py

# Run unit tests
python -m pytest test_fitness_functions.py
```

## How it works

- Simulates 7 services (group buying, payment, logistics, etc.)
- Tests individual service health
- Tests critical path availability
- Calculates overall score (0-100)

Score ≥70 = System is healthy

## GitHub Actions

Automated testing runs on every push/PR. See `.github/workflows/simple-test.yml`

## Files

- `fitness_functions.py` - Core testing logic
- `run_demo.py` - Simple demo scenarios
- `test_fitness_functions.py` - Unit tests
- `.github/workflows/simple-test.yml` - GitHub Actions
git stat
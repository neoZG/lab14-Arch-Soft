# Fitness Functions - Availability Testing

Simple availability testing for a group buying platform using fitness functions.

## What it does

Tests if your system can handle the critical business path:
1. User creates a group cart
2. Others join and add products  
3. Cart closes when minimum reached
4. Order is processed and paid
5. Logistics and delivery handled

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the demo
python run_demo.py

# Run tests
python -m pytest test_fitness_functions.py

# Test locally before GitHub Actions
python test_github_actions.py
```

## Files

- `fitness_functions.py` - Core testing logic
- `run_demo.py` - Interactive demo with different scenarios
- `test_fitness_functions.py` - Unit tests
- `.github/workflows/` - GitHub Actions for automated testing

## How it works

The system simulates 7 services (group buying, payment, logistics, etc.) and tests:
- Individual service health
- Critical path availability  
- Performance under load
- Overall system score (0-100)

A score ≥80 means your system is healthy.

## GitHub Actions

Automated testing runs on:
- Every code change
- Scheduled health checks
- Before deployments

See `GITHUB_ACTIONS_README.md` for details.

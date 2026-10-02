# Contributing

## Adding a New Lab
1. Define the lab metadata in `app/models/core.py` (or seed script).
2. Create a new `Target` class in `app/services/targets.py`.
3. Implement `_evaluate_vulnerable` and `_evaluate_secure` methods using regex/string matching.
4. Update `LabEngine` to route to the new target.

## Adding a Learning Module
1. Define the module and lessons in `scripts/seed_learning.py`.
2. Add corresponding quiz questions to the seed script.
3. Run `python scripts/seed_learning.py` to populate the SQLite database.

## PR Process
1. Run `pytest` locally.
2. Ensure no UI breakages in the SPA.
3. Submit PR with detailed description.\n
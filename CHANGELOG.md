# Changelog

All notable changes to this project will be documented in this file.

## [0.1.2] - 2025-12-14
### Fixed
- Corrected an off-by-one / edge-case bug in `LinkedList.nth_from_end` that could return the wrong element or silently behave incorrectly when `n` was near the list length. Now raises clear `IndexError` messages for invalid `n` or empty lists.
- Bumped package version to `0.1.2`.

### Misc
- Added a small canonical example `examples/canonical_example.py` demonstrating common usage.
- Minor docstring and README clarifications.

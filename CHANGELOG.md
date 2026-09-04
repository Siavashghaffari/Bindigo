# Changelog

All notable changes to Bindigo will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Protein preprocessing pipeline
- Ligand 3D generation
- AutoDock Vina integration
- Pre-trained ML models
- Virtual screening mode

## [0.1.0] - 2025-01-15

### Added
- Initial package structure with src layout
- Command-line interface with Click
  - `bindigo predict` command (skeleton)
  - `bindigo info` command
- Input validation for proteins, ligands, and binding sites
- AutoDock Vina detection with an actionable error when the binary is missing,
  overridable via the `BINDIGO_VINA_PATH` environment variable
- Custom exception hierarchy
- Logging configuration
- Configuration management system
- MIT license
- Comprehensive test suite (70 tests, 73% coverage)
- Documentation (README, CONTRIBUTING, scope, MVP, design)
- Package build system (wheel + source distribution)
- Professional project structure following best practices

### Technical Details
- Python 3.9+ support
- Modern packaging with pyproject.toml
- Automated testing with pytest
- Code coverage reporting

### Notes
This is an alpha release with foundational infrastructure only. `bindigo predict`
validates its inputs and checks for AutoDock Vina, but the docking and machine
learning steps are not implemented yet, so it does not produce a binding
affinity or write a results file. There is no Python API in this release; use
the CLI. Core prediction functionality will be added in subsequent releases as phases 2-4 are implemented.

[Unreleased]: https://github.com/Siavashghaffari/Bindigo/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Siavashghaffari/Bindigo/releases/tag/v0.1.0

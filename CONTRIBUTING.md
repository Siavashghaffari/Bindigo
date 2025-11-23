# Contributing to Bindigo

Thank you for your interest in contributing to Bindigo! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Bindigo version)
- Error messages or logs

### Suggesting Features

For feature requests, create an issue describing:
- The problem you're trying to solve
- Your proposed solution
- How it aligns with Bindigo's scope (see scope.md)

### Contributing Code

#### Development Setup

1. **Fork and clone the repository**:
```bash
git clone https://github.com/YOUR_USERNAME/bindigo.git
cd bindigo
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install in development mode**:
```bash
pip install -e ".[dev]"
```

4. **Install optional dependencies** (if needed):
```bash
pip install -e ".[docking,viz]"
```

#### Development Workflow

1. **Create a feature branch**:
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** following the code style guidelines below

3. **Write tests** for your changes in `tests/`

4. **Run tests** to ensure everything passes:
```bash
pytest tests/
```

5. **Format code** with black:
```bash
black bindigo/ tests/
```

6. **Check code style** with flake8:
```bash
flake8 bindigo/ tests/
```

7. **Commit your changes**:
```bash
git add .
git commit -m "Add feature: description"
```

8. **Push and create a pull request**:
```bash
git push origin feature/your-feature-name
```

#### Code Style Guidelines

**Python Style**:
- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting (line length: 88)
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Write docstrings for all public functions/classes (Google style)

**Example Docstring**:
```python
def predict_affinity(protein: str, ligand: str) -> float:
    """
    Predict binding affinity for protein-ligand pair.

    Args:
        protein: PDB ID or file path to protein structure
        ligand: SMILES string or path to ligand file

    Returns:
        Predicted Kd in nanomolar

    Raises:
        InputError: If inputs are invalid
        PredictionError: If prediction fails
    """
    pass
```

**Naming Conventions**:
- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private functions: `_leading_underscore`

**Import Organization**:
```python
# Standard library
import os
from pathlib import Path

# Third-party
import numpy as np
from rdkit import Chem

# Local
from bindigo.utils.validation import validate_input
```

#### Testing Guidelines

**Write Tests For**:
- All new functions and classes
- Bug fixes (add regression test)
- Edge cases and error conditions

**Test Structure**:
- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- Use pytest fixtures for common test data
- Aim for >80% code coverage

**Example Test**:
```python
def test_validate_pdb_id():
    """Test PDB ID validation with valid input."""
    result = validate_protein_input("1HSG")
    assert result[0] == "pdb_id"
    assert result[1] == "1HSG"
```

**Running Tests**:
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_validation.py

# Run with coverage
pytest tests/ --cov=bindigo --cov-report=html

# Run with verbose output
pytest tests/ -v

# Run only fast tests (skip slow integration tests)
pytest tests/ -m "not slow"
```

#### Documentation

**For New Features**:
- Update README.md with usage examples
- Add docstrings to all public APIs
- Update scope.md or MVP.md if changing project scope
- Add comments for complex logic

**For Bug Fixes**:
- Document the fix in commit messages
- Update CHANGELOG.md (if exists)

### Pull Request Guidelines

**Before Submitting**:
- [ ] All tests pass
- [ ] Code is formatted with Black
- [ ] New code has tests (aim for >80% coverage)
- [ ] Docstrings are complete
- [ ] No merge conflicts with main branch

**PR Description Should Include**:
- What problem does this solve?
- What approach did you take?
- Any breaking changes?
- Screenshots (if UI changes)
- Related issues (#123)

**Review Process**:
- Maintainers will review within 1-2 weeks
- Address review comments
- Keep PR focused (one feature per PR)
- Be patient and respectful

## Project Structure

```
bindigo/
├── bindigo/          # Main package code
│   ├── cli/         # Command-line interface
│   ├── core/        # Core prediction pipeline
│   ├── preprocessing/  # Protein/ligand prep
│   ├── docking/     # Molecular docking
│   ├── ml/          # Machine learning models
│   ├── database/    # Database fetchers
│   └── utils/       # Utilities
├── tests/           # Test suite
│   ├── unit/       # Unit tests
│   └── integration/ # Integration tests
├── docs/            # Documentation (coming soon)
└── examples/        # Example scripts
```

## Development Priorities

See [MVP.md](MVP.md) for current development phases and priorities.

**Current Focus** (v0.1.0):
- Core prediction pipeline
- Preprocessing modules
- Docking integration
- ML model training

**Future Priorities** (v0.2+):
- Python API
- Virtual screening
- Advanced visualizations
- Performance optimization

## Questions?

- Check existing [issues](https://github.com/bindigo/bindigo/issues)
- Start a [discussion](https://github.com/bindigo/bindigo/discussions)
- Read [scope.md](scope.md) and [design.md](design.md)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Bindigo! 🧬

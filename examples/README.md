# Bindigo Examples

This directory contains tutorials, guides, and example scripts for using Bindigo.

## Documentation

### Tutorials

1. **[Getting Started](01_getting_started.md)** - Complete beginner's guide
   - Installation
   - Basic usage
   - Understanding output
   - Common examples
   - Troubleshooting

2. **[Python API Guide](02_python_api_guide.md)** - Python API documentation (v1.1+)
   - Basic usage
   - Batch processing
   - Virtual screening
   - Integration examples
   - Error handling

3. **[Quick Reference](03_quick_reference.md)** - Command cheat sheet
   - CLI commands
   - Input formats
   - Output format
   - Common patterns
   - Troubleshooting

## Example Scripts

### CLI Examples

- **[example_cli_workflow.sh](example_cli_workflow.sh)** - Complete CLI workflow
  ```bash
  chmod +x example_cli_workflow.sh
  ./example_cli_workflow.sh
  ```

### Python Examples (v1.1+)

- **[example_basic_prediction.py](example_basic_prediction.py)** - Basic Python API usage
  ```bash
  python example_basic_prediction.py
  ```

## Quick Start

### 1. Simple Prediction (CLI)

```bash
bindigo predict \
  --protein 1HSG \
  --ligand "CC(=O)Nc1ccc(O)cc1" \
  --output results.csv
```

### 2. Run Example Workflow

```bash
cd examples
chmod +x example_cli_workflow.sh
./example_cli_workflow.sh
```

### 3. Read Tutorials

Start with [Getting Started](01_getting_started.md) for a complete introduction.

## Future Examples

### Planned for v1.1+
- Virtual screening workflows
- Batch processing scripts
- Integration with other tools
- Jupyter notebooks
- Visualization examples

## Need Help?

- See tutorials above
- Check [../README.md](../README.md) for main documentation
- Visit [docs/](../docs/) for detailed documentation
- Open an issue: https://github.com/bindigo/bindigo/issues

## Contributing Examples

Have a useful example? Please contribute!
See [../CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

# Bindigo Quick Reference

Quick reference guide for common Bindigo commands and usage patterns.

## Installation

```bash
pip install bindigo                 # Install from PyPI
pip install bindigo[docking]        # With AutoDock Vina
pip install bindigo[dev]            # Development dependencies
pip install -e .                    # Install from source (editable)
```

## CLI Commands

### Basic Syntax

```bash
bindigo [COMMAND] [OPTIONS]
```

### Main Commands

| Command | Description |
|---------|-------------|
| `predict` | Predict binding affinity |
| `info` | Show package information |
| `--version` | Show version |
| `--help` | Show help |

## Predict Command

### Required Options

```bash
--protein TEXT    # PDB ID or file path (required)
--ligand TEXT     # SMILES or SDF file (required)
--output PATH     # Output CSV file (required)
```

### Optional Options

```bash
--center X Y Z           # Binding site center coordinates
--size FLOAT            # Box size in Angstroms (default: 20)
--save-pose            # Save docking pose (default: True)
--no-save-pose         # Don't save pose
--verbose              # Show detailed output
```

## Common Usage Patterns

### 1. PDB ID + SMILES

```bash
bindigo predict --protein 1HSG --ligand "CCO" --output results.csv
```

### 2. Local Files

```bash
bindigo predict --protein protein.pdb --ligand ligand.sdf --output results.csv
```

### 3. Custom Binding Site

```bash
bindigo predict \
  --protein 1HSG \
  --ligand "CCO" \
  --center 10.5 20.3 15.2 \
  --size 25 \
  --output results.csv
```

### 4. Verbose Mode

```bash
bindigo predict \
  --protein 1HSG \
  --ligand "CCO" \
  --output results.csv \
  --verbose
```

### 5. Without Saving Pose

```bash
bindigo predict \
  --protein 1HSG \
  --ligand "CCO" \
  --output results.csv \
  --no-save-pose
```

## Info Command

```bash
bindigo info              # Show all info
bindigo info --version    # Package version
bindigo info --models     # Available models
bindigo info --cite       # Citation information
```

## Input Formats

### Proteins

| Format | Example | Description |
|--------|---------|-------------|
| PDB ID | `1HSG` | 4-character code |
| PDB file | `protein.pdb` | Local PDB file |
| CIF file | `protein.cif` | mmCIF format (v1.1+) |

### Ligands

| Format | Example | Description |
|--------|---------|-------------|
| SMILES | `CCO` | SMILES string |
| SDF file | `ligand.sdf` | Structure file |
| MOL2 file | `ligand.mol2` | Mol2 format |

## Output Format

### CSV Columns

```csv
ligand_id,smiles,predicted_kd_nM,confidence,docking_score_kcal_mol,pose_file
```

| Column | Description | Unit |
|--------|-------------|------|
| `ligand_id` | Ligand identifier | - |
| `smiles` | Canonical SMILES | - |
| `predicted_kd_nM` | Predicted Kd | nM |
| `confidence` | High/Medium/Low | - |
| `docking_score_kcal_mol` | Vina score | kcal/mol |
| `pose_file` | Pose PDB path | - |

## Binding Affinity Scale

| Kd Range | Classification |
|----------|---------------|
| < 10 nM | Very strong |
| 10-100 nM | Strong |
| 100-1000 nM | Moderate |
| \> 1000 nM | Weak |

## Common SMILES Examples

```bash
# Simple molecules
"CCO"                              # Ethanol
"CC(=O)O"                          # Acetic acid
"c1ccccc1"                         # Benzene

# Drugs
"CC(=O)Nc1ccc(O)cc1"              # Acetaminophen (Tylenol)
"CC(=O)Oc1ccccc1C(=O)O"           # Aspirin
"CN1C=NC2=C1C(=O)N(C(=O)N2C)C"    # Caffeine
```

## Coordinate Examples

### Finding Binding Site Coordinates

1. **Visually with PyMOL:**
   ```python
   # In PyMOL
   select active_site, resi 25+26+27
   get_extent active_site
   # Use center coordinates
   ```

2. **From literature:**
   - Check paper's methods section
   - Look for "binding site" or "active site" coordinates

3. **Let Bindigo auto-detect:**
   ```bash
   # Just omit --center flag
   bindigo predict --protein 1HSG --ligand "CCO" --output results.csv
   ```

## Troubleshooting

### Common Errors

| Error | Solution |
|-------|----------|
| Invalid PDB ID | Check at rcsb.org or use local file |
| Invalid SMILES | Validate at daylight.com/daycgi/depict |
| File not found | Check file path and permissions |
| Low confidence | Ligand outside training domain |

### Quick Checks

```bash
# Verify installation
bindigo --version

# Check help
bindigo predict --help

# Test with simple example
bindigo predict --protein 1HSG --ligand "CCO" --output test.csv

# Verbose for debugging
bindigo predict --protein 1HSG --ligand "CCO" --output test.csv --verbose
```

## Performance Tips

1. **Reduce box size** for faster docking:
   ```bash
   --size 15  # Instead of default 20
   ```

2. **Use simple ligands** for testing:
   ```bash
   --ligand "CCO"  # Ethanol for quick tests
   ```

3. **Skip pose saving** if not needed:
   ```bash
   --no-save-pose
   ```

## Environment Variables

```bash
# Cache directory
export BINDIGO_CACHE_DIR=~/.bindigo/cache

# Temporary files
export BINDIGO_TMP_DIR=/tmp/bindigo

# Log level
export BINDIGO_LOG_LEVEL=DEBUG
```

## File Locations

```
~/.bindigo/               # User config directory
  ├── cache/             # Cached PDB files
  │   └── pdb/
  ├── config.yaml        # User config (optional)
  └── logs/              # Log files
```

## Example Workflows

### Workflow 1: Quick Test

```bash
# Test installation
bindigo predict --protein 1HSG --ligand "CCO" --output test.csv
cat test.csv
```

### Workflow 2: Single Prediction

```bash
# Real prediction
bindigo predict \
  --protein 3ERT \
  --ligand "CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O" \
  --output ibuprofen_er.csv \
  --verbose

# View results
cat ibuprofen_er.csv

# View pose
pymol ligand_1_pose.pdb 3ERT.pdb
```

### Workflow 3: Multiple Ligands

```bash
# Create script
cat > screen.sh << 'EOF'
#!/bin/bash
for smiles in "CCO" "CC(=O)O" "c1ccccc1"; do
  bindigo predict \
    --protein 1HSG \
    --ligand "$smiles" \
    --output "result_${smiles}.csv"
done
EOF

chmod +x screen.sh
./screen.sh
```

## Python API (v1.1+)

```python
from bindigo import BindingPredictor

predictor = BindingPredictor()
result = predictor.predict(protein="1HSG", ligand="CCO")

print(f"Kd: {result.kd_nM} nM")
```

## Resources

- Documentation: https://bindigo.readthedocs.io
- GitHub: https://github.com/bindigo/bindigo
- Issues: https://github.com/bindigo/bindigo/issues
- PyPI: https://pypi.org/project/bindigo

## Version History

| Version | Status | Features |
|---------|--------|----------|
| 0.1.0 | Alpha | CLI, validation, tests |
| 0.2.0 | Planned | Preprocessing pipeline |
| 0.3.0 | Planned | Docking integration |
| 1.0.0 | Planned | Full functionality |

---

**Last Updated**: 2025-01-15
**Version**: 0.1.0

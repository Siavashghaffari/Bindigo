# Getting Started with Bindigo

This tutorial covers the basics of using Bindigo for protein-ligand binding affinity prediction.

## Installation

First, install Bindigo:

```bash
pip install bindigo
```

Or install from source:

```bash
git clone https://github.com/bindigo/bindigo.git
cd bindigo
pip install -e .
```

## Verify Installation

Check that Bindigo is installed correctly:

```bash
bindigo --version
# Output: bindigo, version 0.1.0

bindigo --help
# Shows available commands and options
```

## Basic Usage

### 1. Simple Prediction with PDB ID and SMILES

The simplest way to use Bindigo is with a PDB ID and SMILES string:

```bash
bindigo predict \
  --protein 1HSG \
  --ligand "CC(=O)Nc1ccc(O)cc1" \
  --output results.csv
```

**What this does:**
- Downloads protein structure 1HSG (HIV-1 Protease) from RCSB PDB
- Converts SMILES to 3D structure (Acetaminophen)
- Automatically detects binding site
- Performs docking
- Predicts binding affinity
- Saves results to `results.csv`

### 2. Using Local Files

If you have local PDB and SDF files:

```bash
bindigo predict \
  --protein ./my_protein.pdb \
  --ligand ./my_ligand.sdf \
  --output results.csv
```

### 3. Specifying Binding Site

If you know the binding site coordinates:

```bash
bindigo predict \
  --protein 1HSG \
  --ligand "CCO" \
  --center 10.5 20.3 15.2 \
  --size 25 \
  --output results.csv
```

**Parameters:**
- `--center X Y Z`: Coordinates of binding site center (Ångströms)
- `--size N`: Box size for docking (Ångströms, default: 20)

### 4. Verbose Output

For detailed progress information:

```bash
bindigo predict \
  --protein 1HSG \
  --ligand "CC(=O)Oc1ccccc1C(=O)O" \
  --output results.csv \
  --verbose
```

This shows:
- Detailed preprocessing steps
- Molecular properties
- Docking progress
- Feature extraction details

## Understanding the Output

### CSV File Format

The `results.csv` file contains:

```csv
ligand_id,smiles,predicted_kd_nM,confidence,docking_score_kcal_mol,pose_file
ligand_1,CC(=O)Nc1ccc(O)cc1,245.7,High,-6.2,ligand_1_pose.pdb
```

**Column descriptions:**
- `ligand_id`: Unique identifier for the ligand
- `smiles`: Canonical SMILES representation
- `predicted_kd_nM`: Predicted Kd in nanomolar (lower = stronger binding)
- `confidence`: High/Medium/Low (based on model applicability)
- `docking_score_kcal_mol`: AutoDock Vina score (more negative = better)
- `pose_file`: Path to docked structure PDB file

### Interpreting Results

**Binding Affinity (Kd):**
- < 10 nM: Very strong binder
- 10-100 nM: Strong binder
- 100-1000 nM: Moderate binder
- \> 1000 nM: Weak binder

**Confidence Levels:**
- **High**: Ligand is similar to training data, prediction is reliable
- **Medium**: Moderate similarity, use with caution
- **Low**: Outside model's applicability domain, prediction may be unreliable

### Viewing Docked Poses

The docked structure is saved as a PDB file. View it with PyMOL, Chimera, or VMD:

```bash
# Using PyMOL
pymol ligand_1_pose.pdb protein.pdb

# Using Chimera
chimera ligand_1_pose.pdb protein.pdb
```

## Common Examples

### Example 1: Testing Aspirin Against COX-2

```bash
bindigo predict \
  --protein 5KIR \
  --ligand "CC(=O)Oc1ccccc1C(=O)O" \
  --output aspirin_cox2.csv
```

### Example 2: Local Files with Custom Site

```bash
bindigo predict \
  --protein ./structures/my_target.pdb \
  --ligand ./compounds/compound_001.sdf \
  --center 45.2 -12.8 33.1 \
  --size 30 \
  --output compound_001_results.csv \
  --verbose
```

### Example 3: Quick Test

```bash
# Ethanol (simple molecule for testing)
bindigo predict \
  --protein 1HSG \
  --ligand "CCO" \
  --output test.csv
```

## Getting Package Information

### View Available Models

```bash
bindigo info --models
```

Shows information about pre-trained ML models included with Bindigo.

### Citation Information

```bash
bindigo info --cite
```

Shows how to cite Bindigo and its dependencies in publications.

## Troubleshooting

### Error: "Invalid PDB ID"

- Check the PDB ID is correct at https://www.rcsb.org
- Try using a local PDB file instead

### Error: "Invalid SMILES"

- Validate your SMILES at https://www.daylight.com/daycgi/depict
- Check for unmatched parentheses or brackets
- Use canonical SMILES from PubChem or ChEMBL

### Prediction Takes Too Long

- Reduce binding site box size: `--size 15`
- Use a simpler ligand for testing
- Check your system resources

### Low Confidence Warning

- Your ligand may be very different from training data
- Consider using a different prediction method for validation
- Results should be interpreted cautiously

## Next Steps

1. **Virtual Screening**: See `02_virtual_screening.md` (v1.1+)
2. **Python API**: See `03_python_api.md` (v1.1+)
3. **Advanced Options**: See `04_advanced_usage.md`
4. **Batch Processing**: See `05_batch_processing.md` (v1.1+)

## Need Help?

- Documentation: https://bindigo.readthedocs.io
- Issues: https://github.com/bindigo/bindigo/issues
- Discussions: https://github.com/bindigo/bindigo/discussions

## Summary

```bash
# Basic workflow
bindigo predict --protein <PDB_ID|FILE> --ligand <SMILES|FILE> --output results.csv

# With options
bindigo predict \
  --protein 1HSG \
  --ligand "CC(=O)Nc1ccc(O)cc1" \
  --center 10.5 20.3 15.2 \
  --size 25 \
  --output results.csv \
  --verbose
```

Happy docking! 🧬

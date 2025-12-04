# Bindigo

**Protein-Ligand Binding Affinity Prediction using Molecular Docking and Machine Learning**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Bindigo is a Python package for predicting protein-ligand binding affinities. It combines molecular docking (AutoDock Vina) with machine learning to provide fast, accurate predictions for early-stage drug discovery.

## Features

- **Hybrid Prediction**: Combines AutoDock Vina docking with pre-trained ML models
- **Simple Interface**: Both CLI and Python API (v1.1+)
- **Automated Workflow**: Handles all preprocessing automatically
- **Database Integration**: Fetch structures from PDB, compounds from ChEMBL
- **Flexible Input**: Accepts PDB IDs, files, SMILES strings, or SDF files
- **Fast Results**: Get predictions in minutes

## Installation

### From PyPI (when released)

```bash
pip install bindigo
```

### From Source (Development)

```bash
git clone https://github.com/Siavashghaffari/Bindigo.git
cd bindigo
pip install -e .
```

### Dependencies

Bindigo requires Python 3.9+ and the following packages:
- RDKit (cheminformatics)
- BioPython (protein handling)
- AutoDock Vina (molecular docking)
- scikit-learn (machine learning)
- Click (CLI interface)

All dependencies are installed automatically via pip.

## Quick Start

### Command Line Interface

**Basic prediction** using PDB ID and SMILES:

```bash
bindigo predict --protein 1HSG --ligand "CC(=O)Nc1ccc(O)cc1" --output results.csv
```

**Using local files**:

```bash
bindigo predict --protein protein.pdb --ligand ligand.sdf --output results.csv
```

**Custom binding site**:

```bash
bindigo predict --protein 1HSG --ligand "CCO" --center 10.5 20.3 15.2 --size 25 --output results.csv
```

**Verbose output**:

```bash
bindigo predict --protein 1HSG --ligand "CCO" --output results.csv --verbose
```

### Python API (v1.1+)

```python
from bindigo import BindingPredictor

# Initialize predictor
predictor = BindingPredictor()

# Single prediction
result = predictor.predict(
    protein="1HSG",
    ligand="CC(=O)Nc1ccc(O)cc1"
)

print(f"Predicted Kd: {result.kd_nM:.1f} nM")
print(f"Confidence: {result.confidence}")
```

## Example Output

```
╔══════════════════════════════════════════════════════════════════╗
║                  Bindigo v0.1.0                                  ║
║         Protein-Ligand Binding Affinity Prediction              ║
╚══════════════════════════════════════════════════════════════════╝

[1/5] Loading inputs...
  ✓ Ligand: CC(=O)Nc1ccc(O)cc1 (Acetaminophen)
  ✓ Protein: Fetching PDB ID 1HSG from RCSB...

[2/5] Preparing protein...
  ✓ Loaded structure: HIV-1 Protease (198 residues, Chain A)

[3/5] Preparing ligand...
  ✓ Generated 3D structure (11 atoms)

[4/5] Running molecular docking...
  ✓ Best pose: -6.2 kcal/mol

[5/5] Predicting binding affinity...
  ✓ ML model prediction complete

╔══════════════════════════════════════════════════════════════════╗
║                      PREDICTION RESULTS                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Predicted Kd:           245.7 nM                                ║
║  Confidence:             High                                    ║
║  Docking Score:          -6.2 kcal/mol                           ║
╚══════════════════════════════════════════════════════════════════╝

Results saved to: results.csv
✓ Prediction completed in 2m 34s
```

## Output Format

### CSV Output

```csv
ligand_id,smiles,predicted_kd_nM,confidence,docking_score_kcal_mol,pose_file
ligand_1,CC(=O)Nc1ccc(O)cc1,245.7,High,-6.2,ligand_1_pose.pdb
```

**Fields**:
- `predicted_kd_nM`: Predicted dissociation constant in nanomolar
- `confidence`: High/Medium/Low based on model applicability
- `docking_score_kcal_mol`: AutoDock Vina docking score
- `pose_file`: Path to docked structure PDB file

## Documentation

- **Installation Guide**: See above
- **User Guide**: Coming soon
- **API Reference**: Coming soon
- **Examples**: See `examples/` directory

## Use Cases

- **Virtual Screening**: Screen compound libraries against protein targets
- **Lead Optimization**: Evaluate binding affinities of compound analogs
- **Drug Repurposing**: Test existing drugs against new targets
- **Research**: Computational binding affinity studies

## Limitations

Current version (v0.1.0) has the following limitations:
- Single predictions only (no batch mode yet)
- Rigid protein docking (no flexible residues)
- Small molecule ligands only (MW < 1000 Da)
- CPU only (no GPU acceleration)

See [MVP.md](MVP.md) for development roadmap.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Citation

If you use Bindigo in your research, please cite:

```
Bindigo: A Python package for protein-ligand binding affinity prediction
https://github.com/Siavashghaffari/Bindigo

```

Bindigo uses the following tools:
- **AutoDock Vina**: Eberhardt et al., J. Chem. Inf. Model. 2021
- **RDKit**: https://www.rdkit.org
- **BioPython**: Cock et al., Bioinformatics 2009
- **scikit-learn**: Pedregosa et al., JMLR 2011



## Acknowledgments

- PDBbind database for training data
- RCSB PDB for protein structures
- RDKit and BioPython communities

## Development Status

Current version: **0.1.0 (Alpha)**

This is an early development version. APIs may change. Production use is not recommended yet.

See [scope.md](docs/scope.md) and [MVP.md](docs/MVP.md) for project scope and roadmap.

## Authors 

This work was developed by **Siavash Ghaffari**. For any questions, feedback, or additional information, please feel free to reach out. Your input is highly valued and will help improve and refine this pipeline further.



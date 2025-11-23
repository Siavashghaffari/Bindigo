# Bindigo - Interface Design Document

## Design Philosophy

**Core Principles**:
- Simple by default, powerful when needed
- Clear progress feedback for long operations
- Helpful error messages with suggestions
- Consistent output formats
- Zero configuration for common use cases

---

## Command Structure

```
bindigo
│
├── predict              # Single protein-ligand prediction
│   ├── --protein        # [required] PDB ID or file path
│   ├── --ligand         # [required] SMILES or SDF file
│   ├── --output         # [required] Output CSV file
│   ├── --center         # [optional] Binding site center (X Y Z)
│   ├── --size           # [optional] Box size in Angstroms (default: 20)
│   ├── --save-pose      # [optional] Save docking pose (default: True)
│   └── --verbose        # [optional] Detailed output
│
├── screen               # [v1.1+] Batch virtual screening
│   ├── --protein
│   ├── --ligands        # Multi-molecule SDF file
│   ├── --output
│   └── --jobs           # Parallel jobs
│
├── info                 # Show package information
│   ├── --version        # Package version
│   ├── --models         # Available ML models
│   └── --cite           # Citation information
│
└── --help              # Show help message
```

---

## CLI User Experience

### 1. Basic Prediction Flow

#### Command
```bash
$ bindigo predict --protein 1HSG --ligand "CC(=O)Nc1ccc(O)cc1" --output results.csv
```

#### Terminal Output (Actual User View)

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
  ✓ Added hydrogens (1,542 atoms total)
  ✓ Removed 47 water molecules

[3/5] Preparing ligand...
  ✓ Generated 3D structure (11 atoms, 1 conformer)
  ✓ Assigned charges (Gasteiger method)

[4/5] Running molecular docking...
  ✓ Detected binding site: Center (10.2, 15.8, 20.3)
  ✓ AutoDock Vina: Exhaustiveness=8, Box size=20Å
  ⣷ Docking in progress... [====================] 100%
  ✓ Best pose: -6.2 kcal/mol

[5/5] Predicting binding affinity...
  ✓ Extracted molecular features (8 descriptors)
  ✓ ML model prediction complete

╔══════════════════════════════════════════════════════════════════╗
║                      PREDICTION RESULTS                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Predicted Kd:           245.7 nM                                ║
║  Confidence:             High                                    ║
║  Docking Score:          -6.2 kcal/mol                           ║
║  Binding Site:           Center (10.2, 15.8, 20.3)               ║
╚══════════════════════════════════════════════════════════════════╝

Results saved to: results.csv
Docking pose saved to: ligand_1_pose.pdb

✓ Prediction completed in 2m 34s
```

---

### 2. Prediction with Local Files

#### Command
```bash
$ bindigo predict --protein ./protein.pdb --ligand ./ligand.sdf --output results.csv --verbose
```

#### Terminal Output (Verbose Mode)

```
╔══════════════════════════════════════════════════════════════════╗
║                  Bindigo v0.1.0 (Verbose Mode)                   ║
╚══════════════════════════════════════════════════════════════════╝

[1/5] Loading inputs...
  → Reading ligand from: ./ligand.sdf
    • Molecule name: Compound_X
    • Formula: C15H22N2O3
    • Molecular weight: 278.35 Da
  ✓ Ligand loaded successfully

  → Reading protein from: ./protein.pdb
    • Structure: Custom protein (342 residues)
    • Chains: A, B (using Chain A)
    • Resolution: 2.1 Å
  ✓ Protein loaded successfully

[2/5] Preparing protein...
  → Removing non-protein atoms...
    • Removed 124 water molecules (HOH)
    • Removed 2 sulfate ions (SO4)
  → Adding hydrogens...
    • Added 2,718 hydrogen atoms
  → Validating structure...
    • Total atoms: 5,482
    • Missing residues: None detected
  ✓ Protein preparation complete

[3/5] Preparing ligand...
  → Checking 3D coordinates... ✓ Present
  → Adding hydrogens... ✓ Added 22 atoms
  → Generating partial charges...
    • Method: Gasteiger
    • Total charge: 0.00
  → Detecting rotatable bonds... 5 found
  ✓ Ligand preparation complete

[4/5] Running molecular docking...
  → Detecting binding site...
    • Algorithm: Geometric pocket detection
    • Largest cavity center: (25.4, -12.3, 8.9)
    • Volume: ~800 Å³
  ✓ Binding site identified

  → Configuring AutoDock Vina...
    • Center: (25.4, -12.3, 8.9)
    • Box size: 20 × 20 × 20 Å
    • Exhaustiveness: 8
    • CPU cores: 4

  → Running docking simulation...
    Computing grid maps...              [████████████] 100%
    Performing docking...               [████████████] 100%
    Clustering poses...                 [████████████] 100%

  → Top 3 poses:
    1. Score: -8.7 kcal/mol (selected)
    2. Score: -8.1 kcal/mol
    3. Score: -7.9 kcal/mol
  ✓ Docking complete

[5/5] Predicting binding affinity...
  → Extracting molecular features...
    • Docking score: -8.7 kcal/mol
    • Molecular weight: 278.35 Da
    • LogP: 2.34
    • H-bond donors: 2
    • H-bond acceptors: 5
    • Rotatable bonds: 5
    • TPSA: 64.8 Ų
    • Aromatic rings: 1
  ✓ Features extracted (8 total)

  → Running ML prediction...
    • Model: Random Forest Regressor
    • Training set: PDBbind v2020 (4,852 complexes)
    • Applicability domain check: PASS
  ✓ Prediction complete

╔══════════════════════════════════════════════════════════════════╗
║                      PREDICTION RESULTS                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Predicted Kd:           12.4 nM                                 ║
║  Predicted pKd:          7.91                                    ║
║  Confidence:             High (in-domain)                        ║
║                                                                  ║
║  Docking Score:          -8.7 kcal/mol                           ║
║  Pose RMSD:              N/A (no reference)                      ║
║                                                                  ║
║  Binding Site:           Center (25.4, -12.3, 8.9)               ║
║  Box Size:               20 × 20 × 20 Å                          ║
║                                                                  ║
║  Molecular Properties:                                           ║
║    MW:                   278.35 Da                               ║
║    LogP:                 2.34                                    ║
║    TPSA:                 64.8 Ų                                  ║
║    Rotatable bonds:      5                                       ║
╚══════════════════════════════════════════════════════════════════╝

Output files:
  ✓ results.csv (prediction data)
  ✓ ligand_1_pose.pdb (docked structure)

Total execution time: 3m 12s
Peak memory usage: 1.2 GB
```

---

### 3. Custom Binding Site

#### Command
```bash
$ bindigo predict --protein 1HSG --ligand "CCO" --center 10.5 20.3 15.2 --size 25 --output results.csv
```

#### Terminal Output

```
╔══════════════════════════════════════════════════════════════════╗
║                  Bindigo v0.1.0                                  ║
╚══════════════════════════════════════════════════════════════════╝

[1/5] Loading inputs...
  ✓ Ligand: CCO (Ethanol)
  ✓ Protein: Fetching PDB ID 1HSG...

[2/5] Preparing protein...
  ✓ Processed structure (198 residues)

[3/5] Preparing ligand...
  ✓ Generated 3D structure (3 atoms)

[4/5] Running molecular docking...
  ✓ Using custom binding site: (10.5, 20.3, 15.2)
  ✓ Box size: 25 Å
  ⣾ Docking... [====================] 100%
  ✓ Best pose: -3.1 kcal/mol

[5/5] Predicting binding affinity...
  ⚠ Warning: Low docking score may indicate weak binding
  ✓ Prediction complete

╔══════════════════════════════════════════════════════════════════╗
║                      PREDICTION RESULTS                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Predicted Kd:           >10 µM (weak binder)                    ║
║  Confidence:             Medium                                  ║
║  Docking Score:          -3.1 kcal/mol                           ║
╚══════════════════════════════════════════════════════════════════╝

Results saved to: results.csv

✓ Completed in 1m 45s
```

---

### 4. Error Handling Examples

#### Invalid PDB ID

```bash
$ bindigo predict --protein 9XYZ --ligand "CCO" --output results.csv
```

```
╔══════════════════════════════════════════════════════════════════╗
║                  Bindigo v0.1.0                                  ║
╚══════════════════════════════════════════════════════════════════╝

[1/5] Loading inputs...
  ✓ Ligand: CCO
  ✗ Error: Could not fetch PDB ID '9XYZ' from RCSB PDB

╔══════════════════════════════════════════════════════════════════╗
║  ERROR: Invalid PDB ID                                           ║
╠══════════════════════════════════════════════════════════════════╣
║  The PDB ID '9XYZ' does not exist in the RCSB database.          ║
║                                                                  ║
║  Suggestions:                                                    ║
║    • Check the PDB ID at https://www.rcsb.org                    ║
║    • Use a local file: --protein /path/to/protein.pdb            ║
║    • Try a known PDB ID (e.g., 1HSG, 3ERT, 4AGQ)                 ║
╚══════════════════════════════════════════════════════════════════╝

Prediction failed. Check the error message above.
```

#### Invalid SMILES

```bash
$ bindigo predict --protein 1HSG --ligand "CC(=O" --output results.csv
```

```
╔══════════════════════════════════════════════════════════════════╗
║                  Bindigo v0.1.0                                  ║
╚══════════════════════════════════════════════════════════════════╝

[1/5] Loading inputs...
  ✗ Error: Invalid SMILES string 'CC(=O'

╔══════════════════════════════════════════════════════════════════╗
║  ERROR: Invalid Ligand Structure                                 ║
╠══════════════════════════════════════════════════════════════════╣
║  The SMILES string 'CC(=O' could not be parsed.                  ║
║                                                                  ║
║  Common issues:                                                  ║
║    • Unmatched parentheses/brackets                              ║
║    • Invalid atom symbols                                        ║
║    • Incorrect bond notation                                     ║
║                                                                  ║
║  Suggestions:                                                    ║
║    • Validate SMILES: https://www.daylight.com/daycgi/depict     ║
║    • Use canonical SMILES from PubChem/ChEMBL                    ║
║    • Provide SDF file instead: --ligand ligand.sdf               ║
║                                                                  ║
║  Example valid SMILES:                                           ║
║    • Aspirin: CC(=O)Oc1ccccc1C(=O)O                              ║
║    • Ethanol: CCO                                                ║
╚══════════════════════════════════════════════════════════════════╝
```

#### Missing Required Arguments

```bash
$ bindigo predict --protein 1HSG
```

```
Error: Missing option '--ligand'.

Usage: bindigo predict [OPTIONS]

  Predict protein-ligand binding affinity

Options:
  --protein TEXT   PDB ID or file path [required]
  --ligand TEXT    SMILES string or SDF file [required]
  --output TEXT    Output CSV file path [required]
  --center FLOAT   Binding site center (X Y Z) [optional]
  --size FLOAT     Box size in Angstroms (default: 20)
  --save-pose      Save docking pose PDB (default: True)
  --verbose        Show detailed progress
  --help           Show this message and exit
```

---

### 5. Help Messages

#### Main Help

```bash
$ bindigo --help
```

```
╔══════════════════════════════════════════════════════════════════╗
║                  Bindigo v0.1.0                                  ║
║         Protein-Ligand Binding Affinity Prediction              ║
╚══════════════════════════════════════════════════════════════════╝

Usage: bindigo [OPTIONS] COMMAND [ARGS]...

  Bindigo predicts protein-ligand binding affinities using molecular
  docking and machine learning.

Commands:
  predict    Predict binding affinity for a protein-ligand pair
  screen     Virtual screening of compound libraries [v1.1+]
  info       Show package and model information

Options:
  --version  Show version and exit
  --help     Show this message and exit

Examples:
  # Basic prediction using PDB ID and SMILES
  $ bindigo predict --protein 1HSG --ligand "CC(=O)Oc1ccccc1C(=O)O" --output results.csv

  # Using local files
  $ bindigo predict --protein protein.pdb --ligand ligand.sdf --output results.csv

  # Custom binding site
  $ bindigo predict --protein 1HSG --ligand "CCO" --center 10 20 15 --output results.csv

Documentation: https://github.com/bindigo/bindigo
Report issues: https://github.com/bindigo/bindigo/issues
```

#### Predict Help

```bash
$ bindigo predict --help
```

```
Usage: bindigo predict [OPTIONS]

  Predict protein-ligand binding affinity using docking + ML

  This command performs molecular docking with AutoDock Vina and predicts
  binding affinity (Kd) using a pre-trained machine learning model.

Options:
  --protein TEXT           PDB ID (e.g., '1HSG') or file path (e.g.,
                          './protein.pdb') [required]

  --ligand TEXT           SMILES string (e.g., 'CCO') or SDF file path
                          (e.g., './ligand.sdf') [required]

  --output TEXT           Output CSV file path (e.g., 'results.csv')
                          [required]

  --center FLOAT...       Binding site center coordinates (X Y Z in
                          Angstroms). If not specified, the largest pocket
                          will be detected automatically.
                          Example: --center 10.5 20.3 15.2

  --size FLOAT            Binding site box size in Angstroms (default: 20)
                          Larger values cover more space but increase
                          computation time.

  --save-pose / --no-save-pose
                          Save docked ligand pose as PDB file (default: True)

  --verbose               Show detailed progress and intermediate results

  --help                  Show this message and exit

Input Formats:
  Protein:  PDB file, PDB ID (auto-fetched from RCSB)
  Ligand:   SMILES string, SDF file, MOL2 file

Output Files:
  <output>.csv          Prediction results (Kd, scores, metadata)
  <ligand>_pose.pdb     Docked ligand structure (if --save-pose)

Examples:
  # Fetch protein from PDB, use SMILES
  $ bindigo predict --protein 1HSG --ligand "CC(=O)Nc1ccc(O)cc1" --output results.csv

  # Local files with custom binding site
  $ bindigo predict --protein protein.pdb --ligand ligand.sdf --center 10 20 15 --output results.csv

  # Verbose output for debugging
  $ bindigo predict --protein 1HSG --ligand "CCO" --output test.csv --verbose
```

---

## Output File Formats

### CSV Output (`results.csv`)

```csv
ligand_id,ligand_name,smiles,predicted_kd_nM,predicted_pKd,confidence,docking_score_kcal_mol,binding_site_center,box_size,pose_file,timestamp
ligand_1,Acetaminophen,CC(=O)Nc1ccc(O)cc1,245.7,6.61,High,-6.2,"(10.2, 15.8, 20.3)",20,ligand_1_pose.pdb,2025-01-15T14:32:18
```

**Field Descriptions**:
- `ligand_id`: Unique identifier (auto-generated or from input file)
- `ligand_name`: Molecule name (from SDF) or derived from SMILES
- `smiles`: Canonical SMILES representation
- `predicted_kd_nM`: Predicted dissociation constant in nanomolar
- `predicted_pKd`: Predicted pKd (-log10(Kd in M))
- `confidence`: High/Medium/Low based on applicability domain
- `docking_score_kcal_mol`: AutoDock Vina docking score
- `binding_site_center`: (X, Y, Z) coordinates
- `box_size`: Docking box size in Angstroms
- `pose_file`: Path to docked structure PDB file
- `timestamp`: ISO 8601 timestamp of prediction

---

## Python API Design (v1.1+)

### Basic Usage

```python
from bindigo import BindingPredictor

# Initialize predictor
predictor = BindingPredictor()

# Single prediction
result = predictor.predict(
    protein="1HSG",                    # PDB ID or file path
    ligand="CC(=O)Nc1ccc(O)cc1"       # SMILES or SDF path
)

# Access results
print(f"Predicted Kd: {result.kd_nM:.1f} nM")
print(f"Docking Score: {result.docking_score:.2f} kcal/mol")
print(f"Confidence: {result.confidence}")
```

### Advanced Usage

```python
from bindigo import BindingPredictor
from bindigo.utils import BindingSite

# Initialize with custom settings
predictor = BindingPredictor(
    model="default",           # ML model name
    exhaustiveness=8,          # Vina exhaustiveness
    verbose=True              # Progress output
)

# Define custom binding site
site = BindingSite(
    center=(10.5, 20.3, 15.2),
    size=25.0
)

# Prediction with options
result = predictor.predict(
    protein="./protein.pdb",
    ligand="./ligand.sdf",
    binding_site=site,
    save_pose=True,
    output_dir="./results"
)

# Detailed results
print(result)
# BindingResult(
#     ligand_id='ligand_1',
#     kd_nM=12.4,
#     pKd=7.91,
#     confidence='High',
#     docking_score=-8.7,
#     pose_path='./results/ligand_1_pose.pdb'
# )
```

### Batch Predictions

```python
from bindigo import BindingPredictor

predictor = BindingPredictor()

# List of SMILES
ligands = [
    "CC(=O)Nc1ccc(O)cc1",      # Acetaminophen
    "CC(=O)Oc1ccccc1C(=O)O",   # Aspirin
    "CCO"                       # Ethanol
]

# Batch prediction
results = predictor.predict_batch(
    protein="1HSG",
    ligands=ligands,
    n_jobs=4                    # Parallel processing
)

# Iterate results
for result in results:
    print(f"{result.ligand_id}: {result.kd_nM:.1f} nM")

# Export to DataFrame
import pandas as pd
df = predictor.to_dataframe(results)
df.to_csv("batch_results.csv", index=False)
```

### Result Object API

```python
class BindingResult:
    """Container for prediction results"""

    # Core predictions
    ligand_id: str
    ligand_name: str
    smiles: str
    kd_nM: float                    # Predicted Kd in nanomolar
    pKd: float                      # Predicted pKd
    confidence: str                 # "High", "Medium", "Low"

    # Docking results
    docking_score: float            # kcal/mol
    pose_path: str                  # Path to PDB file
    binding_site: BindingSite       # Binding site info

    # Molecular properties
    molecular_weight: float
    logp: float
    hbd: int                        # H-bond donors
    hba: int                        # H-bond acceptors
    rotatable_bonds: int
    tpsa: float                     # Topological polar surface area

    # Metadata
    timestamp: datetime
    execution_time: float           # seconds

    # Methods
    def to_dict(self) -> dict:
        """Convert to dictionary"""

    def save(self, filepath: str):
        """Save to JSON file"""

    def visualize(self, output="protein_ligand.png"):
        """Generate 2D/3D visualization"""
```

---

## Package Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │   CLI (Click)        │      │   Python API         │        │
│  │                      │      │                      │        │
│  │  • bindigo predict   │      │  • BindingPredictor  │        │
│  │  • bindigo screen    │      │  • predict()         │        │
│  │  • bindigo info      │      │  • predict_batch()   │        │
│  └──────────┬───────────┘      └──────────┬───────────┘        │
│             │                             │                    │
│             └─────────────┬───────────────┘                    │
└───────────────────────────┼────────────────────────────────────┘
                            │
┌───────────────────────────┼────────────────────────────────────┐
│                    CORE PREDICTION ENGINE                       │
├───────────────────────────┼────────────────────────────────────┤
│                           ▼                                     │
│              ┌─────────────────────────┐                        │
│              │   Pipeline Manager      │                        │
│              │                         │                        │
│              │  • Orchestrates flow    │                        │
│              │  • Error handling       │                        │
│              │  • Progress tracking    │                        │
│              └────────────┬────────────┘                        │
│                           │                                     │
│         ┌─────────────────┼─────────────────┐                  │
│         ▼                 ▼                 ▼                  │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│  │   Protein   │   │   Ligand    │   │  Binding    │          │
│  │   Prep      │   │   Prep      │   │  Site       │          │
│  │             │   │             │   │  Detector   │          │
│  │ • PDB fetch │   │ • SMILES→3D │   │ • Pocket    │          │
│  │ • Add H     │   │ • Add H     │   │   detection │          │
│  │ • Clean     │   │ • Charges   │   │ • Validate  │          │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘          │
│         │                 │                 │                  │
│         └─────────────────┼─────────────────┘                  │
│                           ▼                                     │
│              ┌─────────────────────────┐                        │
│              │   Docking Engine        │                        │
│              │                         │                        │
│              │  • Vina wrapper         │                        │
│              │  • PDBQT conversion     │                        │
│              │  • Pose extraction      │                        │
│              └────────────┬────────────┘                        │
│                           │                                     │
│                           ▼                                     │
│              ┌─────────────────────────┐                        │
│              │   Feature Extractor     │                        │
│              │                         │                        │
│              │  • Molecular descriptors│                        │
│              │  • Docking features     │                        │
│              │  • Interaction FPs      │                        │
│              └────────────┬────────────┘                        │
│                           │                                     │
│                           ▼                                     │
│              ┌─────────────────────────┐                        │
│              │   ML Predictor          │                        │
│              │                         │                        │
│              │  • Load model           │                        │
│              │  • Make prediction      │                        │
│              │  • Confidence scoring   │                        │
│              └────────────┬────────────┘                        │
│                           │                                     │
│                           ▼                                     │
│              ┌─────────────────────────┐                        │
│              │   Result Formatter      │                        │
│              │                         │                        │
│              │  • Generate CSV/JSON    │                        │
│              │  • Save poses           │                        │
│              │  • Create visualizations│                        │
│              └─────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼────────────────────────────────────┐
│                      DEPENDENCIES                               │
├───────────────────────────┼────────────────────────────────────┤
│                           ▼                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  RDKit   │  │ BioPython│  │  Vina    │  │ sklearn  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  NumPy   │  │  Pandas  │  │  Click   │  │ requests │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Prediction Workflow Diagram

```
START
  │
  ├─── [User Input] ─────────────────────────────────────┐
  │                                                       │
  ├─→ Protein: PDB ID or file                            │
  ├─→ Ligand: SMILES or SDF                              │
  └─→ Options: binding site, output path                 │
  │                                                       │
  ▼                                                       │
┌────────────────────────────────────┐                   │
│  INPUT VALIDATION                  │                   │
│                                    │                   │
│  ✓ Check protein exists            │                   │
│  ✓ Validate ligand structure       │                   │
│  ✓ Check output path writable      │                   │
└────────────┬───────────────────────┘                   │
             │                                           │
             ▼                                           │
┌────────────────────────────────────┐                   │
│  PROTEIN PREPARATION               │                   │
│                                    │                   │
│  1. Fetch/Load PDB                 │◄──── [PDB API]   │
│  2. Clean structure                │                   │
│  3. Add hydrogens                  │                   │
│  4. Select chain                   │                   │
└────────────┬───────────────────────┘                   │
             │                                           │
             ▼                                           │
┌────────────────────────────────────┐                   │
│  LIGAND PREPARATION                │                   │
│                                    │                   │
│  1. Parse SMILES/SDF               │                   │
│  2. Generate 3D (if SMILES)        │                   │
│  3. Add hydrogens                  │                   │
│  4. Assign charges                 │                   │
└────────────┬───────────────────────┘                   │
             │                                           │
             ▼                                           │
┌────────────────────────────────────┐                   │
│  BINDING SITE DETECTION            │                   │
│                                    │                   │
│  Auto: Find largest pocket         │                   │
│   OR                               │                   │
│  Manual: Use user coordinates      │                   │
└────────────┬───────────────────────┘                   │
             │                                           │
             ▼                                           │
┌────────────────────────────────────┐                   │
│  MOLECULAR DOCKING                 │                   │
│                                    │                   │
│  1. Convert to PDBQT               │                   │
│  2. Run AutoDock Vina              │◄──── [Vina]      │
│  3. Parse results                  │                   │
│  4. Extract best pose              │                   │
└────────────┬───────────────────────┘                   │
             │                                           │
             ▼                                           │
┌────────────────────────────────────┐                   │
│  FEATURE EXTRACTION                │                   │
│                                    │                   │
│  • Docking score                   │                   │
│  • Molecular descriptors (RDKit)   │                   │
│  • Ligand properties               │                   │
└────────────┬───────────────────────┘                   │
             │                                           │
             ▼                                           │
┌────────────────────────────────────┐                   │
│  ML PREDICTION                     │                   │
│                                    │                   │
│  1. Load pre-trained model         │◄──── [Model PKL] │
│  2. Scale features                 │                   │
│  3. Predict Kd                     │                   │
│  4. Calculate confidence           │                   │
└────────────┬───────────────────────┘                   │
             │                                           │
             ▼                                           │
┌────────────────────────────────────┐                   │
│  OUTPUT GENERATION                 │                   │
│                                    │                   │
│  • Format results                  │                   │
│  • Save CSV                        │────► results.csv  │
│  • Save pose PDB                   │────► pose.pdb     │
│  • Display summary                 │                   │
└────────────┬───────────────────────┘                   │
             │                                           │
             ▼                                           │
           END                                           │
```

---

## Module Structure

```
bindigo/
│
├── __init__.py                 # Package exports
├── __version__.py              # Version info
│
├── cli/
│   ├── __init__.py
│   ├── main.py                 # CLI entry point
│   ├── predict.py              # Predict command
│   ├── screen.py               # Screen command (v1.1+)
│   ├── info.py                 # Info command
│   └── utils.py                # CLI helpers (progress bars, formatting)
│
├── core/
│   ├── __init__.py
│   ├── pipeline.py             # Main prediction pipeline
│   ├── predictor.py            # BindingPredictor class (Python API)
│   └── config.py               # Configuration defaults
│
├── preprocessing/
│   ├── __init__.py
│   ├── protein.py              # Protein preparation
│   ├── ligand.py               # Ligand preparation
│   └── binding_site.py         # Binding site detection
│
├── docking/
│   ├── __init__.py
│   ├── vina_wrapper.py         # AutoDock Vina interface
│   ├── pdbqt_converter.py      # PDBQT conversion
│   └── pose_extraction.py      # Extract and format poses
│
├── ml/
│   ├── __init__.py
│   ├── features.py             # Feature extraction
│   ├── models.py               # Model loading and prediction
│   └── confidence.py           # Confidence scoring
│
├── database/
│   ├── __init__.py
│   ├── pdb_fetcher.py          # Fetch from RCSB PDB
│   └── chembl_fetcher.py       # Fetch from ChEMBL (v1.1+)
│
├── visualization/
│   ├── __init__.py
│   ├── mol_viz.py              # 2D molecule rendering
│   └── complex_viz.py          # 3D complex visualization (v1.1+)
│
├── models/
│   ├── default_model.pkl       # Pre-trained ML model
│   ├── scaler.pkl              # Feature scaler
│   └── model_metadata.json     # Model info and training data
│
├── data/
│   ├── examples/               # Example inputs
│   │   ├── 1hsg_protein.pdb
│   │   └── ligands.sdf
│   └── test_cases/             # Test data for validation
│
└── utils/
    ├── __init__.py
    ├── io.py                   # File I/O utilities
    ├── validation.py           # Input validation
    ├── logging.py              # Logging configuration
    └── exceptions.py           # Custom exceptions
```

---

## Data Flow Diagram

```
INPUT                        PROCESSING                      OUTPUT
─────                        ──────────                      ──────

                        ┌─────────────────────┐
Protein PDB     ───────►│  Protein Prep       │
(1HSG or file)          │  • Fetch/Load       │
                        │  • Clean            │
                        │  • Add H            │
                        └──────────┬──────────┘
                                   │
                                   │ protein_prepared.pdb
                                   │
Ligand SMILES   ───────►┌──────────▼──────────┐
(or SDF)                │  Ligand Prep        │
                        │  • Parse            │
                        │  • Generate 3D      │
                        │  • Add H, charges   │
                        └──────────┬──────────┘
                                   │
                                   │ ligand_prepared.mol2
                                   │
Binding Site    ───────►┌──────────▼──────────┐
(auto/manual)           │  Site Detection     │
                        │  • Find pocket      │
                        │  • Set grid         │
                        └──────────┬──────────┘
                                   │
                                   │ grid_config.txt
                                   │
                        ┌──────────▼──────────┐
                        │  AutoDock Vina      │
                        │  • Docking          │
                        │  • Scoring          │
                        └──────────┬──────────┘
                                   │
                                   │ docking_result.pdbqt
                                   │
                        ┌──────────▼──────────┐
                        │  Feature Extract    │
                        │  • Docking score    │
                        │  • Mol descriptors  │
                        │  • Properties       │
                        └──────────┬──────────┘
                                   │
                                   │ feature_vector [8 dims]
                                   │
Pre-trained     ───────►┌──────────▼──────────┐
Model (PKL)             │  ML Prediction      │
                        │  • Load model       │
                        │  • Predict Kd       │
                        │  • Confidence       │
                        └──────────┬──────────┘
                                   │
                                   │ predicted_kd, confidence
                                   │
                        ┌──────────▼──────────┐
                        │  Format Results     │       results.csv ─────►
                        │  • Create CSV       │
                        │  • Save pose        │       pose.pdb ────────►
                        │  • Display summary  │
                        └─────────────────────┘       terminal output ─►
```

---

## Progress Indicator Design

```
Standard Progress Bar:
⣷ Docking in progress... [████████████        ] 60% (ETA: 45s)

Spinner States (animated):
⣾ Loading...
⣽ Loading...
⣻ Loading...
⢿ Loading...
⡿ Loading...
⣟ Loading...
⣯ Loading...
⣷ Loading...

Success/Error Symbols:
✓ Success
✗ Error
⚠ Warning
ℹ Info

Stage Completion:
[1/5] Loading inputs...          ✓
[2/5] Preparing protein...       ✓
[3/5] Preparing ligand...        ✓
[4/5] Running docking...         ⣷ (in progress)
[5/5] ML prediction...           (pending)
```

---

## Color Coding (Terminal with ANSI)

```
Success:    Green   ✓
Error:      Red     ✗
Warning:    Yellow  ⚠
Info:       Blue    ℹ
Progress:   Cyan    ⣷
Headers:    Bold
Values:     White
Paths:      Underline
```

---

## Configuration File Support (v1.2+)

### `.bindigo.yaml` (optional)

```yaml
# Default settings for Bindigo
version: 0.1.0

# Docking parameters
docking:
  exhaustiveness: 8
  num_modes: 9
  energy_range: 3

# Binding site detection
binding_site:
  auto_detect: true
  default_size: 20.0

# ML model
model:
  name: "default"
  confidence_threshold:
    high: 0.8
    medium: 0.5

# Output
output:
  save_poses: true
  format: "csv"
  verbose: false

# Database
database:
  pdb_mirror: "https://files.rcsb.org/download/"
  cache_dir: "~/.bindigo/cache"
```

---

## User Journey Map

```
┌─────────────────────────────────────────────────────────────────┐
│  FIRST-TIME USER JOURNEY                                        │
└─────────────────────────────────────────────────────────────────┘

Step 1: Installation
  $ pip install bindigo
  ✓ All dependencies installed automatically

Step 2: View help
  $ bindigo --help
  ✓ Clear examples shown

Step 3: First prediction (example from README)
  $ bindigo predict --protein 1HSG --ligand "CC(=O)Nc1ccc(O)cc1" --output results.csv
  ✓ Progress bars show what's happening
  ✓ Completes in ~2-3 minutes
  ✓ Results displayed in terminal

Step 4: Check results
  $ cat results.csv
  ✓ Human-readable format
  ✓ Predicted Kd value makes sense

Step 5: View pose
  $ pymol ligand_1_pose.pdb 1HSG.pdb
  ✓ Ligand docked in binding site

→ User is productive in <10 minutes


┌─────────────────────────────────────────────────────────────────┐
│  EXPERIENCED USER JOURNEY                                       │
└─────────────────────────────────────────────────────────────────┘

Goal: Screen 100 compounds against custom protein

Step 1: Prepare inputs
  - protein.pdb (from MD simulation)
  - compounds.sdf (from virtual library)

Step 2: Run virtual screening
  $ bindigo screen --protein protein.pdb --ligands compounds.sdf --output screen.csv --jobs 4
  ✓ Parallel processing (4 cores)
  ✓ Progress: [██████░░░░] 45/100 (ETA: 15m)

Step 3: Analyze results
  $ python
  >>> import pandas as pd
  >>> df = pd.read_csv("screen.csv")
  >>> df.sort_values("predicted_kd_nM").head(10)
  ✓ Top 10 predicted binders identified

Step 4: Validate hits
  - Export top poses
  - Visual inspection
  - Select for experimental testing

→ Efficient virtual screening workflow
```

---

## Design Principles Summary

1. **Zero Configuration**: Works out of the box with sensible defaults
2. **Progressive Disclosure**: Basic usage is simple, advanced features available when needed
3. **Clear Feedback**: Always show what's happening (progress, errors, warnings)
4. **Helpful Errors**: Every error includes suggestions for how to fix it
5. **Consistent Interface**: Same patterns in CLI and Python API
6. **Fast Feedback**: Show progress for long operations, instant for validation
7. **Professional Polish**: Clean formatting, proper terminology, citation info
8. **Beginner Friendly**: Examples everywhere, clear documentation, forgiving UX

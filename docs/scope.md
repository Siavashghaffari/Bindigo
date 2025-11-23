# Bindigo - Project Scope

## Overview

Bindigo is a Python package for protein-ligand binding affinity prediction that combines molecular docking with machine learning. It provides computational chemists with a streamlined tool for early-stage drug discovery, enabling rapid evaluation of compound libraries against protein targets.

**Target Audience**: Computational chemists, medicinal chemists, and drug discovery researchers conducting virtual screening and lead optimization.

**Installation**: `pip install bindigo`

---

## Core Functionality

### Primary Use Case
Users provide a protein structure and one or more ligands, and receive predicted binding affinities with corresponding docking poses.

**Input Options**:
- **Protein**: PDB file (local) OR PDB ID (fetched automatically)
- **Ligand(s)**: SMILES strings OR SDF file

**Output**:
- Predicted binding affinities (Kd/Ki values in nM or μM)
- Docking poses (3D coordinates)
- Confidence scores/uncertainty estimates
- Export formats: CSV, JSON
- Optional visualization: protein-ligand complex images

---

## Technical Approach

### Hybrid Prediction Pipeline

1. **Docking Component** (AutoDock Vina)
   - Generate initial binding poses
   - Calculate docking scores
   - Identify binding site geometry

2. **Machine Learning Component** (scikit-learn)
   - Pre-trained models shipped with package
   - Features derived from:
     - Docking scores
     - Molecular descriptors (RDKit)
     - Protein-ligand interaction fingerprints
     - Binding site properties
   - Output: Refined Kd/Ki predictions

### Automated Preprocessing

All preprocessing handled internally:
- **Protein preparation**: Add hydrogens, assign charges, remove water molecules, handle missing residues
- **Ligand preparation**: Convert SMILES to 3D structures, generate conformers, assign protonation states
- **Binding site detection**: Automatic pocket identification (if not specified by user)
- **Format conversions**: Handle various file formats transparently

---

## Interface Options

### 1. Command-Line Interface (CLI)

```bash
# Single prediction
bindigo predict --protein 1HSG --ligand "CC(=O)Nc1ccc(O)cc1" --output results.csv

# Virtual screening
bindigo screen --protein protein.pdb --ligands compounds.sdf --output screen_results.csv
```

### 2. Python API

```python
from bindigo import BindingPredictor

predictor = BindingPredictor()
results = predictor.predict(
    protein="1HSG",  # or path to PDB file
    ligands=["SMILES1", "SMILES2"],
    output_format="json"
)
```

---

## Feature Set

### Phase 1: Core Prediction Workflow (Initial Release)

**Essential Features**:
- Single protein-ligand affinity prediction
- Virtual screening mode (batch prediction for compound libraries)
- Automatic protein fetching from PDB database
- Automatic ligand structure generation from SMILES
- Binding site detection (automated or user-specified residues/coordinates)
- CSV/JSON export of results
- Basic visualization (2D ligand structures, optional 3D complex rendering)
- Pre-trained ML models included in package
- Progress indicators for long-running jobs
- Result caching for repeated predictions

**Validation & Quality Control**:
- Input validation (check protein/ligand file integrity)
- Warning system for low-confidence predictions
- Logging of all processing steps

**Database Integration**:
- Fetch protein structures from RCSB PDB
- Optional: Fetch compounds from ChEMBL by ID

**Performance Considerations**:
- Parallel processing for virtual screening
- Efficient caching of preprocessed structures
- Memory-efficient handling of large compound libraries

---

## Non-Goals (Out of Scope for Initial Release)

**Explicitly NOT included**:
- Web interface or GUI
- Custom ML model training by users (only pre-trained models)
- Quantum mechanics calculations
- Molecular dynamics simulations
- Protein-protein docking
- Covalent docking
- ADMET predictions
- Deployment as web service
- Real-time interactive visualization

**Future Considerations** (post v1.0):
- Support for additional docking engines (Glide, GOLD)
- User-trainable ML models
- GPU acceleration
- Cloud computing integration
- Additional molecular property predictions

---

## Technical Stack

### Core Dependencies

**Programming Language**: Python 3.9+

**Cheminformatics**:
- RDKit: Molecular descriptor calculation, 2D/3D structure generation, visualization
- OpenBabel: Additional format conversions (if needed)

**Structural Biology**:
- BioPython: PDB file parsing, protein structure handling
- ProDy: Protein dynamics and structural analysis (optional)

**Docking**:
- AutoDock Vina (via Python wrapper): Molecular docking engine
- meeko/oddt: Vina integration and interaction analysis

**Machine Learning**:
- scikit-learn: Pre-trained regression models, feature engineering
- joblib: Model serialization
- NumPy/Pandas: Data handling

**CLI & I/O**:
- Click: Command-line interface framework
- Typer: Alternative CLI framework (evaluate vs Click)
- matplotlib/seaborn: Visualization
- py3Dmol or PyMOL (optional): 3D molecular visualization

**Database Access**:
- requests/urllib: HTTP requests for PDB/ChEMBL APIs
- biopandas: Alternative PDB parsing

**Testing & Quality**:
- pytest: Testing framework
- hypothesis: Property-based testing
- tox: Multi-environment testing

---

## Input Specifications

### Protein Input

**Accepted Formats**:
- PDB ID (4-character code): Auto-fetched from RCSB PDB
- Local PDB file path
- Future: mmCIF, PDBx formats

**Optional Parameters**:
- Binding site specification (residue IDs, coordinates, or auto-detect)
- Chain selection (for multi-chain proteins)
- pH for protonation state assignment

### Ligand Input

**Accepted Formats**:
- SMILES string(s)
- SDF file (single or multi-molecule)
- MOL2 file
- Future: ChEMBL IDs, PubChem CIDs

**Optional Parameters**:
- Protonation state (auto-predicted at pH 7.4 by default)
- Stereochemistry specification
- Charge state

---

## Output Specifications

### Prediction Results

**Standard Fields**:
- Ligand identifier (SMILES, name, or ID)
- Predicted Kd/Ki (nM)
- Confidence score (0-1)
- Docking score (kcal/mol)
- Best pose RMSD (if reference available)
- Binding site residues involved
- Key interactions (H-bonds, hydrophobic, etc.)

**Export Formats**:
- CSV: Tabular results, easy for Excel/analysis
- JSON: Structured data with nested interactions
- SDF: Docked poses with affinity as properties

**Visualization Outputs** (optional):
- PNG/SVG: 2D ligand structures with highlights
- PDB file: Protein-ligand complex for external viewing
- Interactive HTML: Embedded 3D viewer (py3Dmol)

---

## Success Criteria

### Functional Requirements
- Successfully predict binding affinities for benchmark protein-ligand pairs
- Handle virtual screening of 1000+ compounds in reasonable time (<1 hour on standard laptop)
- Achieve correlation >0.7 with experimental binding data on validation set
- Zero-configuration setup: works immediately after `pip install bindigo`

### Usability Requirements
- Clear, minimal CLI with helpful error messages
- Comprehensive documentation with quickstart examples
- Python API follows standard conventions (sklearn-like interface)
- Runs on Windows, macOS, Linux without platform-specific issues

### Quality Requirements
- Pre-trained models included in package distribution
- Automated testing covers >80% of code
- All functions have docstrings
- Example datasets included for testing
- Graceful handling of malformed inputs

---

## Package Structure (Conceptual)

```
bindigo/
├── cli/              # Command-line interface
├── core/             # Core prediction pipeline
├── preprocessing/    # Protein/ligand preparation
├── docking/          # Vina wrapper and utilities
├── ml/               # ML models and feature extraction
├── database/         # PDB/ChEMBL fetchers
├── visualization/    # Result visualization
├── models/           # Pre-trained model files
├── data/             # Example datasets
└── utils/            # Helper functions
```

---

## Development Priorities

### Phase 1: MVP (Minimum Viable Product)
1. Basic protein-ligand docking workflow
2. Simple ML model integration (single pre-trained model)
3. CLI with essential commands
4. CSV output
5. PDB fetching

### Phase 2: Enhanced Functionality
1. Python API
2. Virtual screening optimization
3. Multiple ML models with ensemble predictions
4. JSON output and visualization
5. ChEMBL integration

### Phase 3: Polish & Validation
1. Comprehensive testing
2. Benchmark validation
3. Documentation and tutorials
4. Performance optimization
5. Package distribution on PyPI

---

## Constraints & Assumptions

**Assumptions**:
- Users have basic Python knowledge for API usage
- AutoDock Vina is installable on target platforms
- Internet connection available for PDB/database fetching (optional feature)
- Small molecule ligands only (MW < 1000 Da typically)

**Technical Constraints**:
- Docking accuracy limited by AutoDock Vina's force field
- ML predictions require feature compatibility with training data
- Memory usage scales with compound library size
- Single-machine execution (no distributed computing in v1.0)

**Licensing Considerations**:
- Open-source license (MIT or Apache 2.0)
- Ensure all dependencies have compatible licenses
- Pre-trained models distributed with appropriate attribution

---

## Risk Assessment

**Potential Challenges**:
1. **AutoDock Vina installation**: May require compilation on some platforms
   - Mitigation: Provide conda package, pre-compiled binaries

2. **ML model generalization**: May not perform well on novel protein families
   - Mitigation: Confidence scoring, uncertainty estimates

3. **Performance**: Virtual screening may be slow for large libraries
   - Mitigation: Parallel processing, progress indicators, caching

4. **Dependency conflicts**: Scientific packages often have version conflicts
   - Mitigation: Strict dependency version pinning, conda environment

---

## Deliverables

1. **Python Package**: Installable via pip, includes all dependencies
2. **Pre-trained Models**: Bundled with package or auto-downloaded
3. **Documentation**:
   - Installation guide
   - Quickstart tutorial
   - API reference
   - CLI command reference
   - Example workflows
4. **Test Suite**: Automated tests with example data
5. **Benchmark Results**: Validation on public datasets

---

## Timeline Guidance

**Not prescriptive, but conceptual phases**:
- Foundation: Core pipeline, docking integration, basic preprocessing
- Enhancement: ML models, database integration, virtual screening
- Refinement: Visualization, API design, optimization
- Validation: Testing, benchmarking, documentation
- Release: PyPI publication, community feedback

**Success Metric**: Package is ready when a computational chemist can install it and get meaningful predictions on their own data within 10 minutes of first use.

# Bindigo - Minimum Viable Product (MVP)

## MVP Goal

Create a working, installable Python package that performs protein-ligand binding affinity prediction using docking + ML. A computational chemist should be able to install it and get their first prediction result within 10 minutes.

**Success Criteria**: `pip install bindigo` → run prediction → get Kd/Ki value + docking pose

---

## Core MVP Features (Must Have)

### 1. Single Prediction Workflow

**Input**:
- Protein: Local PDB file OR PDB ID (auto-fetch from RCSB)
- Ligand: Single SMILES string OR single-molecule SDF file
- Binding site: Auto-detect (largest pocket) OR user-specified center coordinates

**Output**:
- Predicted binding affinity (Kd in nM)
- Docking score (kcal/mol)
- Best docking pose (saved as PDB file)
- Simple CSV with results

**Command**:
```bash
bindigo predict --protein 1HSG --ligand "CC(=O)Nc1ccc(O)cc1" --output results.csv
bindigo predict --protein protein.pdb --ligand ligand.sdf --output results.csv
```

### 2. Automated Preprocessing

**Protein Preparation** (fully automatic):
- Add hydrogens
- Remove water molecules
- Handle first model if NMR structure
- Basic validation (check for atoms, chains)

**Ligand Preparation** (fully automatic):
- SMILES → 3D structure generation (RDKit)
- Add hydrogens
- Generate single low-energy conformer
- Assign Gasteiger charges

**Binding Site Detection**:
- Auto-detect largest pocket using simple geometric algorithm
- OR accept user coordinates (`--center X Y Z --size 20`)

### 3. Docking Engine

- AutoDock Vina integration via Python wrapper
- Single docking run per ligand
- Exhaustiveness = 8 (default, good balance)
- Return top pose only for MVP

### 4. Machine Learning Prediction

**Pre-trained Model**:
- Single scikit-learn model (Random Forest or Gradient Boosting)
- Trained on public dataset (e.g., PDBbind refined set)
- Model file bundled with package installation

**Features** (simple set):
- Vina docking score
- Molecular weight
- LogP
- Number of H-bond donors/acceptors
- Number of rotatable bonds
- Topological polar surface area (TPSA)
- Number of aromatic rings
- Vina-specific: Number of active torsions

**Output**:
- Predicted Kd (nM) - regression output
- Confidence: "High/Medium/Low" based on applicability domain

### 5. Command-Line Interface

**Essential Commands**:

```bash
# Single prediction
bindigo predict --protein <PDB_ID|PDB_FILE> --ligand <SMILES|SDF_FILE> --output <CSV_FILE>

# With custom binding site
bindigo predict --protein 1HSG --ligand "CCO" --center 10.5 20.3 15.2 --size 20 --output results.csv

# Help
bindigo --help
bindigo predict --help

# Version
bindigo --version
```

**Required Flags**:
- `--protein`: PDB ID or file path
- `--ligand`: SMILES string or SDF file path
- `--output`: Output CSV file path

**Optional Flags**:
- `--center X Y Z`: Binding site center coordinates (Angstroms)
- `--size N`: Binding site box size (Angstroms, default=20)
- `--save-pose`: Save docking pose PDB file (default=True)
- `--verbose`: Show detailed progress

### 6. Output Format

**CSV File** (primary output):
```csv
ligand_id,smiles,predicted_kd_nM,confidence,docking_score_kcal_mol,pose_file
ligand_1,CC(=O)Nc1ccc(O)cc1,125.3,High,-8.2,ligand_1_pose.pdb
```

**Files Created**:
- `results.csv`: Prediction results
- `<ligand_id>_pose.pdb`: Docked ligand pose (if `--save-pose`)

### 7. Error Handling

**Must Handle**:
- Invalid PDB ID → clear error message
- Invalid SMILES → clear error + suggestion
- Missing protein file → clear error
- Vina execution failure → clear error with logs
- No binding site found → clear error with suggestion

**Error Message Format**:
```
Error: Could not fetch PDB ID '1XYZ' from RCSB PDB.
Suggestion: Check the PDB ID or provide a local PDB file with --protein protein.pdb
```

### 8. Installation & Dependencies

**Installation**:
```bash
pip install bindigo
```

**Core Dependencies** (minimal set):
- Python >= 3.9
- RDKit >= 2022.09
- BioPython >= 1.79
- numpy >= 1.21
- pandas >= 1.3
- scikit-learn >= 1.0
- click >= 8.0
- vina (Python wrapper for AutoDock Vina)
- requests (for PDB fetching)

**Pre-trained Model**:
- Bundled in `bindigo/models/default_model.pkl`
- Auto-loaded on first prediction

### 9. Documentation

**Must Include**:

1. **README.md**:
   - Installation instructions
   - Quickstart example (1HSG + aspirin)
   - Basic usage
   - Link to full docs

2. **Quickstart Guide**:
   - Installation
   - First prediction example
   - Interpreting results
   - Common issues

3. **API Reference** (minimal):
   - CLI command reference
   - Input/output specifications
   - Error codes

### 10. Testing

**Essential Tests**:
- Unit tests for core functions (preprocessing, feature extraction)
- Integration test: Full prediction pipeline with example data
- Test data included: 1 protein PDB, 3 ligands SMILES
- All tests pass on Linux, macOS, Windows

**Test Command**:
```bash
pytest tests/
```

---

## Explicitly OUT of Scope for MVP

### Not in v1.0:

❌ **Python API** - CLI only for MVP
❌ **Virtual screening mode** - Single predictions only
❌ **Multiple ML models** - One pre-trained model
❌ **Ensemble predictions** - Single model output
❌ **ChEMBL integration** - PDB only
❌ **Advanced visualizations** - No 3D viewers, no plots
❌ **JSON output** - CSV only
❌ **Batch processing** - One ligand at a time
❌ **Parallel processing** - Sequential execution
❌ **Result caching** - No caching
❌ **Custom model training** - Pre-trained only
❌ **Interaction fingerprints** - Not in output
❌ **Multiple binding sites** - Single site only
❌ **Flexible residues** - Rigid protein
❌ **GPU acceleration** - CPU only

**Rationale**: Get core prediction working first, validate approach, gather user feedback, then expand.

---

## MVP Development Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Project structure and setup
- [ ] Package configuration (setup.py, pyproject.toml)
- [ ] Core CLI skeleton (Click)
- [ ] Basic logging and error handling

### Phase 2: Preprocessing (Week 2-3)
- [ ] PDB fetcher (download from RCSB)
- [ ] Protein preparation pipeline (BioPython + RDKit)
- [ ] SMILES to 3D converter (RDKit)
- [ ] Ligand preparation pipeline
- [ ] Binding site detection (geometric method)

### Phase 3: Docking Integration (Week 3-4)
- [ ] AutoDock Vina wrapper
- [ ] Input file generation (PDBQT conversion)
- [ ] Docking execution and output parsing
- [ ] Pose extraction

### Phase 4: ML Model (Week 4-5)
- [ ] Feature extraction pipeline
- [ ] Train initial model on PDBbind dataset
- [ ] Model serialization and bundling
- [ ] Prediction pipeline integration
- [ ] Confidence scoring

### Phase 5: Integration & Testing (Week 5-6)
- [ ] End-to-end pipeline integration
- [ ] Comprehensive error handling
- [ ] Unit and integration tests
- [ ] Test on diverse protein-ligand pairs
- [ ] Performance optimization

### Phase 6: Documentation & Release (Week 6-7)
- [ ] README with examples
- [ ] Quickstart tutorial
- [ ] CLI reference docs
- [ ] Example data preparation
- [ ] PyPI package preparation
- [ ] Test installation on clean environments

---

## MVP Deliverables Checklist

### Functionality
- ✓ Single protein-ligand prediction works end-to-end
- ✓ PDB fetching works (tested with 5+ different PDB IDs)
- ✓ SMILES input works (tested with 10+ diverse compounds)
- ✓ Automatic preprocessing completes without errors
- ✓ Docking produces reasonable poses
- ✓ ML prediction produces Kd values in reasonable range (pM-mM)
- ✓ Output CSV is well-formatted and human-readable

### Usability
- ✓ Install works: `pip install bindigo` (test on 3 platforms)
- ✓ First prediction completes in <5 minutes
- ✓ Error messages are clear and actionable
- ✓ Help text is comprehensive (`--help`)
- ✓ Example in README works copy-paste

### Quality
- ✓ All tests pass (`pytest`)
- ✓ No critical bugs in issue tracker
- ✓ Works offline (after model download)
- ✓ Memory usage <2GB for typical prediction
- ✓ Code follows PEP 8 style guide

### Documentation
- ✓ README with installation and quickstart
- ✓ At least 3 working examples
- ✓ Troubleshooting section for common errors
- ✓ Clear explanation of output fields
- ✓ Citation information for underlying tools

---

## MVP Validation Test

**Standard Test Case**: Reproduce known binding affinity

**Example**: HIV-1 Protease (1HSG) + Indinavir

```bash
bindigo predict \
  --protein 1HSG \
  --ligand "CC(C)(C)NC(=O)[C@@H]1CN(Cc2cccnc2)CCN1C[C@@H](O)[C@H](Cc1ccccc1)NC(=O)[C@H](CC(N)=O)NC(=O)c1ccc2ccccc2n1" \
  --output 1hsg_indinavir.csv
```

**Expected**:
- Prediction completes in <3 minutes
- Predicted Kd within 1-2 orders of magnitude of experimental (5 nM)
- Docking pose RMSD <2Å from crystal structure ligand
- No errors or warnings

**Success**: If this works reliably, MVP is ready for release.

---

## Post-MVP Roadmap (v1.1+)

After MVP validation, prioritize based on user feedback:

**High Priority** (v1.1):
- Python API
- Batch prediction mode (multi-ligand SDF)
- JSON output format
- Basic 2D visualization

**Medium Priority** (v1.2):
- Virtual screening optimization (parallel processing)
- Multiple ML models with ensemble
- ChEMBL integration
- Interaction analysis in output

**Low Priority** (v1.3+):
- Advanced visualizations
- Custom model training
- Alternative docking engines
- GPU acceleration

---

## Technical Constraints & Assumptions

**Assumptions**:
- Users have conda or pip working
- AutoDock Vina is installable via pip (or conda fallback)
- Internet connection for initial PDB fetch (optional after cache)
- Ligands are small molecules (MW <1000 Da, <50 rotatable bonds)
- Proteins are single-chain or user knows which chain (use chain A default)

**Performance Targets**:
- Prediction time: <3 minutes per ligand on laptop (2.5 GHz, 8GB RAM)
- Package size: <50 MB (including model)
- Memory usage: <2 GB peak

**Known Limitations** (document clearly):
- Accuracy depends on binding site quality
- May not generalize to very novel scaffolds
- No metal coordination handling
- No covalent docking
- Rigid protein assumption

---

## MVP Launch Criteria

**Ready to Release When**:
1. ✅ All MVP features working
2. ✅ Test suite passes on CI (Linux, macOS, Windows)
3. ✅ Successfully tested by 2+ beta users
4. ✅ Documentation complete
5. ✅ Validated on 10+ diverse protein-ligand pairs
6. ✅ Performance meets targets
7. ✅ PyPI package builds successfully
8. ✅ No critical or high-severity bugs

**Release Checklist**:
- [ ] Version number: 0.1.0
- [ ] GitHub repo public with README
- [ ] PyPI package published
- [ ] Conda package (optional but recommended)
- [ ] Announcement (Twitter, Reddit r/Cheminformatics)
- [ ] Feedback mechanism (GitHub Issues)

---

## Success Metrics (3 months post-launch)

**Adoption**:
- 100+ PyPI downloads
- 5+ GitHub stars
- 3+ community issues/questions

**Quality**:
- <5 critical bugs reported
- Average prediction accuracy within 1 log unit of experimental

**Engagement**:
- 1+ external contributor
- 10+ citations or mentions in projects

---

## MVP Philosophy

**Keep It Simple**:
- One way to do each task
- Sensible defaults (users shouldn't need to tune parameters)
- Fail fast with clear errors
- Progressive disclosure (basic → advanced features over versions)

**Make It Work, Then Make It Better**:
- v0.1: Core prediction works reliably
- v0.2+: Add features based on real usage
- v1.0: Production-ready with comprehensive testing

**User-Centric**:
- Optimize for first-time user experience
- Documentation as important as code
- Listen to feedback, iterate quickly

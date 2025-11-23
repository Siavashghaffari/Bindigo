# Pre-trained Models

This directory will contain pre-trained machine learning models for binding affinity prediction.

## Models

### default_model.pkl (Coming in Phase 4)
- **Algorithm**: Random Forest or Gradient Boosting
- **Training Data**: PDBbind refined set
- **Features**: 8 molecular descriptors
  - Docking score
  - Molecular weight
  - LogP
  - H-bond donors/acceptors
  - Rotatable bonds
  - TPSA
  - Aromatic rings
  - Active torsions

### scaler.pkl
- Feature scaler for input normalization
- Required for consistent predictions

### model_metadata.json
- Model information
- Training set details
- Performance metrics
- Feature names and descriptions

## Notes

Models will be trained and added during Phase 4: ML Model development.
The models will be bundled with the package for distribution.

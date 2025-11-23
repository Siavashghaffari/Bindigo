# Python API Guide (v1.1+)

This guide shows how to use Bindigo's Python API for integration into your own scripts and workflows.

> **Note**: Python API is planned for v1.1+. Current v0.1.0 provides CLI only.

## Basic Usage

### Simple Prediction

```python
from bindigo import BindingPredictor

# Initialize predictor
predictor = BindingPredictor()

# Run prediction
result = predictor.predict(
    protein="1HSG",                    # PDB ID
    ligand="CC(=O)Nc1ccc(O)cc1"       # SMILES string
)

# Access results
print(f"Predicted Kd: {result.kd_nM:.1f} nM")
print(f"Confidence: {result.confidence}")
print(f"Docking Score: {result.docking_score:.2f} kcal/mol")
```

### Using Local Files

```python
from bindigo import BindingPredictor

predictor = BindingPredictor()

result = predictor.predict(
    protein="./data/protein.pdb",
    ligand="./data/ligand.sdf"
)

print(result)
```

## Advanced Usage

### Custom Binding Site

```python
from bindigo import BindingPredictor
from bindigo.utils import BindingSite

# Define binding site
site = BindingSite(
    center=(10.5, 20.3, 15.2),  # X, Y, Z coordinates
    size=25.0                    # Box size in Angstroms
)

# Predict with custom site
predictor = BindingPredictor()
result = predictor.predict(
    protein="1HSG",
    ligand="CCO",
    binding_site=site
)
```

### Configuration Options

```python
from bindigo import BindingPredictor

# Initialize with custom settings
predictor = BindingPredictor(
    model="default",           # ML model to use
    exhaustiveness=8,          # Vina exhaustiveness
    num_modes=9,              # Number of docking modes
    verbose=True              # Show progress
)

result = predictor.predict(
    protein="1HSG",
    ligand="CC(=O)Oc1ccccc1C(=O)O",
    save_pose=True,
    output_dir="./results"
)
```

## Batch Processing

### Multiple Ligands, Single Protein

```python
from bindigo import BindingPredictor

predictor = BindingPredictor()

# List of SMILES
ligands = [
    "CC(=O)Nc1ccc(O)cc1",      # Acetaminophen
    "CC(=O)Oc1ccccc1C(=O)O",   # Aspirin
    "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",  # Caffeine
]

# Batch prediction
results = predictor.predict_batch(
    protein="1HSG",
    ligands=ligands,
    n_jobs=4  # Parallel processing
)

# Process results
for result in results:
    print(f"{result.ligand_id}: Kd = {result.kd_nM:.1f} nM")
```

### Virtual Screening

```python
from bindigo import BindingPredictor
import pandas as pd

predictor = BindingPredictor()

# Load compound library
compounds = pd.read_csv("compound_library.csv")
smiles_list = compounds["smiles"].tolist()

# Screen all compounds
results = predictor.predict_batch(
    protein="my_target.pdb",
    ligands=smiles_list,
    n_jobs=8,  # Use 8 CPU cores
    verbose=True
)

# Convert to DataFrame
df = pd.DataFrame([r.to_dict() for r in results])

# Sort by predicted affinity
df_sorted = df.sort_values("predicted_kd_nM")

# Save top hits
df_sorted.head(100).to_csv("top_100_hits.csv", index=False)

print(f"Screened {len(results)} compounds")
print(f"Top hit: {df_sorted.iloc[0]['smiles']} (Kd = {df_sorted.iloc[0]['predicted_kd_nM']:.1f} nM)")
```

## Working with Results

### Result Object

```python
from bindigo import BindingPredictor

predictor = BindingPredictor()
result = predictor.predict(protein="1HSG", ligand="CCO")

# Access attributes
print(f"Ligand ID: {result.ligand_id}")
print(f"SMILES: {result.smiles}")
print(f"Kd (nM): {result.kd_nM}")
print(f"pKd: {result.pKd}")
print(f"Confidence: {result.confidence}")
print(f"Docking Score: {result.docking_score} kcal/mol")
print(f"Pose file: {result.pose_path}")

# Molecular properties
print(f"MW: {result.molecular_weight}")
print(f"LogP: {result.logp}")
print(f"H-bond donors: {result.hbd}")
print(f"H-bond acceptors: {result.hba}")
```

### Converting to Dictionary

```python
result = predictor.predict(protein="1HSG", ligand="CCO")

# Convert to dict
result_dict = result.to_dict()
print(result_dict)

# Save to JSON
import json
with open("result.json", "w") as f:
    json.dump(result_dict, f, indent=2)
```

### Converting to DataFrame

```python
import pandas as pd

results = predictor.predict_batch(
    protein="1HSG",
    ligands=["CCO", "CC(=O)O", "c1ccccc1"]
)

# Convert to DataFrame
df = pd.DataFrame([r.to_dict() for r in results])

# Save to CSV
df.to_csv("predictions.csv", index=False)

# Analyze
print(df.describe())
```

## Integration Examples

### With RDKit

```python
from bindigo import BindingPredictor
from rdkit import Chem
from rdkit.Chem import Descriptors

predictor = BindingPredictor()

# Generate SMILES from molecule
mol = Chem.MolFromSmiles("CC(=O)Nc1ccc(O)cc1")
smiles = Chem.MolToSmiles(mol)

# Predict
result = predictor.predict(protein="1HSG", ligand=smiles)

# Calculate additional properties
mw = Descriptors.MolWt(mol)
logp = Descriptors.MolLogP(mol)

print(f"MW: {mw:.2f}, LogP: {logp:.2f}")
print(f"Predicted Kd: {result.kd_nM:.1f} nM")
```

### With Pandas

```python
import pandas as pd
from bindigo import BindingPredictor

# Load compound library
df = pd.read_csv("compounds.csv")

predictor = BindingPredictor()

# Predict for each compound
predictions = []
for idx, row in df.iterrows():
    result = predictor.predict(
        protein=row["target_pdb"],
        ligand=row["smiles"]
    )
    predictions.append({
        "compound_id": row["id"],
        "name": row["name"],
        "predicted_kd": result.kd_nM,
        "confidence": result.confidence
    })

# Create results DataFrame
results_df = pd.DataFrame(predictions)

# Merge with original data
final_df = df.merge(results_df, left_on="id", right_on="compound_id")

# Export
final_df.to_csv("predictions_with_metadata.csv", index=False)
```

### Pipeline Integration

```python
from bindigo import BindingPredictor

class DrugDiscoveryPipeline:
    def __init__(self):
        self.predictor = BindingPredictor()

    def screen_library(self, target_pdb, compound_smiles_list):
        """Screen compound library against target."""
        results = self.predictor.predict_batch(
            protein=target_pdb,
            ligands=compound_smiles_list,
            n_jobs=8
        )
        return results

    def filter_hits(self, results, kd_threshold=100):
        """Filter results by Kd threshold."""
        hits = [r for r in results if r.kd_nM < kd_threshold]
        return sorted(hits, key=lambda x: x.kd_nM)

    def run(self, target, compounds):
        """Run complete pipeline."""
        print(f"Screening {len(compounds)} compounds...")
        results = self.screen_library(target, compounds)

        hits = self.filter_hits(results)
        print(f"Found {len(hits)} hits (Kd < 100 nM)")

        return hits

# Usage
pipeline = DrugDiscoveryPipeline()
hits = pipeline.run("1HSG", ["CCO", "CC(=O)O", "c1ccccc1"])
```

## Error Handling

```python
from bindigo import BindingPredictor
from bindigo.utils.exceptions import BindigoError, InputError, DockingError

predictor = BindingPredictor()

try:
    result = predictor.predict(
        protein="INVALID",
        ligand="CCO"
    )
except InputError as e:
    print(f"Input error: {e}")
except DockingError as e:
    print(f"Docking failed: {e}")
except BindigoError as e:
    print(f"Bindigo error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Configuration

### Using Config File

Create `.bindigo.yaml`:

```yaml
docking:
  exhaustiveness: 16
  num_modes: 20

model:
  name: "default"
  confidence_threshold:
    high: 0.85
    medium: 0.6

output:
  save_poses: true
  format: "csv"
```

Load in Python:

```python
from bindigo import BindingPredictor
from bindigo.core.config import Config

# Update config
Config.update(
    docking_exhaustiveness=16,
    docking_num_modes=20
)

predictor = BindingPredictor()
# Now uses updated settings
```

## Visualization (v1.2+)

```python
from bindigo import BindingPredictor

predictor = BindingPredictor()
result = predictor.predict(protein="1HSG", ligand="CCO")

# Generate 2D visualization
result.visualize_2d("ligand_2d.png")

# Generate 3D visualization
result.visualize_3d("complex_3d.png")

# Interactive viewer
result.view_interactive()  # Opens in browser
```

## Performance Tips

1. **Use batch processing** for multiple predictions
2. **Parallelize** with `n_jobs` parameter
3. **Cache** preprocessed structures
4. **Reduce exhaustiveness** for faster (less accurate) results

```python
# Fast screening (less accurate)
predictor = BindingPredictor(exhaustiveness=4)

# Accurate prediction (slower)
predictor = BindingPredictor(exhaustiveness=16)
```

## Next Steps

- See `03_cli_reference.md` for CLI documentation
- See `04_advanced_usage.md` for advanced features
- See API reference at https://bindigo.readthedocs.io/api

---

**Note**: This API is planned for v1.1+. Current v0.1.0 provides CLI interface only.

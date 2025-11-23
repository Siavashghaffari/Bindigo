#!/bin/bash
# Bindigo CLI Workflow Example
#
# This script demonstrates a complete workflow using Bindigo's CLI.
# It tests several common drugs against HIV-1 Protease (1HSG).

set -e  # Exit on error

echo "=========================================="
echo "  Bindigo CLI Workflow Example"
echo "=========================================="
echo ""

# Check if bindigo is installed
if ! command -v bindigo &> /dev/null; then
    echo "Error: bindigo not found. Please install:"
    echo "  pip install bindigo"
    exit 1
fi

# Show version
echo "[1/6] Checking Bindigo version..."
bindigo --version
echo ""

# Create output directory
OUTPUT_DIR="./bindigo_example_results"
echo "[2/6] Creating output directory: $OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"
echo ""

# Example 1: Acetaminophen (Tylenol)
echo "[3/6] Example 1: Acetaminophen vs HIV-1 Protease"
echo "  SMILES: CC(=O)Nc1ccc(O)cc1"
bindigo predict \
  --protein 1HSG \
  --ligand "CC(=O)Nc1ccc(O)cc1" \
  --output acetaminophen.csv

echo "  ✓ Results saved to acetaminophen.csv"
echo ""

# Example 2: Aspirin
echo "[4/6] Example 2: Aspirin vs HIV-1 Protease"
echo "  SMILES: CC(=O)Oc1ccccc1C(=O)O"
bindigo predict \
  --protein 1HSG \
  --ligand "CC(=O)Oc1ccccc1C(=O)O" \
  --output aspirin.csv

echo "  ✓ Results saved to aspirin.csv"
echo ""

# Example 3: Caffeine
echo "[5/6] Example 3: Caffeine vs HIV-1 Protease"
echo "  SMILES: CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
bindigo predict \
  --protein 1HSG \
  --ligand "CN1C=NC2=C1C(=O)N(C(=O)N2C)C" \
  --output caffeine.csv

echo "  ✓ Results saved to caffeine.csv"
echo ""

# Example 4: Custom binding site
echo "[6/6] Example 4: Ethanol with custom binding site"
echo "  Using active site coordinates"
bindigo predict \
  --protein 1HSG \
  --ligand "CCO" \
  --center 10.5 20.3 15.2 \
  --size 25 \
  --output ethanol_custom_site.csv \
  --verbose

echo "  ✓ Results saved to ethanol_custom_site.csv"
echo ""

# Display summary
echo "=========================================="
echo "  Results Summary"
echo "=========================================="
echo ""
echo "Files created in: $OUTPUT_DIR"
ls -lh *.csv

echo ""
echo "View results:"
echo "  cat acetaminophen.csv"
echo "  cat aspirin.csv"
echo "  cat caffeine.csv"
echo ""

echo "✓ Workflow completed successfully!"
echo ""
echo "Next steps:"
echo "  1. Examine CSV files"
echo "  2. View docked poses with PyMOL or Chimera"
echo "  3. Analyze binding affinities"

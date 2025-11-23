#!/usr/bin/env python
"""
Basic Bindigo prediction example (Python API - v1.1+).

This example shows how to use Bindigo's Python API for binding affinity prediction.

Note: This requires v1.1+ with Python API implemented.
For v0.1.0, use the CLI instead:
    bindigo predict --protein 1HSG --ligand "CCO" --output results.csv
"""

def main():
    """Run basic prediction example."""
    print("=" * 60)
    print("  Bindigo Basic Prediction Example")
    print("=" * 60)
    print()

    # This is example code for when Python API is implemented (v1.1+)
    # Currently (v0.1.0), use CLI instead

    try:
        from bindigo import BindingPredictor

        # Initialize predictor
        print("[1/4] Initializing predictor...")
        predictor = BindingPredictor(verbose=True)

        # Define inputs
        protein = "1HSG"  # HIV-1 Protease
        ligand = "CC(=O)Nc1ccc(O)cc1"  # Acetaminophen

        print(f"[2/4] Setting up prediction...")
        print(f"  Protein: {protein}")
        print(f"  Ligand: {ligand}")
        print()

        # Run prediction
        print("[3/4] Running prediction...")
        result = predictor.predict(
            protein=protein,
            ligand=ligand
        )

        # Display results
        print()
        print("[4/4] Results:")
        print("-" * 60)
        print(f"  Predicted Kd:     {result.kd_nM:.2f} nM")
        print(f"  Predicted pKd:    {result.pKd:.2f}")
        print(f"  Confidence:       {result.confidence}")
        print(f"  Docking Score:    {result.docking_score:.2f} kcal/mol")
        print(f"  Molecular Weight: {result.molecular_weight:.2f} Da")
        print(f"  LogP:             {result.logp:.2f}")
        print("-" * 60)
        print()

        # Save results
        result.save("example_result.json")
        print("✓ Results saved to example_result.json")

    except ImportError:
        print("⚠ Python API not yet available (requires v1.1+)")
        print()
        print("Current version (v0.1.0) provides CLI interface.")
        print("Use the CLI instead:")
        print()
        print('  bindigo predict \\')
        print('    --protein 1HSG \\')
        print('    --ligand "CC(=O)Nc1ccc(O)cc1" \\')
        print('    --output results.csv')
        print()


if __name__ == "__main__":
    main()

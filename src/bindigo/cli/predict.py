"""
Predict command for Bindigo CLI.

Handles single protein-ligand binding affinity predictions.
"""

import click
from pathlib import Path

from bindigo.cli.utils import print_header, print_error, print_success


@click.command()
@click.option(
    "--protein",
    required=True,
    type=str,
    help="PDB ID (e.g., '1HSG') or file path (e.g., './protein.pdb')",
)
@click.option(
    "--ligand",
    required=True,
    type=str,
    help="SMILES string (e.g., 'CCO') or SDF file path (e.g., './ligand.sdf')",
)
@click.option(
    "--output",
    required=True,
    type=click.Path(),
    help="Output CSV file path (e.g., 'results.csv')",
)
@click.option(
    "--center",
    type=float,
    nargs=3,
    metavar="X Y Z",
    help="Binding site center coordinates (X Y Z in Angstroms). "
    "If not specified, the largest pocket will be detected automatically.",
)
@click.option(
    "--size",
    type=float,
    default=20.0,
    show_default=True,
    help="Binding site box size in Angstroms. "
    "Larger values cover more space but increase computation time.",
)
@click.option(
    "--save-pose/--no-save-pose",
    default=True,
    show_default=True,
    help="Save docked ligand pose as PDB file",
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Show detailed progress and intermediate results",
)
def predict(protein, ligand, output, center, size, save_pose, verbose):
    """
    Predict protein-ligand binding affinity using docking + ML.

    This command performs molecular docking with AutoDock Vina and predicts
    binding affinity (Kd) using a pre-trained machine learning model.

    \b
    Input Formats:
      Protein:  PDB file, PDB ID (auto-fetched from RCSB)
      Ligand:   SMILES string, SDF file, MOL2 file

    \b
    Output Files:
      <output>.csv          Prediction results (Kd, scores, metadata)
      <ligand>_pose.pdb     Docked ligand structure (if --save-pose)

    \b
    Examples:
      # Fetch protein from PDB, use SMILES
      $ bindigo predict --protein 1HSG --ligand "CC(=O)Nc1ccc(O)cc1" --output results.csv

      # Local files with custom binding site
      $ bindigo predict --protein protein.pdb --ligand ligand.sdf --center 10 20 15 --output results.csv

      # Verbose output for debugging
      $ bindigo predict --protein 1HSG --ligand "CCO" --output test.csv --verbose
    """
    try:
        # Print header
        print_header(verbose=verbose)

        # Import here to avoid slow startup
        from bindigo.core.pipeline import run_prediction

        # Run prediction pipeline
        result = run_prediction(
            protein=protein,
            ligand=ligand,
            output=output,
            center=center,
            box_size=size,
            save_pose=save_pose,
            verbose=verbose,
        )

        # Print success message
        print_success(f"Results saved to: {output}")
        if save_pose and result.get("pose_file"):
            print_success(f"Docking pose saved to: {result['pose_file']}")

        click.echo(f"\n✓ Prediction completed in {result.get('execution_time', 0):.0f}s")

    except Exception as e:
        print_error(str(e))
        raise click.Abort()

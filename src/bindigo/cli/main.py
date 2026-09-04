"""
Main CLI entry point for Bindigo.

This module defines the main command group and imports subcommands.
"""

import click

from bindigo.__version__ import __version__
from bindigo.cli.predict import predict
from bindigo.cli.info import info


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="bindigo")
@click.pass_context
def cli(ctx):
    """
    Bindigo - Protein-Ligand Binding Affinity Prediction

    Predicts protein-ligand binding affinities using molecular docking
    (AutoDock Vina) combined with machine learning.

    \b
    Examples:
      # Basic prediction using PDB ID and SMILES
      $ bindigo predict --protein 1HSG --ligand "CC(=O)Oc1ccccc1C(=O)O" --output results.csv

      # Using local files
      $ bindigo predict --protein protein.pdb --ligand ligand.sdf --output results.csv

      # Custom binding site
      $ bindigo predict --protein 1HSG --ligand "CCO" --center 10 20 15 --output results.csv

    \b
    Documentation: https://github.com/Siavashghaffari/Bindigo
    Report issues: https://github.com/Siavashghaffari/Bindigo/issues
    """
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Running `bindigo` with no subcommand is a discovery gesture, not a usage
    # error: show the help text and exit successfully. Handled explicitly rather
    # than via Click's default, which exits 2 on Click >= 8.2.
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit(0)


# Register subcommands
cli.add_command(predict)
cli.add_command(info)


def main():
    """Entry point for the bindigo command."""
    cli(obj={})


if __name__ == "__main__":
    main()

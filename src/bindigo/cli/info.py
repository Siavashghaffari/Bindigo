"""
Info command for Bindigo CLI.

Displays package information, version, models, and citation details.
"""

import click

from bindigo.__version__ import __version__, __description__, __url__


@click.command()
@click.option(
    "--version",
    "show_version",
    is_flag=True,
    help="Show package version",
)
@click.option(
    "--models",
    "show_models",
    is_flag=True,
    help="Show available ML models",
)
@click.option(
    "--cite",
    "show_citation",
    is_flag=True,
    help="Show citation information",
)
def info(show_version, show_models, show_citation):
    """
    Show package and model information.

    \b
    Examples:
      $ bindigo info --version
      $ bindigo info --models
      $ bindigo info --cite
    """
    # If no flags, show everything
    if not any([show_version, show_models, show_citation]):
        show_version = True
        show_models = True
        show_citation = True

    if show_version:
        click.echo("╔══════════════════════════════════════════════════════════════════╗")
        click.echo("║                  Bindigo Package Information                     ║")
        click.echo("╚══════════════════════════════════════════════════════════════════╝")
        click.echo(f"\nVersion:     {__version__}")
        click.echo(f"Description: {__description__}")
        click.echo(f"Homepage:    {__url__}")
        click.echo()

    if show_models:
        click.echo("╔══════════════════════════════════════════════════════════════════╗")
        click.echo("║                  Available ML Models                             ║")
        click.echo("╚══════════════════════════════════════════════════════════════════╝")
        try:
            from bindigo.ml.models import list_available_models
            models = list_available_models()
            for model in models:
                click.echo(f"\n  • {model['name']}")
                click.echo(f"    Algorithm: {model.get('algorithm', 'N/A')}")
                click.echo(f"    Training set: {model.get('training_set', 'N/A')}")
                click.echo(f"    Features: {model.get('n_features', 'N/A')}")
        except ImportError:
            click.echo("\n  • default (Random Forest, PDBbind v2020, 8 features)")
        click.echo()

    if show_citation:
        click.echo("╔══════════════════════════════════════════════════════════════════╗")
        click.echo("║                  Citation Information                            ║")
        click.echo("╚══════════════════════════════════════════════════════════════════╝")
        click.echo("""
If you use Bindigo in your research, please cite:

  Bindigo: A Python package for protein-ligand binding affinity prediction
  https://github.com/bindigo/bindigo

Bindigo uses the following tools:
  • AutoDock Vina: Eberhardt et al., J. Chem. Inf. Model. 2021
  • RDKit: https://www.rdkit.org
  • BioPython: Cock et al., Bioinformatics 2009
  • scikit-learn: Pedregosa et al., JMLR 2011
        """)

"""
Utility functions for CLI interface.

Provides formatting helpers, progress indicators, and output utilities.
"""

import sys
import click
from typing import Optional


def print_header(verbose: bool = False):
    """Print Bindigo header with version info."""
    from bindigo.__version__ import __version__

    mode = " (Verbose Mode)" if verbose else ""
    click.echo("╔══════════════════════════════════════════════════════════════════╗")
    click.echo(f"║                  Bindigo v{__version__}{mode:<28}║")
    if not verbose:
        click.echo("║         Protein-Ligand Binding Affinity Prediction              ║")
    click.echo("╚══════════════════════════════════════════════════════════════════╝")
    click.echo()


def print_box_result(title: str, content: dict):
    """
    Print results in a formatted box.

    Args:
        title: Box title
        content: Dictionary of key-value pairs to display
    """
    click.echo("╔══════════════════════════════════════════════════════════════════╗")
    click.echo(f"║{title:^66}║")
    click.echo("╠══════════════════════════════════════════════════════════════════╣")

    for key, value in content.items():
        # Format line with proper spacing
        line = f"║  {key + ':':<30} {str(value):<32}║"
        click.echo(line)

    click.echo("╚══════════════════════════════════════════════════════════════════╝")


def print_step(step: int, total: int, message: str):
    """
    Print a processing step indicator.

    Args:
        step: Current step number
        total: Total number of steps
        message: Step description
    """
    click.echo(f"[{step}/{total}] {message}")


def print_substep(message: str, status: str = "progress"):
    """
    Print a substep with status indicator.

    Args:
        message: Substep message
        status: One of 'progress', 'success', 'error', 'warning', 'info'
    """
    icons = {
        "progress": "⣷",
        "success": "✓",
        "error": "✗",
        "warning": "⚠",
        "info": "ℹ",
    }

    colors = {
        "progress": "cyan",
        "success": "green",
        "error": "red",
        "warning": "yellow",
        "info": "blue",
    }

    icon = icons.get(status, "•")
    color = colors.get(status, None)

    click.echo(f"  {click.style(icon, fg=color)} {message}")


def print_success(message: str):
    """Print a success message."""
    click.echo(click.style(f"✓ {message}", fg="green"))


def print_error(message: str, suggestion: Optional[str] = None):
    """
    Print an error message in a formatted box.

    Args:
        message: Error message
        suggestion: Optional suggestion for fixing the error
    """
    click.echo()
    click.echo("╔══════════════════════════════════════════════════════════════════╗")
    click.echo("║  " + click.style("ERROR", fg="red", bold=True) + "                                                            ║")
    click.echo("╠══════════════════════════════════════════════════════════════════╣")

    # Wrap long messages
    max_width = 64
    words = message.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 <= max_width:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)

    if current_line:
        lines.append(" ".join(current_line))

    for line in lines:
        click.echo(f"║  {line:<64}║")

    if suggestion:
        click.echo("║                                                                  ║")
        click.echo("║  Suggestion:                                                     ║")

        # Wrap suggestion
        words = suggestion.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= max_width - 4:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(" ".join(current_line))

        for line in lines:
            click.echo(f"║    {line:<62}║")

    click.echo("╚══════════════════════════════════════════════════════════════════╝")
    click.echo()


def print_warning(message: str):
    """Print a warning message."""
    click.echo(click.style(f"⚠ Warning: {message}", fg="yellow"))


def print_progress_bar(progress: float, width: int = 20):
    """
    Print a progress bar.

    Args:
        progress: Progress value between 0 and 1
        width: Width of the progress bar in characters
    """
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(progress * 100)
    click.echo(f"  [{bar}] {percentage}%", nl=False)
    click.echo("\r", nl=False)
    sys.stdout.flush()


class ProgressTracker:
    """Context manager for tracking multi-step progress."""

    def __init__(self, total_steps: int, verbose: bool = False):
        """
        Initialize progress tracker.

        Args:
            total_steps: Total number of steps
            verbose: Whether to show detailed output
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.verbose = verbose

    def step(self, message: str):
        """
        Move to next step.

        Args:
            message: Step description
        """
        self.current_step += 1
        print_step(self.current_step, self.total_steps, message)

    def substep(self, message: str, status: str = "progress"):
        """
        Print a substep (only in verbose mode).

        Args:
            message: Substep message
            status: Status indicator
        """
        if self.verbose:
            print_substep(message, status)

    def complete(self, message: str):
        """
        Mark current step as complete.

        Args:
            message: Completion message
        """
        print_substep(message, "success")


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Ask user for confirmation.

    Args:
        message: Confirmation message
        default: Default value if user just presses Enter

    Returns:
        True if user confirms, False otherwise
    """
    return click.confirm(message, default=default)

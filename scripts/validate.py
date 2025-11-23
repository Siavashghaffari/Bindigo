#!/usr/bin/env python
"""
Comprehensive package validation for PyPI readiness.
"""

import os
import sys
from pathlib import Path
import subprocess

# Colors for terminal output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color


def check(name, condition, error_msg=""):
    """Check a condition and print result."""
    if condition:
        print(f"  {GREEN}✓{NC} {name}")
        return True
    else:
        msg = f"  {RED}✗{NC} {name}"
        if error_msg:
            msg += f": {error_msg}"
        print(msg)
        return False


def main():
    """Run validation checks."""
    print("=" * 60)
    print("  Bindigo Package Validation")
    print("=" * 60)
    print()

    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    passed = 0
    failed = 0

    # Check 1: Required files
    print(f"{BLUE}[1] Checking required files...{NC}")
    required_files = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "pyproject.toml",
        "setup.py",
        "MANIFEST.in",
    ]

    for file in required_files:
        if check(f"{file} exists", Path(file).exists()):
            passed += 1
        else:
            failed += 1

    # Check 2: Package structure
    print(f"\n{BLUE}[2] Checking package structure...{NC}")
    required_dirs = [
        ("src/bindigo", "Package source"),
        ("tests", "Test suite"),
        ("docs", "Documentation"),
        ("examples", "Examples directory"),
        ("scripts", "Scripts directory"),
    ]

    for dir_path, desc in required_dirs:
        if check(desc, Path(dir_path).exists()):
            passed += 1
        else:
            failed += 1

    # Check 3: Distribution files
    print(f"\n{BLUE}[3] Checking distribution files...{NC}")
    if check("Wheel file exists", Path("dist/bindigo-0.1.0-py3-none-any.whl").exists()):
        passed += 1
    else:
        failed += 1

    if check("Source tarball exists", Path("dist/bindigo-0.1.0.tar.gz").exists()):
        passed += 1
    else:
        failed += 1

    # Check 4: Package metadata
    print(f"\n{BLUE}[4] Checking package metadata...{NC}")
    sys.path.insert(0, str(project_root / "src"))

    try:
        import bindigo

        if check("Package imports", True):
            passed += 1
        else:
            failed += 1

        if check("Version defined", hasattr(bindigo, "__version__")):
            passed += 1
        else:
            failed += 1

        if hasattr(bindigo, "__version__"):
            version = bindigo.__version__
            if check(f"Version format valid ({version})", len(version.split(".")) == 3):
                passed += 1
            else:
                failed += 1

    except Exception as e:
        check("Package imports", False, str(e))
        failed += 3

    # Check 5: CLI entry point
    print(f"\n{BLUE}[5] Checking CLI entry point...{NC}")
    try:
        result = subprocess.run(
            ["bindigo", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if check("CLI command works", result.returncode == 0):
            passed += 1
        else:
            failed += 1
    except Exception as e:
        check("CLI command works", False, str(e))
        failed += 1

    # Check 6: Test suite
    print(f"\n{BLUE}[6] Running test suite...{NC}")
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/", "-q", "--tb=no"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if check("Tests pass", result.returncode == 0):
            passed += 1
            # Count tests
            output = result.stdout
            if "passed" in output:
                print(f"    {output.strip().split()[-1]}")
        else:
            check("Tests pass", False, "Some tests failed")
            failed += 1
    except Exception as e:
        check("Tests pass", False, str(e))
        failed += 1

    # Summary
    print()
    print("=" * 60)
    print(f"{GREEN}Validation Summary{NC}")
    print("=" * 60)
    print(f"Checks passed: {GREEN}{passed}{NC}")
    print(f"Checks failed: {RED}{failed}{NC}")
    print()

    if failed == 0:
        print(f"{GREEN}✓ Package is ready for publication!{NC}")
        print()
        print("Next steps:")
        print("  1. Review CHANGELOG.md")
        print("  2. Test: python -m twine check dist/*")
        print("  3. Publish: python -m twine upload dist/*")
        return 0
    else:
        print(f"{RED}✗ Package is NOT ready for publication{NC}")
        print(f"\nPlease fix the {failed} failed check(s) above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

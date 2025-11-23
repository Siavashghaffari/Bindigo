#!/bin/bash
# Test Bindigo installation in clean virtual environment

set -e  # Exit on error

echo "=========================================="
echo "  Bindigo Installation Test"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}[1/7] Creating clean virtual environment...${NC}"
cd /tmp
rm -rf bindigo_test_venv
python3 -m venv bindigo_test_venv
source bindigo_test_venv/bin/activate

echo -e "${BLUE}[2/7] Installing package from wheel...${NC}"
pip install -q "$PROJECT_ROOT/dist/bindigo-0.1.0-py3-none-any.whl"

echo -e "${BLUE}[3/7] Testing package import...${NC}"
python -c "import bindigo; print(f'✓ Bindigo v{bindigo.__version__} imported successfully')"

echo -e "${BLUE}[4/7] Testing CLI availability...${NC}"
which bindigo
bindigo --version

echo -e "${BLUE}[5/7] Testing CLI commands...${NC}"
echo "  - Testing: bindigo --help"
bindigo --help > /dev/null
echo "  ✓ Main help works"

echo "  - Testing: bindigo predict --help"
bindigo predict --help > /dev/null
echo "  ✓ Predict help works"

echo "  - Testing: bindigo info --version"
bindigo info --version > /dev/null
echo "  ✓ Info command works"

echo -e "${BLUE}[6/7] Testing Python API imports...${NC}"
python << 'EOF'
# Test all major imports
from bindigo import __version__
from bindigo.cli.main import cli
from bindigo.core.config import config
from bindigo.core.pipeline import run_prediction
from bindigo.utils.validation import validate_protein_input
from bindigo.utils.exceptions import BindigoError

print("  ✓ All major imports successful")
EOF

echo -e "${BLUE}[7/7] Cleaning up...${NC}"
deactivate
cd "$PROJECT_ROOT"
rm -rf /tmp/bindigo_test_venv

echo ""
echo -e "${GREEN}=========================================="
echo -e "  ✓ ALL TESTS PASSED"
echo -e "  Package is installable and functional!"
echo -e "==========================================${NC}"

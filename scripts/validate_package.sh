#!/bin/bash
# Comprehensive package validation for PyPI readiness

set -e

echo "=========================================="
echo "  Bindigo Package Validation"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Validation checks
PASSED=0
FAILED=0

check_pass() {
    echo -e "  ${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "  ${RED}✗${NC} $1"
    ((FAILED++))
}

echo -e "${BLUE}[1] Checking required files...${NC}"
for file in README.md LICENSE CONTRIBUTING.md pyproject.toml setup.py MANIFEST.in CHANGELOG.md; do
    if [ -f "$file" ]; then
        check_pass "$file exists"
    else
        check_fail "$file missing"
    fi
done

echo ""
echo -e "${BLUE}[2] Checking package structure...${NC}"
if [ -d "src/bindigo" ]; then
    check_pass "src/bindigo/ directory exists"
else
    check_fail "src/bindigo/ directory missing"
fi

if [ -d "tests" ]; then
    check_pass "tests/ directory exists"
else
    check_fail "tests/ directory missing"
fi

if [ -d "docs" ]; then
    check_pass "docs/ directory exists"
else
    check_fail "docs/ directory missing"
fi

echo ""
echo -e "${BLUE}[3] Checking distribution files...${NC}"
if [ -f "dist/bindigo-0.1.0-py3-none-any.whl" ]; then
    check_pass "Wheel file exists"
else
    check_fail "Wheel file missing"
fi

if [ -f "dist/bindigo-0.1.0.tar.gz" ]; then
    check_pass "Source distribution exists"
else
    check_fail "Source distribution missing"
fi

echo ""
echo -e "${BLUE}[4] Running test suite...${NC}"
if python -m pytest tests/ -q; then
    check_pass "All tests pass"
else
    check_fail "Some tests failed"
fi

echo ""
echo -e "${BLUE}[5] Checking package metadata...${NC}"
python << 'EOF'
import sys
sys.path.insert(0, 'src')
import bindigo

checks = [
    ('Version defined', hasattr(bindigo, '__version__')),
    ('Version is string', isinstance(bindigo.__version__, str)),
    ('Version format valid', len(bindigo.__version__.split('.')) == 3),
]

for check_name, result in checks:
    if result:
        print(f"  \033[0;32m✓\033[0m {check_name}")
    else:
        print(f"  \033[0;31m✗\033[0m {check_name}")
EOF

echo ""
echo -e "${BLUE}[6] Checking entry points...${NC}"
if command -v bindigo &> /dev/null; then
    check_pass "bindigo command available"

    if bindigo --version &> /dev/null; then
        check_pass "bindigo --version works"
    else
        check_fail "bindigo --version fails"
    fi
else
    check_fail "bindigo command not found"
fi

echo ""
echo -e "${BLUE}[7] Checking imports...${NC}"
python << 'EOF'
import sys
sys.path.insert(0, 'src')

try:
    import bindigo
    print(f"  \033[0;32m✓\033[0m bindigo imports successfully")
except Exception as e:
    print(f"  \033[0;31m✗\033[0m bindigo import failed: {e}")

try:
    from bindigo.cli.main import cli
    print(f"  \033[0;32m✓\033[0m CLI imports successfully")
except Exception as e:
    print(f"  \033[0;31m✗\033[0m CLI import failed: {e}")
EOF

echo ""
echo "=========================================="
echo -e "${GREEN}Validation Summary${NC}"
echo "=========================================="
echo -e "Checks passed: ${GREEN}${PASSED}${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "Checks failed: ${RED}${FAILED}${NC}"
    echo ""
    echo -e "${RED}Package is NOT ready for publication${NC}"
    exit 1
else
    echo ""
    echo -e "${GREEN}✓ Package is ready for publication!${NC}"
    exit 0
fi

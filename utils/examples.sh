#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Function to print header
print_header() {
    echo -e "\n${YELLOW}==============================================${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${YELLOW}==============================================${NC}\n"
}

# Function to print error and exit
print_error() {
    echo -e "${RED}Error: $1${NC}"
    exit 1
}

# Function to print success
print_success() {
    echo -e "${GREEN}$1${NC}"
}

# Function to print info
print_info() {
    echo -e "${YELLOW}$1${NC}"
}

# Check if we're in the correct directory
if [ ! -f "$PROJECT_ROOT/setup.py" ]; then
    print_error "setup.py not found in $PROJECT_ROOT"
fi

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "python3 is not installed"
fi

# Check if venv module is available
if ! python3 -c "import venv" &> /dev/null; then
    print_error "python3-venv is not installed. Please install it using: sudo apt-get install python3-venv"
fi

# Create and activate virtual environment
print_header "Setting up virtual environment"
VENV_DIR="$PROJECT_ROOT/venv"

if [ ! -d "$VENV_DIR" ]; then
    if ! python3 -m venv "$VENV_DIR"; then
        print_error "Failed to create virtual environment"
    fi
    print_success "✓ Virtual environment created successfully"
else
    print_info "Virtual environment already exists"
fi

# Find all examples
print_header "Finding examples"
EXAMPLES=$(find "$PROJECT_ROOT/examples" -name "*_example.py" | grep -v "validation_example.py" | sed "s|$PROJECT_ROOT/||")

if [ -z "$EXAMPLES" ]; then
    print_error "No examples found!"
fi

# Print list of found examples
print_header "Found examples:"
echo "$EXAMPLES" | nl

# Run all examples
print_header "Running examples"
success_count=0
failed_count=0

# Add project root to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

for example in $EXAMPLES; do
    print_header "Running: $example"
    if python "$PROJECT_ROOT/$example"; then
        print_success "✓ Example completed successfully"
        ((success_count++))
    else
        print_error "✗ Example failed"
        ((failed_count++))
    fi
done

# Print final statistics
print_header "Final Statistics"
print_success "Successfully completed: $success_count"
print_error "Failed: $failed_count"
print_info "Total examples: $((success_count + failed_count))"

# Deactivate virtual environment
deactivate

# Return error code if there were any failed examples
[ $failed_count -eq 0 ]
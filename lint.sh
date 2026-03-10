#!/bin/bash
# Script to run rpmlint on SPEC files
set -e

if ! command -v rpmlint &> /dev/null; then
    echo "rpmlint not found. Installing..."
    sudo dnf install -y rpmlint
fi

echo "=== Running rpmlint on all SPEC files ==="
rpmlint *.spec

echo "=== All SPEC files checked ==="

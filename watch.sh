#!/bin/bash
# Quick launcher for watch mode
# Usage: ./watch.sh

cd "$(dirname "$0")"
python3 install.py --watch

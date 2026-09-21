#!/usr/bin/env bash
# Made by Sinfallas <sinfallas@yahoo.com>
# Licence: GPL-2
LC_ALL=C

if [[ "$EUID" != "0" ]]; then
        echo "ERROR: debe ser root."
        exit 1
fi

clear
rm -f .coverage
rm -rf .mypy_cache
rm -rf .pytest_cache
rm -rf .ruff_cache
rm -rf .tox
rm -rf tests/__pycache__
rm -rf src/ecoflow_reader/__pycache__
echo "Finalizado."
exit 0

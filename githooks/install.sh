#!/bin/sh
ln -sf ../githooks/pre-commit "$(dirname "$0")/../.git/hooks/pre-commit"

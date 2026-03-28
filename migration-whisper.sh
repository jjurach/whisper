#!/bin/bash
# Auto-generated migration script - REVIEW BEFORE EXECUTION
# Project: whisper

set -e

# Create safety tag before migration
git tag -a -m 'pre-dev_notes-cleanup' pre-dev_notes-cleanup

# Create planning directory structure
mkdir -p planning/inbox

# Remove empty directories
rmdir dev_notes/specs 2>/dev/null || true
rmdir dev_notes/project_plans 2>/dev/null || true
rmdir dev_notes/inbox 2>/dev/null || true

echo '✓ Migration complete for whisper'
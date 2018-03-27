#!/bin/sh

# Stash unstaged changes before running tests
# to avoid testing code that isn't part of the
# upcoming commit.
STASH_NAME="pre-commit-$(date +%s)"
git stash save -q --keep-index "$STASH_NAME"

# Run tests
pytest
RESULT=$?

# Restore stash
STASH=$(git stash list | grep "$STASH_NAME" | cut -d":" -f1)
git stash pop "$STASH" -q

# Act on test results
[ $RESULT -ne 0 ] && exit 1
exit 0

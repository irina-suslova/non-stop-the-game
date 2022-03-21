#!/bin/bash
pylint $(ls -d */) | tee pylint.txt
cat pylint.txt

mkdir public
score=$(sed -n 's/^Your code has been rated at \([-0-9.]*\)\/.*/\1/p' pylint.txt)
anybadge --value=$score --file=public/pylint.svg pylint
echo "Pylint score was $score"

exit 0


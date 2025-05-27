#!/bin/sh
set -euxo pipefail

CC="gcc"
PROGRAM=""
SOURCES=$(ls ./*.c)
LINKS=""
STD="-std=c99"
OPTIMIZE="-O0"
ERROR="-Werror -Wall -Wextra -Wpedantic"
SANITIZE="-fsanitize=undefined,address" # doesn't work on windows lol

$CC $STD $OPTIMIZE $ERROR $SANITIZE $SOURCES -o $PROGRAM $LINKS

exit 0

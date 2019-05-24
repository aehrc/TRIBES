#!/bin/sh
set -e
make all
mkdir -p "${PREFIX}/bin"
cp germline "${PREFIX}/bin/"


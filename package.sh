#!/bin/bash

pushd $(dirname "${0}") > /dev/null
basedir=$(pwd -L)
# Use "pwd -P" for the path without links. man bash for more info.
popd > /dev/null

echo "${basedir}"


git pull

cd "${basedir}/frontend"

npm install

npm run build

rm -rf "${basedir}/nginx/dist"

cp -r "${basedir}/frontend/build" "${basedir}/nginx/dist"
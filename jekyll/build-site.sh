#! /usr/bin/env bash

cd "$(dirname "$0")"
JEKYLL_GITHUB_TOKEN=`cat token.txt` jekyll build -d ../docs/
rm -f ../docs/*.md ../docs/Gemfile ../docs/Gemfile.lock

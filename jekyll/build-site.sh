#! /usr/bin/env bash

JEKYLL_GITHUB_TOKEN=`cat token.txt` jekyll build -d ../docs/

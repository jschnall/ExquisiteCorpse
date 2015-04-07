#!/bin/bash
# compass/compass.sh - properly invoke the "Compass" program
# brew install coreutils for greadlink
#
# compass create -r bootstrap-sass --using bootstrap
# add require 'bootstrap-sass' to config.rb and fix paths
# rm -r stylesheets/
# compass.watch while working on scss files

BASE=$(dirname $(greadlink -f $(which "$0")))
export GEM_HOME=$BASE/Gem
export RUBYLIB=$BASE/Gem/lib
$BASE/Gem/bin/compass "$@"

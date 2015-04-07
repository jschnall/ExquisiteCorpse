#!/bin/bash
# compass/install.sh - install Compass under the "./Gem" directory
# brew install coreutils for greadlink

if ! which gem >/dev/null ;then
    echo 'Error: no "gem" command available'
    echo 'Please "sudo aptitude install rubygems1.8" or "ruby1.9.1"'
    exit 1
fi
BASE=$(dirname $(greadlink -f $(which "$0")))
cd $BASE  # the directory where this script lives
gem install -i Gem compass
gem install -i Gem compass-susy-plugin
gem install -i Gem bootstrap-sass
gem install -i Gem bundler

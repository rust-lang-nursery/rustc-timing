# Script for compiling rust and processing the time info

git checkout master
git pull upstream master
# TODO save the date in a variable
git show HEAD >/home/ncameron/times/raw/$(date +%F).log
touch src/librustc/middle/ty.rs
export CC=clang
export CXX=clang++
export RUSTFLAGS_STAGE2=-Ztime-passes
# TODO sometimes need to configure
make >>/home/ncameron/times/raw/$(date +%F).log

cd /home/ncameron/times
python process.py $(date +%F)
git add raw/$(date +%F).log
git add processed/$(date +%F).json
git commit -m "Added data for $(date +%F)"
git push origin master

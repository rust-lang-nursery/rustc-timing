DATE=$(date +%F)
START=$(pwd)

git checkout master
git pull upstream master

export CC=clang-3.5
export CXX=clang++-3.5
export RUSTFLAGS_STAGE2=-Ztime-passes

./configure

for i in 0 1 2
do
    git show HEAD -s >/home/ncameron/times/raw/rustc-$DATE-$i.log
    touch src/librustc/middle/ty.rs
    make >>/home/ncameron/times/raw/rustc-$DATE-$i.log
done

cd /home/ncameron/times
python process.py rustc $DATE 3
for i in 0 1 2
do
    git add raw/rustc-$DATE-$i.log
    git add processed/rustc-$DATE-$i.json
done

export RUSTC=$START/x86_64-unknown-linux-gnu/stage2/bin/rustc
export LD_LIBRARY_PATH=$START/x86_64-unknown-linux-gnu/stage2/lib
/home/ncameron/benchmarks/process.py

git commit -m "Added data for $DATE"
git push origin master

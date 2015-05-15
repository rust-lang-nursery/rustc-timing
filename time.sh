DATE=$(date +%F)

git checkout master
git pull upstream master
git show HEAD >/home/ncameron/times/raw/$DATE.log

export CC=clang-3.5
export CXX=clang++-3.5
export RUSTFLAGS_STAGE2=-Ztime-passes

for i in 0 1 2
do
    touch src/librustc/middle/ty.rs
    make >>/home/ncameron/times/raw/$DATE-$i.log || (./configure && make >>/home/ncameron/times/raw/$DATE-$i.log)
done

cd /home/ncameron/times
python process.py $DATE 3
git add raw/$DATE-0.log
git add raw/$DATE-1.log
git add raw/$DATE-2.log
git add processed/$DATE.json
git commit -m "Added data for $DATE"
git push origin master

#!/bin/bash
#REPO=$1
#git clone $1 ass4
#cd ass4
#mv freetests.py freetests.py.student
#wget /usr/bin/wget http://172.17.0.1:8000/CMPUT404-assignment-ajax/freetests.py
#wget /usr/bin/wget http://172.17.0.1:8000/runner.py
#timeout 30 python2.7 freetests.py
#python runner.py
#
#!/bin/bash
REPO=$1
git clone $1 ass5
cd ass5
mv freetests.py freetests.py.student
mv runtests.sh runtests.sh.student
wget /usr/bin/wget http://172.17.0.1:8000/freetests.py
wget /usr/bin/wget http://172.17.0.1:8000/run.py
wget /usr/bin/wget http://172.17.0.1:8000/drun.sh
wget /usr/bin/wget http://172.17.0.1:8000/CMPUT404-assignment-websockets/runtests.sh
wget /usr/bin/wget http://172.17.0.1:8000/CMPUT404-assignment-websockets/freetests.py
mv run.sh run.sh.student
wget /usr/bin/wget http://172.17.0.1:8000/CMPUT404-assignment-websockets/run.sh
echo "###############################"
bash runtests.sh
echo "###############################"
echo So those were the tests
echo Now run the server!
pgrep gunicorn | xargs -i kill -9 {} || echo OK
bash drun.sh

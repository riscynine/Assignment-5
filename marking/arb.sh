cd /home/me
/usr/bin/wget http://172.17.0.1:8000/runtest.sh
/bin/bash runtest.sh $1
if [ "$2" == 1 ];
then
	/bin/bash
fi

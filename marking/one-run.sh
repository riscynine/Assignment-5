file=$1
two=$2
#(sleep 3; killall firefox ) &
#(sleep 4; killall firefox ) &
(sleep 8; bash cacheless-browser.sh -new-window  http://127.0.0.1:5000/static/index.html  \
 -new-window  http://127.0.0.1:5000/static/index.html  ) &
#(sleep 10; firefox -new-window  http://127.0.0.1:5000/static/index.html  \
# -new-window  http://127.0.0.1:5000/static/index.html  ) &
docker run -P -p 127.0.0.1:5000:5000 -u=me -i -t cmput404 /bin/bash /home/me/arb.sh  `perl 2txt.pl "$file" | perl grepgh.pl` $two | tee $file.out

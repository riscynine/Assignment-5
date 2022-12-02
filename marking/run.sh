# ps aux | fgrep 'python -m SimpleHTTPServer' | awk '{print $2}' | xargs kill
# python -m SimpleHTTPServer 8000 &
python3 -m http.server &
ID=$!
#for file in html/*.html
for file in html/*_/*.html
do
echo $file
echo $file | gview -
#(sleep 10; firefox  --new-window  http://localhost:5000/static/index.html --safe-mode --new-window & \
# firefox  --new-window  http://localhost:5000/static/index.html --safe-mode --new-window & ) &
bash one-run.sh $file
#docker run -u=me -i -t cmput404 /bin/bash /home/me/arb.sh  `perl 2txt.pl "$file" | perl grepgh.pl` | tee $file.out
done
kill $ID

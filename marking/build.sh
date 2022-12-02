mkdir Docker
cp Dockerfile arb.sh Docker
cp requirements.txt Docker
cd Docker
docker rmi -f cmput404
docker build --force-rm -t cmput404 .

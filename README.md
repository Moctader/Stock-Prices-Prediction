# Financial Stock Prices Prediction

# Clear Fully Dcoker

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q) -f
docker volume rm $(docker volume ls -q)

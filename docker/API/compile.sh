sudo docker image rm miningAPI
sudo docker build --no-cache -t miningapi ./docker/API/

# docker run -v ./:/mining/ miningAPI
sudo docker image rm prediction2
sudo docker build --no-cache -t prediction2 ./docker/prediction2/

# docker run -v ./:/mining/ prediction2
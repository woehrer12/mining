sudo docker image rm prediction1
sudo docker build --no-cache -t prediction1 ./docker/prediction1/

# docker run -v ./:/mining/ prediction1
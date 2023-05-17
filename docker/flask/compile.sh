sudo docker image rm flask
sudo docker build --no-cache -t flask ./docker/flask/

# docker run -v ./:/mining/ flask
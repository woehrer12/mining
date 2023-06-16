sudo docker image rm ownphp
sudo docker build --no-cache -t ownphp ./docker/php/

# docker run -v ./:/mining/ -v ./www:/var/www/html -p 80:80 ownphp
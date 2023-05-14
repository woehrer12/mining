mkdir mysql
mkdir grafana

sudo docker image rm miningAPI
sudo docker build --no-cache -t miningapi ./docker/API/

sudo docker image rm hiveos
sudo docker build --no-cache -t hiveos ./docker/hiveos/

sudo docker-compose -p mining -f docker-compose-mysql.yml up -d

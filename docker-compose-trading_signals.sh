sudo docker image rm trading_signals
sudo docker build --no-cache -t trading_signals ./docker/trading_signals/

sudo docker image rm flask
sudo docker build --no-cache -t flask ./docker/flask/

sudo docker-compose -p trading -f docker-compose-trading_signals.yml up -d

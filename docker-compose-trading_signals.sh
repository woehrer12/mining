docker image rm trading_signals
docker build --no-cache -t trading_signals ./docker/trading_signals/

docker image rm flask
docker build --no-cache -t flask ./docker/flask/

docker image rm ownphp
docker build --no-cache -t ownphp ./docker/php/

docker-compose -p trading -f docker-compose-trading_signals.yml up -d

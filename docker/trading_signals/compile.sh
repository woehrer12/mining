sudo docker image rm trading_signals
sudo docker build --no-cache -t trading_signals ./docker/trading_signals/

# docker run -v ./:/mining/ trading_signals
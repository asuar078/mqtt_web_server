
### Installation on MQTT Server

Install mosquitto 
```bash
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
```

Install flask and Paho-MQTT

```bash
sudo apt-get install python3-pip
sudo pip3 install flask
sudo pip3 install paho-mqtt
```
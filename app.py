import paho.mqtt.client as mqtt
from flask import Flask, jsonify
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

app = Flask(__name__)

mqttc = mqtt.Client()
mqttc.connect("localhost", 1883, 60)

mqttc.loop_start()

# Create a dictionary called apartment to store the rooms
apartment = {
    1: ['ground'],
    2: ['all', '201', '202', '203', 'fitness', 'lobby'],
    3: ['all', '301', '302', '303', '304', '305', '306', '307', '308'],
    4: ['all', '401', '402', '403', '404', '405', '406', '407', '408'],
    5: ['all', '501', '502', '503', '504', '505', '506'],
    6: ['all', '601', '602', '603', '604', '605', '506'],
    7: ['all', '701', '702', '703', '704', '705', '706'],
    8: ['all', 'pha', 'phb', 'phc', 'phd']
}


@app.route("/apartment_topics", methods=['GET'])
def get_pin_data():
    return jsonify(apartment)


@app.route("/floor/<floor_num>/<room>/<action>", methods=['GET', 'POST'])
def publish_event(floor_num, room, action):
    logging.debug("received, floor: {}, num: {}, action: {}".
                  format(floor_num, room, action))
    # check if floor number is valid
    if apartment.get(int(floor_num)) is None:
        logging.error("no key exists in dict")
        return jsonify(message="FAIL")

    # print("Yes key exists in dict")
    floor = apartment[int(floor_num)]

    # check if room is valid
    if str(room) not in floor:
        logging.error("no room in floor")
        return jsonify(message="FAIL")

    # print("Yes room in floor")

    # check if action if valid
    if action == '1' or action == '0':
        topic = "floor/{}".format(int(floor_num))
        act = "{}/{}".format(room, action)

        logging.debug("publishing request")

        # publish on mqtt for esp to see
        mqttc.publish(topic, act)
        return jsonify(message="OK")

    logging.error("action not allowed")
    return jsonify(message="FAIL")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181, debug=True)

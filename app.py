from csv import DictWriter

from flask import Flask, request
from lifx import Lifx
import light_sensor

app = Flask(__name__)
lifx = Lifx()


@app.route('/toggle', methods=['POST'])
def toggle():
    try:
        state = lifx.toggle()
        return state, 200
    except:
        return 'Bad Gateway', 502


@app.route('/on', methods=['POST'])
def on():
    try:
        lifx.on()
        return 'on', 200
    except:
        return 'Bad Gateway', 502


@app.route('/off', methods=['POST'])
def off():
    try:
        lifx.off()
        return 'off', 200
    except:
        return 'Bad Gateway', 502


@app.route('/brightness', methods=['POST'])
def brightness():
    try:
        value = request.args.get('value', default=0, type=int)
        if value < 0 or value > 65535:
            return 'Invalid Brightness', 400
        else:
            lifx.set_brightness(value)
            return 'ok', 200
    except:
        return 'Bad Gateway', 502


@app.route('/results', methods=['POST'])
def results():
    time = request.args.get('time', default=0, type=int)
    try:
        headersCSV = ['Time', 'Brightness', 'Lux']
        with open('data.csv', 'a', newline='') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
            list_data = {"Time": time, 'Brightness': lifx.get_brightness(), 'Lux': light_sensor.get_lux()}
            dictwriter_object.writerow(list_data)
            f_object.close()
        return 'ok', 200
    except:
        return 'Bad Gateway', 502


@app.route('/')
def get_power():
    try:
        return lifx.power_state(), 200
    except:
        return 'Bad Gateway', 502


if __name__ == '__main__':
    app.run()

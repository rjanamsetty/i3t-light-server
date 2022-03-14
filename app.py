from flask import Flask, request
import lifx

app = Flask(__name__)


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
        value = request.args.get('value', default=1, type=int)
        if value < 0 or value > 65535:
            return 'Invalid Brightness', 400
        else:
            lifx.set_brightness(value)
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

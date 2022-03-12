from flask import Flask
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


@app.route('/')
def get_power():
    try:
        return lifx.power_state(), 200
    except:
        return 'Bad Gateway', 502


if __name__ == '__main__':
    app.run(host="192.168.1.9")

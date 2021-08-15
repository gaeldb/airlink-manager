
import os
import asyncio
from time import sleep

from flask import Flask
from flask import render_template
from flask import redirect



from airlink import monitoring
from airlink import actions


LOOP = asyncio.get_event_loop()

app = Flask(__name__)


# async def print_param():
#     # See https://panoramisk.readthedocs.io/en/latest/manager.html
#     ami = Manager(host='127.0.0.1', username='admin', secret='1234', port=5038, ssl=False, encoding='utf8')
#     await ami.connect()
#     params = await ami.send_command('aradio param')
#     ami.close()
#     print(params)


@app.route('/')
def index():
    #LOOP.run_until_complete(print_param())
    return render_template('index.html', data = monitoring.get_datas())


@app.route('/stream')
def stream():
    return app.response_class(monitoring.generate_log_report(), mimetype = 'text/plain')


@app.route('/action/reboot')
def reboot():
    actions.reboot()
    return redirect('/')

@app.route('/action/reset')
def reset():
    LOOP.run_until_complete(actions.radio_reset())
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

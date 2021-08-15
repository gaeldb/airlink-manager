import os
from panoramisk import Manager


AMI = Manager(host='127.0.0.1', username='admin', secret='1234', port=5038, ssl=False, encoding='utf8')


def reboot():
    os.system('systemctl reboot -i')


async def radio_reset():
    await AMI.connect()
    params = await AMI.send_command('aradio reset')
    AMI.close()

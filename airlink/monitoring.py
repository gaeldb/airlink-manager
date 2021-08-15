import socket
import psutil
import netifaces as ni
from gpiozero import CPUTemperature, DiskUsage, LoadAverage, PingServer


def is_process_running(pname):
    for proc in psutil.process_iter():
        try:
            if pname.lower() in proc.name().lower():
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    return None


def get_interface_ip(iface):
    try:
        return ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
    except ValueError:
        return None


def get_datas():
    data = {}
    data['airlink_hostname'] = socket.gethostname()
    data['airlink_interface_ip'] = get_interface_ip('eth0')
    data['airlink_vpn_ip'] = get_interface_ip('nebula1')
    data['airlink_process_sshd'] = is_process_running('sshd')
    data['airlink_process_asterisk'] = is_process_running('asterisk')
    data['airlink_process_vpn'] = is_process_running('nebula')
    data['airlink_temp'] = CPUTemperature().temperature
    data['airlink_disk_usage'] = DiskUsage().usage #.value
    data['airlink_load_average'] = LoadAverage().value
    data['airlink_lighthouse_connected'] = PingServer('nebula.ip').is_active
    data['airlink_internet_connected'] = PingServer('google.com').is_active
    data['temp_repeater'] = "XX"
    return data


def generate_log_report():
    with open('/var/log/asterisk/radio.log') as f:
        lines = f.readlines()
        last_lines = lines[-30:]
        yield "".join(last_lines)

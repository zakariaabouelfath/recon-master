"""
Module Scanner
Fonctions scan réseau
"""

import socket
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor


def ping_host(host, timeout=1):
    """Teste si host répond au ping"""
    param = '-n' if sys.platform == 'win32' else '-c'
    command = ['ping', param, '1', '-W' if sys.platform != 'win32' else '-w', str(timeout), host]

    try:
        result = subprocess.run(command, capture_output=True, timeout=timeout + 1)
        return result.returncode == 0
    except:
        return False


def test_port(host, port, timeout=1):
    """Teste si port TCP ouvert"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def get_service_name(port):
    """Retourne nom service pour port"""
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
        5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Alt"
    }
    return services.get(port, "Unknown")


def scan_port(host, port, timeout):
    """Scanne un port"""
    if test_port(host, port, timeout):
        return {
            'port': port,
            'status': 'open',
            'service': get_service_name(port)
        }
    return None


def scan_ports(host, ports, timeout=1, threads=50):
    """Scanne plusieurs ports (multi-thread)"""
    ports_ouverts = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, host, port, timeout) for port in ports]

        for future in futures:
            result = future.result()
            if result:
                ports_ouverts.append(result)

    return sorted(ports_ouverts, key=lambda x: x['port'])
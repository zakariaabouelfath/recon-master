"""
Module Enumeration
Fonctions énumération DNS, etc.
"""

import socket


def dns_recon(target):
    """Reconnaissance DNS"""
    info = {
        'ip': None,
        'hostname': None
    }

    try:
        # Résolution DNS
        ip = socket.gethostbyname(target)
        info['ip'] = ip

        # Reverse DNS
        try:
            hostname = socket.gethostbyaddr(ip)
            info['hostname'] = hostname[0]
        except:
            pass
    except:
        # Déjà une IP
        info['ip'] = target
        try:
            hostname = socket.gethostbyaddr(target)
            info['hostname'] = hostname[0]
        except:
            pass

    return info
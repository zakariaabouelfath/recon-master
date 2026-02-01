"""
Module Web Scanning
Fonctions scan sites web
"""

import requests
from urllib.parse import urljoin


def scan_website(url, config):
    """Scanne site web basique"""
    info = {
        'accessible': False,
        'status_code': None,
        'headers_manquants': [],
        'server': None
    }

    try:
        headers = {'User-Agent': config['user_agent']}
        response = requests.get(url, headers=headers, timeout=config['timeout'], verify=False)

        info['accessible'] = True
        info['status_code'] = response.status_code

        # Vérifier headers sécurité
        headers_securite = [
            'X-Frame-Options',
            'X-XSS-Protection',
            'X-Content-Type-Options',
            'Strict-Transport-Security',
            'Content-Security-Policy'
        ]

        for header in headers_securite:
            if header not in response.headers:
                info['headers_manquants'].append(header)

        # Info serveur
        if 'Server' in response.headers:
            info['server'] = response.headers['Server']

    except:
        pass

    return info


def enum_directories(base_url, config):
    """Énumère directories communs"""
    wordlist = [
        'admin', 'login', 'dashboard', 'api', 'backup',
        'config', 'test', 'dev', 'uploads', 'files',
        'images', 'css', 'js', 'phpmyadmin', 'wp-admin'
    ]

    trouves = []
    headers = {'User-Agent': config['user_agent']}

    for directory in wordlist:
        url = urljoin(base_url, directory)

        try:
            response = requests.get(url, headers=headers, timeout=config['timeout'], verify=False,
                                    allow_redirects=False)

            if response.status_code in [200, 301, 302, 403]:
                trouves.append({
                    'path': directory,
                    'code': response.status_code
                })
        except:
            pass

    return trouves
"""
Module Reporter
Génération rapports multiples formats
"""

import json
import csv
from datetime import datetime


def generer_json(resultats, filename):
    """Génère rapport JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(resultats, f, indent=2, ensure_ascii=False)


def generer_txt(resultats, filename):
    """Génère rapport TXT"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("RECON MASTER - RAPPORT DE RECONNAISSANCE\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Cible    : {resultats['cible']}\n")
        f.write(f"Date     : {resultats['timestamp']}\n")
        f.write(f"Modules  : {', '.join(resultats['modules'].keys())}\n\n")

        # Network
        if 'network' in resultats['modules']:
            net = resultats['modules']['network']
            f.write("-" * 60 + "\n")
            f.write("NETWORK SCANNING\n")
            f.write("-" * 60 + "\n")
            f.write(f"Alive    : {net.get('alive', False)}\n")

            if net.get('ports'):
                f.write(f"\nPorts ouverts : {len(net['ports'])}\n\n")
                for port in net['ports']:
                    f.write(f"  {port['port']:5d}  {port['service']}\n")
            f.write("\n")

        # Web
        if 'web' in resultats['modules']:
            web = resultats['modules']['web']
            f.write("-" * 60 + "\n")
            f.write("WEB SCANNING\n")
            f.write("-" * 60 + "\n")
            f.write(f"Accessible : {web.get('accessible', False)}\n")

            if web.get('accessible'):
                f.write(f"Status     : {web.get('status_code')}\n")
                f.write(f"Server     : {web.get('server', 'N/A')}\n")
                f.write(f"Headers manquants : {len(web.get('headers_manquants', []))}\n")

                if web.get('directories'):
                    f.write(f"\nDirectories : {len(web['directories'])}\n")
                    for d in web['directories']:
                        f.write(f"  /{d['path']} ({d['code']})\n")
            f.write("\n")

        # DNS
        if 'dns' in resultats['modules']:
            dns = resultats['modules']['dns']
            f.write("-" * 60 + "\n")
            f.write("DNS ENUMERATION\n")
            f.write("-" * 60 + "\n")
            f.write(f"IP       : {dns.get('ip', 'N/A')}\n")
            f.write(f"Hostname : {dns.get('hostname', 'N/A')}\n\n")


def generer_csv(resultats, filename):
    """Génère rapport CSV (ports)"""
    if 'network' not in resultats['modules']:
        return

    ports = resultats['modules']['network'].get('ports', [])

    if not ports:
        return

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['port', 'status', 'service'])
        writer.writeheader()
        for port in ports:
            writer.writerow(port)


def generer_html(resultats, filename):
    """Génère rapport HTML"""
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Recon Master Report - {resultats['cible']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .info {{ background: #ecf0f1; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #3498db; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .success {{ color: #27ae60; }}
        .warning {{ color: #e67e22; }}
        .danger {{ color: #e74c3c; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>RECON MASTER - Rapport de Reconnaissance</h1>

        <div class="info">
            <strong>Cible :</strong> {resultats['cible']}<br>
            <strong>Date :</strong> {resultats['timestamp']}<br>
            <strong>Modules :</strong> {', '.join(resultats['modules'].keys())}
        </div>
"""

    # Network
    if 'network' in resultats['modules']:
        net = resultats['modules']['network']
        html += f"""
        <h2>Network Scanning</h2>
        <p><strong>Status:</strong> <span class="{'success' if net.get('alive') else 'danger'}">
        {'Alive' if net.get('alive') else 'Down'}</span></p>
        """

        if net.get('ports'):
            html += f"""
            <p><strong>Ports ouverts :</strong> {len(net['ports'])}</p>
            <table>
                <tr><th>Port</th><th>Service</th><th>Status</th></tr>
            """
            for port in net['ports']:
                html += f"""
                <tr>
                    <td>{port['port']}</td>
                    <td>{port['service']}</td>
                    <td class="success">{port['status']}</td>
                </tr>
                """
            html += "</table>"

    # Web
    if 'web' in resultats['modules']:
        web = resultats['modules']['web']
        html += f"""
        <h2>Web Scanning</h2>
        <p><strong>Accessible:</strong> <span class="{'success' if web.get('accessible') else 'danger'}">
        {'Yes' if web.get('accessible') else 'No'}</span></p>
        """

        if web.get('accessible'):
            html += f"""
            <p><strong>Status Code:</strong> {web.get('status_code')}</p>
            <p><strong>Server:</strong> {web.get('server', 'N/A')}</p>
            <p><strong>Headers manquants:</strong> <span class="warning">{len(web.get('headers_manquants', []))}</span></p>
            """

            if web.get('directories'):
                html += """
                <h3>Directories trouves</h3>
                <table>
                    <tr><th>Path</th><th>Code</th></tr>
                """
                for d in web['directories']:
                    html += f"<tr><td>/{d['path']}</td><td>{d['code']}</td></tr>"
                html += "</table>"

    # DNS
    if 'dns' in resultats['modules']:
        dns = resultats['modules']['dns']
        html += f"""
        <h2>DNS Enumeration</h2>
        <p><strong>IP:</strong> {dns.get('ip', 'N/A')}</p>
        <p><strong>Hostname:</strong> {dns.get('hostname', 'N/A')}</p>
        """

    html += """
    </div>
</body>
</html>
    """

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
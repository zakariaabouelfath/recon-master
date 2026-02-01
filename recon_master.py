#!/usr/bin/env python3
"""
RECON MASTER v1.0
Advanced Network Reconnaissance Toolkit
Author: Zakaria Abouelfat
Date: 2025-02-01
"""

import sys
import os
import time
import argparse
import json
from datetime import datetime

# Modules custom
try:
    from modules import scanner, web_scan, enumeration, reporter
except ImportError:
    print("⚠️  Erreur : Modules manquants. Assurez-vous que le dossier 'modules/' existe.")
    sys.exit(1)

# ============================================
# CONFIGURATION
# ============================================

VERSION = "1.0"
BANNER = f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗           ║
║   ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║           ║
║   ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║           ║
║   ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║           ║
║   ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║           ║
║   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝           ║
║                                                           ║
║        M A S T E R    v{VERSION}                            ║
║        Advanced Network Reconnaissance                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""


# ============================================
# FONCTIONS PRINCIPALES
# ============================================

def afficher_banner():
    """Affiche le banner"""
    os.system('clear' if sys.platform != 'win32' else 'cls')
    print(BANNER)
    print(f"  🎯 Author : Zakaria Abouelfat")
    print(f"  📅 Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  💻 Python : {sys.version.split()[0]}")
    print(f"  🖥️  System : {sys.platform}")
    print("=" * 63)
    print()


def charger_config():
    """Charge configuration depuis config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Configuration par défaut
        config = {
            "timeout": 1,
            "threads": 10,
            "user_agent": "ReconMaster/1.0",
            "output_dir": "reports"
        }
        # Sauvegarder config par défaut
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        return config


def creer_dossiers():
    """Crée dossiers nécessaires"""
    dossiers = ['reports', 'wordlists', 'modules']
    for dossier in dossiers:
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            print(f"📁 Dossier créé : {dossier}")


def valider_cible(cible):
    """Valide format cible (IP ou domaine)"""
    import re

    # Pattern IP
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    # Pattern domaine
    domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$'

    if re.match(ip_pattern, cible) or re.match(domain_pattern, cible):
        return True
    return False


def mode_interactif():
    """Mode interactif si pas d'arguments"""
    print("🎯 MODE INTERACTIF\n")

    cible = input("Entre la cible (IP ou domaine) : ").strip()

    if not valider_cible(cible):
        print("❌ Format cible invalide")
        sys.exit(1)

    print("\n📋 Modules disponibles :")
    print("  1. Scan réseau (Ping sweep + Port scan)")
    print("  2. Web scanning (HTTP + Directories)")
    print("  3. DNS enumeration")
    print("  4. Scan complet (ALL)")

    choix = input("\nChoix (1-4) : ").strip()

    modules_map = {
        "1": ["network"],
        "2": ["web"],
        "3": ["dns"],
        "4": ["network", "web", "dns"]
    }

    modules = modules_map.get(choix, ["network"])

    return cible, modules


def executer_scan(cible, modules_actifs, config):
    """Exécute scan selon modules activés"""

    print(f"\n🎯 Cible : {cible}")
    print(f"📦 Modules : {', '.join(modules_actifs)}")
    print(f"⏱️  Timeout : {config['timeout']}s")
    print()

    resultats = {
        "cible": cible,
        "timestamp": datetime.now().isoformat(),
        "modules": {}
    }

    # Module Network Scanning
    if "network" in modules_actifs:
        print("=" * 63)
        print("🔍 MODULE : NETWORK SCANNING")
        print("=" * 63)

        # Ping test
        print("\n[*] Test connectivité...")
        alive = scanner.ping_host(cible, config['timeout'])
        resultats['modules']['network'] = {'alive': alive}

        if alive:
            print(f"✅ {cible} est accessible")

            # Port scan
            print("\n[*] Scan ports...")
            ports_ouverts = scanner.scan_ports(
                cible,
                range(1, 1001),
                config['timeout']
            )

            resultats['modules']['network']['ports'] = ports_ouverts

            if ports_ouverts:
                print(f"\n✅ {len(ports_ouverts)} port(s) ouvert(s)")
                for port_info in ports_ouverts:
                    print(f"   {port_info['port']:5d} → {port_info['service']}")
            else:
                print("\n❌ Aucun port ouvert (1-1000)")
        else:
            print(f"❌ {cible} ne répond pas au ping")

    # Module Web Scanning
    if "web" in modules_actifs:
        print("\n" + "=" * 63)
        print("🌐 MODULE : WEB SCANNING")
        print("=" * 63)

        # Détecter protocole
        url = cible if cible.startswith('http') else f"http://{cible}"

        print(f"\n[*] Test {url}...")
        web_info = web_scan.scan_website(url, config)
        resultats['modules']['web'] = web_info

        if web_info['accessible']:
            print(f"✅ Site accessible (code {web_info['status_code']})")

            # Headers sécurité
            if web_info['headers_manquants']:
                print(f"\n⚠️  {len(web_info['headers_manquants'])} header(s) sécurité manquant(s)")
                for header in web_info['headers_manquants']:
                    print(f"   - {header}")

            # Directory enumeration
            print("\n[*] Énumération directories...")
            dirs_trouves = web_scan.enum_directories(url, config)
            resultats['modules']['web']['directories'] = dirs_trouves

            if dirs_trouves:
                print(f"✅ {len(dirs_trouves)} directory/fichier(s) trouvé(s)")
                for d in dirs_trouves[:10]:  # Top 10
                    print(f"   /{d['path']} ({d['code']})")
        else:
            print(f"❌ Site inaccessible")

    # Module DNS
    if "dns" in modules_actifs:
        print("\n" + "=" * 63)
        print("🔎 MODULE : DNS ENUMERATION")
        print("=" * 63)

        dns_info = enumeration.dns_recon(cible)
        resultats['modules']['dns'] = dns_info

        if dns_info['ip']:
            print(f"✅ IP : {dns_info['ip']}")
        if dns_info['hostname']:
            print(f"✅ Hostname : {dns_info['hostname']}")

    return resultats


def generer_rapports(resultats, config):
    """Génère rapports multiples formats"""

    cible = resultats['cible'].replace('.', '_').replace(':', '_')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = f"{config['output_dir']}/recon_{cible}_{timestamp}"

    print("\n" + "=" * 63)
    print("📊 GÉNÉRATION RAPPORTS")
    print("=" * 63)

    # Rapport JSON
    reporter.generer_json(resultats, f"{base_filename}.json")
    print(f"✅ JSON  : {base_filename}.json")

    # Rapport TXT
    reporter.generer_txt(resultats, f"{base_filename}.txt")
    print(f"✅ TXT   : {base_filename}.txt")

    # Rapport HTML
    reporter.generer_html(resultats, f"{base_filename}.html")
    print(f"✅ HTML  : {base_filename}.html")

    # Rapport CSV (si ports trouvés)
    if 'network' in resultats['modules'] and resultats['modules']['network'].get('ports'):
        reporter.generer_csv(resultats, f"{base_filename}.csv")
        print(f"✅ CSV   : {base_filename}.csv")

    print()


# ============================================
# MAIN
# ============================================

def main():
    """Fonction principale"""

    # Parser arguments
    parser = argparse.ArgumentParser(
        description='RECON MASTER - Advanced Network Reconnaissance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python recon_master.py -t 192.168.1.1
  python recon_master.py -t example.com -m network,web
  python recon_master.py -t 10.0.0.1 --timeout 2
  python recon_master.py  (mode interactif)
        """
    )

    parser.add_argument('-t', '--target', help='Cible (IP ou domaine)')
    parser.add_argument('-m', '--modules', help='Modules (network,web,dns)', default='network')
    parser.add_argument('--timeout', type=int, help='Timeout connexion (secondes)')
    parser.add_argument('-q', '--quiet', action='store_true', help='Mode silencieux')
    parser.add_argument('-v', '--version', action='version', version=f'Recon Master v{VERSION}')

    args = parser.parse_args()

    # Banner
    if not args.quiet:
        afficher_banner()

    # Créer dossiers
    creer_dossiers()

    # Charger config
    config = charger_config()

    # Override timeout si spécifié
    if args.timeout:
        config['timeout'] = args.timeout

    # Déterminer cible et modules
    if args.target:
        cible = args.target
        modules = args.modules.split(',')

        if not valider_cible(cible):
            print("❌ Format cible invalide")
            sys.exit(1)
    else:
        # Mode interactif
        cible, modules = mode_interactif()

    # Exécuter scan
    print("\n🚀 Démarrage scan...")
    debut = time.time()

    try:
        resultats = executer_scan(cible, modules, config)

        # Générer rapports
        generer_rapports(resultats, config)

        duree = time.time() - debut

        # Résumé final
        print("=" * 63)
        print("✅ SCAN TERMINÉ")
        print("=" * 63)
        print(f"⏱️  Durée : {duree:.2f}s")
        print(f"📁 Rapports : {config['output_dir']}/")
        print()

    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrompu par utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
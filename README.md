# 🎯 RECON MASTER v1.0

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-red.svg)

Advanced Network Reconnaissance Toolkit

---

## 📋 Description

Recon Master est un outil professionnel de reconnaissance réseau développé en Python.
Il intègre plusieurs modules pour effectuer des scans complets de sécurité.

## ✨ Fonctionnalités

- 🔍 **Network Scanning**
  - Ping sweep (ICMP)
  - Port scanning (TCP) multi-threaded
  - Service detection automatique
  - Scan rapide ou complet

- 🌐 **Web Scanning**
  - Test accessibilité HTTP/HTTPS
  - Analyse headers sécurité
  - Directory enumeration
  - Détection serveur web

- 🔎 **DNS Enumeration**
  - Résolution DNS
  - Reverse DNS lookup
  - Subdomain enumeration (à venir)

- 📊 **Reporting Multi-format**
  - JSON (structuré)
  - TXT (lisible)
  - CSV (import Excel)
  - HTML (visualisation)

## 🚀 Installation
```bash
# Cloner le repository
git clone https://github.com/zakariaabouelfath/recon-master.git
cd recon-master

# Installer dépendances
pip install -r requirements.txt

# Tester
python recon_master.py --help
```

## 💻 Utilisation

### Mode interactif
```bash
python recon_master.py
```

### Mode ligne de commande
```bash
# Scan réseau simple
python recon_master.py -t 192.168.1.1

# Scan web uniquement
python recon_master.py -t example.com -m web

# Scan complet (network + web + dns)
python recon_master.py -t target.com -m network,web,dns

# Custom timeout
python recon_master.py -t 192.168.1.1 --timeout 2
```

## 📂 Structure du projet
```
recon_master/
├── recon_master.py       # Script principal
├── modules/
│   ├── __init__.py
│   ├── scanner.py        # Network scanning
│   ├── web_scan.py       # Web vulnerability scanning
│   ├── enumeration.py    # DNS enumeration
│   └── reporter.py       # Report generation
├── wordlists/
│   ├── directories.txt
│   └── subdomains.txt
├── reports/              # Generated reports
├── config.json           # Configuration
├── requirements.txt      # Dependencies
└── README.md
```

## ⚙️ Configuration

Modifier `config.json` pour personnaliser :
```json
{
  "timeout": 1,
  "threads": 50,
  "user_agent": "ReconMaster/1.0",
  "output_dir": "reports"
}
```

## 📝 Exemples de sortie

Les rapports sont générés dans le dossier `reports/` :
```
reports/
├── recon_192_168_1_1_20250201_120000.json
├── recon_192_168_1_1_20250201_120000.txt
├── recon_192_168_1_1_20250201_120000.html
└── recon_192_168_1_1_20250201_120000.csv
```

## 🛡️ Disclaimer

**⚠️ Important :** Cet outil est destiné à un usage **éducatif** et pour des **tests autorisés uniquement**.

L'utilisation de cet outil contre des systèmes sans autorisation explicite est **illégale**.
L'auteur n'est pas responsable de toute utilisation malveillante.

## 🎓 Compétences démontrées

- Python avancé (modules, threading, OOP)
- Programmation réseau (sockets, TCP/IP)
- Sécurité web (HTTP, headers, vulnerabilities)
- Manipulation de fichiers (JSON, CSV, HTML)
- Interface CLI professionnelle (argparse)
- Documentation technique
- Architecture logicielle modulaire

## 👨‍💻 Auteur

**Zakaria Abouelfat**
- GitHub: [@zakariaabouelfath](https://github.com/zakariaabouelfath)
- LinkedIn: [Zakaria Abouelfat](https://www.linkedin.com/in/zakaria-abouelfat)

## 📄 Licence

MIT License - Libre d'utilisation pour l'apprentissage

## 🤝 Contributions

Les contributions, issues et feature requests sont les bienvenues !

## 📬 Contact

Pour toute question ou suggestion : [GitHub Issues](https://github.com/zakariaabouelfath/recon-master/issues)

---

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !
```

---

## **ÉTAPE 2 : Crée `requirements.txt`**

**À la racine, crée fichier `requirements.txt` :**
```
requests>=2.28.0   
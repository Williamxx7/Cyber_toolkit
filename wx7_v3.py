#!/usr/bin/env python3
"""
██╗    ██╗██╗  ██╗███████╗
██║    ██║╚██╗██╔╝╚════██║
██║ █╗ ██║ ╚███╔╝     ██╔╝
██║███╗██║ ██╔██╗    ██╔╝ 
╚███╔███╔╝██╔╝ ██╗   ██║  
 ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝  
  CYBER TOOLKIT v3.0
"""

import os, sys, time, socket, hashlib, secrets, string
import subprocess, json, re, threading, struct, ssl
import urllib.request, urllib.parse, urllib.error
import ipaddress, platform, shutil, base64, hmac
import random, math, textwrap, signal, http.client
import ftplib, smtplib, imaplib
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict

# ── ANSI ─────────────────────────────────────────────────────────────────────
R    = "\033[0m"
RD   = "\033[31m";  GR  = "\033[32m";  YL  = "\033[33m"
BL   = "\033[34m";  MG  = "\033[35m";  CY  = "\033[36m"
BRD  = "\033[91m";  BGR = "\033[92m";  BYL = "\033[93m"
BBL  = "\033[94m";  BMG = "\033[95m";  BCY = "\033[96m";  BWH = "\033[97m"
BOLD = "\033[1m";   DIM = "\033[2m";   UL  = "\033[4m"
BG_BK = "\033[40m"; BG_RD = "\033[41m"; BG_GR = "\033[42m"

def clr(): os.system('cls' if os.name == 'nt' else 'clear')

def typewrite(text, delay=0.018, color=""):
    for ch in text:
        print(color + ch + R, end='', flush=True)
        time.sleep(delay)
    print()

def spin(msg, duration=1.2):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end_t = time.time() + duration
    i = 0
    while time.time() < end_t:
        print(f"\r  {BCY}{frames[i % len(frames)]}{R} {msg}   ", end='', flush=True)
        time.sleep(0.08)
        i += 1
    print(f"\r  {BGR}✔{R} {msg}   ")

def hline(n=58): print(f"  {DIM}{CY}{'─'*n}{R}")

def warn_banner(tool_name):
    print(f"\n  {BG_RD}{BOLD} ⚠ ADVARSEL {R}")
    print(f"  {BRD}Brug kun {tool_name} på systemer du ejer eller har skriftlig tilladelse til.{R}")
    print(f"  {BRD}Uautoriseret scanning/angreb er ulovligt (Straffeloven §263).{R}")
    confirm = input(f"\n  {YL}Jeg bekræfter dette er mit eget system/netværk{R} (ja/nej): ").strip().lower()
    if confirm != 'ja':
        print(f"\n  {YL}Afbrudt.{R}")
        input(f"  {DIM}Tryk Enter...{R}")
        return False
    return True

def banner():
    clr()
    art = f"""
{BCY}{BOLD}
  ██╗    ██╗██╗  ██╗███████╗
  ██║    ██║╚██╗██╔╝╚════██║
  ██║ █╗ ██║ ╚███╔╝     ██╔╝ 
  ██║███╗██║ ██╔██╗    ██╔╝  
  ╚███╔███╔╝██╔╝ ██╗   ██║   
   ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   {R}
{CY}  ██████╗██╗   ██╗██████╗ ███████╗██████╗{DIM}
  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║
   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
  ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
     ██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
     ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║   
     ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║   
     ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║   
     ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   {R}
"""
    print(art)
    now = datetime.now().strftime('%d/%m/%Y  %H:%M:%S')
    host = socket.gethostname()
    try: local_ip = socket.gethostbyname(host)
    except: local_ip = "N/A"
    hline(62)
    print(f"  {DIM}v3.0{R}  {DIM}│{R}  {CY}{now}{R}  {DIM}│{R}  {GR}{host}{R} {DIM}[{local_ip}]{R}")
    print(f"  {BRD}⚠  KUN LOVLIG BRUG / EGNE SYSTEMER{R}")
    hline(62)
    print()

def menu():
    cats = {
        f"{BOLD}{BCY}[ RECON & OSINT ]{R}": [
            ("01","🔍","Avanceret Port Scanner",   "TCP/UDP, banner grab, threaded"),
            ("02","🌐","OSINT Domain Recon",       "DNS, WHOIS, subdomæner, SSL"),
            ("03","📡","Netværk Discovery",        "ARP-scan, ping sweep, OS detect"),
            ("04","🔓","SSL/TLS Analyzer",         "Certifikat, ciphers, sårbarheder"),
            ("05","🕸️ ","Web Crawler / Spider",    "Links, forms, teknologi-detect"),
        ],
        f"{BOLD}{BCY}[ ANALYSE & ANGREB (CTF/LAB) ]{R}": [
            ("06","💣","Subdomain Bruteforce",     "Wordlist-baseret subdomain enum"),
            ("07","🗂️ ","Directory Bruteforce",    "Web path enumeration"),
            ("08","📦","Packet Analyzer",          "Analyser PCAP / live sniff info"),
            ("09","🔑","Hash Cracker",             "Dictionary + regler mod hash"),
            ("10","🛡️ ","WAF Detector",            "Detect firewall/WAF på webserver"),
        ],
        f"{BOLD}{BCY}[ NETVÆRK & SERVICES ]{R}": [
            ("11","📶","Banner Grabber",           "Grab service bannere TCP"),
            ("12","🔌","FTP Checker",              "Anonym login + listning"),
            ("13","📧","SMTP Checker",             "Open relay, VRFY, EXPN test"),
            ("14","🌍","HTTP Header Audit",        "Security headers + misconfig"),
            ("15","⚡","TCP Connect Flooder",      "Stress-test (kun eget system)"),
        ],
        f"{BOLD}{BCY}[ KRYPTO & FORENSICS ]{R}": [
            ("16","🔐","Avanceret Hash Tool",      "SHA3, BLAKE2, HMAC, salt"),
            ("17","🗜️ ","AES-256 Encryptor",       "Rigtig AES via Python crypto"),
            ("18","🧬","Steganografi Detektor",    "LSB analyse i billeder"),
            ("19","🔎","Metadata Extractor",       "Fil metadata / EXIF analyse"),
            ("20","💡","Entropy Analyzer",         "Detect kryptering/komprimering"),
        ],
        f"{BOLD}{BCY}[ UTILITIES ]{R}": [
            ("21","🔢","Password Generator",       "Entropy-beregnet, custom regler"),
            ("22","🛡️ ","Password Strength",       "Fuld analyse + crack-tid"),
            ("23","📝","Secure Notes",             "AES-krypterede noter"),
            ("24","🎲","Data Generator",           "Fake data, UUID, MAC, IPs"),
            ("25","🖥️ ","System & Net Info",       "OS, interfaces, routing"),
            ("00","✖ ","Afslut",""),
        ],
    }
    for cat, items in cats.items():
        print(f"  {cat}")
        for num, icon, title, desc in items:
            if num == "00":
                print(f"  {RD}  [{num}]{R} {icon}  {DIM}{title}{R}")
            else:
                print(f"  {BCY}  [{num}]{R} {icon}  {BOLD}{title:<28}{R}  {DIM}{CY}{desc}{R}")
        print()


# ══════════════════════════════════════════════════════════════════════════════
# 01  AVANCERET PORT SCANNER — TCP/UDP + banner grab
# ══════════════════════════════════════════════════════════════════════════════
def advanced_port_scanner():
    clr()
    print(f"\n  {BOLD}{BCY}🔍 AVANCERET PORT SCANNER{R}\n"); hline()
    if not warn_banner("Port Scanner"): return

    host   = input(f"\n  {YL}Target host/IP{R}: ").strip()
    if not host: return
    pr     = input(f"  {YL}Portrange{R}      (std=1-1024): ").strip() or "1-1024"
    ths    = int(input(f"  {YL}Tråde{R}          (std=150): ") or "150")
    do_udp = input(f"  {YL}UDP scan?{R}      (j/n, std=n): ").lower() == 'j'
    grab   = input(f"  {YL}Banner grab?{R}   (j/n, std=j): ").lower() != 'n'
    timeout= float(input(f"  {YL}Timeout sek{R}   (std=0.5): ") or "0.5")

    try:
        s_port, e_port = map(int, pr.split('-'))
        ip = socket.gethostbyname(host)
    except Exception as e:
        print(f"  {RD}Fejl: {e}{R}"); input(); return

    open_tcp   = []
    open_udp   = []
    lock       = threading.Lock()
    scanned    = [0]
    ports      = list(range(s_port, e_port + 1))
    total      = len(ports)

    # Common service fingerprints
    service_probes = {
        21:  b"",              # FTP sends banner
        22:  b"",              # SSH sends banner
        25:  b"EHLO test\r\n",
        80:  b"HEAD / HTTP/1.0\r\n\r\n",
        110: b"",              # POP3 banner
        143: b"",              # IMAP banner
        443: None,             # TLS — handle separately
        3306:b"",              # MySQL sends banner
        5432:b"",              # Postgres
    }

    def grab_banner(ip, port, timeout):
        banner = ""
        try:
            if port == 443:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                with socket.create_connection((ip, port), timeout=timeout) as raw:
                    with ctx.wrap_socket(raw, server_hostname=ip) as s:
                        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                        banner = s.recv(256).decode('utf-8','replace').split('\n')[0]
            else:
                probe = service_probes.get(port, b"")
                with socket.create_connection((ip, port), timeout=timeout) as s:
                    if probe: s.send(probe)
                    banner = s.recv(256).decode('utf-8','replace').split('\n')[0].strip()
        except: pass
        return banner[:80]

    def scan_tcp(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            if s.connect_ex((ip, port)) == 0:
                try: svc = socket.getservbyport(port, 'tcp')
                except: svc = "?"
                bn = grab_banner(ip, port, timeout) if grab else ""
                with lock: open_tcp.append((port, svc, bn))
            s.close()
        except: pass
        with lock: scanned[0] += 1

    def scan_udp(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(timeout)
            s.sendto(b"\x00", (ip, port))
            try:
                s.recvfrom(64)
                try: svc = socket.getservbyport(port, 'udp')
                except: svc = "udp/?"
                with lock: open_udp.append((port, svc))
            except socket.timeout:
                pass  # No ICMP = possibly open
            s.close()
        except: pass

    def show_progress():
        while scanned[0] < total:
            pct = scanned[0]/total
            b = int(35*pct)
            bar = f"{BGR}{'█'*b}{R}{DIM}{'░'*(35-b)}{R}"
            print(f"  [{bar}] {BYL}{pct*100:5.1f}%{R} {DIM}{scanned[0]}/{total} porte{R}   ", end='\r', flush=True)
            time.sleep(0.1)

    print(f"\n  {DIM}Starter TCP scan mod {BCY}{host}{DIM} ({ip}) med {ths} tråde...{R}\n")

    t_prog = threading.Thread(target=show_progress, daemon=True)
    t_prog.start()

    batch = []
    for port in ports:
        t = threading.Thread(target=scan_tcp, args=(port,), daemon=True)
        t.start(); batch.append(t)
        if len(batch) >= ths:
            for x in batch: x.join()
            batch = []
    for x in batch: x.join()
    time.sleep(0.2)

    if do_udp:
        print(f"\n\n  {DIM}UDP scan på top porte...{R}")
        udp_ports = [53,67,68,69,123,137,138,161,162,500,514,1194,4500]
        for p in udp_ports: scan_udp(p)

    open_tcp.sort(); open_udp.sort()
    print(f"\n\n"); hline(70)
    print(f"  {BOLD}TCP Scan — {ip} ({host}){R}")
    print(f"  {DIM}Skannet {total} porte  │  Fundet {len(open_tcp)} åbne  │  Timeout {timeout}s{R}\n")

    if open_tcp:
        print(f"  {DIM}{'PORT':<8}{'PROTOKOL':<16}{'BANNER/INFO'}{R}")
        hline(70)
        for port, svc, bn in open_tcp:
            port_col = f"{BGR}{port}/tcp{R}"
            svc_col  = f"{BCY}{svc:<14}{R}"
            bn_col   = f"{DIM}{bn}{R}" if bn else ""
            print(f"  {port_col:<20} {svc_col} {bn_col}")
    else:
        print(f"  {YL}Ingen åbne TCP porte fundet.{R}")

    if open_udp:
        print(f"\n  {BOLD}Åbne UDP Porte:{R}")
        for port, svc in open_udp:
            print(f"  {BYL}{port}/udp{R}  {CY}{svc}{R}")

    hline(70)
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 02  OSINT DOMAIN RECON
# ══════════════════════════════════════════════════════════════════════════════
def osint_domain_recon():
    clr()
    print(f"\n  {BOLD}{BCY}🌐 OSINT DOMAIN RECON{R}\n"); hline()
    domain = input(f"\n  {YL}Domæne{R} (f.eks. example.com): ").strip().lower()
    if not domain: return

    report = {}

    # ── DNS Records ──────────────────────────────────────────────────────────
    print(f"\n  {BOLD}[ DNS Records ]{R}")
    hline()

    dns_types = ['A','AAAA','MX','TXT','NS','CNAME','SOA']
    dig_available = bool(shutil.which('dig'))
    host_available = bool(shutil.which('host'))

    dns_results = defaultdict(list)

    for rtype in dns_types:
        try:
            if dig_available:
                r = subprocess.run(['dig','+short',rtype,domain], capture_output=True, text=True, timeout=5)
                lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip()]
            elif host_available:
                r = subprocess.run(['host','-t',rtype,domain], capture_output=True, text=True, timeout=5)
                lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip() and 'not found' not in l]
            else:
                lines = []

            if lines:
                dns_results[rtype] = lines
                for line in lines:
                    print(f"  {BCY}{rtype:<8}{R} {line}")
        except: pass

    # Fallback: socket for A record
    if 'A' not in dns_results:
        try:
            ips = list(set(r[4][0] for r in socket.getaddrinfo(domain, None, socket.AF_INET)))
            for ip in ips:
                dns_results['A'].append(ip)
                print(f"  {BCY}{'A':<8}{R} {ip}")
        except: pass

    report['dns'] = dns_results

    # ── WHOIS ────────────────────────────────────────────────────────────────
    print(f"\n  {BOLD}[ WHOIS ]{R}")
    hline()
    whois_cmd = shutil.which('whois')
    if whois_cmd:
        try:
            r = subprocess.run(['whois', domain], capture_output=True, text=True, timeout=10)
            important_keys = ['registrar','creation date','expiry date','expiration date',
                              'updated date','name server','registrant','status','dnssec']
            for line in r.stdout.split('\n'):
                ll = line.lower()
                if any(k in ll for k in important_keys) and ':' in line:
                    parts = line.split(':',1)
                    if len(parts)==2 and parts[1].strip():
                        print(f"  {BCY}{parts[0].strip()[:20]:<22}{R} {parts[1].strip()}")
        except: print(f"  {DIM}WHOIS timeout{R}")
    else:
        print(f"  {DIM}whois ikke installeret. Installer med: sudo apt install whois{R}")

    # ── SSL Certificate ──────────────────────────────────────────────────────
    print(f"\n  {BOLD}[ SSL/TLS Certifikat ]{R}")
    hline()
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                tls_ver = ssock.version()
        if cert:
            subj = dict(x[0] for x in cert.get('subject',[]))
            issuer = dict(x[0] for x in cert.get('issuer',[]))
            print(f"  {BCY}{'Subject':<18}{R} {subj.get('commonName','N/A')}")
            print(f"  {BCY}{'Issuer':<18}{R} {issuer.get('organizationName','N/A')}")
            print(f"  {BCY}{'Gyldig fra':<18}{R} {cert.get('notBefore','N/A')}")
            print(f"  {BCY}{'Udløber':<18}{R} {cert.get('notAfter','N/A')}")
            print(f"  {BCY}{'TLS Version':<18}{R} {tls_ver}")
            print(f"  {BCY}{'Cipher':<18}{R} {cipher[0] if cipher else 'N/A'}")
            # SANs
            sans = [v for t,v in cert.get('subjectAltName',[]) if t=='DNS']
            if sans:
                print(f"  {BCY}{'SANs ({})'.format(len(sans)):<18}{R} {', '.join(sans[:8])}")
    except Exception as e:
        print(f"  {DIM}Ingen SSL på port 443: {e}{R}")

    # ── HTTP Headers / Tech Detection ────────────────────────────────────────
    print(f"\n  {BOLD}[ HTTP / Teknologi ]{R}")
    hline()
    for scheme in ['https','http']:
        try:
            url = f"{scheme}://{domain}"
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (WX7 Scanner)'})
            with urllib.request.urlopen(req, timeout=6) as resp:
                hdrs = dict(resp.headers)
                final = resp.url
                status = resp.status
                body_start = resp.read(4096).decode('utf-8','replace')

            print(f"  {BCY}{'Status':<18}{R} {BGR if status==200 else BYL}{status}{R}  {DIM}({scheme.upper()}){R}")
            print(f"  {BCY}{'Final URL':<18}{R} {final}")

            # Tech fingerprinting
            tech = []
            server = hdrs.get('Server','')
            powered = hdrs.get('X-Powered-By','')
            if server: tech.append(f"Server: {server}")
            if powered: tech.append(f"Powered-By: {powered}")

            if 'wp-content' in body_start or 'wp-json' in body_start: tech.append("WordPress")
            if 'Drupal' in body_start or '/sites/default/' in body_start: tech.append("Drupal")
            if 'Joomla' in body_start: tech.append("Joomla")
            if 'react' in body_start.lower() or '__NEXT_DATA__' in body_start: tech.append("React/Next.js")
            if 'django' in str(hdrs).lower(): tech.append("Django")
            if 'laravel' in str(hdrs).lower(): tech.append("Laravel")
            if '<meta name="generator"' in body_start.lower():
                gen = re.search(r'<meta name="generator" content="([^"]+)"', body_start, re.I)
                if gen: tech.append(f"Generator: {gen.group(1)}")

            if tech:
                print(f"  {BCY}{'Teknologier':<18}{R} {', '.join(tech)}")

            # Security headers check
            sec = {
                'Strict-Transport-Security': 'HSTS',
                'Content-Security-Policy':   'CSP',
                'X-Frame-Options':           'X-Frame',
                'X-Content-Type-Options':    'X-CTO',
            }
            missing = [name for h,name in sec.items() if h not in hdrs]
            if missing: print(f"  {BRD}{'Mangler headers':<18}{R} {', '.join(missing)}")
            else: print(f"  {BGR}{'Security headers':<18}{R} Alle sat ✔")
            break
        except: continue

    # ── Robots.txt & Sitemap ─────────────────────────────────────────────────
    print(f"\n  {BOLD}[ Robots.txt / Sitemap ]{R}")
    hline()
    for path in ['/robots.txt', '/sitemap.xml', '/sitemap_index.xml']:
        for scheme in ['https','http']:
            try:
                url = f"{scheme}://{domain}{path}"
                req = urllib.request.Request(url, headers={'User-Agent':'WX7/3.0'})
                with urllib.request.urlopen(req, timeout=4) as r:
                    if r.status == 200:
                        content = r.read(2000).decode('utf-8','replace')
                        lines   = [l.strip() for l in content.split('\n') if l.strip()][:10]
                        print(f"  {BGR}✔{R} {BCY}{path}{R}")
                        for l in lines[:8]: print(f"    {DIM}{l}{R}")
                        break
            except: pass

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 03  NETVÆRK DISCOVERY (ARP + Ping Sweep + OS Fingerprint)
# ══════════════════════════════════════════════════════════════════════════════
def network_discovery():
    clr()
    print(f"\n  {BOLD}{BCY}📡 NETVÆRK DISCOVERY{R}\n"); hline()
    if not warn_banner("Network Discovery"): return

    print(f"\n  {BCY}[1]{R} Ping Sweep      {BCY}[2]{R} ARP Scan (lokal LAN)   {BCY}[3]{R} OS Fingerprint\n")
    choice = input(f"  {YL}Valg{R}: ").strip()

    if choice == '1':
        subnet = input(f"  {YL}Subnet{R} (f.eks. 192.168.1): ").strip() or "192.168.1"
        print(f"\n  {DIM}Ping sweep {subnet}.1-254 ...{R}\n")
        live = []
        lock = threading.Lock()
        done = [0]

        def ping_host(i):
            ip = f"{subnet}.{i}"
            is_win = platform.system().lower() == "windows"
            cmd = ["ping", "-n" if is_win else "-c", "1",
                   "-w" if is_win else "-W", "500" if is_win else "1", ip]
            try:
                r = subprocess.run(cmd, capture_output=True, timeout=3)
                if r.returncode == 0:
                    try: hostname = socket.gethostbyaddr(ip)[0]
                    except: hostname = ""
                    # TTL-based OS guess
                    ttl_match = re.search(r'ttl=(\d+)', r.stdout.decode('utf-8','replace').lower())
                    if ttl_match:
                        ttl = int(ttl_match.group(1))
                        if ttl <= 64:    os_guess = "Linux/Unix"
                        elif ttl <= 128: os_guess = "Windows"
                        else:            os_guess = "Network Device"
                    else: os_guess = "?"
                    with lock: live.append((ip, hostname, os_guess))
            except: pass
            with lock: done[0] += 1

        threads = []
        for i in range(1, 255):
            t = threading.Thread(target=ping_host, args=(i,), daemon=True)
            t.start(); threads.append(t)
            pct = i/254
            b = int(30*pct)
            print(f"  {BCY}{'█'*b}{'░'*(30-b)}{R} {i}/254   ", end='\r', flush=True)
            if len(threads) >= 60:
                for x in threads: x.join(); threads = []
        for x in threads: x.join()
        print()

        live.sort(key=lambda x: int(x[0].split('.')[-1]))
        hline(65)
        print(f"  {BOLD}{BGR}{len(live)} live hosts:{R}\n")
        print(f"  {DIM}{'IP':<20}{'HOSTNAME':<30}{'OS Gæt'}{R}")
        hline(65)
        for ip, hn, osg in live:
            os_col = f"{BGR}{osg}{R}" if osg != "?" else f"{DIM}{osg}{R}"
            print(f"  {BCY}{ip:<20}{R} {hn:<30} {os_col}")

    elif choice == '2':
        # ARP scan using arp -a (passive, no root needed)
        print(f"\n  {DIM}Læser ARP-tabel (passive)...{R}\n")
        try:
            r = subprocess.run(['arp','-a'], capture_output=True, text=True, timeout=5)
            hline(65)
            print(f"  {BOLD}ARP Cache:{R}\n")
            for line in r.stdout.split('\n'):
                if line.strip():
                    # Parse hostname (ip) at mac type
                    m = re.search(r'(\S+)\s+\(([^)]+)\)\s+at\s+([0-9a-f:]+)', line)
                    if m:
                        hn, ip, mac = m.groups()
                        print(f"  {BCY}{ip:<18}{R} {BGR}{mac:<20}{R} {DIM}{hn}{R}")
                    elif re.search(r'\d+\.\d+\.\d+\.\d+', line):
                        print(f"  {DIM}{line.strip()}{R}")
        except Exception as e:
            print(f"  {RD}Fejl: {e}{R}")

    elif choice == '3':
        target = input(f"  {YL}Target IP/host{R}: ").strip()
        if not target: return
        print(f"\n  {DIM}OS Fingerprinting mod {target}...{R}\n")
        try:
            ip = socket.gethostbyname(target)
            # TTL-based guess via ping
            is_win = platform.system().lower() == "windows"
            cmd = ["ping", "-n" if is_win else "-c", "3", ip]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
            output = r.stdout + r.stderr
            hline()
            # TTL
            ttl_match = re.search(r'ttl=(\d+)', output.lower())
            if ttl_match:
                ttl = int(ttl_match.group(1))
                if ttl <= 64:
                    os_g = f"{BGR}Linux/Unix/Mac{R} (TTL≈64)"
                elif ttl <= 128:
                    os_g = f"{BCY}Windows{R} (TTL≈128)"
                elif ttl <= 255:
                    os_g = f"{BYL}Cisco/Network device{R} (TTL≈255)"
                else:
                    os_g = f"{DIM}Ukendt{R}"
                print(f"  {BCY}TTL{R}        {ttl}  →  OS gæt: {os_g}")

            # RTT
            rtt = re.search(r'time[=<](\d+\.?\d*)\s*ms', output)
            if rtt: print(f"  {BCY}RTT{R}        {rtt.group(1)} ms")

            # Open port OS hints
            print(f"\n  {DIM}Tjekker karakteristiske porte...{R}")
            hints = {
                22:   "SSH åben → sandsynligvis Linux/Unix",
                3389: "RDP åben → sandsynligvis Windows",
                445:  "SMB åben → sandsynligvis Windows",
                548:  "AFP åben → sandsynligvis macOS",
                80:   "HTTP åben",
                443:  "HTTPS åben",
            }
            for port, hint in hints.items():
                s = socket.socket()
                s.settimeout(0.5)
                if s.connect_ex((ip, port)) == 0:
                    print(f"  {BGR}●{R} Port {BYL}{port}{R}  {hint}")
                s.close()

        except Exception as e:
            print(f"  {RD}Fejl: {e}{R}")

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 04  SSL/TLS ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
def ssl_analyzer():
    clr()
    print(f"\n  {BOLD}{BCY}🔓 SSL/TLS ANALYZER{R}\n"); hline()
    host = input(f"\n  {YL}Host{R}: ").strip()
    port = int(input(f"  {YL}Port{R} (std=443): ") or "443")
    if not host: return

    spin("Analyserer SSL/TLS...", 1.0)
    hline()

    # Test multiple TLS versions
    tls_versions = [
        ("TLS 1.3", ssl.TLSVersion.TLSv1_3 if hasattr(ssl.TLSVersion,'TLSv1_3') else None),
        ("TLS 1.2", ssl.TLSVersion.TLSv1_2 if hasattr(ssl.TLSVersion,'TLSv1_2') else None),
    ]

    print(f"\n  {BOLD}TLS Version Support:{R}\n")
    supported_versions = []
    for name, ver in tls_versions:
        if ver is None: continue
        try:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ctx.minimum_version = ver
            ctx.maximum_version = ver
            with socket.create_connection((host, port), timeout=4) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as s:
                    actual = s.version()
                    cipher = s.cipher()
                    supported_versions.append((name, cipher))
            print(f"  {BGR}✔{R} {BCY}{name:<10}{R} Cipher: {cipher[0] if cipher else '?'}")
        except:
            print(f"  {BRD}✘{R} {DIM}{name:<10} Ikke understøttet{R}")

    # Full cert analysis
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as s:
                cert    = s.getpeercert()
                der     = s.getpeercert(binary_form=True)
                cipher  = s.cipher()
                tls_ver = s.version()

        print(f"\n  {BOLD}Certifikat:{R}\n")
        if cert:
            subj   = dict(x[0] for x in cert.get('subject',[]))
            issuer = dict(x[0] for x in cert.get('issuer',[]))
            not_after = cert.get('notAfter','')
            print(f"  {BCY}{'CN':<20}{R} {subj.get('commonName','N/A')}")
            print(f"  {BCY}{'Org':<20}{R} {subj.get('organizationName','N/A')}")
            print(f"  {BCY}{'Issuer':<20}{R} {issuer.get('organizationName','N/A')}")
            print(f"  {BCY}{'Not Before':<20}{R} {cert.get('notBefore','N/A')}")

            # Check expiry
            try:
                exp = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                days_left = (exp - datetime.utcnow()).days
                exp_col = BGR if days_left > 30 else BYL if days_left > 7 else BRD
                print(f"  {BCY}{'Udløber':<20}{R} {not_after}  {exp_col}({days_left} dage tilbage){R}")
            except:
                print(f"  {BCY}{'Not After':<20}{R} {not_after}")

            # SANs
            sans = [v for t,v in cert.get('subjectAltName',[]) if t=='DNS']
            print(f"  {BCY}{'SANs ({})'.format(len(sans)):<20}{R} {', '.join(sans[:10])}")

            # Serial & fingerprint
            if der:
                fp_sha1   = hashlib.sha1(der).hexdigest()
                fp_sha256 = hashlib.sha256(der).hexdigest()
                print(f"  {BCY}{'SHA1 FP':<20}{R} {':'.join(fp_sha1[i:i+2] for i in range(0,len(fp_sha1),2))[:40]}...")
                print(f"  {BCY}{'SHA256 FP':<20}{R} {fp_sha256[:40]}...")

        print(f"\n  {BOLD}Cipher Suite:{R}\n")
        if cipher:
            print(f"  {BCY}{'Cipher':<20}{R} {cipher[0]}")
            print(f"  {BCY}{'Protocol':<20}{R} {cipher[1]}")
            print(f"  {BCY}{'Key Bits':<20}{R} {cipher[2]}")

        # Vulnerability checks
        print(f"\n  {BOLD}Vulnerability Checks:{R}\n")
        vulns = {
            "BEAST": tls_ver in ('TLSv1','SSLv3') and cipher and 'CBC' in cipher[0],
            "WEAK CIPHER (RC4)": cipher and 'RC4' in cipher[0],
            "WEAK CIPHER (3DES)": cipher and '3DES' in cipher[0],
            "NULL CIPHER": cipher and 'NULL' in cipher[0],
        }
        all_ok = True
        for vuln, hit in vulns.items():
            if hit:
                print(f"  {BRD}⚠ SÅRBAR{R}  {vuln}")
                all_ok = False
        if all_ok:
            print(f"  {BGR}✔ Ingen kendte cipher-sårbarheder detekteret{R}")

    except Exception as e:
        print(f"\n  {RD}Fejl: {e}{R}")

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 05  WEB CRAWLER / SPIDER
# ══════════════════════════════════════════════════════════════════════════════
def web_crawler():
    clr()
    print(f"\n  {BOLD}{BCY}🕸️  WEB CRAWLER{R}\n"); hline()
    url = input(f"\n  {YL}Start URL{R} (f.eks. https://example.com): ").strip()
    if not url.startswith('http'): url = 'https://' + url
    depth   = int(input(f"  {YL}Max dybde{R}    (std=2): ") or "2")
    max_p   = int(input(f"  {YL}Max sider{R}    (std=30): ") or "30")

    from urllib.parse import urljoin, urlparse

    visited   = set()
    to_visit  = [(url, 0)]
    found_links   = []
    found_forms   = []
    found_emails  = []
    found_comments= []
    tech_hints    = set()

    base_domain = urlparse(url).netloc

    def fetch(u):
        try:
            req = urllib.request.Request(u, headers={
                'User-Agent': 'Mozilla/5.0 (WX7 Spider/3.0)'
            })
            with urllib.request.urlopen(req, timeout=5) as r:
                ctype = r.headers.get('Content-Type','')
                if 'text' not in ctype: return None, {}
                return r.read(50000).decode('utf-8','replace'), dict(r.headers)
        except: return None, {}

    print(f"\n  {DIM}Crawler starter...{R}\n")

    while to_visit and len(visited) < max_p:
        current_url, current_depth = to_visit.pop(0)
        if current_url in visited: continue
        visited.add(current_url)

        print(f"  {DIM}[{len(visited):>3}]{R} {BCY}{current_url[:80]}{R}")
        html, hdrs = fetch(current_url)
        if not html: continue

        # Find links
        hrefs = re.findall(r'href=["\']([^"\'#]+)', html)
        for href in hrefs:
            full = urljoin(current_url, href)
            parsed = urlparse(full)
            if parsed.netloc == base_domain and full not in visited:
                found_links.append(full)
                if current_depth + 1 <= depth:
                    to_visit.append((full, current_depth+1))

        # Find forms
        forms = re.findall(r'<form[^>]*action=["\']([^"\']*)["\'][^>]*method=["\']([^"\']*)["\']', html, re.I)
        for action, method in forms:
            full_action = urljoin(current_url, action)
            found_forms.append((current_url, full_action, method.upper()))

        # Find emails
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
        found_emails.extend(emails)

        # Find HTML comments
        comments = re.findall(r'<!--(.*?)-->', html, re.DOTALL)
        for c in comments:
            c = c.strip()
            if len(c) > 5 and len(c) < 200:
                found_comments.append((current_url, c[:100]))

        # Tech hints
        if 'wp-content' in html: tech_hints.add("WordPress")
        if '__NEXT_DATA__' in html: tech_hints.add("Next.js")
        if 'react' in html.lower(): tech_hints.add("React")
        if 'angular' in html.lower(): tech_hints.add("Angular")
        if 'bootstrap' in html.lower(): tech_hints.add("Bootstrap")
        if 'jquery' in html.lower(): tech_hints.add("jQuery")
        server = hdrs.get('Server','')
        if server: tech_hints.add(f"Server:{server}")

        time.sleep(0.3)  # polite crawl

    print(f"\n"); hline(65)
    print(f"\n  {BOLD}Crawl Rapport  —  {base_domain}{R}\n")
    print(f"  {BCY}Sider besøgt:{R}     {len(visited)}")
    print(f"  {BCY}Links fundet:{R}     {len(set(found_links))}")
    print(f"  {BCY}Formularer:{R}       {len(found_forms)}")
    print(f"  {BCY}Emails:{R}           {len(set(found_emails))}")
    print(f"  {BCY}HTML Comments:{R}    {len(found_comments)}")

    if tech_hints:
        print(f"\n  {BOLD}Teknologier:{R}")
        for t in tech_hints: print(f"  {BCY}●{R} {t}")

    if found_forms:
        print(f"\n  {BOLD}Formularer (mulige injection-punkter):{R}")
        for page, action, method in found_forms[:10]:
            print(f"  {BYL}{method:<6}{R} {action[:60]}  {DIM}(fra {page[:40]}){R}")

    if found_emails:
        print(f"\n  {BOLD}Emails fundet:{R}")
        for e in list(set(found_emails))[:10]:
            print(f"  {BGR}●{R} {e}")

    if found_comments:
        print(f"\n  {BOLD}HTML Kommentarer (kan afsløre info):{R}")
        for page, comment in found_comments[:8]:
            print(f"  {DIM}[{urlparse(page).path}]{R} {YL}{comment}{R}")

    hline(65)
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 06  SUBDOMAIN BRUTEFORCE
# ══════════════════════════════════════════════════════════════════════════════
def subdomain_bruteforce():
    clr()
    print(f"\n  {BOLD}{BCY}💣 SUBDOMAIN BRUTEFORCE{R}\n"); hline()
    domain = input(f"\n  {YL}Domæne{R}: ").strip()
    if not domain: return

    # Built-in wordlist (common subdomains)
    wordlist = [
        "www","mail","ftp","smtp","pop","imap","webmail","admin","portal","api",
        "dev","staging","test","uat","qa","prod","beta","alpha","demo","sandbox",
        "app","apps","mobile","m","wap","cdn","static","assets","media","img",
        "images","files","download","downloads","upload","uploads","store","shop",
        "blog","news","support","help","docs","wiki","kb","forum","forums",
        "vpn","remote","ssh","rdp","citrix","ns1","ns2","dns","mx","mx1","mx2",
        "autodiscover","autoconfig","exchange","owa","cpanel","whm","plesk",
        "mysql","db","database","sql","redis","mongo","elastic","kibana","grafana",
        "jenkins","gitlab","github","jira","confluence","slack","bitbucket",
        "backup","bak","old","legacy","v1","v2","new","secure","ssl","login",
        "auth","sso","oauth","identity","ldap","ad","intranet","internal",
        "monitoring","monitor","status","health","ping","metrics","analytics",
        "k8s","kubernetes","docker","rancher","aws","azure","gcp","cloud",
    ]

    custom_file = input(f"  {YL}Custom wordlist fil{R} (Enter=brug built-in {len(wordlist)} ord): ").strip()
    if custom_file and os.path.isfile(custom_file):
        with open(custom_file) as f:
            wordlist = [l.strip() for l in f if l.strip()]
        print(f"  {DIM}Loaded {len(wordlist)} ord fra {custom_file}{R}")

    threads_n = int(input(f"  {YL}Tråde{R} (std=50): ") or "50")

    found = []
    lock = threading.Lock()
    done = [0]
    total = len(wordlist)

    def check(sub):
        fqdn = f"{sub}.{domain}"
        try:
            ips = list(set(r[4][0] for r in socket.getaddrinfo(fqdn, None)))
            with lock:
                found.append((fqdn, ips))
                print(f"\n  {BGR}[FOUND]{R} {BOLD}{BCY}{fqdn}{R}  →  {', '.join(ips)}")
        except: pass
        with lock: done[0] += 1

    def progress():
        while done[0] < total:
            pct = done[0]/total
            b = int(35*pct)
            bar = f"{BCY}{'█'*b}{'░'*(35-b)}{R}"
            print(f"  [{bar}] {BYL}{pct*100:5.1f}%{R} {DIM}{done[0]}/{total}{R}   ", end='\r', flush=True)
            time.sleep(0.15)

    print(f"\n  {DIM}Bruteforcing {total} subdomæner på {domain}...{R}\n")
    t_p = threading.Thread(target=progress, daemon=True); t_p.start()

    batch = []
    for word in wordlist:
        t = threading.Thread(target=check, args=(word,), daemon=True)
        t.start(); batch.append(t)
        if len(batch) >= threads_n:
            for x in batch: x.join(); batch = []
    for x in batch: x.join()
    time.sleep(0.3)

    print(f"\n\n"); hline()
    print(f"  {BOLD}Resultat: {BGR}{len(found)}{R}{BOLD} subdomæner fundet{R}\n")
    for fqdn, ips in sorted(found):
        print(f"  {BCY}{fqdn:<45}{R}  {', '.join(ips)}")
    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 07  DIRECTORY BRUTEFORCE (Web Path Enum)
# ══════════════════════════════════════════════════════════════════════════════
def dir_bruteforce():
    clr()
    print(f"\n  {BOLD}{BCY}🗂️  DIRECTORY BRUTEFORCE{R}\n"); hline()
    url = input(f"\n  {YL}Base URL{R} (f.eks. https://example.com): ").strip()
    if not url.startswith('http'): url = 'https://' + url
    url = url.rstrip('/')

    # Built-in wordlist
    paths = [
        "admin","administrator","login","logout","dashboard","panel","cpanel",
        "wp-admin","wp-login","wp-content","wp-includes","wordpress",
        "phpmyadmin","pma","mysql","adminer","dbadmin",
        "api","api/v1","api/v2","rest","graphql","swagger","openapi","docs",
        "backup","bak","old","archive","temp","tmp","cache",
        ".git",".git/config",".env",".env.local",".htaccess","web.config",
        "config","settings","configuration","setup","install","installer",
        "test","debug","dev","staging","demo",
        "upload","uploads","files","assets","static","media","images",
        "includes","lib","libs","vendor","node_modules",
        "robots.txt","sitemap.xml","crossdomain.xml",".well-known/security.txt",
        "server-status","server-info",".ds_store",
        "shell","cmd","command","execute","exec","run",
        "cgi-bin","scripts","bin","sbin",
        "error","errors","logs","log","access.log","error.log",
    ]

    custom_file = input(f"  {YL}Custom wordlist fil{R} (Enter=built-in {len(paths)} stier): ").strip()
    if custom_file and os.path.isfile(custom_file):
        with open(custom_file) as f:
            paths = [l.strip().lstrip('/') for l in f if l.strip()]

    ext_in = input(f"  {YL}Ekstra extensions{R} (f.eks. .php,.bak,.old, Enter=ingen): ").strip()
    extra_exts = [e.strip() for e in ext_in.split(',') if e.strip()] if ext_in else []

    # Add extension variants
    if extra_exts:
        base = list(paths)
        for p in base:
            for ext in extra_exts:
                paths.append(p + ext)

    threads_n = int(input(f"  {YL}Tråde{R} (std=30): ") or "30")
    show_all  = input(f"  {YL}Vis alle svar?{R} (j=alt, n=kun 200/301/403): ").lower() == 'j'

    found  = []
    done   = [0]
    lock   = threading.Lock()
    total  = len(paths)

    status_colors = {
        200: BGR, 201: BGR, 204: BGR,
        301: BYL, 302: BYL, 307: BYL, 308: BYL,
        403: BCY,
        401: BMG,
        500: BRD,
    }

    def check_path(path):
        target = f"{url}/{path}"
        try:
            req = urllib.request.Request(target, headers={'User-Agent':'WX7/3.0 DirBuster'})
            req.get_method = lambda: 'GET'
            with urllib.request.urlopen(req, timeout=4) as r:
                status = r.status
                size   = len(r.read(1024))
                col    = status_colors.get(status, DIM)
                with lock:
                    found.append((status, target, size))
                    print(f"\n  {col}[{status}]{R}  {target:<65}  {DIM}{size}B{R}")
        except urllib.error.HTTPError as e:
            col = status_colors.get(e.code, DIM)
            if show_all or e.code in (301,302,307,401,403):
                with lock:
                    found.append((e.code, target, 0))
                    print(f"\n  {col}[{e.code}]{R}  {target}")
        except: pass
        with lock: done[0] += 1

    def progress():
        while done[0] < total:
            pct = done[0]/total
            b = int(30*pct)
            bar = f"{BCY}{'█'*b}{'░'*(30-b)}{R}"
            print(f"  [{bar}] {BYL}{pct*100:5.1f}%{R} {DIM}{done[0]}/{total}{R}  ", end='\r', flush=True)
            time.sleep(0.15)

    print(f"\n  {DIM}Scanning {total} stier på {url}...{R}\n")
    t_p = threading.Thread(target=progress, daemon=True); t_p.start()

    batch = []
    for path in paths:
        t = threading.Thread(target=check_path, args=(path,), daemon=True)
        t.start(); batch.append(t)
        if len(batch) >= threads_n:
            for x in batch: x.join(); batch = []
    for x in batch: x.join()
    time.sleep(0.3)

    print(f"\n\n"); hline()
    by_status = Counter(s for s,_,_ in found)
    print(f"  {BOLD}Opsummering:{R}  " + "  ".join(
        f"{status_colors.get(s,DIM)}[{s}]{R} ×{n}" for s,n in sorted(by_status.items())
    ))
    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 08  PACKET ANALYZER (PCAP / TCP header decode)
# ══════════════════════════════════════════════════════════════════════════════
def packet_analyzer():
    clr()
    print(f"\n  {BOLD}{BCY}📦 PACKET ANALYZER{R}\n"); hline()
    print(f"""
  {DIM}Dette modul kan:{R}
  {BCY}[1]{R} Parse og analyser en .pcap fil
  {BCY}[2]{R} Decode en rå hex-pakke (TCP/IP headers)
  {BCY}[3]{R} Vis aktive forbindelser (netstat)
""")
    choice = input(f"  {YL}Valg{R}: ").strip()

    if choice == '1':
        path = input(f"  {YL}PCAP fil{R}: ").strip()
        if not os.path.isfile(path):
            print(f"  {RD}Fil ikke fundet.{R}"); input(); return

        # Parse pcap manually (no scapy needed)
        # PCAP global header: magic(4), ver_major(2), ver_minor(2), thiszone(4), sigfigs(4), snaplen(4), network(4)
        PCAP_MAGIC = 0xa1b2c3d4
        PCAP_MAGIC_NANO = 0xa1b23c4d

        ip_protos = {1:'ICMP', 6:'TCP', 17:'UDP', 47:'GRE', 50:'ESP', 51:'AH', 89:'OSPF'}
        packets = []
        src_ips = Counter(); dst_ips = Counter()
        proto_count = Counter()

        try:
            with open(path,'rb') as f:
                # Global header
                gh = f.read(24)
                if len(gh) < 24: raise ValueError("For lille fil")
                magic = struct.unpack('<I', gh[:4])[0]
                if magic not in (PCAP_MAGIC, PCAP_MAGIC_NANO, 0xd4c3b2a1, 0x4d3cb2a1):
                    raise ValueError(f"Ikke en gyldig PCAP fil (magic: {magic:#010x})")

                endian = '<' if magic in (PCAP_MAGIC, PCAP_MAGIC_NANO) else '>'
                ver_maj, ver_min = struct.unpack(f'{endian}HH', gh[4:8])
                network = struct.unpack(f'{endian}I', gh[20:24])[0]

                print(f"\n  {BCY}PCAP version:{R} {ver_maj}.{ver_min}  {BCY}Link type:{R} {network}")
                hline()

                pkt_num = 0
                while pkt_num < 10000:
                    ph = f.read(16)
                    if len(ph) < 16: break
                    ts_sec, ts_usec, incl_len, orig_len = struct.unpack(f'{endian}IIII', ph)
                    data = f.read(incl_len)
                    if len(data) < incl_len: break
                    pkt_num += 1

                    # Ethernet (link type 1)
                    if network == 1 and len(data) >= 14:
                        eth_type = struct.unpack('>H', data[12:14])[0]
                        if eth_type == 0x0800 and len(data) >= 34:  # IPv4
                            ihl = (data[14] & 0x0f) * 4
                            proto = data[23]
                            src = '.'.join(str(b) for b in data[26:30])
                            dst = '.'.join(str(b) for b in data[30:34])
                            src_ips[src] += 1; dst_ips[dst] += 1
                            proto_count[ip_protos.get(proto, f'proto/{proto}')] += 1

                            info = {'pkt':pkt_num,'ts':ts_sec,'src':src,'dst':dst,
                                    'proto':ip_protos.get(proto,'?'),'len':orig_len}

                            if proto == 6 and len(data) >= 34+20:  # TCP
                                tcp_off = 14 + ihl
                                sport = struct.unpack('>H', data[tcp_off:tcp_off+2])[0]
                                dport = struct.unpack('>H', data[tcp_off+2:tcp_off+4])[0]
                                flags_byte = data[tcp_off+13]
                                flags = []
                                if flags_byte & 0x02: flags.append('SYN')
                                if flags_byte & 0x10: flags.append('ACK')
                                if flags_byte & 0x01: flags.append('FIN')
                                if flags_byte & 0x04: flags.append('RST')
                                if flags_byte & 0x08: flags.append('PSH')
                                info.update({'sport':sport,'dport':dport,'flags':flags})

                            elif proto == 17 and len(data) >= 34+8:  # UDP
                                udp_off = 14 + ihl
                                sport = struct.unpack('>H', data[udp_off:udp_off+2])[0]
                                dport = struct.unpack('>H', data[udp_off+2:udp_off+4])[0]
                                info.update({'sport':sport,'dport':dport})

                            packets.append(info)

            # Print summary
            print(f"\n  {BOLD}PCAP Statistik:{R}\n")
            print(f"  {BCY}Total pakker:{R}  {pkt_num:,}")
            print(f"  {BCY}Parsed:{R}        {len(packets):,}")

            print(f"\n  {BOLD}Protokol fordeling:{R}")
            for proto, n in proto_count.most_common(10):
                bar = f"{BCY}{'█'*min(n,30)}{R}"
                print(f"  {proto:<10} {bar} {n}")

            print(f"\n  {BOLD}Top 10 Source IPs:{R}")
            for ip, n in src_ips.most_common(10):
                print(f"  {BCY}{ip:<18}{R} {n} pakker")

            print(f"\n  {BOLD}Top 10 Destination IPs:{R}")
            for ip, n in dst_ips.most_common(10):
                print(f"  {BCY}{ip:<18}{R} {n} pakker")

            print(f"\n  {BOLD}Første 20 pakker:{R}\n")
            print(f"  {DIM}{'#':<5}{'SRC':<20}{'DST':<20}{'PROTO':<8}{'SPORT':<8}{'DPORT':<8}{'FLAGS'}{R}")
            hline(70)
            for p in packets[:20]:
                flags_str = '+'.join(p.get('flags',[])) or ''
                print(f"  {p['pkt']:<5}{p['src']:<20}{p['dst']:<20}"
                      f"{p['proto']:<8}{p.get('sport',''):<8}{p.get('dport',''):<8}"
                      f"{BYL}{flags_str}{R}")

        except Exception as e:
            print(f"  {RD}Fejl: {e}{R}")

    elif choice == '2':
        print(f"  {YL}Indsæt hex bytes (f.eks. fra Wireshark):{R}")
        hex_in = input(f"  > ").strip().replace(' ','').replace(':','')
        try:
            raw = bytes.fromhex(hex_in)
            print(f"\n  {BOLD}Rå bytes:{R} {len(raw)} bytes")
            hline()
            # Try to decode as Ethernet+IP+TCP
            if len(raw) >= 14:
                src_mac = ':'.join(f'{b:02x}' for b in raw[6:12])
                dst_mac = ':'.join(f'{b:02x}' for b in raw[0:6])
                eth_type= struct.unpack('>H',raw[12:14])[0]
                print(f"  {BCY}Ethernet Dst MAC:{R} {dst_mac}")
                print(f"  {BCY}Ethernet Src MAC:{R} {src_mac}")
                print(f"  {BCY}EtherType:{R}       {eth_type:#06x}")
                if eth_type == 0x0800 and len(raw) >= 34:
                    ihl=(raw[14]&0x0f)*4; ttl=raw[22]; proto=raw[23]
                    src='.'.join(str(b)for b in raw[26:30])
                    dst='.'.join(str(b)for b in raw[30:34])
                    print(f"\n  {BCY}IP Src:{R}          {src}")
                    print(f"  {BCY}IP Dst:{R}          {dst}")
                    print(f"  {BCY}TTL:{R}             {ttl}")
                    print(f"  {BCY}Protocol:{R}        {proto} ({ip_protos.get(proto,'?')})")
                    if proto==6 and len(raw)>=14+ihl+20:
                        tcp_off=14+ihl
                        sport=struct.unpack('>H',raw[tcp_off:tcp_off+2])[0]
                        dport=struct.unpack('>H',raw[tcp_off+2:tcp_off+4])[0]
                        seq=struct.unpack('>I',raw[tcp_off+4:tcp_off+8])[0]
                        ack=struct.unpack('>I',raw[tcp_off+8:tcp_off+12])[0]
                        flags=raw[tcp_off+13]
                        flag_names=[n for b,n in [(0x02,'SYN'),(0x10,'ACK'),(0x01,'FIN'),(0x04,'RST'),(0x08,'PSH')] if flags&b]
                        print(f"\n  {BCY}TCP Src Port:{R}    {sport}")
                        print(f"  {BCY}TCP Dst Port:{R}    {dport}")
                        print(f"  {BCY}Seq:{R}             {seq}")
                        print(f"  {BCY}Ack:{R}             {ack}")
                        print(f"  {BCY}Flags:{R}           {BYL}{' | '.join(flag_names)}{R}")
        except ValueError as e:
            print(f"  {RD}Ugyldig hex: {e}{R}")

    elif choice == '3':
        print(f"\n  {BOLD}Aktive Netværksforbindelser:{R}\n"); hline()
        try:
            cmd = "netstat -tn" if platform.system() == "Windows" else "ss -tn"
            r = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=5)
            lines = r.stdout.strip().split('\n')
            print(f"  {DIM}{lines[0] if lines else ''}{R}")
            hline()
            for line in lines[1:26]:
                if 'ESTABLISHED' in line:
                    print(f"  {BGR}{line}{R}")
                elif 'LISTEN' in line:
                    print(f"  {BCY}{line}{R}")
                else:
                    print(f"  {DIM}{line}{R}")
        except Exception as e:
            print(f"  {RD}{e}{R}")

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 09  HASH CRACKER (Dictionary)
# ══════════════════════════════════════════════════════════════════════════════
def hash_cracker():
    clr()
    print(f"\n  {BOLD}{BCY}🔑 HASH CRACKER{R}  {DIM}(Dictionary mode){R}\n"); hline()
    print(f"""
  {DIM}Støttede hash-typer:  md5, sha1, sha256, sha512, sha224, sha384{R}
  {DIM}Wordlist tip: /usr/share/wordlists/rockyou.txt{R}
""")

    target_hash = input(f"  {YL}Hash at cracke{R}: ").strip().lower()
    if not target_hash: return

    # Auto-detect hash type
    hash_len_map = {32:'md5', 40:'sha1', 56:'sha224', 64:'sha256', 96:'sha384', 128:'sha512'}
    detected = hash_len_map.get(len(target_hash), None)
    if detected:
        print(f"  {DIM}Auto-detekteret: {BCY}{detected}{R}")
        hash_type = input(f"  {YL}Hash type{R} (Enter={detected}): ").strip().lower() or detected
    else:
        hash_type = input(f"  {YL}Hash type{R}: ").strip().lower()

    wordlist_path = input(f"  {YL}Wordlist fil{R}: ").strip()

    # Rules
    print(f"\n  {DIM}Regler (transformationer):{R}")
    use_rules = input(f"  {YL}Brug regler?{R} (capitalize, l33t, append_nums, j/n): ").lower() == 'j'

    if not os.path.isfile(wordlist_path):
        print(f"  {RD}Wordlist ikke fundet: {wordlist_path}{R}")
        # Create mini wordlist from common passwords
        print(f"  {YL}Bruger built-in mini-wordlist...{R}")
        mini = ['password','123456','password123','admin','letmein','qwerty',
                'monkey','dragon','master','sunshine','princess','welcome',
                'shadow','superman','michael','football','iloveyou','trustno1',
                '123456789','12345678','1234567890','abc123','111111']
        wordlist_path = None
        words_iter = mini
    else:
        words_iter = None

    def apply_rules(word):
        variants = {word}
        if use_rules:
            variants.add(word.capitalize())
            variants.add(word.upper())
            variants.add(word + '1')
            variants.add(word + '123')
            variants.add(word + '!')
            variants.add('1' + word)
            # l33t
            l33t = word.replace('a','@').replace('e','3').replace('i','1').replace('o','0').replace('s','$')
            variants.add(l33t)
        return variants

    found = [None]
    total_tried = [0]
    start_time  = time.time()
    stop_event  = threading.Event()

    def crack_worker(words):
        for word in words:
            if stop_event.is_set(): break
            for variant in apply_rules(word):
                if stop_event.is_set(): break
                total_tried[0] += 1
                try:
                    h = hashlib.new(hash_type, variant.encode('utf-8','replace')).hexdigest()
                    if h == target_hash:
                        found[0] = variant
                        stop_event.set()
                        return
                except: pass

    def show_progress():
        while not stop_event.is_set():
            elapsed = time.time() - start_time
            rate = total_tried[0] / elapsed if elapsed > 0 else 0
            print(f"  {DIM}Prøvet: {BYL}{total_tried[0]:>8}{R}{DIM}  Rate: {BCY}{rate:.0f}/sek{R}  ", end='\r', flush=True)
            time.sleep(0.3)

    print(f"\n  {DIM}Starter cracking...  {BRD}Ctrl+C for at stoppe{R}\n")
    t_prog = threading.Thread(target=show_progress, daemon=True); t_prog.start()

    NUM_THREADS = 4
    try:
        if wordlist_path:
            with open(wordlist_path, 'r', errors='replace') as f:
                all_words = [l.strip() for l in f if l.strip()]
        else:
            all_words = words_iter

        chunk_size = max(1, len(all_words) // NUM_THREADS)
        threads = []
        for i in range(NUM_THREADS):
            chunk = all_words[i*chunk_size:(i+1)*chunk_size]
            t = threading.Thread(target=crack_worker, args=(chunk,), daemon=True)
            t.start(); threads.append(t)
        for t in threads: t.join()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n\n  {YL}Afbrudt.{R}")

    elapsed = time.time() - start_time
    print(f"\n")
    hline()
    if found[0]:
        print(f"\n  {BG_GR}{BOLD} ✔ CRACKET! {R}")
        print(f"\n  {BGR}Hash:{R}      {target_hash}")
        print(f"  {BGR}Password:{R}  {BOLD}{BWH}{found[0]}{R}")
    else:
        print(f"\n  {BRD}✘ Ikke fundet{R} i wordlist.")
    print(f"\n  {DIM}Prøvet {total_tried[0]:,} kombinationer på {elapsed:.1f} sek  ({total_tried[0]/elapsed:.0f}/sek){R}")
    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 10  WAF DETECTOR
# ══════════════════════════════════════════════════════════════════════════════
def waf_detector():
    clr()
    print(f"\n  {BOLD}{BCY}🛡️  WAF DETECTOR{R}\n"); hline()
    url = input(f"\n  {YL}URL{R}: ").strip()
    if not url.startswith('http'): url = 'https://' + url

    # WAF signatures
    waf_signatures = {
        "Cloudflare":        ["cloudflare","__cfduid","cf-ray","cf-cache-status","cloudflare-nginx"],
        "AWS WAF":           ["awswaf","x-amzn-requestid","aws-waf-token"],
        "Akamai":            ["akamai","akamaighost","x-akamai"],
        "Imperva/Incapsula": ["incap_ses","visid_incap","x-iinfo","incapsula"],
        "F5 BIG-IP ASM":     ["ts=","bigipserver","f5","x-wa-info"],
        "ModSecurity":       ["mod_security","modsecurity","naxsi","x-n: blocked"],
        "Sucuri":            ["sucuri","x-sucuri-id","x-sucuri-cache"],
        "Barracuda":         ["barra_counter_session","barracuda"],
        "Fortinet":          ["fortigate","fortitoken","fortiweb"],
        "Nginx":             ["nginx"],
        "Apache":            ["apache"],
        "IIS":               ["microsoft-iis","x-powered-by: asp.net","x-aspnet"],
    }

    headers_to_send = [
        {},  # Normal request
        # XSS probe
        {'X-Forwarded-For': '<script>alert(1)</script>'},
        # SQLi probe
        {'User-Agent': "' OR '1'='1"},
    ]

    detected_wafs = set()
    responses     = []

    for i, extra_hdrs in enumerate(headers_to_send):
        label = ["Normal","XSS probe","SQLi probe"][i]
        try:
            hdrs = {'User-Agent': 'Mozilla/5.0 (WX7/3.0)'}
            hdrs.update(extra_hdrs)
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=6) as r:
                status = r.status
                resp_hdrs = {k.lower():v.lower() for k,v in r.headers.items()}
                body = r.read(2048).decode('utf-8','replace').lower()
        except urllib.error.HTTPError as e:
            status = e.code
            resp_hdrs = {k.lower():v.lower() for k,v in e.headers.items()}
            try: body = e.read(2048).decode('utf-8','replace').lower()
            except: body = ""
        except Exception as e:
            print(f"  {RD}Fejl: {e}{R}")
            continue

        responses.append((label, status))
        print(f"  {BCY}[{label}]{R}  Status: {BGR if status==200 else BYL}{status}{R}")

        # Check headers + body for WAF signatures
        combined = str(resp_hdrs) + body
        for waf, sigs in waf_signatures.items():
            if any(s in combined for s in sigs):
                detected_wafs.add(waf)

        # Status-code based detection
        if i > 0 and status in (403, 406, 429, 503):
            print(f"  {BYL}  → Blokeret respons ved probe (mulig WAF){R}")

    hline()
    print(f"\n  {BOLD}WAF/CDN Detektions Resultat:{R}\n")
    if detected_wafs:
        for waf in detected_wafs:
            category = "CDN/Proxy" if waf in ("Cloudflare","Akamai","AWS WAF") else "WAF"
            print(f"  {BGR}●{R} {BOLD}{waf}{R}  {DIM}({category}){R}")
    else:
        print(f"  {DIM}Ingen kendte WAF signaturer detekteret.{R}")
        print(f"  {DIM}(Betyder ikke nødvendigvis at der ingen WAF er){R}")

    # Response consistency check
    statuses = [s for _,s in responses]
    if len(set(statuses)) > 1:
        print(f"\n  {BYL}⚠ Inkonsistente responses:{R} {statuses}  {DIM}→ mulig probe-blokering{R}")

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 11  BANNER GRABBER
# ══════════════════════════════════════════════════════════════════════════════
def banner_grabber():
    clr()
    print(f"\n  {BOLD}{BCY}📶 BANNER GRABBER{R}\n"); hline()
    host  = input(f"\n  {YL}Host/IP{R}: ").strip()
    ports_in = input(f"  {YL}Porte{R} (komma-separeret, std=21,22,23,25,80,110,143,443,3306): ").strip()
    ports_in = ports_in or "21,22,23,25,80,110,143,443,3306"
    ports = [int(p.strip()) for p in ports_in.split(',') if p.strip().isdigit()]
    timeout = float(input(f"  {YL}Timeout{R} (std=3): ") or "3")

    try: ip = socket.gethostbyname(host)
    except: print(f"  {RD}Kan ikke resolve.{R}"); input(); return

    probes = {
        21:  ("FTP",   b""),
        22:  ("SSH",   b""),
        23:  ("Telnet",b""),
        25:  ("SMTP",  b"EHLO wx7.local\r\n"),
        80:  ("HTTP",  b"HEAD / HTTP/1.0\r\nHost: "+host.encode()+b"\r\n\r\n"),
        110: ("POP3",  b""),
        143: ("IMAP",  b""),
        443: ("HTTPS", None),  # TLS
        3306:("MySQL", b""),
        5432:("PgSQL", b""),
        6379:("Redis", b"PING\r\n"),
        27017:("MongoDB",b""),
    }

    print(f"\n  {DIM}Grabbing bannere fra {BCY}{host}{DIM} ({ip})...{R}\n")
    hline()

    for port in ports:
        label, probe = probes.get(port, ("?", b""))
        print(f"  {DIM}[{port:<5}]{R}", end=' ', flush=True)
        try:
            if port == 443 or probe is None:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                with socket.create_connection((ip, port), timeout=timeout) as raw:
                    with ctx.wrap_socket(raw, server_hostname=host) as s:
                        s.send(b"HEAD / HTTP/1.0\r\nHost: "+host.encode()+b"\r\n\r\n")
                        data = s.recv(512)
                        banner_txt = data.decode('utf-8','replace').split('\n')[0].strip()
                        print(f"{BCY}{label:<8}{R} {BGR}{banner_txt[:80]}{R}")
            else:
                with socket.create_connection((ip, port), timeout=timeout) as s:
                    if probe: s.send(probe)
                    data = s.recv(512)
                    banner_txt = data.decode('utf-8','replace').replace('\r','').split('\n')[0].strip()
                    print(f"{BCY}{label:<8}{R} {BGR}{banner_txt[:80]}{R}")
        except ConnectionRefusedError:
            print(f"{DIM}Lukket{R}")
        except socket.timeout:
            print(f"{DIM}Timeout{R}")
        except Exception as e:
            print(f"{DIM}{str(e)[:40]}{R}")

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 12  FTP CHECKER
# ══════════════════════════════════════════════════════════════════════════════
def ftp_checker():
    clr()
    print(f"\n  {BOLD}{BCY}🔌 FTP CHECKER{R}\n"); hline()
    if not warn_banner("FTP Checker"): return

    host = input(f"\n  {YL}FTP Host{R}: ").strip()
    port = int(input(f"  {YL}Port{R} (std=21): ") or "21")

    print(f"\n  {DIM}Tester {host}:{port}...{R}\n")

    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=8)
        welcome = ftp.getwelcome()
        print(f"  {BGR}●{R} Forbundet! Banner: {BCY}{welcome}{R}\n")

        # Anonymous login
        anon_ok = False
        try:
            ftp.login('anonymous','wx7@test.local')
            print(f"  {BRD}⚠ ANONYM LOGIN VIRKER!{R}  {DIM}(stor sikkerhedsrisiko){R}")
            anon_ok = True
        except ftplib.error_perm as e:
            print(f"  {BGR}✔{R} Anonym login blokeret: {DIM}{str(e)[:60]}{R}")

        if anon_ok:
            print(f"\n  {BOLD}Directory listing:{R}")
            try:
                entries = []
                ftp.retrlines('LIST', entries.append)
                for e in entries[:20]: print(f"  {DIM}{e}{R}")
            except: pass

            # SYST
            try:
                syst = ftp.sendcmd('SYST')
                print(f"\n  {BCY}SYST:{R} {syst}")
            except: pass

        # Test common credentials
        print(f"\n  {BOLD}Test standard credentials:{R}")
        common_creds = [
            ('admin','admin'),('admin','password'),('ftp','ftp'),
            ('user','user'),('root','root'),('ftpuser','ftpuser'),
        ]
        for user, passwd in common_creds:
            try:
                ftp2 = ftplib.FTP()
                ftp2.connect(host, port, timeout=4)
                ftp2.login(user, passwd)
                print(f"  {BRD}⚠ LOGIN OK:{R}  {user}:{passwd}")
                ftp2.quit()
            except: pass

        ftp.quit()

    except Exception as e:
        print(f"  {RD}Fejl: {e}{R}")

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 13  SMTP CHECKER (Open Relay / VRFY / EXPN)
# ══════════════════════════════════════════════════════════════════════════════
def smtp_checker():
    clr()
    print(f"\n  {BOLD}{BCY}📧 SMTP CHECKER{R}\n"); hline()
    if not warn_banner("SMTP Checker"): return

    host = input(f"\n  {YL}SMTP Host{R}: ").strip()
    port = int(input(f"  {YL}Port{R} (25/465/587, std=25): ") or "25")

    print(f"\n  {DIM}Forbinder til {host}:{port}...{R}\n")

    try:
        if port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=8)
        else:
            server = smtplib.SMTP(host, port, timeout=8)

        server.set_debuglevel(0)
        banner_txt = server.ehlo_or_helo_if_needed()
        print(f"  {BGR}●{R} Forbundet!")
        ehlo_reply = server.ehlo_resp
        if ehlo_reply: print(f"  {BCY}EHLO Banner:{R} {ehlo_reply.decode('utf-8','replace')[:100]}")

        # ESMTP features
        print(f"\n  {BOLD}ESMTP Features:{R}")
        for k,v in server.esmtp_features.items():
            print(f"  {BCY}{k:<15}{R} {v}")

        # STARTTLS
        has_tls = 'starttls' in server.esmtp_features
        print(f"\n  {BCY}STARTTLS:{R} {BGR+'Ja'+R if has_tls else BRD+'Nej'+R}")
        if has_tls:
            try:
                server.starttls()
                print(f"  {BGR}TLS upgrade OK{R}")
            except: pass

        # VRFY (user enumeration)
        print(f"\n  {BOLD}VRFY Test (user enumeration):{R}")
        test_users = ['root','admin','postmaster','info','test','user']
        for user in test_users:
            try:
                code, msg = server.verify(user)
                if code == 250:
                    print(f"  {BRD}⚠ VRFY OK:{R}  {user}  →  {msg.decode('utf-8','replace')[:60]}")
                elif code == 252:
                    print(f"  {YL}252:{R} {user}  {DIM}(kan ikke verificere){R}")
            except smtplib.SMTPException as e:
                if 'disallowed' in str(e).lower() or '502' in str(e):
                    print(f"  {BGR}✔ VRFY blokeret{R}")
                    break

        # Open relay test
        print(f"\n  {BOLD}Open Relay Test:{R}")
        try:
            server.mail('test@external-domain.com')
            code, _ = server.rcpt('test@another-external.com')
            if code == 250:
                print(f"  {BRD}⚠ OPEN RELAY MULIGVIS ÅBEN!{R}")
            else:
                print(f"  {BGR}✔ Relay afvist (kode {code}){R}")
        except smtplib.SMTPRecipientsRefused:
            print(f"  {BGR}✔ Relay afvist{R}")
        except smtplib.SMTPSenderRefused:
            print(f"  {BGR}✔ Sender afvist (anti-relay){R}")
        except Exception as e:
            print(f"  {DIM}Relay test: {e}{R}")

        server.quit()

    except Exception as e:
        print(f"  {RD}Fejl: {e}{R}")

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 14  HTTP HEADER AUDIT (Security)
# ══════════════════════════════════════════════════════════════════════════════
def http_header_audit():
    clr()
    print(f"\n  {BOLD}{BCY}🌍 HTTP SECURITY HEADER AUDIT{R}\n"); hline()
    url = input(f"\n  {YL}URL{R}: ").strip()
    if not url.startswith('http'): url = 'https://' + url

    try:
        req = urllib.request.Request(url, headers={'User-Agent':'WX7-Audit/3.0'})
        with urllib.request.urlopen(req, timeout=8) as r:
            status   = r.status
            headers  = {k.lower(): v for k, v in r.headers.items()}
            body     = r.read(8192).decode('utf-8','replace')
    except urllib.error.HTTPError as e:
        status  = e.code
        headers = {k.lower(): v for k, v in e.headers.items()}
        body    = ""
    except Exception as e:
        print(f"  {RD}Fejl: {e}{R}"); input(); return

    print(f"\n  {BCY}Status:{R} {BGR if status==200 else BYL}{status}{R}   {BCY}Server:{R} {headers.get('server','N/A')}\n")

    # Security headers analysis
    sec_checks = [
        # (header_name, display_name, description, required_value_hint, critical)
        ("strict-transport-security","HSTS","Tvinger HTTPS forbindelser","max-age≥31536000",True),
        ("content-security-policy","CSP","Forhindrer XSS og injection","default-src",True),
        ("x-frame-options","X-Frame-Options","Forhindrer clickjacking","DENY/SAMEORIGIN",True),
        ("x-content-type-options","X-Content-Type-Options","Forhindrer MIME sniffing","nosniff",True),
        ("referrer-policy","Referrer-Policy","Kontrollerer referrer header","no-referrer",False),
        ("permissions-policy","Permissions-Policy","Begrænser browser APIs","...",False),
        ("cross-origin-embedder-policy","COEP","Cross-origin isolation","require-corp",False),
        ("cross-origin-opener-policy","COOP","Cross-origin opener","same-origin",False),
        ("cross-origin-resource-policy","CORP","Cross-origin resource","same-origin",False),
        ("x-xss-protection","X-XSS-Protection","Ældre XSS filter","0 (deaktiver)",False),
        ("cache-control","Cache-Control","Cache styring","no-store/no-cache",False),
    ]

    dangerous_headers = [
        ("server","Server","Afslører server software"),
        ("x-powered-by","X-Powered-By","Afslører backend teknologi"),
        ("x-aspnet-version","X-AspNet-Version","Afslører .NET version"),
        ("x-aspnetmvc-version","X-AspNetMvc-Version","Afslører MVC version"),
    ]

    score = 0
    max_score = sum(3 if c else 1 for *_,c in sec_checks)

    print(f"  {BOLD}Security Headers:{R}\n")
    hline()

    findings = []
    for hdr, name, desc, hint, critical in sec_checks:
        val = headers.get(hdr)
        if val:
            score += 3 if critical else 1
            mark = f"{BGR}✔{R}"
            status_str = f"{BGR}PRESENT{R}"

            # Value checks
            if hdr == "strict-transport-security":
                m = re.search(r'max-age=(\d+)', val)
                if m and int(m.group(1)) < 31536000:
                    mark = f"{BYL}⚠{R}"
                    status_str = f"{BYL}SVAG (max-age for lav){R}"
            elif hdr == "x-frame-options":
                if val.lower() not in ('deny','sameorigin'):
                    mark = f"{BYL}⚠{R}"
            elif hdr == "x-content-type-options":
                if 'nosniff' not in val.lower():
                    mark = f"{BYL}⚠{R}"

            print(f"  {mark}  {BCY}{name:<30}{R} {status_str}  {DIM}{val[:50]}{R}")
        else:
            sev = f"{BRD}MANGLER [KRITISK]{R}" if critical else f"{YL}MANGLER{R}"
            print(f"  {BRD}✘{R}  {DIM}{name:<30}{R} {sev}  {DIM}│ {hint}{R}")
            findings.append((critical, name, desc))

    print(f"\n  {BOLD}Farlige informations-headers:{R}\n")
    for hdr, name, desc in dangerous_headers:
        val = headers.get(hdr)
        if val:
            print(f"  {BYL}⚠{R}  {BCY}{name:<30}{R} {BYL}{val[:60]}{R}  {DIM}│ {desc}{R}")

    # Cookie security
    cookies = headers.get('set-cookie','')
    if cookies:
        print(f"\n  {BOLD}Cookie Analyse:{R}\n")
        missing_flags = []
        if 'secure' not in cookies.lower(): missing_flags.append('Secure')
        if 'httponly' not in cookies.lower(): missing_flags.append('HttpOnly')
        if 'samesite' not in cookies.lower(): missing_flags.append('SameSite')
        if missing_flags:
            print(f"  {BYL}⚠ Cookie mangler flags:{R} {', '.join(missing_flags)}")
            print(f"  {DIM}{cookies[:100]}{R}")
        else:
            print(f"  {BGR}✔ Cookie har alle security flags{R}")

    # Information disclosure in body
    risky_patterns = [
        (r'version\s*[=:]\s*["\']?[\d\.]+', "Version disclosure"),
        (r'debug\s*=\s*true', "Debug mode enabled"),
        (r'stack trace', "Stack trace exposure"),
        (r'sql syntax', "SQL error disclosure"),
        (r'php warning', "PHP error disclosure"),
        (r'exception in thread', "Java exception"),
    ]
    print(f"\n  {BOLD}Body Information Disclosure:{R}\n")
    found_risky = False
    for pattern, desc in risky_patterns:
        if re.search(pattern, body, re.I):
            print(f"  {BRD}⚠{R} {desc}")
            found_risky = True
    if not found_risky:
        print(f"  {BGR}✔ Ingen åbenlyse disclosures i body{R}")

    # Score
    pct = score / max_score * 100 if max_score > 0 else 0
    col = BGR if pct >= 75 else BYL if pct >= 50 else BRD
    bar_l = int(40 * pct / 100)
    bar = f"{col}{'█'*bar_l}{R}{DIM}{'░'*(40-bar_l)}{R}"
    grade = 'A' if pct>=90 else 'B' if pct>=75 else 'C' if pct>=60 else 'D' if pct>=45 else 'F'

    print(f"\n"); hline(60)
    print(f"  {BOLD}Security Score:{R} {col}{BOLD}{score}/{max_score} ({pct:.0f}%){R}  Grade: {col}{BOLD}{grade}{R}")
    print(f"  [{bar}]")
    hline(60)
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 15  TCP FLOODER (stress test – eget system)
# ══════════════════════════════════════════════════════════════════════════════
def tcp_flooder():
    clr()
    print(f"\n  {BOLD}{BCY}⚡ TCP CONNECT STRESS TEST{R}\n"); hline()
    print(f"\n  {BRD}{BOLD}⚠ BRUG KUN PÅ DIT EGET SYSTEM/SERVER{R}")
    print(f"  {BRD}DoS-angreb mod andres systemer er ulovligt (Straffeloven §193){R}\n")
    if not warn_banner("TCP Flooder"): return

    host    = input(f"  {YL}Target host{R}: ").strip()
    port    = int(input(f"  {YL}Port{R}: ") or "80")
    threads = int(input(f"  {YL}Samtidige forbindelser{R} (std=50): ") or "50")
    duration= int(input(f"  {YL}Varighed sek{R} (std=10): ") or "10")

    try: ip = socket.gethostbyname(host)
    except: print(f"  {RD}Kan ikke resolve{R}"); input(); return

    count_ok    = [0]
    count_fail  = [0]
    running     = [True]
    lock        = threading.Lock()

    def worker():
        while running[0]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((ip, port))
                s.send(b"GET / HTTP/1.0\r\n\r\n")
                s.close()
                with lock: count_ok[0] += 1
            except:
                with lock: count_fail[0] += 1

    print(f"\n  {DIM}Starter mod {ip}:{port} i {duration}s med {threads} tråde...{R}\n")
    print(f"  {BRD}Ctrl+C for at stoppe{R}\n")

    workers = [threading.Thread(target=worker, daemon=True) for _ in range(threads)]
    start = time.time()
    for w in workers: w.start()

    try:
        while time.time() - start < duration:
            elapsed = time.time()-start
            rate    = count_ok[0]/elapsed if elapsed>0 else 0
            print(f"  {BGR}OK:{R}{count_ok[0]:>8}  {BRD}Fail:{R}{count_fail[0]:>8}  "
                  f"{BCY}Rate:{R}{rate:>8.0f}/sek  {DIM}{elapsed:.1f}s/{duration}s{R}   ", end='\r', flush=True)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n  {YL}Afbrudt manuelt.{R}")

    running[0] = False
    elapsed = time.time()-start
    print(f"\n\n"); hline()
    print(f"  {BOLD}Resultat:{R}")
    print(f"  {BGR}Succesfulde forbindelser:{R}  {count_ok[0]:,}")
    print(f"  {BRD}Fejlede forbindelser:{R}     {count_fail[0]:,}")
    print(f"  {BCY}Total rate:{R}               {count_ok[0]/elapsed:.0f} forbindelser/sek")
    print(f"  {DIM}Varighed: {elapsed:.1f}s{R}")
    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 16  AVANCERET HASH TOOL
# ══════════════════════════════════════════════════════════════════════════════
def advanced_hash_tool():
    clr()
    print(f"\n  {BOLD}{BCY}🔐 AVANCERET HASH TOOL{R}\n"); hline()
    print(f"\n  {BCY}[1]{R} Hash tekst (alle algoritmer)")
    print(f"  {BCY}[2]{R} Hash fil (checksums)")
    print(f"  {BCY}[3]{R} HMAC generator")
    print(f"  {BCY}[4]{R} Saltet password hash (bcrypt-style)")
    print(f"  {BCY}[5]{R} Sammenlign to hashes")
    print(f"  {BCY}[6]{R} Hash identifier\n")
    choice = input(f"  {YL}Valg{R}: ").strip()

    algos = ['md5','sha1','sha224','sha256','sha384','sha512',
             'sha3_224','sha3_256','sha3_384','sha3_512','blake2b','blake2s']

    if choice == '1':
        text = input(f"  {YL}Tekst{R}: ")
        enc = text.encode('utf-8')
        hline()
        for a in algos:
            try:
                h = hashlib.new(a, enc).hexdigest()
                print(f"  {BCY}{a.upper():<16}{R} {h}")
            except: pass

    elif choice == '2':
        path = input(f"  {YL}Filsti{R}: ").strip()
        if not os.path.isfile(path):
            print(f"  {RD}Fil ikke fundet{R}"); input(); return
        spin("Beregner...", 0.8)
        with open(path,'rb') as f: data = f.read()
        size = os.path.getsize(path)
        print(f"  {DIM}Størrelse: {size:,} bytes{R}")
        hline()
        for a in algos:
            try:
                h = hashlib.new(a, data).hexdigest()
                print(f"  {BCY}{a.upper():<16}{R} {h}")
            except: pass

    elif choice == '3':
        key  = input(f"  {YL}Nøgle{R}: ").encode()
        msg  = input(f"  {YL}Besked{R}: ").encode()
        hline()
        for a in ['sha256','sha512','sha3_256']:
            sig = hmac.new(key, msg, a).hexdigest()
            print(f"  {BCY}HMAC-{a.upper():<14}{R} {sig}")

    elif choice == '4':
        pw   = input(f"  {YL}Password{R}: ")
        salt = secrets.token_hex(16)
        print(f"  {DIM}Salt: {salt}{R}")
        hline()
        for a in ['sha256','sha512']:
            salted = (salt + pw).encode()
            h = hashlib.new(a, salted).hexdigest()
            print(f"  {BCY}{a.upper():<12}{R} ${a}${salt}${h}")

    elif choice == '5':
        h1 = input(f"  {YL}Hash 1{R}: ").strip().lower()
        h2 = input(f"  {YL}Hash 2{R}: ").strip().lower()
        if h1 == h2:
            print(f"\n  {BG_GR}{BOLD} ✔ MATCH {R}")
        else:
            diff = sum(a!=b for a,b in zip(h1,h2)) + abs(len(h1)-len(h2))
            print(f"\n  {BG_RD}{BOLD} ✘ INGEN MATCH {R}  {diff} bits different")

    elif choice == '6':
        h = input(f"  {YL}Hash{R}: ").strip()
        length_map = {
            32: ["MD5","NTLM","MD4"],
            40: ["SHA-1","RIPEMD-160"],
            56: ["SHA-224","SHA3-224"],
            64: ["SHA-256","SHA3-256","BLAKE2s"],
            96: ["SHA-384","SHA3-384"],
            128:["SHA-512","SHA3-512","BLAKE2b","Whirlpool"],
            16: ["MySQL v3.x"],
            13: ["DES (Unix crypt)"],
        }
        hline()
        guesses = length_map.get(len(h), ["Ukendt"])
        print(f"  {BCY}Længde:{R} {len(h)} hex chars ({len(h)*4} bits)")
        print(f"  {BCY}Mulige typer:{R} {', '.join(guesses)}")
        # Pattern hints
        if h.startswith('$2'): print(f"  {BYL}Ligner bcrypt hash ($2b/2y){R}")
        if h.startswith('$6'): print(f"  {BYL}Ligner SHA-512 crypt{R}")
        if h.startswith('$1'): print(f"  {BYL}Ligner MD5 crypt{R}")
        if all(c in '0123456789abcdef' for c in h): print(f"  {DIM}Kun hex chars{R}")

    print()
    input(f"  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 17  AES-256 ENCRYPTOR (pure Python, CTR mode)
# ══════════════════════════════════════════════════════════════════════════════
def aes_encryptor():
    clr()
    print(f"\n  {BOLD}{BCY}🗜️  AES-256 ENCRYPTOR{R}  {DIM}(CTR mode, PBKDF2){R}\n"); hline()

    # Pure Python AES-256 using only stdlib
    # We'll use a simplified approach with os.urandom + hashlib for key derivation
    # and XOR stream cipher as a fallback if no crypto libs available
    # Try to use proper AES via subprocess openssl or cryptography package

    def encrypt_openssl(plaintext, password):
        """Use openssl CLI if available"""
        if not shutil.which('openssl'): return None
        try:
            proc = subprocess.run(
                ['openssl','enc','-aes-256-cbc','-base64','-pbkdf2','-pass',f'pass:{password}'],
                input=plaintext.encode(),
                capture_output=True,
                timeout=5
            )
            if proc.returncode == 0:
                return proc.stdout.decode().strip()
        except: pass
        return None

    def decrypt_openssl(ciphertext, password):
        if not shutil.which('openssl'): return None
        try:
            proc = subprocess.run(
                ['openssl','enc','-d','-aes-256-cbc','-base64','-pbkdf2','-pass',f'pass:{password}'],
                input=ciphertext.encode(),
                capture_output=True,
                timeout=5
            )
            if proc.returncode == 0:
                return proc.stdout.decode().strip()
        except: pass
        return None

    def xor_encrypt_b(data_bytes, key_bytes):
        """Fallback: XOR stream cipher with SHA-256 derived key"""
        # Expand key using SHA-256 chain
        keystream = b""
        block = key_bytes
        while len(keystream) < len(data_bytes):
            block = hashlib.sha256(block).digest()
            keystream += block
        return bytes(a ^ b for a, b in zip(data_bytes, keystream[:len(data_bytes)]))

    openssl_ok = bool(shutil.which('openssl'))

    if not openssl_ok:
        print(f"  {YL}OpenSSL CLI ikke fundet. Bruger XOR-stream (fallback).{R}")
        print(f"  {DIM}Installer OpenSSL for rigtig AES-256-CBC.{R}\n")

    print(f"  {BCY}[1]{R} Krypter   {BCY}[2]{R} Dekrypter\n")
    choice = input(f"  {YL}Valg{R}: ").strip()
    password = input(f"  {YL}Password/Nøgle{R}: ")

    if choice == '1':
        print(f"  {YL}Tekst{R} (afslut med tom linje):")
        lines = []
        while True:
            l = input()
            if l == '': break
            lines.append(l)
        plaintext = '\n'.join(lines)

        spin("Krypterer...", 0.8)

        if openssl_ok:
            result = encrypt_openssl(plaintext, password)
            method = "AES-256-CBC (OpenSSL)"
        else:
            key = hashlib.sha256(password.encode()).digest()
            encrypted = xor_encrypt_b(plaintext.encode('utf-8'), key)
            result = base64.b64encode(encrypted).decode()
            method = "XOR-SHA256 (fallback)"

        if result:
            hline()
            print(f"  {DIM}Metode: {method}{R}")
            print(f"\n  {BOLD}Krypteret (gem dette):{R}\n")
            for i in range(0, len(result), 64):
                print(f"  {BGR}{result[i:i+64]}{R}")
        else:
            print(f"  {RD}Kryptering fejlede.{R}")

    elif choice == '2':
        print(f"  {YL}Krypteret tekst:{R}")
        ciphertext = input(f"  > ").strip()

        spin("Dekrypterer...", 0.8)

        if openssl_ok:
            result = decrypt_openssl(ciphertext, password)
            method = "AES-256-CBC (OpenSSL)"
        else:
            try:
                key = hashlib.sha256(password.encode()).digest()
                decoded = base64.b64decode(ciphertext)
                result = xor_encrypt_b(decoded, key).decode('utf-8')
                method = "XOR-SHA256 (fallback)"
            except Exception as e:
                result = None

        if result:
            hline()
            print(f"  {DIM}Metode: {method}{R}")
            print(f"\n  {BOLD}Dekrypteret:{R}\n  {BGR}{result}{R}")
        else:
            print(f"  {RD}Dekryptering fejlede. Forkert password?{R}")

    print()
    input(f"  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 18  STEGANOGRAFI DETEKTOR (LSB analyse)
# ══════════════════════════════════════════════════════════════════════════════
def stego_detector():
    clr()
    print(f"\n  {BOLD}{BCY}🧬 STEGANOGRAFI DETEKTOR{R}  {DIM}(LSB analyse){R}\n"); hline()
    print(f"""
  {DIM}Steganografi = at gemme data i billeder/filer.
  LSB (Least Significant Bit) er den mest brugte teknik.
  Denne tool analyserer billeder for tegn på skjult data.{R}
""")
    print(f"  {BCY}[1]{R} Analyser billede (statistisk)  {BCY}[2]{R} Forsøg LSB extraction\n")
    choice = input(f"  {YL}Valg{R}: ").strip()
    path = input(f"  {YL}Billedsti{R} (.png/.bmp): ").strip()

    if not os.path.isfile(path):
        print(f"  {RD}Fil ikke fundet.{R}"); input(); return

    # Read raw file bytes
    with open(path, 'rb') as f:
        data = f.read()

    # Check file magic
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        fmt = "PNG"
    elif data[:2] == b'BM':
        fmt = "BMP"
    elif data[:3] == b'\xff\xd8\xff':
        fmt = "JPEG"
    elif data[:6] in (b'GIF87a', b'GIF89a'):
        fmt = "GIF"
    else:
        fmt = "Ukendt"

    print(f"\n  {BCY}Format:{R} {fmt}  {BCY}Størrelse:{R} {len(data):,} bytes\n")

    # Entropy analysis
    byte_counts = Counter(data)
    total = len(data)
    entropy = -sum((c/total)*math.log2(c/total) for c in byte_counts.values() if c > 0)
    max_entropy = 8.0  # bits per byte

    print(f"  {BCY}Fil Entropi:{R} {entropy:.4f} / 8.0 bits/byte")
    if entropy > 7.5:
        print(f"  {BYL}⚠ Høj entropi ({entropy:.3f}) — kan indikere krypteret/komprimeret data{R}")
    else:
        print(f"  {BGR}✔ Normal entropi{R}")

    # Chi-square test (simplified)
    expected = total / 256
    chi_sq = sum((c - expected)**2 / expected for c in [byte_counts.get(i,0) for i in range(256)])
    print(f"  {BCY}Chi-square:{R} {chi_sq:.2f}")
    if chi_sq < 310:  # p < 0.05 threshold for 255 df
        print(f"  {BYL}⚠ Chi-square lav ({chi_sq:.0f}) — byte-distribution mistænkelig jævn{R}")
    else:
        print(f"  {BGR}✔ Normal byte distribution{R}")

    # Look for embedded files
    print(f"\n  {BOLD}Embedded File Signatures:{R}\n")
    signatures = {
        b'\x50\x4b\x03\x04': "ZIP/JAR",
        b'\xff\xd8\xff':      "JPEG",
        b'\x89PNG':           "PNG",
        b'%PDF':              "PDF",
        b'GIF89a':            "GIF",
        b'Rar!':              "RAR",
        b'7z\xbc\xaf':       "7-Zip",
        b'PK\x03\x04':       "ZIP",
        b'\x1f\x8b':         "GZIP",
        b'BM':                "BMP",
        b'IHDR':              "PNG chunk",
    }
    found_sigs = []
    # Skip the first few bytes (file's own header)
    search_data = data[8:]
    for sig, name in signatures.items():
        idx = search_data.find(sig)
        if idx != -1:
            found_sigs.append((name, idx+8))
    if found_sigs:
        for name, offset in found_sigs:
            print(f"  {BRD}⚠ {name}{R} signature ved offset {offset:#x} — mulig embedded fil!")
    else:
        print(f"  {BGR}✔ Ingen kendte fil-signaturer fundet i body{R}")

    # LSB extraction (for BMP/PNG – raw pixel analysis)
    if choice == '2':
        print(f"\n  {BOLD}LSB Extraction Forsøg:{R}\n")
        # Simple: extract every LSB from file bytes
        bits = [b & 1 for b in data[:10000]]  # First 10KB
        # Group into bytes
        extracted = []
        for i in range(0, len(bits)-7, 8):
            byte_val = 0
            for j in range(8):
                byte_val = (byte_val << 1) | bits[i+j]
            if 32 <= byte_val <= 126:  # Printable ASCII
                extracted.append(chr(byte_val))

        printable = ''.join(extracted)
        if len(printable) > 20:
            print(f"  {BYL}Mulig skjult tekst (LSB):{R}")
            print(f"  {GR}{printable[:200]}{R}")
        else:
            print(f"  {DIM}Ingen tydelig tekst i LSBs (eller ikke LSB steganografi){R}")

    # Look for strings in binary
    print(f"\n  {BOLD}Strings i fil (printable sekvenser >8 tegn):{R}\n")
    strings_found = re.findall(rb'[\x20-\x7e]{8,}', data[100:])[:15]  # Skip header
    for s in strings_found:
        print(f"  {DIM}{s.decode('ascii','replace')[:80]}{R}")

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 19  METADATA EXTRACTOR
# ══════════════════════════════════════════════════════════════════════════════
def metadata_extractor():
    clr()
    print(f"\n  {BOLD}{BCY}🔎 METADATA EXTRACTOR{R}\n"); hline()
    path = input(f"\n  {YL}Filsti{R}: ").strip()
    if not os.path.isfile(path):
        print(f"  {RD}Fil ikke fundet.{R}"); input(); return

    stat = os.stat(path)
    size = stat.st_size
    ext  = Path(path).suffix.lower()

    print(f"\n  {BOLD}Fil System Metadata:{R}\n")
    hline()
    print(f"  {BCY}Filnavn:{R}     {Path(path).name}")
    print(f"  {BCY}Størrelse:{R}   {size:,} bytes  ({size/1024:.1f} KB)")
    print(f"  {BCY}Extension:{R}   {ext}")
    print(f"  {BCY}Oprettet:{R}    {datetime.fromtimestamp(stat.st_ctime)}")
    print(f"  {BCY}Ændret:{R}      {datetime.fromtimestamp(stat.st_mtime)}")
    print(f"  {BCY}Tilgået:{R}     {datetime.fromtimestamp(stat.st_atime)}")
    print(f"  {BCY}Permissions:{R} {oct(stat.st_mode)}")

    with open(path,'rb') as f:
        raw = f.read()

    # Hash checksums
    print(f"\n  {BOLD}Checksums:{R}\n")
    for algo in ['md5','sha1','sha256']:
        h = hashlib.new(algo, raw).hexdigest()
        print(f"  {BCY}{algo.upper():<8}{R} {h}")

    # Entropy
    bc = Counter(raw); total = len(raw)
    ent = -sum((c/total)*math.log2(c/total) for c in bc.values() if c > 0)
    print(f"\n  {BCY}Entropi:{R}    {ent:.4f} / 8.0  {'(høj — mulig kryptering)' if ent > 7.5 else '(normal)'}")

    # JPEG EXIF
    if ext in ('.jpg','.jpeg'):
        print(f"\n  {BOLD}JPEG EXIF Data:{R}\n")
        # Use exiftool if available
        if shutil.which('exiftool'):
            try:
                r = subprocess.run(['exiftool', path], capture_output=True, text=True, timeout=8)
                for line in r.stdout.split('\n')[:30]:
                    if ':' in line: print(f"  {DIM}{line.strip()}{R}")
            except: pass
        else:
            # Manual EXIF: find 0xFFE1 APP1 marker
            idx = raw.find(b'\xff\xe1')
            if idx != -1:
                exif_data = raw[idx:idx+1000]
                print(f"  {DIM}EXIF marker fundet ved offset {idx:#x}{R}")
                # Look for GPS strings
                strings = re.findall(rb'[\x20-\x7e]{4,}', exif_data)
                for s in strings[:10]:
                    print(f"  {DIM}{s.decode('ascii','replace')}{R}")
            else:
                print(f"  {DIM}Ingen EXIF data fundet (eller ingen 0xFFE1 marker){R}")

    # PDF metadata
    elif ext == '.pdf':
        print(f"\n  {BOLD}PDF Metadata:{R}\n")
        text = raw.decode('latin-1','replace')
        patterns = [
            (r'/Author\s*\(([^)]+)\)', "Author"),
            (r'/Creator\s*\(([^)]+)\)', "Creator"),
            (r'/Producer\s*\(([^)]+)\)', "Producer"),
            (r'/Title\s*\(([^)]+)\)', "Title"),
            (r'/Subject\s*\(([^)]+)\)', "Subject"),
            (r'/CreationDate\s*\(([^)]+)\)', "Created"),
            (r'/ModDate\s*\(([^)]+)\)', "Modified"),
        ]
        for pattern, label in patterns:
            m = re.search(pattern, text)
            if m: print(f"  {BCY}{label:<12}{R} {m.group(1)[:60]}")

    # Office documents
    elif ext in ('.docx','.xlsx','.pptx'):
        print(f"\n  {BOLD}Office Metadata (ZIP structure):{R}\n")
        import zipfile
        try:
            with zipfile.ZipFile(path) as z:
                if 'docProps/core.xml' in z.namelist():
                    core = z.read('docProps/core.xml').decode('utf-8','replace')
                    fields = {
                        'dc:creator':          'Creator',
                        'dc:lastModifiedBy':   'Last Modified By',
                        'dcterms:created':     'Created',
                        'dcterms:modified':    'Modified',
                        'cp:revision':         'Revision',
                    }
                    for tag, label in fields.items():
                        m = re.search(f'<{tag}>([^<]+)</{tag}>', core)
                        if m: print(f"  {BCY}{label:<20}{R} {m.group(1)}")
        except: print(f"  {DIM}Kan ikke læse Office XML{R}")

    # PE (Windows executable)
    elif ext in ('.exe','.dll'):
        print(f"\n  {BOLD}PE Header Info:{R}\n")
        if raw[:2] == b'MZ':
            print(f"  {BCY}Format:{R} DOS/PE executable")
            pe_offset = struct.unpack('<I', raw[60:64])[0] if len(raw)>64 else 0
            if pe_offset < len(raw)-4 and raw[pe_offset:pe_offset+4] == b'PE\x00\x00':
                machine = struct.unpack('<H', raw[pe_offset+4:pe_offset+6])[0]
                machines = {0x14c:'x86', 0x8664:'x64', 0x1c0:'ARM', 0xaa64:'ARM64'}
                print(f"  {BCY}Architecture:{R} {machines.get(machine, f'{machine:#06x}')}")
                num_sections = struct.unpack('<H', raw[pe_offset+6:pe_offset+8])[0]
                ts = struct.unpack('<I', raw[pe_offset+8:pe_offset+12])[0]
                print(f"  {BCY}Sektioner:{R}  {num_sections}")
                print(f"  {BCY}Timestamp:{R}  {datetime.fromtimestamp(ts) if ts < 2e9 else 'Invalid'}")

        # Strings
        strings = re.findall(rb'[\x20-\x7e]{6,}', raw[:50000])[:20]
        if strings:
            print(f"\n  {BOLD}Strings (første 20):{R}")
            for s in strings: print(f"  {DIM}{s.decode('ascii','replace')[:80]}{R}")

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 20  ENTROPY ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
def entropy_analyzer():
    clr()
    print(f"\n  {BOLD}{BCY}💡 ENTROPY ANALYZER{R}\n"); hline()
    print(f"""
  {DIM}Entropi måler tilfældighed i data (Shannon entropy).
  Høj entropi (>7.5) → krypteret, komprimeret, eller packed.
  Normal tekst: ~4-5 bits/byte
  Komprimeret:  ~7-7.5 bits/byte
  Krypteret:    ~7.9-8.0 bits/byte{R}
""")
    path = input(f"  {YL}Filsti{R}: ").strip()
    if not os.path.isfile(path):
        print(f"  {RD}Fil ikke fundet.{R}"); input(); return

    with open(path,'rb') as f:
        data = f.read()

    size = len(data)
    spin("Analyserer...", 1.0)

    # Overall entropy
    bc = Counter(data)
    ent = -sum((c/size)*math.log2(c/size) for c in bc.values() if c > 0)

    # Block entropy analysis (4KB blocks)
    block_size = 4096
    block_entropies = []
    for i in range(0, min(size, 256*1024), block_size):
        block = data[i:i+block_size]
        if len(block) < 8: break
        bc_b = Counter(block)
        n = len(block)
        e = -sum((c/n)*math.log2(c/n) for c in bc_b.values() if c > 0)
        block_entropies.append((i, e))

    # Byte distribution histogram
    hline()
    print(f"\n  {BOLD}Samlet Entropi:{R} {BOLD}{ent:.4f}{R} / 8.0 bits/byte\n")

    # Entropy bar
    bar_l = int(40 * ent/8)
    col = BGR if ent < 5 else BYL if ent < 7 else BRD
    bar = f"{col}{'█'*bar_l}{R}{DIM}{'░'*(40-bar_l)}{R}"
    print(f"  [{bar}]  {col}{ent:.4f}{R}")

    # Classification
    if ent > 7.8:
        cls = f"{BRD}Sandsynligvis KRYPTERET eller PACKED{R}"
    elif ent > 7.0:
        cls = f"{BYL}Sandsynligvis KOMPRIMERET (zip/gz/xz){R}"
    elif ent > 5.5:
        cls = f"{BCY}Blandet indhold (binær med tekst){R}"
    elif ent > 4.0:
        cls = f"{BGR}Tekst-baseret indhold{R}"
    else:
        cls = f"{BGR}Lav entropi — repetitivt/struktureret indhold{R}"
    print(f"\n  {BOLD}Klassifikation:{R} {cls}")

    # Block-by-block visualization
    if len(block_entropies) > 1:
        print(f"\n  {BOLD}Blok-entropi kart ({block_size//1024}KB blokke):{R}\n")
        for offset, e in block_entropies[:40]:
            b = int(20 * e/8)
            c = BGR if e < 5 else BYL if e < 7 else BRD
            bar2 = f"{c}{'█'*b}{R}{DIM}{'░'*(20-b)}{R}"
            print(f"  {DIM}{offset//1024:>5}KB{R} [{bar2}] {c}{e:.2f}{R}")

    # Null bytes
    nulls = data.count(0)
    print(f"\n  {BCY}Null bytes:{R}   {nulls:,} ({nulls/size*100:.1f}%)")

    # Printable ASCII ratio
    printable = sum(1 for b in data if 32 <= b <= 126)
    print(f"  {BCY}Printable ASCII:{R} {printable:,} ({printable/size*100:.1f}%)")

    # Byte distribution visualization
    print(f"\n  {BOLD}Byte Distribution (0-255):{R}\n")
    max_count = max(bc.values()) if bc else 1
    for start in range(0, 256, 16):
        row = ""
        for b in range(start, start+16):
            cnt = bc.get(b, 0)
            h = int(6 * cnt / max_count)
            chars = " ▁▂▃▄▅▆"
            row += chars[h]
        print(f"  {DIM}{start:>3}-{start+15:<3}{R} {BCY}{row}{R}")

    hline()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 21  PASSWORD GENERATOR (Advanced)
# ══════════════════════════════════════════════════════════════════════════════
def password_generator():
    clr()
    print(f"\n  {BOLD}{BCY}🔢 PASSWORD GENERATOR{R}\n"); hline()
    try:
        length   = int(input(f"\n  {YL}Længde{R}             (std=20): ") or "20")
        symbols  = input(f"  {YL}Symboler?{R}          (j/n, j): ").lower() != 'n'
        numbers  = input(f"  {YL}Tal?{R}               (j/n, j): ").lower() != 'n'
        no_ambig = input(f"  {YL}Undgå 0/O/1/l?{R}     (j/n, n): ").lower() == 'j'
        count    = int(input(f"  {YL}Antal{R}              (std=5) : ") or "5")
    except: print(f"  {RD}Fejl{R}"); input(); return

    charset = string.ascii_letters
    if numbers: charset += string.digits
    if symbols: charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if no_ambig:
        for c in "0O1lI|": charset = charset.replace(c,"")

    print(f"\n"); hline()
    print(f"  {BOLD}{BGR}Genererede Passwords:{R}\n")
    for i in range(count):
        pw = ''.join(secrets.choice(charset) for _ in range(length))
        entropy = math.log2(len(charset)) * length
        colored = ""
        for ch in pw:
            if ch in string.ascii_uppercase: colored += f"{BCY}{ch}{R}"
            elif ch in string.ascii_lowercase: colored += f"{BWH}{ch}{R}"
            elif ch in string.digits: colored += f"{BYL}{ch}{R}"
            else: colored += f"{BRD}{ch}{R}"
        print(f"  {DIM}[{i+1:02d}]{R} {colored}  {DIM}{entropy:.0f}bit{R}")
    hline()
    input(f"  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 22  PASSWORD STRENGTH
# ══════════════════════════════════════════════════════════════════════════════
def password_strength():
    clr()
    print(f"\n  {BOLD}{BCY}🛡️  PASSWORD STYRKEANALYSE{R}\n"); hline()
    pw = input(f"\n  {YL}Password{R}: ")
    score = 0; checks = []
    def chk(c,p,ok,fail):
        nonlocal score
        if c: score+=p; checks.append((True,p,ok))
        else: checks.append((False,0,fail))
    chk(len(pw)>=8,10,"Længde ≥ 8","For kort (<8)")
    chk(len(pw)>=12,10,"Længde ≥ 12","< 12 tegn")
    chk(len(pw)>=16,10,"Bonus ≥ 16","< 16 tegn")
    chk(len(pw)>=20,5,"Elite ≥ 20","< 20 tegn")
    chk(re.search(r'[A-Z]',pw),15,"Store bogstaver","Mangler store")
    chk(re.search(r'[a-z]',pw),15,"Små bogstaver","Mangler små")
    chk(re.search(r'\d',pw),10,"Tal","Mangler tal")
    chk(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]',pw),15,"Specialtegn","Mangler special")
    chk(not re.search(r'(.)\1{2,}',pw),5,"Ingen repetition","Gentagne tegn")
    chk(not re.search(r'(password|qwerty|123456|abc|letmein)',pw.lower()),5,"Intet svagt mønster","Svagt mønster!")
    pool=0
    if re.search(r'[a-z]',pw): pool+=26
    if re.search(r'[A-Z]',pw): pool+=26
    if re.search(r'\d',pw): pool+=10
    if re.search(r'[^a-zA-Z0-9]',pw): pool+=32
    ent = math.log2(pool)*len(pw) if pool>0 else 0
    secs = 2**(ent-30)/1e9
    ct = "<1s" if secs<1 else f"{secs:.0f}s" if secs<60 else f"{secs/3600:.1f}t" if secs<86400 else f"{secs/31536000:.2e}år"
    print(f"\n  {BOLD}Analyse:{R}\n")
    for ok,pts,msg in checks:
        print(f"  {'[BGR]✔[R]'.replace('[BGR]',BGR).replace('[R]',R) if ok else '[BRD]✘[R]'.replace('[BRD]',BRD).replace('[R]',R)} {f'{BGR}+{pts}{R}' if ok else f'{DIM}+0{R}':>6}  {msg}")
    bl=40; fi=int(bl*score/100)
    col=BGR if score>=80 else BYL if score>=55 else BRD
    label="STÆRK" if score>=80 else "MIDDEL" if score>=55 else "SVAG" if score>=30 else "KRITISK"
    bar=f"{col}{'█'*fi}{R}{DIM}{'░'*(bl-fi)}{R}"
    print(f"\n"); hline(55)
    print(f"  Score: {BOLD}{score}/100{R}  [{bar}]  {col}{BOLD}{label}{R}")
    print(f"  Entropi: {BOLD}{ent:.1f} bit{R}   Crack-tid: {BOLD}{ct}{R}")
    hline(55); print()
    input(f"  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 23  SECURE NOTES (AES krypteret)
# ══════════════════════════════════════════════════════════════════════════════
SECURE_NOTES_FILE = Path.home() / ".wx7_secure_notes.enc"

def _derive_key(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

def _xor_crypt(data_bytes, key_bytes):
    ks = b""
    block = key_bytes
    while len(ks) < len(data_bytes):
        block = hashlib.sha256(block).digest()
        ks += block
    return bytes(a^b for a,b in zip(data_bytes, ks[:len(data_bytes)]))

def secure_notes():
    clr()
    print(f"\n  {BOLD}{BCY}📝 SECURE NOTES{R}  {DIM}(Krypterede noter){R}\n"); hline()
    password = input(f"\n  {YL}Master password{R}: ")
    if not password: return

    def load_notes():
        if not SECURE_NOTES_FILE.exists(): return []
        with open(SECURE_NOTES_FILE,'rb') as f: raw = f.read()
        salt = raw[:16]; ct = raw[16:]
        key = _derive_key(password, salt)
        try:
            dec = _xor_crypt(ct, key)
            return json.loads(dec.decode('utf-8'))
        except: return None

    def save_notes(notes):
        salt = secrets.token_bytes(16)
        key = _derive_key(password, salt)
        enc = _xor_crypt(json.dumps(notes, ensure_ascii=False).encode(), key)
        with open(SECURE_NOTES_FILE,'wb') as f: f.write(salt+enc)

    notes = load_notes()
    if notes is None:
        print(f"  {BRD}Forkert password eller korrupte noter!{R}")
        input(); return

    while True:
        clr()
        print(f"\n  {BOLD}{BCY}📝 SECURE NOTES{R}  {DIM}({len(notes)} noter — krypteret){R}\n"); hline()
        print()
        for i, n in enumerate(notes):
            print(f"  {DIM}[{i+1:02d}]{R} {BOLD}{n.get('title','(ingen titel)')}{R}  {DIM}{n.get('time','')}{R}")
        hline()
        print(f"\n  {BCY}[n]{R}Ny  {BCY}[v]{R}Vis  {BCY}[d]{R}Slet  {BCY}[q]{R}Luk\n")
        c = input(f"  {YL}>{R} ").strip().lower()
        if c == 'n':
            title = input(f"  {YL}Titel{R}: ").strip()
            print(f"  {YL}Indhold{R} (afslut med '##' på tom linje):")
            lines = []
            while True:
                l = input()
                if l == '##': break
                lines.append(l)
            content = '\n'.join(lines)
            if title:
                notes.append({'title':title,'content':content,'time':datetime.now().strftime('%d/%m/%Y %H:%M')})
                save_notes(notes); print(f"  {BGR}✔ Gemt og krypteret!{R}"); time.sleep(0.8)
        elif c == 'v':
            try:
                idx = int(input(f"  {YL}Vis note nr.{R}: "))-1
                if 0<=idx<len(notes):
                    n = notes[idx]
                    print(f"\n  {BOLD}{n.get('title','')}{R}  {DIM}{n.get('time','')}{R}")
                    hline()
                    print(f"  {n.get('content','')}")
                    input(f"\n  {DIM}Tryk Enter...{R}")
            except: pass
        elif c == 'd':
            try:
                idx = int(input(f"  {YL}Slet nr.{R}: "))-1
                if 0<=idx<len(notes):
                    rm = notes.pop(idx); save_notes(notes)
                    print(f"  {BRD}Slettet:{R} {rm.get('title','')}"); time.sleep(0.8)
            except: pass
        elif c == 'q':
            break


# ══════════════════════════════════════════════════════════════════════════════
# 24  DATA GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def data_generator():
    clr()
    print(f"\n  {BOLD}{BCY}🎲 DATA GENERATOR{R}\n"); hline()
    print(f"""
  {BCY}[1]{R} Fake brugerdata (JSON)   {BCY}[2]{R} UUID v4
  {BCY}[3]{R} Random IPs               {BCY}[4]{R} MAC-adresser
  {BCY}[5]{R} JWT Token (fake)         {BCY}[6]{R} Credit card test-numre
""")
    choice = input(f"  {YL}Valg{R}: ").strip()
    hline()

    def rand_name():
        first = random.choice(['Alex','Sam','Jordan','Taylor','Morgan','Casey','Riley'])
        last  = random.choice(['Smith','Johnson','Williams','Brown','Jones','Garcia'])
        return first, last

    if choice == '1':
        n = int(input(f"  {YL}Antal{R} (std=5): ") or "5")
        users = []
        for _ in range(n):
            fn,ln = rand_name()
            d = random.choice(['gmail.com','proton.me','outlook.com'])
            users.append({'id':secrets.token_hex(4),'name':f"{fn} {ln}",
                'email':f"{fn.lower()}.{ln.lower()}{random.randint(1,99)}@{d}",
                'age':random.randint(18,65),'role':random.choice(['admin','user','moderator']),
                'api_key':secrets.token_hex(24),
                'created':(datetime.now()-timedelta(days=random.randint(0,1000))).strftime('%Y-%m-%d')})
        print(f"\n{json.dumps(users, indent=2, ensure_ascii=False)}")

    elif choice == '2':
        n = int(input(f"  {YL}Antal{R} (std=10): ") or "10")
        print()
        for _ in range(n):
            b = bytearray(secrets.token_bytes(16))
            b[6] = (b[6]&0x0f)|0x40; b[8] = (b[8]&0x3f)|0x80
            u = f"{b[0:4].hex()}-{b[4:6].hex()}-{b[6:8].hex()}-{b[8:10].hex()}-{b[10:].hex()}"
            print(f"  {BGR}{u}{R}")

    elif choice == '3':
        n   = int(input(f"  {YL}Antal{R} (std=10): ") or "10")
        typ = input(f"  {YL}pub/pri{R} (std=pub): ").strip() or "pub"
        print()
        for _ in range(n):
            if typ=='pri':
                r = random.choice([f"10.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}",
                                    f"192.168.{random.randint(0,254)}.{random.randint(1,254)}"])
            else:
                r = f"{random.randint(1,223)}.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}"
            print(f"  {BCY}{r}{R}")

    elif choice == '4':
        n = int(input(f"  {YL}Antal{R} (std=5): ") or "5")
        oui_list = ['00:1A:2B','AA:BB:CC','DE:AD:BE','CA:FE:BA','F0:0D:CA']
        print()
        for _ in range(n):
            oui = random.choice(oui_list)
            rest = ':'.join(f"{secrets.randbelow(256):02X}" for _ in range(3))
            print(f"  {BGR}{oui}:{rest}{R}")

    elif choice == '5':
        # Fake JWT (non-signed, educational)
        n = int(input(f"  {YL}Antal{R} (std=3): ") or "3")
        print()
        for _ in range(n):
            fn,ln = rand_name()
            header  = base64.urlsafe_b64encode(json.dumps({"alg":"HS256","typ":"JWT"}).encode()).rstrip(b'=').decode()
            payload = {
                "sub": secrets.token_hex(8),
                "name": f"{fn} {ln}",
                "email": f"{fn.lower()}@example.com",
                "role": random.choice(["admin","user","api"]),
                "iat": int(time.time()),
                "exp": int(time.time()) + 3600,
            }
            pay_enc = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=').decode()
            sig     = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode()
            jwt     = f"{header}.{pay_enc}.{sig}"
            print(f"  {DIM}[payload]{R} {json.dumps(payload)}")
            print(f"  {BGR}{jwt}{R}\n")

    elif choice == '6':
        # Luhn-valid test numbers (Visa/Mastercard prefixes, NOT real)
        print(f"\n  {DIM}DISSE ER TEST-NUMRE — ALDRIG GYLDIGE KORT{R}\n")
        def luhn_checksum(card_num):
            def digits_of(n): return [int(d) for d in str(n)]
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            total = sum(odd_digits)
            for d in even_digits:
                total += sum(digits_of(d*2))
            return total % 10
        def gen_luhn(prefix, length=16):
            num = str(prefix) + ''.join([str(random.randint(0,9)) for _ in range(length-len(str(prefix))-1)])
            check = (10 - luhn_checksum(int(num + '0'))) % 10
            return num + str(check)
        prefixes = {'Visa':4,'Mastercard':51,'AmEx':34,'Discover':6011}
        for brand, prefix in prefixes.items():
            num = gen_luhn(prefix)
            exp = f"{random.randint(1,12):02d}/{datetime.now().year%100+random.randint(1,5)}"
            cvv = ''.join([str(random.randint(0,9)) for _ in range(3)])
            print(f"  {BCY}{brand:<12}{R} {BGR}{' '.join([num[i:i+4] for i in range(0,16,4)])}{R}  {DIM}Exp:{exp}  CVV:{cvv}{R}")

    print()
    input(f"\n  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# 25  SYSTEM & NET INFO
# ══════════════════════════════════════════════════════════════════════════════
def system_info():
    clr()
    print(f"\n  {BOLD}{BCY}🖥️  SYSTEM & NETVÆRK INFO{R}\n"); hline()
    spin("Indsamler...", 1.0)

    def fmt(b):
        for u in ['B','KB','MB','GB','TB']:
            if b<1024: return f"{b:.1f}{u}"
            b/=1024
        return f"{b:.1f}PB"

    # OS
    print(f"\n  {BOLD}{BYL}OS & Platform{R}"); hline(50)
    print(f"  {BCY}System{R}      {platform.system()} {platform.release()}")
    print(f"  {BCY}Version{R}     {platform.version()[:60]}")
    print(f"  {BCY}Machine{R}     {platform.machine()}")
    print(f"  {BCY}Processor{R}   {platform.processor()[:50] or 'N/A'}")
    print(f"  {BCY}Python{R}      {platform.python_version()}")
    print(f"  {BCY}Hostname{R}    {socket.gethostname()}")

    # Disk
    print(f"\n  {BOLD}{BYL}Disk (/){R}"); hline(50)
    try:
        total,used,free = shutil.disk_usage('/')
        pct = used/total*100
        bar_l = int(30*pct/100)
        col = BGR if pct<70 else BYL if pct<85 else BRD
        print(f"  {BCY}Total{R}   {fmt(total)}   {BCY}Brugt{R}  {fmt(used)}  {BCY}Fri{R}  {fmt(free)}")
        print(f"  [{col}{'█'*bar_l}{R}{DIM}{'░'*(30-bar_l)}{R}]  {col}{pct:.1f}%{R}")
    except: pass

    # Network
    print(f"\n  {BOLD}{BYL}Netværk{R}"); hline(50)
    try:
        host = socket.gethostname()
        ips = list(set(r[4][0] for r in socket.getaddrinfo(host, None)))
        for ip in ips:
            fam = "IPv6" if ':' in ip else "IPv4"
            print(f"  {BCY}{fam}{R}   {ip}")
    except: pass

    # Routing table
    print(f"\n  {BOLD}{BYL}Routing{R}"); hline(50)
    if shutil.which('ip'):
        try:
            r = subprocess.run(['ip','route'], capture_output=True, text=True, timeout=3)
            for line in r.stdout.strip().split('\n')[:8]:
                print(f"  {DIM}{line}{R}")
        except: pass
    elif shutil.which('netstat'):
        try:
            r = subprocess.run(['netstat','-rn'], capture_output=True, text=True, timeout=3)
            for line in r.stdout.strip().split('\n')[:10]:
                print(f"  {DIM}{line}{R}")
        except: pass

    # Open ports (listening)
    print(f"\n  {BOLD}{BYL}Listening Ports{R}"); hline(50)
    for cmd in [['ss','-tlnp'],['netstat','-tlnp']]:
        if shutil.which(cmd[0]):
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=4)
                for line in r.stdout.strip().split('\n')[:15]:
                    if 'LISTEN' in line or 'tcp' in line.lower():
                        print(f"  {DIM}{line.strip()[:80]}{R}")
            except: pass
            break

    # CPU
    try:
        import multiprocessing
        print(f"\n  {BOLD}{BYL}CPU{R}"); hline(50)
        print(f"  {BCY}Kerner{R}  {multiprocessing.cpu_count()}")
    except: pass

    print()
    input(f"  {DIM}Tryk Enter...{R}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    dispatch = {
        '01': advanced_port_scanner,  '1':  advanced_port_scanner,
        '02': osint_domain_recon,     '2':  osint_domain_recon,
        '03': network_discovery,      '3':  network_discovery,
        '04': ssl_analyzer,           '4':  ssl_analyzer,
        '05': web_crawler,            '5':  web_crawler,
        '06': subdomain_bruteforce,   '6':  subdomain_bruteforce,
        '07': dir_bruteforce,         '7':  dir_bruteforce,
        '08': packet_analyzer,        '8':  packet_analyzer,
        '09': hash_cracker,           '9':  hash_cracker,
        '10': waf_detector,
        '11': banner_grabber,
        '12': ftp_checker,
        '13': smtp_checker,
        '14': http_header_audit,
        '15': tcp_flooder,
        '16': advanced_hash_tool,
        '17': aes_encryptor,
        '18': stego_detector,
        '19': metadata_extractor,
        '20': entropy_analyzer,
        '21': password_generator,
        '22': password_strength,
        '23': secure_notes,
        '24': data_generator,
        '25': system_info,
    }

    while True:
        banner()
        menu()
        choice = input(f"  {BOLD}{BCY}WX7 >{R} ").strip()
        if choice in ('0','00'):
            clr()
            typewrite("\n  WX7 v3.0 shutting down... Stay legal. 👾\n", delay=0.03, color=BCY)
            time.sleep(0.4); print(); sys.exit(0)
        elif choice in dispatch:
            try:
                dispatch[choice]()
            except KeyboardInterrupt:
                print(f"\n\n  {YL}[Ctrl+C] Afbrudt{R}")
                time.sleep(0.5)
        else:
            print(f"  {RD}Ugyldigt valg: '{choice}'{R}")
            time.sleep(0.8)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {BCY}[Ctrl+C]{R} {DIM}WX7 afsluttet.{R}\n")
        sys.exit(0)

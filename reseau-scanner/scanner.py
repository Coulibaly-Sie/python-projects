import socket
import argparse
import threading
from datetime import datetime

# resultats partagés entre threads
resultats = []
lock = threading.Lock()

def tester_port(ip, port, timeout=0.5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        res = s.connect_ex((ip, port))
        s.close()
        if res == 0:
            with lock:
                resultats.append((ip, port))
            print(f"[+] {ip}:{port} OUVERT")
    except socket.error as e:
        # debug parfois utile
        # print(f"erreur socket {ip}:{port} -> {e}")
        pass

def parser_plage_ip(plage):
    # format attendu: 192.168.1.1-254 ou juste 192.168.1.1
    if '-' in plage:
        base, fin = plage.rsplit('.', 1)[0], plage.split('-')
        debut = int(plage.rsplit('.', 1)[1].split('-')[0])
        fin_val = int(fin[-1])
        base_ip = plage.rsplit('.', 1)[0]
        ips = [f"{base_ip}.{i}" for i in range(debut, fin_val + 1)]
    else:
        ips = [plage]
    return ips

def scanner_reseau(ips, ports, nb_threads=50):
    threads = []
    print(f"\n[*] Scan de {len(ips)} IP(s) sur {len(ports)} port(s)...")
    print(f"[*] Debut: {datetime.now().strftime('%H:%M:%S')}\n")

    for ip in ips:
        for port in ports:
            t = threading.Thread(target=tester_port, args=(ip, port))
            threads.append(t)
            t.start()

            # limiter le nombre de threads actifs
            actifs = [x for x in threads if x.is_alive()]
            while len(actifs) >= nb_threads:
                actifs = [x for x in threads if x.is_alive()]

    # attendre la fin de tous les threads
    for t in threads:
        t.join()

def main():
    parser = argparse.ArgumentParser(description='Scanner de ports reseau')
    parser.add_argument('plage', help='Plage IP ex: 192.168.1.1-254 ou 192.168.1.1')
    parser.add_argument('-p', '--ports', default='80,443,22,21,8080',
                        help='Ports a scanner, ex: 22,80,443 (defaut: 80,443,22,21,8080)')
    parser.add_argument('-t', '--threads', type=int, default=50,
                        help='Nombre de threads (defaut: 50)')
    parser.add_argument('--timeout', type=float, default=0.5,
                        help='Timeout par connexion en secondes')
    args = parser.parse_args()

    # parser les ports
    ports = []
    for p in args.ports.split(','):
        if '-' in p:
            debut, fin = p.split('-')
            ports.extend(range(int(debut), int(fin) + 1))
        else:
            ports.append(int(p.strip()))

    ips = parser_plage_ip(args.plage)
    print(f"IPs a scanner: {ips[0]} -> {ips[-1]} ({len(ips)} total)")
    print(f"Ports: {ports}")

    debut = datetime.now()
    scanner_reseau(ips, ports, args.threads)
    duree = (datetime.now() - debut).total_seconds()

    print(f"\n--- Resultats ---")
    print(f"Ports ouverts trouves: {len(resultats)}")
    for ip, port in sorted(resultats):
        print(f"  {ip}:{port}")
    print(f"Scan termine en {duree:.2f}s")

if __name__ == '__main__':
    main()

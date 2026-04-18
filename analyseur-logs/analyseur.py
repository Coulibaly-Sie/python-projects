import re
import argparse
from collections import Counter

# format Combined Log Apache/Nginx
# ex: 127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/4.08"
PATTERN = r'(\d+\.\d+\.\d+\.\d+) - \S+ \[.*?\] "(\w+) (\S+) \S+" (\d{3}) \d+'

def lire_logs(fichier):
    lignes = []
    with open(fichier, 'r') as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne:
                lignes.append(ligne)
    return lignes

def analyser(lignes):
    ips = []
    codes = []
    pages = []
    erreurs = []

    for ligne in lignes:
        m = re.match(PATTERN, ligne)
        if not m:
            # ligne mal formatee, on skip
            continue
        ip, methode, url, code = m.group(1), m.group(2), m.group(3), m.group(4)
        ips.append(ip)
        codes.append(code)
        pages.append(url)
        code_int = int(code)
        if code_int >= 400:
            erreurs.append((ip, methode, url, code))

    return ips, codes, pages, erreurs

def afficher_top(counter, titre, n=10):
    print(f"\n{titre}")
    print("-" * 40)
    for valeur, count in counter.most_common(n):
        print(f"  {valeur:<35} {count}")

def main():
    parser = argparse.ArgumentParser(description='Analyseur de logs Apache/Nginx')
    parser.add_argument('fichier', help='Fichier de log a analyser')
    parser.add_argument('-n', '--top', type=int, default=10,
                        help='Nombre de resultats a afficher (defaut: 10)')
    args = parser.parse_args()

    print(f"Lecture du fichier: {args.fichier}")
    lignes = lire_logs(args.fichier)
    print(f"Lignes lues: {len(lignes)}")

    ips, codes, pages, erreurs = analyser(lignes)

    print(f"\n=== RESUME ===")
    print(f"Total requetes parsees: {len(ips)}")
    print(f"IPs uniques: {len(set(ips))}")
    print(f"Erreurs 4xx/5xx: {len(erreurs)}")

    afficher_top(Counter(ips), f"Top {args.top} IPs les plus actives", args.top)
    afficher_top(Counter(pages), f"Top {args.top} pages les plus visitees", args.top)

    # codes d'erreur
    codes_erreur = [c for c in codes if int(c) >= 400]
    if codes_erreur:
        print(f"\nCodes erreur:")
        print("-" * 40)
        for code, count in Counter(codes_erreur).most_common():
            print(f"  HTTP {code}: {count} fois")

    # distribution globale des codes
    print(f"\nDistribution codes HTTP:")
    print("-" * 40)
    for code, count in sorted(Counter(codes).items()):
        print(f"  {code}: {count}")

if __name__ == '__main__':
    main()

import psutil
import os
import time
import argparse

def get_uptime():
    # uptime en secondes depuis le boot
    boot = psutil.boot_time()
    uptime_sec = time.time() - boot
    heures = int(uptime_sec // 3600)
    minutes = int((uptime_sec % 3600) // 60)
    secondes = int(uptime_sec % 60)
    return f"{heures}h {minutes}m {secondes}s"

def afficher_infos():
    os.system('clear' if os.name != 'nt' else 'cls')

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disque = psutil.disk_usage('/')
    uptime = get_uptime()

    print("=" * 45)
    print("       MONITEUR SYSTEME")
    print("=" * 45)

    # CPU
    barre_cpu = int(cpu / 5)
    print(f"\nCPU:   [{('#' * barre_cpu):<20}] {cpu:.1f}%")

    # RAM
    ram_pct = ram.percent
    barre_ram = int(ram_pct / 5)
    ram_utilise = ram.used / (1024**3)
    ram_total = ram.total / (1024**3)
    print(f"RAM:   [{('#' * barre_ram):<20}] {ram_pct:.1f}%  ({ram_utilise:.1f}/{ram_total:.1f} GB)")

    # Disque
    disk_pct = disque.percent
    barre_disk = int(disk_pct / 5)
    disk_utilise = disque.used / (1024**3)
    disk_total = disque.total / (1024**3)
    print(f"Disque:[{('#' * barre_disk):<20}] {disk_pct:.1f}%  ({disk_utilise:.1f}/{disk_total:.1f} GB)")

    print(f"\nUptime: {uptime}")

    # infos supplementaires
    nb_process = len(psutil.pids())
    print(f"Processus actifs: {nb_process}")

    # charge systeme (linux/mac seulement)
    try:
        load = os.getloadavg()
        print(f"Load average: {load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}")
    except AttributeError:
        pass  # windows ne supporte pas getloadavg

    print(f"\n[{time.strftime('%H:%M:%S')}] Ctrl+C pour quitter")

def main():
    parser = argparse.ArgumentParser(description='Moniteur systeme basique')
    parser.add_argument('-n', '--intervalle', type=int, default=2,
                        help='Intervalle de rafraichissement en secondes (defaut: 2)')
    args = parser.parse_args()

    print(f"Demarrage du moniteur (rafraichissement: {args.intervalle}s)")
    time.sleep(0.5)

    try:
        while True:
            afficher_infos()
            time.sleep(args.intervalle)
    except KeyboardInterrupt:
        print("\nArret du moniteur.")

if __name__ == '__main__':
    main()

# reseau-scanner

Scanner de ports réseau en Python (stdlib uniquement). Prend une plage IP et une liste de ports, teste les connexions en parallèle avec du threading et affiche les ports ouverts en temps réel.

## Utilisation

```bash
python scanner.py 192.168.1.1-254 -p 22,80,443,8080
python scanner.py 192.168.1.1 -p 1-1024 -t 100
```

# analyseur-logs

Script Python pour analyser des fichiers de logs Apache/Nginx au format Combined Log. Affiche les IPs les plus actives, les pages les plus visitées et les erreurs HTTP 4xx/5xx.

## Utilisation

```bash
python analyseur.py exemple.log
python analyseur.py /var/log/nginx/access.log -n 5
```

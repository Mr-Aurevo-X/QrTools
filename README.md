# QrMake

**© 2026 Mr-Aurevo-X · QrMake · 100% local · free · updates not guaranteed**

Générateur de QR codes multi-payloads — 100 % local, 100 % gratuit.  
Multi-payload QR generator — 100% local, 100% free.

Public showcase: [github.com/Mr-Aurevo-X/QrMake](https://github.com/Mr-Aurevo-X/QrMake)

Local SoT (public vitrine, **not** in L’Atelier Windows / PC Command):

`C:\Users\aurel\Documents\Dev Central Tree\Git Vitrine Public\QrMake`

## Legal / Légal

| FR | EN |
|:--|:--|
| **100 % gratuit** | **100% free** |
| **100 % local** — aucun cloud, aucune télémétrie | **100% local** — no cloud, no telemetry |
| **Mise à jour non garantie** — pas d’obligation / pas de SLA ; l’app *peut* vérifier GitHub Releases et proposer une màj des **sources** | **Updates not guaranteed** — no obligation / no SLA; the app *can* check GitHub Releases and offer a **source** update |
| **Copyright © 2026 Mr-Aurevo-X** — tous droits réservés | **Copyright © 2026 Mr-Aurevo-X** — all rights reserved |

Licence : **proprietary / all rights reserved** (voir `LICENSE`).  
Redistribution, reverse engineering ou suppression des mentions de copyright **interdits** sans accord écrit.  
Aligné avec les CGU Suite Mr-Aurevo-X (`MrAurevoX-UI/legal/`).

## Lancer (bat only)

Pas de `.exe` au quotidien — double-clic silencieux via `pythonw` + venv (pas de flash CMD).

```powershell
cd "C:\Users\aurel\Documents\Dev Central Tree\Git Vitrine Public\QrMake"
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\Lancer.bat
```

| Fichier | Usage |
|:--|:--|
| `Lancer.bat` / `QrMake.bat` | Double-clic **sans** fenêtre CMD (`pythonw` + `.venv`) |
| `Lancer.cmd` | Alias optionnel (`pythonw host\host.py`) — **pas** enregistré dans PC Command |

## Version & mises à jour (optionnel)

- Fichier version : `VERSION` à la racine (ex. `1.0.0`) — à bumper à chaque release.
- Au démarrage, vérif. **non bloquante** de  
  `https://api.github.com/repos/Mr-Aurevo-X/QrMake/releases/latest`
- Si le tag release est plus récent : bannière **Nouvelle version disponible** → **Mettre à jour** / **Plus tard**.
- **Mettre à jour** :
  - clone git → `git pull` (fast-forward)
  - sinon → télécharge le **zipball** sources GitHub et rafraîchit `host/`, `ui/`, etc.
- Aucun asset `QrMake.exe` requis.
- Mode auto : `%LOCALAPPDATA%\Mr-Aurevo-X\qrmake-settings.json` → `"autoUpdate": true`
- **Seul appel réseau optionnel** : cette vérif. / màj sources. La génération QR reste 100 % locale.
- « Mise à jour non garantie » = **juridique** (aucune promesse de futures releases).

## Modes (v1)

- Texte · URL (normalise `https://`) · Wi‑Fi (`WIFI:T:…;S:;P:;H:;;`)
- Mot de passe (secret, champ masquable)
- Contact vCard 3.0 · Email `mailto` · Tel · SMS · Geo · Event `VEVENT` · WhatsApp `wa.me` · Brut
- Aperçu live · ECC L/M/Q/H (défaut M) · taille PNG 256–1024
- Sauver PNG · copier image · copier payload

## UI kit

Chrome propriétaire : SoT `Dev Central Tree\UI proprietaire\` → `ui\vendor\pc-command-kit`  
Sync : `.\scripts\Sync-All-UiKit.ps1` depuis la racine Dev Central Tree (**ne pas** éditer le vendor à la main).

## Stack

Python · pywebview · qrcode[pil] · Pillow · PC Command kit  
(`Build.cmd` / `QrMake.spec` restent dans le dépôt mais ne sont **pas** le chemin de lancement quotidien.)

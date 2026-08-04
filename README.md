# QrMake

**© 2026 Mr-Aurevo-X · QrMake · 100% local · free · updates not guaranteed**

Générateur de QR codes multi-payloads — 100 % local, 100 % gratuit.  
Multi-payload QR generator — 100% local, 100% free.

Public showcase: [github.com/Mr-Aurevo-X/QrMake](https://github.com/Mr-Aurevo-X/QrMake)

## Legal / Légal

| FR | EN |
|:--|:--|
| **100 % gratuit** | **100% free** |
| **100 % local** — aucun cloud, aucune télémétrie | **100% local** — no cloud, no telemetry |
| **Mise à jour non garantie** — pas d’obligation / pas de SLA ; l’app *peut* se mettre à jour depuis GitHub Releases si une release existe | **Updates not guaranteed** — no obligation / no SLA; the app *can* update from GitHub Releases when a release exists |
| **Copyright © 2026 Mr-Aurevo-X** — tous droits réservés | **Copyright © 2026 Mr-Aurevo-X** — all rights reserved |

Licence : **proprietary / all rights reserved** (voir `LICENSE`).  
Redistribution, reverse engineering ou suppression des mentions de copyright **interdits** sans accord écrit.  
Aligné avec les CGU Suite Mr-Aurevo-X (`MrAurevoX-UI/legal/`).

Le binaire PyInstaller (`QrMake.exe`) est windowed ; les sources ne sont pas destinées à la redistribution.

## Version & mises à jour (optionnel)

- Fichier version : `VERSION` à la racine (ex. `1.0.0`) — à bumper à chaque release.
- Au démarrage, QrMake fait une vérif. **non bloquante** de  
  `https://api.github.com/repos/Mr-Aurevo-X/QrMake/releases/latest`
- Si une release plus récente publie l’asset `QrMake.exe` (ou un zip le contenant) : bannière  
  **Nouvelle version disponible** → **Mettre à jour** / **Plus tard**.
- Mode auto : `%LOCALAPPDATA%\Mr-Aurevo-X\qrmake-settings.json` → `"autoUpdate": true`  
  (applique dès qu’une release plus récente est trouvée).
- **Seul appel réseau optionnel** : cette vérif. / téléchargement. La génération QR reste 100 % locale.
- « Mise à jour non garantie » = **juridique** (aucune promesse de futures releases).  
  L’auto-update = **confort technique** quand *vous* publiez une GitHub Release.

## Modes (v1)

- Texte · URL (normalise `https://`) · Wi‑Fi (`WIFI:T:…;S:;P:;H:;;`)
- Mot de passe (secret, champ masquable)
- Contact vCard 3.0 · Email `mailto` · Tel · SMS · Geo · Event `VEVENT` · WhatsApp `wa.me` · Brut
- Aperçu live · ECC L/M/Q/H (défaut M) · taille PNG 256–1024
- Sauver PNG · copier image · copier payload

## Lancer en local (tests)

SoT path:

`C:\Users\aurel\Documents\Dev Central Tree\L'Atelier Windows\QrMake`

```powershell
cd "C:\Users\aurel\Documents\Dev Central Tree\L'Atelier Windows\QrMake"
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\Lancer.bat
```

| Fichier | Usage |
|:--|:--|
| `Lancer.bat` / `QrMake.bat` | Double-clic **sans** fenêtre CMD noire (`pythonw` / exe) |
| `Lancer.cmd` | Hub PC Command → `pythonw host\host.py` (ou exe si présent) |
| `QrMake.exe` | Binaire windowed (après `Build.cmd`) |

## Build .exe

```powershell
cd "C:\Users\aurel\Documents\Dev Central Tree\L'Atelier Windows\QrMake"
.\Build.cmd
```

Produit `dist\QrMake.exe` puis copie vers `QrMake.exe` à la racine.  
Le `.exe` peut être gitignoré / non poussé (artefact local) — rebuild via `Build.cmd`.

Pour publier une mise à jour : bumper `VERSION`, build, créer une **GitHub Release** avec l’asset `QrMake.exe` (tag `v1.x.y` ou `1.x.y`).

## UI kit

Chrome propriétaire : SoT `Dev Central Tree\UI proprietaire\` → `ui\vendor\pc-command-kit`  
Sync : `.\scripts\Sync-All-UiKit.ps1` depuis la racine Dev Central Tree (**ne pas** éditer le vendor à la main).

## Stack

Python · pywebview · qrcode[pil] · Pillow · PyInstaller · PC Command kit

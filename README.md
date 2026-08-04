# QrMake

**[Download QrMake.exe](https://github.com/Mr-Aurevo-X/QrMake/releases/latest/download/QrMake.exe)** · **[All releases](https://github.com/Mr-Aurevo-X/QrMake/releases)**

> Direct Windows binary (latest). Open [Releases](https://github.com/Mr-Aurevo-X/QrMake/releases) if the right-sidebar “Releases” link is scrolled away — downloads are **not** under “Tags”.

**© 2026 Mr-Aurevo-X — QrMake — 100% local — free — updates not guaranteed**

Générateur de QR codes multi-payloads — 100 % local, 100 % gratuit.  
Multi-payload QR generator — 100% local, 100% free.

## Download / Téléchargement

- **One-click:** [QrMake.exe](https://github.com/Mr-Aurevo-X/QrMake/releases/latest/download/QrMake.exe)
- **Release notes / all versions:** [github.com/Mr-Aurevo-X/QrMake/releases](https://github.com/Mr-Aurevo-X/QrMake/releases)

Double-cliquer sur `QrMake.exe` pour lancer (pas d'installation).  
Double-click `QrMake.exe` to run (no install).

Local SoT (public vitrine, **not** in L’Atelier Windows / PC Command):

`C:\Users\aurel\Documents\Dev Central Tree\Git Vitrine Public\QrMake`

## Legal / Légal

| FR | EN |
|:--|:--|
| **100 % gratuit** | **100% free** |
| **100 % local** — aucun cloud, aucune télémétrie | **100% local** — no cloud, no telemetry |
| **Mise à jour non garantie** — pas d’obligation / pas de SLA ; l’app *peut* vérifier GitHub Releases et proposer une màj | **Updates not guaranteed** — no obligation / no SLA; the app *can* check GitHub Releases and offer an update |
| **Copyright © 2026 Mr-Aurevo-X** — tous droits réservés | **Copyright © 2026 Mr-Aurevo-X** — all rights reserved |

Licence : **proprietary / all rights reserved** (voir `LICENSE`).  
Redistribution, reverse engineering ou suppression des mentions de copyright **interdits** sans accord écrit.  
Aligné avec les CGU Suite Mr-Aurevo-X (`MrAurevoX-UI/legal/`).

Le binaire PyInstaller (`QrMake.exe`) est windowed ; redistribution des sources/exe sans accord écrit interdite.

## Lancer (exe primary)

**Double-clic `QrMake.exe`** — lancement principal, sans flash CMD.

```powershell
cd "C:\Users\aurel\Documents\Dev Central Tree\Git Vitrine Public\QrMake"
# After Build.cmd:
.\QrMake.exe
```

| Fichier | Usage |
|:--|:--|
| `QrMake.exe` | **Principal** — binaire windowed (après `Build.cmd`) |
| `Lancer.bat` / `QrMake.bat` | Si `QrMake.exe` est présent → `start` l’exe puis exit ; sinon fallback `pythonw` détaché |
| `Lancer.cmd` | Même logique (alias optionnel — **pas** enregistré dans PC Command) |

Dev / sans exe :

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\Lancer.bat
```

## Version & mises à jour (optionnel)

- Fichier version : `VERSION` à la racine (ex. `1.0.1`) — à bumper à chaque release.
- Au démarrage, vérif. **non bloquante** de  
  `https://api.github.com/repos/Mr-Aurevo-X/QrMake/releases/latest`
- Si le tag release est plus récent :
  - **mode exe (frozen)** → asset GitHub `QrMake.exe` (ou zip le contenant) → remplace + relance
  - **mode sources** → `git pull` (clone) ou zipball sources GitHub
- Mode auto : `%LOCALAPPDATA%\Mr-Aurevo-X\qrmake-settings.json` → `"autoUpdate": true`
- **Seul appel réseau optionnel** : cette vérif. / màj. La génération QR reste 100 % locale.
- « Mise à jour non garantie » = **juridique** (aucune promesse de futures releases).

## Build .exe

```powershell
cd "C:\Users\aurel\Documents\Dev Central Tree\Git Vitrine Public\QrMake"
.\Build.cmd
```

Ou :

```powershell
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean QrMake.spec
copy /Y dist\QrMake.exe QrMake.exe
```

Produit `dist\QrMake.exe` puis copie vers `QrMake.exe` à la racine.  
Le `.exe` peut être gitignoré — rebuild via `Build.cmd`.  
Pour publier une màj : bumper `VERSION`, build, créer une **GitHub Release** avec l’asset `QrMake.exe`.

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

Python · pywebview · qrcode[pil] · Pillow · PyInstaller · PC Command kit

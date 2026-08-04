"""Optional GitHub Releases updater for QrMake.

Legal: updates are not guaranteed (no SLA). This module only checks / applies
a published GitHub Release when one exists — the sole optional network call.
"""
# © 2026 Mr-Aurevo-X · QrMake · 100% local · free · updates not guaranteed
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

RELEASE_REPO = "Mr-Aurevo-X/QrMake"
API_LATEST = f"https://api.github.com/repos/{RELEASE_REPO}/releases/latest"
USER_AGENT = "QrMake-Updater/1.0 (+https://github.com/Mr-Aurevo-X/QrMake)"
EXE_NAME = "QrMake.exe"
VERSION_NAME = "VERSION"
SETTINGS_NAME = "qrmake-settings.json"


def _local_appdata() -> Path:
    local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(local) / "Mr-Aurevo-X"


def settings_path() -> Path:
    return _local_appdata() / SETTINGS_NAME


def load_settings() -> dict[str, Any]:
    path = settings_path()
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError, TypeError):
        return {}


def save_settings(patch: dict[str, Any]) -> dict[str, Any]:
    path = settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = load_settings()
    data.update(patch)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def read_local_version(root: Path | None = None) -> str:
    root = root or app_dir()
    candidates = [root / VERSION_NAME]
    if getattr(sys, "frozen", False):
        meipass = Path(getattr(sys, "_MEIPASS", root))
        candidates.append(meipass / VERSION_NAME)
    for path in candidates:
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8").strip()
                if text:
                    return _normalize_version(text)
            except OSError:
                continue
    return "0.0.0"


def _normalize_version(raw: str) -> str:
    s = (raw or "").strip()
    if s.lower().startswith("v"):
        s = s[1:]
    # tag_name may be "1.0.1" or "v1.0.1-qr"
    m = re.match(r"^(\d+(?:\.\d+)*)", s)
    return m.group(1) if m else s


def parse_version(raw: str) -> tuple[int, ...]:
    parts = _normalize_version(raw).split(".")
    out: list[int] = []
    for p in parts:
        try:
            out.append(int(p))
        except ValueError:
            out.append(0)
    while len(out) < 3:
        out.append(0)
    return tuple(out)


def is_newer(remote: str, local: str) -> bool:
    return parse_version(remote) > parse_version(local)


def _http_get(url: str, accept: str = "application/vnd.github+json") -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    token = (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or "").strip()
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read()


def _pick_asset(release: dict) -> dict | None:
    assets = release.get("assets") or []
    if not isinstance(assets, list):
        return None
    exe = None
    zip_asset = None
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        name = str(asset.get("name") or "").strip()
        lower = name.lower()
        if lower == EXE_NAME.lower():
            exe = asset
            break
        if lower.endswith(".zip") and zip_asset is None:
            zip_asset = asset
    return exe or zip_asset


def check_for_update() -> dict[str, Any]:
    """Non-blocking friendly: call from a worker / JS after UI boot."""
    local = read_local_version()
    settings = load_settings()
    skipped = str(settings.get("skipVersion") or "").strip()
    try:
        raw = _http_get(API_LATEST)
        release = json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # 404 = no releases yet — not an error for the user
        if exc.code == 404:
            return {
                "ok": True,
                "updateAvailable": False,
                "local": local,
                "remote": None,
                "error": None,
                "reason": "no_releases",
                "autoUpdate": bool(settings.get("autoUpdate")),
                "repo": RELEASE_REPO,
            }
        return {
            "ok": False,
            "updateAvailable": False,
            "local": local,
            "remote": None,
            "error": f"HTTP {exc.code}",
            "autoUpdate": bool(settings.get("autoUpdate")),
            "repo": RELEASE_REPO,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "updateAvailable": False,
            "local": local,
            "remote": None,
            "error": str(exc),
            "autoUpdate": bool(settings.get("autoUpdate")),
            "repo": RELEASE_REPO,
        }

    tag = str(release.get("tag_name") or release.get("name") or "").strip()
    remote = _normalize_version(tag)
    asset = _pick_asset(release)
    available = bool(remote and is_newer(remote, local) and asset)
    if skipped and _normalize_version(skipped) == remote:
        available = False
    return {
        "ok": True,
        "updateAvailable": available,
        "local": local,
        "remote": remote or None,
        "tag": tag or None,
        "name": release.get("name"),
        "body": (release.get("body") or "")[:2000],
        "htmlUrl": release.get("html_url"),
        "assetName": (asset or {}).get("name"),
        "assetUrl": (asset or {}).get("browser_download_url"),
        "assetApiUrl": (asset or {}).get("url"),
        "autoUpdate": bool(settings.get("autoUpdate")),
        "error": None if asset or not is_newer(remote, local) else "no_asset",
        "repo": RELEASE_REPO,
    }


def dismiss_update(version: str | None = None) -> dict[str, Any]:
    """Remember 'Later' for this remote version (session + persist skip)."""
    ver = _normalize_version(version or "")
    if ver:
        save_settings({"skipVersion": ver})
    return {"ok": True, "skipVersion": ver or None}


def set_auto_update(enabled: bool) -> dict[str, Any]:
    data = save_settings({"autoUpdate": bool(enabled)})
    return {"ok": True, "autoUpdate": bool(data.get("autoUpdate"))}


def _download_asset(asset_api_url: str | None, browser_url: str | None, dest: Path) -> None:
    url = (asset_api_url or browser_url or "").strip()
    if not url:
        raise RuntimeError("Asset URL manquante")
    # Prefer API octet-stream when we have an API asset URL
    accept = "application/octet-stream" if asset_api_url else "*/*"
    data = _http_get(url if asset_api_url else (browser_url or url), accept=accept)
    dest.write_bytes(data)


def _extract_exe_from_zip(zip_path: Path, dest_exe: Path) -> None:
    with zipfile.ZipFile(zip_path, "r") as zf:
        members = [n for n in zf.namelist() if n.replace("\\", "/").rstrip("/").split("/")[-1].lower() == EXE_NAME.lower()]
        if not members:
            raise RuntimeError(f"{EXE_NAME} introuvable dans le zip")
        # Prefer shallowest path
        members.sort(key=lambda n: n.count("/"))
        with zf.open(members[0]) as src, dest_exe.open("wb") as out:
            out.write(src.read())
        # Optional VERSION inside zip
        ver_members = [
            n
            for n in zf.namelist()
            if n.replace("\\", "/").rstrip("/").split("/")[-1].upper() == VERSION_NAME
        ]
        if ver_members:
            ver_members.sort(key=lambda n: n.count("/"))
            try:
                text = zf.read(ver_members[0]).decode("utf-8").strip()
                if text:
                    (dest_exe.parent / VERSION_NAME).write_text(text + "\n", encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                pass


def _write_finish_script(target_exe: Path, staged_exe: Path, version: str) -> Path:
    """Batch that waits for this process to exit, replaces exe, writes VERSION, relaunches."""
    script = target_exe.parent / "_qrmake_update_finish.cmd"
    pid = os.getpid()
    # Escape for cmd: use short paths via quotes
    lines = [
        "@echo off",
        "setlocal",
        f'set "TARGET={target_exe}"',
        f'set "STAGED={staged_exe}"',
        f'set "VERFILE={target_exe.parent / VERSION_NAME}"',
        f"set \"PID={pid}\"",
        f'set "NEWVER={version}"',
        ":wait",
        'tasklist /FI "PID eq %PID%" 2>nul | find "%PID%" >nul',
        "if not errorlevel 1 (",
        "  timeout /t 1 /nobreak >nul",
        "  goto wait",
        ")",
        'copy /Y "%STAGED%" "%TARGET%" >nul',
        'if exist "%STAGED%" del /F /Q "%STAGED%" >nul 2>&1',
        'echo %NEWVER%>"%VERFILE%"',
        'start "" "%TARGET%"',
        'del /F /Q "%~f0" >nul 2>&1',
    ]
    script.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")
    return script


def apply_update() -> dict[str, Any]:
    """Download latest release asset and schedule replace + relaunch when frozen."""
    local = read_local_version()
    try:
        raw = _http_get(API_LATEST)
        release = json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"ok": False, "applied": False, "local": local, "error": f"HTTP {exc.code}"}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "applied": False, "local": local, "error": str(exc)}

    tag = str(release.get("tag_name") or release.get("name") or "").strip()
    remote = _normalize_version(tag)
    asset = _pick_asset(release)
    if not remote or not asset:
        return {
            "ok": True,
            "applied": False,
            "local": local,
            "remote": remote or None,
            "error": None,
            "reason": "no_asset" if remote else "no_releases",
        }
    if not is_newer(remote, local):
        return {
            "ok": True,
            "applied": False,
            "updateAvailable": False,
            "local": local,
            "remote": remote,
            "error": None,
            "reason": "up_to_date",
        }

    asset_name = str(asset.get("name") or "")
    root = app_dir()
    target_exe = Path(sys.executable).resolve() if getattr(sys, "frozen", False) else root / EXE_NAME

    try:
        tmp_dir = Path(tempfile.mkdtemp(prefix="qrmake-upd-"))
        staged = tmp_dir / EXE_NAME
        if asset_name.lower().endswith(".zip"):
            zip_path = tmp_dir / "release.zip"
            _download_asset(asset.get("url"), asset.get("browser_download_url"), zip_path)
            _extract_exe_from_zip(zip_path, staged)
        else:
            _download_asset(asset.get("url"), asset.get("browser_download_url"), staged)

        if not staged.is_file() or staged.stat().st_size < 1024:
            raise RuntimeError("Téléchargement invalide")

        (root / VERSION_NAME).write_text(remote + "\n", encoding="utf-8")
        save_settings({"skipVersion": ""})

        # Replace running / existing exe via finish script (file may be locked)
        if getattr(sys, "frozen", False) or target_exe.is_file():
            beside = target_exe.with_suffix(".exe.new")
            beside.write_bytes(staged.read_bytes())
            script = _write_finish_script(target_exe, beside, remote)
            creationflags = 0x08000000  # CREATE_NO_WINDOW
            subprocess.Popen(  # noqa: S603
                ["cmd.exe", "/c", str(script)],
                cwd=str(target_exe.parent),
                creationflags=creationflags,
                close_fds=True,
            )
            return {
                "ok": True,
                "applied": True,
                "restarting": True,
                "local": local,
                "remote": remote,
                "error": None,
            }

        target_exe.write_bytes(staged.read_bytes())
        return {
            "ok": True,
            "applied": True,
            "restarting": False,
            "local": local,
            "remote": remote,
            "path": str(target_exe),
            "error": None,
            "note": "QrMake.exe mis à jour — relancez via Lancer.bat",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "applied": False,
            "error": str(exc),
            "local": local,
            "remote": remote,
        }

"""Optional GitHub update check for QrMake (sources / bat-only).

Legal: updates are not guaranteed (no SLA). Compares local VERSION to the
latest GitHub release tag. Apply prefers `git pull` in a clone; otherwise
refreshes tracked files from the release source zip. No .exe asset required.
"""
# © 2026 Mr-Aurevo-X · QrMake · 100% local · free · updates not guaranteed
from __future__ import annotations

import json
import os
import re
import shutil
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
VERSION_NAME = "VERSION"
SETTINGS_NAME = "qrmake-settings.json"

# Paths refreshed from a source zip (never wipe .venv / local exe leftovers)
REFRESH_TOP = ("host", "ui", "VERSION", "requirements.txt", "Lancer.bat", "QrMake.bat", "Lancer.cmd", "README.md", "LICENSE", "brand-icon.ico")


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
    return Path(__file__).resolve().parent.parent


def read_local_version(root: Path | None = None) -> str:
    root = root or app_dir()
    path = root / VERSION_NAME
    if path.is_file():
        try:
            text = path.read_text(encoding="utf-8").strip()
            if text:
                return _normalize_version(text)
        except OSError:
            pass
    return "0.0.0"


def _normalize_version(raw: str) -> str:
    s = (raw or "").strip()
    if s.lower().startswith("v"):
        s = s[1:]
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


def is_git_clone(root: Path | None = None) -> bool:
    root = root or app_dir()
    return (root / ".git").is_dir()


def _git(args: list[str], root: Path | None = None) -> subprocess.CompletedProcess[str]:
    root = root or app_dir()
    return subprocess.run(  # noqa: S603
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def check_for_update() -> dict[str, Any]:
    """Non-blocking friendly: call from JS after UI boot. No exe asset required."""
    local = read_local_version()
    settings = load_settings()
    skipped = str(settings.get("skipVersion") or "").strip()
    try:
        raw = _http_get(API_LATEST)
        release = json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {
                "ok": True,
                "updateAvailable": False,
                "local": local,
                "remote": None,
                "error": None,
                "reason": "no_releases",
                "autoUpdate": bool(settings.get("autoUpdate")),
                "mode": "sources",
                "gitClone": is_git_clone(),
                "repo": RELEASE_REPO,
            }
        return {
            "ok": False,
            "updateAvailable": False,
            "local": local,
            "remote": None,
            "error": f"HTTP {exc.code}",
            "autoUpdate": bool(settings.get("autoUpdate")),
            "mode": "sources",
            "gitClone": is_git_clone(),
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
            "mode": "sources",
            "gitClone": is_git_clone(),
            "repo": RELEASE_REPO,
        }

    tag = str(release.get("tag_name") or release.get("name") or "").strip()
    remote = _normalize_version(tag)
    available = bool(remote and is_newer(remote, local))
    if skipped and _normalize_version(skipped) == remote:
        available = False
    zipball = release.get("zipball_url") or f"https://api.github.com/repos/{RELEASE_REPO}/zipball/{tag}"
    return {
        "ok": True,
        "updateAvailable": available,
        "local": local,
        "remote": remote or None,
        "tag": tag or None,
        "name": release.get("name"),
        "body": (release.get("body") or "")[:2000],
        "htmlUrl": release.get("html_url"),
        "zipballUrl": zipball,
        "autoUpdate": bool(settings.get("autoUpdate")),
        "mode": "sources",
        "gitClone": is_git_clone(),
        "error": None,
        "repo": RELEASE_REPO,
    }


def dismiss_update(version: str | None = None) -> dict[str, Any]:
    ver = _normalize_version(version or "")
    if ver:
        save_settings({"skipVersion": ver})
    return {"ok": True, "skipVersion": ver or None}


def set_auto_update(enabled: bool) -> dict[str, Any]:
    data = save_settings({"autoUpdate": bool(enabled)})
    return {"ok": True, "autoUpdate": bool(data.get("autoUpdate"))}


def _apply_via_git_pull(remote: str) -> dict[str, Any]:
    root = app_dir()
    local = read_local_version(root)
    fetch = _git(["fetch", "--tags", "origin"], root)
    if fetch.returncode != 0:
        return {
            "ok": False,
            "applied": False,
            "local": local,
            "remote": remote,
            "error": (fetch.stderr or fetch.stdout or "git fetch failed").strip()[:500],
            "method": "git_pull",
        }
    pull = _git(["pull", "--ff-only", "origin", "HEAD"], root)
    if pull.returncode != 0:
        # Fallback: pull current branch
        branch = _git(["rev-parse", "--abbrev-ref", "HEAD"], root)
        br = (branch.stdout or "main").strip() or "main"
        pull = _git(["pull", "--ff-only", "origin", br], root)
    if pull.returncode != 0:
        return {
            "ok": False,
            "applied": False,
            "local": local,
            "remote": remote,
            "error": (pull.stderr or pull.stdout or "git pull failed").strip()[:500],
            "method": "git_pull",
        }
    save_settings({"skipVersion": ""})
    new_local = read_local_version(root)
    return {
        "ok": True,
        "applied": True,
        "restarting": False,
        "local": local,
        "remote": remote,
        "newLocal": new_local,
        "method": "git_pull",
        "error": None,
        "note": "Sources mises à jour via git pull — relancez Lancer.bat",
    }


def _copy_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def _apply_via_source_zip(release: dict, remote: str) -> dict[str, Any]:
    root = app_dir()
    local = read_local_version(root)
    tag = str(release.get("tag_name") or "").strip()
    zip_url = str(release.get("zipball_url") or "").strip()
    if not zip_url and tag:
        zip_url = f"https://api.github.com/repos/{RELEASE_REPO}/zipball/{tag}"
    if not zip_url:
        return {
            "ok": False,
            "applied": False,
            "local": local,
            "remote": remote,
            "error": "zipball URL manquante",
            "method": "source_zip",
        }

    tmp_dir = Path(tempfile.mkdtemp(prefix="qrmake-src-"))
    try:
        zip_path = tmp_dir / "source.zip"
        zip_path.write_bytes(_http_get(zip_url, accept="application/vnd.github+json"))
        extract_dir = tmp_dir / "extracted"
        extract_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)
        tops = [p for p in extract_dir.iterdir() if p.is_dir()]
        if not tops:
            raise RuntimeError("Archive source vide")
        # GitHub zipball has a single top folder repo-sha
        src_root = tops[0]
        for name in REFRESH_TOP:
            src = src_root / name
            if not src.exists():
                continue
            _copy_tree(src, root / name)
        # Always write VERSION from remote tag when present
        (root / VERSION_NAME).write_text(remote + "\n", encoding="utf-8")
        save_settings({"skipVersion": ""})
        return {
            "ok": True,
            "applied": True,
            "restarting": False,
            "local": local,
            "remote": remote,
            "newLocal": read_local_version(root),
            "method": "source_zip",
            "error": None,
            "note": "Sources rafraîchies depuis GitHub — relancez Lancer.bat",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "applied": False,
            "local": local,
            "remote": remote,
            "error": str(exc),
            "method": "source_zip",
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def apply_update() -> dict[str, Any]:
    """Update sources: git pull if clone, else release source zipball. No .exe."""
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
    if not remote:
        return {
            "ok": True,
            "applied": False,
            "local": local,
            "remote": None,
            "error": None,
            "reason": "no_releases",
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

    if is_git_clone():
        return _apply_via_git_pull(remote)
    return _apply_via_source_zip(release, remote)

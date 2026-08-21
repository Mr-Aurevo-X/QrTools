# Copyright (c) 2026 Mr-Aurevo-X. All rights reserved.
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Author: Mr-Aurevo-X | https://github.com/Mr-Aurevo-X

"""QrTools — générateur de QR codes multi-payloads (100 % local).

© 2026 Mr-Aurevo-X · QrTools · 100% local · free · updates not guaranteed
All rights reserved. Redistribution / reverse engineering without written consent forbidden.
"""
# © 2026 Mr-Aurevo-X · QrTools · 100% local · free · updates not guaranteed
from __future__ import annotations

import base64
import csv as csv_mod
import io
import json
import os
import urllib.parse
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote

import qrcode
from qrcode.constants import (
    ERROR_CORRECT_H,
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
)
from qrcode.image.pil import PilImage

import webview

_HOST_DIR = Path(__file__).resolve().parent
if str(_HOST_DIR) not in sys.path:
    sys.path.insert(0, str(_HOST_DIR))

import updater as QrTools_updater
from window_chrome import WindowChromeMixin, create_tool_window

DEFAULT_ACCENT = "#e03545"
ENV_ACCENT = "MRAUREVOX_ACCENT"
ENV_LANG = "MRAUREVOX_LANG"

ECC_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def ui_dir() -> Path:
    external = app_dir() / "ui"
    if (external / "index.html").is_file():
        return external
    if getattr(sys, "frozen", False):
        base = Path(getattr(sys, "_MEIPASS", app_dir()))
        nested = base / "ui"
        return nested if nested.is_dir() else base
    return app_dir() / "ui"


def _local_appdata() -> Path:
    local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(local) / "Mr-Aurevo-X"


def resolve_suite_accent(default: str = DEFAULT_ACCENT) -> str:
    env = (os.environ.get(ENV_ACCENT) or "").strip()
    if env.startswith("#") and len(env) in (4, 7):
        return env
    path = _local_appdata() / "user-settings.json"
    if path.is_file():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8-sig"))
            accent = str((loaded or {}).get("accent") or "").strip()
            if accent.startswith("#") and len(accent) in (4, 7):
                return accent
        except (OSError, json.JSONDecodeError, TypeError):
            pass
    return default


def resolve_suite_language(default: str = "fr") -> str:
    env = (os.environ.get(ENV_LANG) or "").strip().lower()
    if env in ("fr", "en"):
        return env
    path = _local_appdata() / "user-settings.json"
    if path.is_file():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8-sig"))
            lang = str((loaded or {}).get("language") or "").strip().lower()
            if lang in ("fr", "en"):
                return lang
        except (OSError, json.JSONDecodeError, TypeError):
            pass
    return default if default in ("fr", "en") else "fr"


def resolve_suite_theme(default: str = "dark") -> str:
    path = _local_appdata() / "user-settings.json"
    if path.is_file():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8-sig"))
            theme = str((loaded or {}).get("theme") or "").strip().lower()
            if theme in ("dark", "light"):
                return theme
        except (OSError, json.JSONDecodeError, TypeError):
            pass
    return default if default in ("dark", "light") else "dark"


def _wifi_escape(value: str) -> str:
    return (
        str(value or "")
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace(":", "\\:")
        .replace('"', '\\"')
    )


def _normalize_url(raw: str) -> str:
    text = (raw or "").strip()
    if not text:
        return ""
    if re.match(r"^[a-z][a-z0-9+.-]*:", text, re.I):
        return text
    return "https://" + text


def _escape_vcard(value: str) -> str:
    return (
        str(value or "")
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _format_ics_dt(value: str, all_day: bool = False) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    # Accept ISO local or date-only
    if all_day or re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        day = text[:10].replace("-", "")
        return day
    try:
        if text.endswith("Z"):
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
            return dt.strftime("%Y%m%dT%H%M%SZ")
        dt = datetime.fromisoformat(text)
        return dt.strftime("%Y%m%dT%H%M%S")
    except ValueError:
        digits = re.sub(r"[^0-9TZ]", "", text.upper())
        return digits


def build_payload(mode: str, fields: dict[str, Any] | None = None) -> dict[str, Any]:
    # © 2026 Mr-Aurevo-X · QrTools · payload builders · 100% local
    mode = (mode or "text").strip().lower()
    f = fields if isinstance(fields, dict) else {}

    if mode == "text":
        payload = str(f.get("text") or "")
    elif mode == "url":
        payload = _normalize_url(str(f.get("url") or ""))
    elif mode == "wifi":
        ssid = _wifi_escape(str(f.get("ssid") or ""))
        password = _wifi_escape(str(f.get("password") or ""))
        auth = str(f.get("auth") or "WPA").strip().upper()
        if auth not in ("WPA", "WEP", "NOPASS"):
            auth = "WPA"
        hidden = "true" if f.get("hidden") else "false"
        payload = f"WIFI:T:{auth};S:{ssid};"
        if auth != "NOPASS":
            payload += f"P:{password};"
        payload += f"H:{hidden};;"
    elif mode in ("password", "secret"):
        payload = str(f.get("password") or f.get("text") or "")
    elif mode == "vcard":
        fn = str(f.get("fullName") or f.get("name") or "").strip()
        org = str(f.get("org") or "").strip()
        title = str(f.get("title") or "").strip()
        tel = str(f.get("tel") or "").strip()
        email = str(f.get("email") or "").strip()
        url = _normalize_url(str(f.get("url") or "").strip()) if f.get("url") else ""
        note = str(f.get("note") or "").strip()
        lines = ["BEGIN:VCARD", "VERSION:3.0"]
        if fn:
            lines.append(f"FN:{_escape_vcard(fn)}")
            parts = fn.split(None, 1)
            if len(parts) == 1:
                lines.append(f"N:{_escape_vcard(parts[0])};;;;")
            else:
                lines.append(f"N:{_escape_vcard(parts[-1])};{_escape_vcard(parts[0])};;;")
        if org:
            lines.append(f"ORG:{_escape_vcard(org)}")
        if title:
            lines.append(f"TITLE:{_escape_vcard(title)}")
        if tel:
            lines.append(f"TEL;TYPE=CELL:{_escape_vcard(tel)}")
        if email:
            lines.append(f"EMAIL;TYPE=INTERNET:{_escape_vcard(email)}")
        if url:
            lines.append(f"URL:{_escape_vcard(url)}")
        if note:
            lines.append(f"NOTE:{_escape_vcard(note)}")
        lines.append("END:VCARD")
        payload = "\n".join(lines)
    elif mode == "email":
        to = str(f.get("to") or f.get("email") or "").strip()
        subject = str(f.get("subject") or "")
        body = str(f.get("body") or "")
        q = []
        if subject:
            q.append("subject=" + quote(subject, safe=""))
        if body:
            q.append("body=" + quote(body, safe=""))
        payload = f"mailto:{to}"
        if q:
            payload += "?" + "&".join(q)
    elif mode == "tel":
        number = re.sub(r"[^\d+]", "", str(f.get("tel") or f.get("number") or ""))
        payload = f"tel:{number}"
    elif mode == "sms":
        number = re.sub(r"[^\d+]", "", str(f.get("tel") or f.get("number") or ""))
        body = str(f.get("body") or f.get("message") or "")
        payload = f"sms:{number}"
        if body:
            payload += "?body=" + quote(body, safe="")
    elif mode == "geo":
        lat = str(f.get("lat") or f.get("latitude") or "").strip()
        lon = str(f.get("lon") or f.get("longitude") or "").strip()
        label = str(f.get("label") or "").strip()
        payload = f"geo:{lat},{lon}"
        if label:
            payload += "?q=" + quote(label, safe="")
    elif mode == "event":
        summary = str(f.get("summary") or f.get("title") or "Event").strip()
        location = str(f.get("location") or "").strip()
        description = str(f.get("description") or "").strip()
        all_day = bool(f.get("allDay"))
        dtstart = _format_ics_dt(str(f.get("start") or ""), all_day=all_day)
        dtend = _format_ics_dt(str(f.get("end") or ""), all_day=all_day)
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Mr-Aurevo-X//QrTools//EN",
            "BEGIN:VEVENT",
            f"SUMMARY:{summary}",
        ]
        if dtstart:
            if all_day or len(dtstart) == 8:
                lines.append(f"DTSTART;VALUE=DATE:{dtstart}")
            else:
                lines.append(f"DTSTART:{dtstart}")
        if dtend:
            if all_day or len(dtend) == 8:
                lines.append(f"DTEND;VALUE=DATE:{dtend}")
            else:
                lines.append(f"DTEND:{dtend}")
        if location:
            lines.append(f"LOCATION:{location}")
        if description:
            lines.append(f"DESCRIPTION:{description.replace(chr(10), '\\n')}")
        lines.extend(["END:VEVENT", "END:VCALENDAR"])
        payload = "\r\n".join(lines)
    elif mode == "whatsapp":
        number = re.sub(r"\D", "", str(f.get("tel") or f.get("number") or ""))
        text = str(f.get("text") or f.get("message") or "")
        payload = f"https://wa.me/{number}"
        if text:
            payload += "?text=" + quote(text, safe="")
    elif mode in ("raw", "custom", "brut"):
        payload = str(f.get("raw") or f.get("text") or f.get("payload") or "")
    else:
        return {"ok": False, "error": f"Unknown mode: {mode}"}

    if not str(payload).strip():
        return {"ok": False, "error": "Empty payload", "payload": "", "mode": mode}
    return {"ok": True, "payload": str(payload), "mode": mode}


def render_qr_png(
    payload: str,
    ecc: str = "M",
    size: int = 512,
    border: int = 2,
) -> dict[str, Any]:
    # © 2026 Mr-Aurevo-X · QrTools · PNG render · free · updates not guaranteed
    payload = str(payload or "")
    if not payload:
        return {"ok": False, "error": "Empty payload"}
    ecc_key = str(ecc or "M").strip().upper()
    if ecc_key not in ECC_MAP:
        ecc_key = "M"
    size = max(256, min(1024, int(size or 512)))
    border = max(1, min(8, int(border or 2)))

    qr = qrcode.QRCode(
        version=None,
        error_correction=ECC_MAP[ecc_key],
        box_size=10,
        border=border,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")
    img = img.convert("RGB").resize((size, size))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    raw = buf.getvalue()
    b64 = base64.b64encode(raw).decode("ascii")
    return {
        "ok": True,
        "pngBase64": b64,
        "dataUrl": f"data:image/png;base64,{b64}",
        "size": size,
        "ecc": ecc_key,
        "bytes": len(raw),
        "version": qr.version,
    }


MAX_ROWS = 2000
_SLUG_RE = re.compile(r"[^A-Za-z0-9._-]+")


def _slugify(value: str, fallback: str = "qr") -> str:
    text = (value or "").strip()
    text = text.replace("https://", "").replace("http://", "")
    text = _SLUG_RE.sub("-", text).strip("-_.")
    text = text[:48]
    return text or fallback


def _parse_rows(text: str, csv_mode: bool) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    raw = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln for ln in raw.split("\n")]
    if csv_mode:
        reader = csv_mod.reader(lines)
        for cells in reader:
            if not cells:
                continue
            payload = (cells[0] or "").strip()
            if not payload:
                continue
            name = (cells[1].strip() if len(cells) > 1 and cells[1] else "")
            rows.append({"payload": payload, "name": name})
    else:
        for ln in lines:
            payload = ln.strip()
            if payload:
                rows.append({"payload": payload, "name": ""})
    return rows[:MAX_ROWS]


def render_qr_png_bytes(payload: str, ecc: str, size: int, border: int) -> bytes:
    ecc_key = str(ecc or "M").strip().upper()
    if ecc_key not in ECC_MAP:
        ecc_key = "M"
    size = max(128, min(2048, int(size or 512)))
    border = max(1, min(16, int(border or 2)))
    qr = qrcode.QRCode(
        version=None,
        error_correction=ECC_MAP[ecc_key],
        box_size=10,
        border=border,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")
    img = img.convert("RGB").resize((size, size))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class Api(WindowChromeMixin):
    """JS bridge — © 2026 Mr-Aurevo-X · QrTools · all rights reserved."""

    def __init__(self) -> None:
        self._window = None
        self._maximized = False
        self._last_png: bytes | None = None
        self._last_payload: str = ""

    def set_window(self, window) -> None:
        WindowChromeMixin.set_window(self, window)


    def open_support_url(self, kind: str = "") -> dict:
        """Open Discord / PayPal / Revolut in the default browser (allowlisted)."""
        urls = {
            "discord": "https://discord.com/users/406891052516114442",
            "paypal": "https://www.paypal.com/paypalme/aurevo1",
            "revolut": "https://revolut.me/mr_aurevo_x",
        }
        allowed = frozenset(
            {"discord.com", "www.paypal.com", "paypal.com", "revolut.me"}
        )
        key = (kind or "").strip().lower()
        url = urls.get(key)
        if not url:
            return {"ok": False, "error": f"unknown support kind: {kind!r}"}
        parsed = urllib.parse.urlparse(url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or host not in allowed:
            return {"ok": False, "error": "support URL rejected"}
        try:
            os.startfile(url)  # type: ignore[attr-defined]
            return {"ok": True, "kind": key, "url": url}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": str(exc), "url": url}


    def get_suite_accent(self) -> dict:
        return {"ok": True, "accent": resolve_suite_accent()}

    def get_suite_language(self) -> dict:
        return {"ok": True, "language": resolve_suite_language()}

    def get_suite_theme(self) -> dict:
        return {"ok": True, "theme": resolve_suite_theme()}

    def get_suite_settings(self) -> dict:
        return {
            "ok": True,
            "accent": resolve_suite_accent(),
            "language": resolve_suite_language(),
            "theme": resolve_suite_theme(),
        }

    def get_version(self) -> dict:
        return {
            "ok": True,
            "version": QrTools_updater.read_local_version(),
            "repo": QrTools_updater.RELEASE_REPO,
        }

    def check_for_update(self) -> dict:
        return QrTools_updater.check_for_update()

    def apply_update(self) -> dict:
        # Bat-only: refresh sources (git pull / zip). User relaunches via Lancer.bat.
        return QrTools_updater.apply_update()

    def dismiss_update(self, version: str | None = None) -> dict:
        return QrTools_updater.dismiss_update(version)

    def set_auto_update(self, enabled: bool = False) -> dict:
        return QrTools_updater.set_auto_update(bool(enabled))

    def build_payload(self, mode: str = "text", fields: dict | None = None) -> dict:
        return build_payload(mode, fields)

    def generate(
        self,
        mode: str = "text",
        fields: dict | None = None,
        ecc: str = "M",
        size: int = 512,
        border: int = 2,
        payload: str | None = None,
    ) -> dict:
        if payload is None or payload == "":
            built = build_payload(mode, fields)
            if not built.get("ok"):
                return built
            payload = built["payload"]
        else:
            payload = str(payload)
            built = {"ok": True, "payload": payload, "mode": mode}

        rendered = render_qr_png(payload, ecc=ecc, size=size, border=border)
        if not rendered.get("ok"):
            return rendered
        self._last_png = base64.b64decode(rendered["pngBase64"])
        self._last_payload = payload
        return {
            "ok": True,
            "mode": built.get("mode") or mode,
            "payload": payload,
            "dataUrl": rendered["dataUrl"],
            "pngBase64": rendered["pngBase64"],
            "size": rendered["size"],
            "ecc": rendered["ecc"],
            "bytes": rendered["bytes"],
            "version": rendered.get("version"),
        }

    def save_png(self, suggested_name: str = "QrTools.png") -> dict:
        if not self._last_png:
            return {"ok": False, "error": "No QR generated yet"}
        name = (suggested_name or "QrTools.png").strip() or "QrTools.png"
        if not name.lower().endswith(".png"):
            name += ".png"
        try:
            path = None
            if self._window is not None:
                path = self._window.create_file_dialog(
                    webview.SAVE_DIALOG,
                    directory=str(Path.home() / "Downloads"),
                    save_filename=name,
                    file_types=("PNG (*.png)",),
                )
            if not path:
                return {"ok": False, "error": "cancelled"}
            if isinstance(path, (list, tuple)):
                path = path[0] if path else None
            if not path:
                return {"ok": False, "error": "cancelled"}
            Path(path).write_bytes(self._last_png)
            return {"ok": True, "path": str(path)}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def copy_image(self) -> dict:
        # © 2026 Mr-Aurevo-X · QrTools · clipboard image helper
        if not self._last_png:
            return {"ok": False, "error": "No QR generated yet"}
        try:
            from PIL import Image
            import ctypes

            img = Image.open(io.BytesIO(self._last_png)).convert("RGB")
            out = io.BytesIO()
            img.save(out, "BMP")
            data = out.getvalue()[14:]  # strip BMP file header
            out.close()

            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            CF_DIB = 8
            GMEM_MOVEABLE = 0x0002

            if not user32.OpenClipboard(None):
                raise OSError("OpenClipboard failed")
            try:
                user32.EmptyClipboard()
                h_global = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(data))
                if not h_global:
                    raise OSError("GlobalAlloc failed")
                locked = kernel32.GlobalLock(h_global)
                ctypes.memmove(locked, data, len(data))
                kernel32.GlobalUnlock(h_global)
                if not user32.SetClipboardData(CF_DIB, h_global):
                    raise OSError("SetClipboardData failed")
            finally:
                user32.CloseClipboard()
            return {"ok": True}
        except Exception:
            try:
                b64 = base64.b64encode(self._last_png).decode("ascii")
                return self.copy_text(f"data:image/png;base64,{b64}")
            except Exception as exc:
                return {"ok": False, "error": str(exc)}

    def print_image(self) -> dict:
        # © 2026 Mr-Aurevo-X · QrTools · direct print via Windows shell
        if not self._last_png:
            return {"ok": False, "error": "No QR generated yet"}
        try:
            import tempfile

            fd, tmp = tempfile.mkstemp(prefix="QrTools_", suffix=".png")
            os.close(fd)
            path = Path(tmp)
            path.write_bytes(self._last_png)
            # Opens the system print dialog for the PNG (default image handler).
            os.startfile(str(path), "print")  # noqa: S606 — intentional Windows print
            return {"ok": True, "path": str(path)}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def copy_payload(self, text: str | None = None) -> dict:
        payload = text if text is not None else self._last_payload
        return self.copy_text(payload or "")

    # ---- batch (Lot) -------------------------------------------------

    def import_file(self) -> dict:
        try:
            paths = None
            if self._window is not None:
                paths = self._window.create_file_dialog(
                    webview.OPEN_DIALOG,
                    allow_multiple=False,
                    file_types=("Listes (*.csv;*.txt)", "Tous les fichiers (*.*)"),
                )
            if not paths:
                return {"ok": False, "error": "cancelled"}
            path = paths[0] if isinstance(paths, (list, tuple)) else paths
            data = Path(path).read_bytes()
            for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
                try:
                    text = data.decode(enc)
                    break
                except UnicodeDecodeError:
                    text = data.decode("utf-8", errors="replace")
            return {"ok": True, "text": text, "name": Path(path).name}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def preview(
        self,
        text: str = "",
        ecc: str = "M",
        size: int = 512,
        border: int = 2,
        csv_mode: bool = False,
    ) -> dict:
        rows = _parse_rows(text, bool(csv_mode))
        count = len(rows)
        preview_url = None
        if count:
            try:
                png = render_qr_png_bytes(
                    rows[0]["payload"], ecc, min(int(size or 512), 512), border
                )
                preview_url = "data:image/png;base64," + base64.b64encode(png).decode("ascii")
            except Exception:
                preview_url = None
        sample = [r["payload"] for r in rows[:5]]
        return {
            "ok": True,
            "count": count,
            "truncated": count >= MAX_ROWS,
            "sample": sample,
            "previewUrl": preview_url,
        }

    def generate_batch(
        self,
        text: str = "",
        ecc: str = "M",
        size: int = 512,
        border: int = 2,
        csv_mode: bool = False,
        make_zip: bool = False,
    ) -> dict:
        rows = _parse_rows(text, bool(csv_mode))
        if not rows:
            return {"ok": False, "error": "empty"}

        folder = None
        try:
            if self._window is not None:
                folder = self._window.create_file_dialog(
                    webview.FOLDER_DIALOG,
                    directory=str(Path.home() / "Downloads"),
                )
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
        if not folder:
            return {"ok": False, "error": "cancelled"}
        out_dir = Path(folder[0] if isinstance(folder, (list, tuple)) else folder)
        batch_dir = out_dir / "QrTools"
        i = 2
        while batch_dir.exists():
            batch_dir = out_dir / f"QrTools_{i}"
            i += 1
        batch_dir.mkdir(parents=True, exist_ok=True)

        pad = max(3, len(str(len(rows))))
        used: set[str] = set()
        written: list[Path] = []
        failures: list[dict] = []

        for idx, row in enumerate(rows, start=1):
            payload = row["payload"]
            base = row["name"].strip() if row.get("name") else ""
            if base:
                stem = _slugify(base, f"qr-{idx:0{pad}d}")
            else:
                stem = f"{idx:0{pad}d}_{_slugify(payload, f'qr-{idx:0{pad}d}')}"
            name = f"{stem}.png"
            n = 2
            while name.lower() in used:
                name = f"{stem}_{n}.png"
                n += 1
            used.add(name.lower())
            try:
                png = render_qr_png_bytes(payload, ecc, size, border)
                (batch_dir / name).write_bytes(png)
                written.append(batch_dir / name)
            except Exception as exc:
                failures.append({"row": idx, "payload": payload[:80], "error": str(exc)})

        zip_path = None
        if make_zip and written:
            zip_path = batch_dir.with_suffix(".zip")
            try:
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for p in written:
                        zf.write(p, arcname=p.name)
            except Exception as exc:
                failures.append({"row": 0, "payload": "(zip)", "error": str(exc)})
                zip_path = None

        return {
            "ok": True,
            "count": len(written),
            "total": len(rows),
            "folder": str(batch_dir),
            "zipPath": str(zip_path) if zip_path else None,
            "failures": failures,
            "ecc": str(ecc or "M").upper(),
            "size": int(size or 512),
        }

    def reveal(self, path: str) -> dict:
        try:
            target = Path(path)
            if target.exists():
                os.startfile(str(target if target.is_dir() else target.parent))  # noqa: S606
                return {"ok": True}
            return {"ok": False, "error": "not_found"}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def copy_text(self, text: str) -> dict:
        text = text if isinstance(text, str) else str(text or "")
        try:
            import tkinter as tk

            root = tk.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update()
            root.destroy()
            return {"ok": True}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}


def main() -> None:
    # © 2026 Mr-Aurevo-X · QrTools · windowed host entry
    ui = ui_dir()
    index = ui / "index.html"
    if not index.is_file():
        raise SystemExit(f"UI missing: {index}")
    api = Api()
    create_tool_window(
        title="QrTools — Mr-Aurevo-X",
        url=index.as_uri(),
        js_api=api,
        width=1180,
        height=820,
        min_size=(960, 640),
        background_color="#030304",
    )
    webview.start()


if __name__ == "__main__":
    # © 2026 Mr-Aurevo-X · QrTools · 100% local · free · updates not guaranteed
    main()

#!/usr/bin/env python3
"""Real-time system monitoring dashboard — FastAPI backend."""

import asyncio
import json
import os
import platform
import time
from datetime import datetime
from pathlib import Path

import psutil
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="System Dashboard")

START_TIME = time.time()

STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _bytes_fmt(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def _uptime_str() -> str:
    secs = int(time.time() - START_TIME)
    days, secs = divmod(secs, 86400)
    hours, secs = divmod(secs, 3600)
    mins, secs = divmod(secs, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    parts.append(f"{mins}m")
    parts.append(f"{secs}s")
    return " ".join(parts)


def gather_stats() -> dict:
    cpu = psutil.cpu_percent(interval=0)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_percent": cpu,
        "cpu_count": psutil.cpu_count(),
        "ram_total": mem.total,
        "ram_used": mem.used,
        "ram_percent": mem.percent,
        "disk_total": disk.total,
        "disk_used": disk.used,
        "disk_percent": disk.percent,
        "net_sent": net.bytes_sent,
        "net_recv": net.bytes_recv,
        "uptime": _uptime_str(),
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
    }


# ---------------------------------------------------------------------------
# REST endpoints
# ---------------------------------------------------------------------------

@app.get("/api/stats")
async def api_stats():
    return JSONResponse(gather_stats())


@app.get("/api/processes")
async def api_processes():
    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
        try:
            info = p.info
            procs.append({
                "pid": info["pid"],
                "name": info["name"] or "—",
                "cpu": round(info["cpu_percent"] or 0, 1),
                "mem": round(info["memory_percent"] or 0, 1),
                "status": info["status"] or "?",
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    procs.sort(key=lambda p: p["cpu"], reverse=True)
    return JSONResponse(procs[:10])


@app.get("/api/docker")
async def api_docker():
    """Return running docker containers or an error message."""
    import shutil, subprocess
    if not shutil.which("docker"):
        return JSONResponse({"available": False, "message": "Docker is not installed"})
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0:
            return JSONResponse({"available": True, "containers": [], "error": result.stderr.strip()})
        containers = []
        for line in result.stdout.strip().splitlines():
            parts = line.split("\t")
            if len(parts) >= 4:
                containers.append({
                    "id": parts[0][:12], "name": parts[1],
                    "image": parts[2], "status": parts[3],
                })
        return JSONResponse({"available": True, "containers": containers})
    except Exception as exc:
        return JSONResponse({"available": True, "containers": [], "error": str(exc)})


@app.get("/api/logs")
async def api_logs():
    """Return last 50 lines from syslog / journalctl."""
    import subprocess
    log_paths = ["/var/log/syslog", "/var/log/messages"]
    for p in log_paths:
        if os.path.isfile(p):
            try:
                with open(p, "r", errors="replace") as f:
                    lines = f.readlines()
                return JSONResponse({"source": p, "lines": [l.rstrip() for l in lines[-50:]]})
            except PermissionError:
                break
    # Fallback: journalctl
    try:
        result = subprocess.run(
            ["journalctl", "-n", "50", "--no-pager", "-q"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return JSONResponse({"source": "journalctl", "lines": result.stdout.strip().splitlines()})
    except FileNotFoundError:
        pass
    return JSONResponse({"source": "none", "lines": ["No log source available on this system."]})


# ---------------------------------------------------------------------------
# WebSocket — live stats every 2 s
# ---------------------------------------------------------------------------

@app.websocket("/ws/live")
async def ws_live(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_json(gather_stats())
            await asyncio.sleep(2)
    except (WebSocketDisconnect, asyncio.CancelledError):
        pass


# ---------------------------------------------------------------------------
# Serve frontend
# ---------------------------------------------------------------------------

@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "dashboard.html")


if __name__ == "__main__":
    import uvicorn
    print("Starting dashboard on http://0.0.0.0:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

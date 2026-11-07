"""FreeAV - jednoduchý antivirus nad ClamAV s webovým rozhraním.
Spuštění: python app.py  ->  http://127.0.0.1:8765
"""
import json, os, shutil, subprocess, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST, PORT = "127.0.0.1", 8765  # jen lokálně, nikdy ne do sítě
Q = Path.home() / ".freeav_quarantine"
Q.mkdir(exist_ok=True)
INDEX = Path(__file__).with_name("index.html")
CLAM = shutil.which("clamscan")
FRESH = shutil.which("freshclam")


def remove(f, virus, action):
    try:
        if action == "delete":
            os.remove(f)
            return "smazáno"
        qid = uuid.uuid4().hex
        shutil.move(f, Q / qid)
        os.chmod(Q / qid, 0o600)
        (Q / (qid + ".json")).write_text(json.dumps({"file": f, "virus": virus}))
        return "v karanténě"
    except Exception as e:
        return f"nepodařilo se odstranit: {e}"


def scan(path, action):
    if not CLAM:
        return {"error": "ClamAV není nainstalovaný (viz README)."}
    if not os.path.exists(path):
        return {"error": "Tato cesta neexistuje."}
    p = subprocess.run([CLAM, "-r", "--infected", "--no-summary", path],
                       capture_output=True, text=True)
    found = []
    for line in p.stdout.splitlines():
        if line.endswith(" FOUND"):
            f, _, virus = line[:-6].rpartition(": ")
            found.append({"file": f, "virus": virus, "status": remove(f, virus, action)})
    if p.returncode == 2 and not found:
        return {"error": "Skenování selhalo: " + p.stderr.strip()[:300]}
    return {"found": found}


def quarantine():
    items = []
    for m in sorted(Q.glob("*.json")):
        d = json.loads(m.read_text())
        d["id"] = m.stem
        items.append(d)
    return {"items": items}


def clear():
    n = 0
    for m in Q.glob("*.json"):
        (Q / m.stem).unlink(missing_ok=True)
        m.unlink()
        n += 1
    return {"deleted": n}


def update():
    if not FRESH:
        return {"error": "freshclam nenalezen."}
    p = subprocess.run([FRESH], capture_output=True, text=True)
    return {"ok": p.returncode == 0, "log": (p.stdout + p.stderr)[-400:]}


class H(BaseHTTPRequestHandler):
    def send(self, data, ctype="application/json", code=200):
        body = data if isinstance(data, bytes) else json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def allowed(self):
        # ochrana proti cizím webům, které by posílaly požadavky na localhost
        return self.headers.get("X-FreeAV") == "1" and \
            self.headers.get("Host", "").split(":")[0] in ("127.0.0.1", "localhost")

    def do_GET(self):
        if self.path == "/":
            return self.send(INDEX.read_bytes(), "text/html")
        if self.path == "/api/quarantine" and self.allowed():
            return self.send(quarantine())
        self.send({"error": "nenalezeno"}, code=404)

    def do_POST(self):
        if not self.allowed():
            return self.send({"error": "zakázáno"}, code=403)
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(n) or b"{}")
        if self.path == "/api/scan":
            act = "delete" if body.get("action") == "delete" else "quarantine"
            return self.send(scan(os.path.expanduser(body.get("path", "")), act))
        if self.path == "/api/update":
            return self.send(update())
        if self.path == "/api/clear":
            return self.send(clear())
        self.send({"error": "nenalezeno"}, code=404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"FreeAV běží na http://{HOST}:{PORT}  (ukončení: Ctrl+C)")
    ThreadingHTTPServer((HOST, PORT), H).serve_forever()

"""Serve the slap game.

Usage: python serve_https.py [port]          -> HTTPS on the LAN (self-signed cert)
       python serve_https.py 8090 --http    -> plain HTTP on 127.0.0.1 only, for a tunnel
"""
import http.server, ssl, socket, os, sys, shutil

PLAIN = "--http" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
PORT = int(args[0]) if args else 8443
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

# Only the game itself is served; never the private key or other project files.
ALLOWED = {"/", "/index.html", "/favicon.ico", "/media/the-slap-2-360p.mp4"}


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1)); return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


class Handler(http.server.SimpleHTTPRequestHandler):
    def _path(self):
        return self.path.split("?")[0].split("#")[0]

    def do_GET(self):
        path = self._path()
        if path not in ALLOWED:
            self.send_error(404); return
        if path.endswith(".mp4"):
            self.send_video(path); return
        super().do_GET()

    def do_HEAD(self):
        path = self._path()
        if path not in ALLOWED:
            self.send_error(404); return
        if path.endswith(".mp4"):
            self.send_video(path, head=True); return
        super().do_HEAD()

    def send_video(self, path, head=False):
        """Byte-range responses: iOS Safari won't play video without them."""
        fp = os.path.join(ROOT, path.lstrip("/"))
        size = os.path.getsize(fp)
        start, end, status = 0, size - 1, 200
        rng = self.headers.get("Range")
        if rng and rng.startswith("bytes="):
            s, _, e = rng[6:].split(",")[0].strip().partition("-")
            try:
                if s:
                    start = int(s); end = min(int(e), size - 1) if e else size - 1
                else:
                    start = max(0, size - int(e))
            except ValueError:
                start, end = 0, size - 1
            if start > end or start >= size:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers(); return
            status = 206
        length = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "public, max-age=3600")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        if head:
            return
        try:
            with open(fp, "rb") as f:
                f.seek(start)
                remaining = length
                while remaining > 0:
                    chunk = f.read(min(256 * 1024, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            pass  # browser cancelled the request (normal while seeking)

    def log_message(self, fmt, *a):
        pass


if PLAIN:
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Serving for tunnel on http://127.0.0.1:{PORT}/", flush=True)
else:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("certs/cert.pem", "certs/key.pem")
    httpd = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    print(f"Open on your phone:  https://{lan_ip()}:{PORT}/", flush=True)
httpd.serve_forever()

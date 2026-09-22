#!/usr/bin/env python3
"""Focused HTTP regression checks for marker-safe bodies and bounded responses."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parent.parent
MAX_HTTP_BYTES = 1024 * 1024


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/marker":
            body = b"before\n__CLARO_HTTP_STATUS__999\nafter"
            status = 200
        elif self.path == "/large":
            body = b"x" * (MAX_HTTP_BYTES + 1)
            status = 200
        else:
            body = b"not found"
            status = 404
        self.send_response(status)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="claro-http-") as tmp:
        tmp_path = Path(tmp)
        script = tmp_path / "http.claro"
        script.write_text(
            'HTTP GET URL_MARKER AS body STATUS status\n'
            'SAY body\n'
            'SAY status\n'
            'HTTP GET URL_LARGE AS ignored\n',
            encoding="utf-8",
        )
        binary = tmp_path / "claro-http"
        build = subprocess.run(
            ["gcc", "-std=c99", "-O0", "src/claro.c", "-o", str(binary), "-lm"],
            cwd=ROOT, text=True, capture_output=True,
        )
        if build.returncode:
            print(build.stderr, end="")
            return build.returncode
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            marker = f'"http://127.0.0.1:{server.server_port}/marker"'
            large = f'"http://127.0.0.1:{server.server_port}/large"'
            text = script.read_text(encoding="utf-8").replace("URL_MARKER", marker).replace("URL_LARGE", large)
            script.write_text(text, encoding="utf-8")
            run = subprocess.run([str(binary), str(script)], cwd=ROOT, text=True, capture_output=True)
        finally:
            server.shutdown()
            server.server_close()
        expected_body = "before\n__CLARO_HTTP_STATUS__999\nafter\n200\n"
        if run.returncode == 0:
            print("FAIL: oversized HTTP response was accepted")
            print(run.stdout, end="")
            return 1
        if expected_body not in run.stdout:
            print("FAIL: marker-like response body was altered")
            print(run.stdout, end="")
            print(run.stderr, end="")
            return 1
        if "HTTP response exceeds the safe size limit" not in run.stderr and "HTTP response exceeds the safe size limit" not in run.stdout:
            print("FAIL: oversized response did not get a beginner-facing diagnostic")
            print(run.stdout, end="")
            print(run.stderr, end="")
            return 1
        print("PASS: HTTP status is separated from marker-like bodies and responses are bounded")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

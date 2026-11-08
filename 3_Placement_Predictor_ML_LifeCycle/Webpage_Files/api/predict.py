import json
import os
import pickle
from http.server import BaseHTTPRequestHandler

BASE = os.path.join(os.path.dirname(__file__), "..")

with open(os.path.join(BASE, "model.pkl"), "rb") as f:
    model = pickle.load(f)
with open(os.path.join(BASE, "scaler.pkl"), "rb") as f:
    scaler = pickle.load(f)


class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or "{}")
            cgpa = float(data["cgpa"])
            iq = float(data["iq"])

            # Same order as training: [cgpa, iq], then the SAME scaler
            scaled = scaler.transform([[cgpa, iq]])
            label = int(model.predict(scaled)[0])
            probability = float(model.predict_proba(scaled)[0][1])

            self._send(200, {
                "placed": label == 1,
                "probability": probability,
                "scaled": [float(scaled[0][0]), float(scaled[0][1])],
            })
        except (KeyError, ValueError, TypeError):
            self._send(400, {"error": "Enter valid numbers for CGPA and IQ."})
        except Exception:
            self._send(500, {"error": "Prediction failed. Please try again."})
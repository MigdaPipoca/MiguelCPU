import os
from flask import Flask, jsonify, redirect, render_template
from flask_cors import CORS
from cpu import cpu

app = Flask(__name__, static_folder="static", template_folder="templates")

# The browser frontend is hosted separately on GitHub Pages.
frontend_origin = os.environ.get("FRONTEND_ORIGIN", "https://migdaPipoca.github.io")
CORS(app, resources={r"/api/*": {"origins": frontend_origin}})


@app.get("/")
def home():
    return render_template("home.html")


@app.get("/pc")
def pc_page():
    return redirect(f"{frontend_origin}/MiguelCPU/pc/index.html")


@app.get("/cpu")
def cpu_page():
    return redirect(f"{frontend_origin}/MiguelCPU/cpu/index.html")


@app.get("/api/status")
def status():
    return jsonify(cpu.snapshot())


@app.get("/api/catalog")
def catalog():
    return jsonify(cpu.catalog())


@app.post("/api/programs/<program_id>/launch")
def launch(program_id):
    ok, message = cpu.launch(program_id)
    return jsonify({"ok": ok, "message": message}), (200 if ok else 400)


@app.post("/api/programs/<program_id>/close")
def close(program_id):
    ok, message = cpu.close(program_id)
    return jsonify({"ok": ok, "message": message}), (200 if ok else 400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False, threaded=True)

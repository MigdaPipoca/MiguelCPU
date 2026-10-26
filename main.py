from flask import Flask, jsonify, render_template, request
from cpu import cpu

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.get("/")
def home():
    return render_template("home.html")


@app.get("/pc")
def pc_page():
    return render_template("pc/index.html")


@app.get("/cpu")
def cpu_page():
    return render_template("cpu_view/index.html")


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
    # Debug is disabled by default; the server is intended for local use.
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)

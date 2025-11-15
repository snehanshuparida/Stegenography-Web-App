import os
import sys
import uuid
import time
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, Response
from werkzeug.utils import secure_filename

# Ensure backend import path (parent directory of this webapp)
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from project import (
    lsb_encode, lsb_decode,
    palette_encode, palette_decode,
    dct_encode, dct_decode,
    xor_encode, xor_decode,
    evaluate_images
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "gif"}

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-key")

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
PLOTS_DIR = OUTPUT_DIR / "plots"
for d in (UPLOAD_DIR, OUTPUT_DIR, PLOTS_DIR):
    d.mkdir(parents=True, exist_ok=True)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def method_map():
    return {
        "LSB": (lsb_encode, lsb_decode),
        "Palette": (palette_encode, palette_decode),
        "DCT": (dct_encode, dct_decode),
        "XOR": (xor_encode, xor_decode),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manual", methods=["GET", "POST"])
def manual():
    if request.method == "GET":
        return render_template("manual.html", methods=list(method_map().keys()))

    # POST
    if "image" not in request.files:
        flash("Please upload an image file.")
        return redirect(request.url)

    file = request.files["image"]
    if file.filename == "":
        flash("No selected file.")
        return redirect(request.url)

    if not allowed_file(file.filename):
        flash("Unsupported file type.")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    input_path = UPLOAD_DIR / f"{uuid.uuid4().hex}_{filename}"
    file.save(str(input_path))

    mode = request.form.get("mode")  # encode or decode
    method_key = request.form.get("method")

    methods = method_map()
    if method_key not in methods:
        flash("Invalid method selected.")
        return redirect(request.url)

    method_name, (enc_func, dec_func) = method_key, methods[method_key]

    context: Dict[str, Any] = {
        "method": method_name,
        "input_image_url": url_for("uploaded_file", filename=input_path.name),
    }

    try:
        if mode == "encode":
            message = request.form.get("message", "").strip()
            if not message:
                flash("Please provide a secret message to encode.")
                return redirect(request.url)

            out_name = request.form.get("outname", "").strip() or f"output_{method_name.lower()}"
            out_file = secure_filename(out_name) + ".png"
            output_path = OUTPUT_DIR / out_file

            encoded_path, enc_time = enc_func(str(input_path), message, str(output_path))

            ssim_val, psnr_val = evaluate_images(str(input_path), str(encoded_path))

            context.update({
                "mode": "encode",
                "message": message,
                "encode_time": round(enc_time, 4),
                "ssim": None if ssim_val is None else round(ssim_val, 4),
                "psnr": None if psnr_val is None else round(psnr_val, 2),
                "output_image_url": url_for("output_file", filename=Path(encoded_path).name),
                "download_url": url_for("download_output", filename=Path(encoded_path).name),
            })

        elif mode == "decode":
            decoded_msg, dec_time = dec_func(str(input_path))
            context.update({
                "mode": "decode",
                "decoded_message": decoded_msg,
                "decode_time": round(dec_time, 4),
            })
        else:
            flash("Invalid mode.")
            return redirect(request.url)

        return render_template("manual.html", methods=list(method_map().keys()), **context)

    except Exception as e:
        flash(f"Error: {e}")
        return redirect(request.url)


@app.route("/auto", methods=["GET", "POST"])
def auto_mode():
    if request.method == "GET":
        return render_template("auto.html")

    # POST
    if "image" not in request.files:
        flash("Please upload an image file.")
        return redirect(request.url)

    file = request.files["image"]
    if file.filename == "":
        flash("No selected file.")
        return redirect(request.url)

    if not allowed_file(file.filename):
        flash("Unsupported file type.")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    input_path = UPLOAD_DIR / f"{uuid.uuid4().hex}_{filename}"
    file.save(str(input_path))

    message = request.form.get("message", "").strip()
    if not message:
        flash("Please provide a secret message to encode.")
        return redirect(request.url)

    methods = method_map()

    results = []
    for method_name, (enc_func, dec_func) in methods.items():
        try:
            out_file = f"auto_{method_name.lower()}_{uuid.uuid4().hex[:8]}.png"
            output_path = OUTPUT_DIR / out_file

            encoded_path, enc_time = enc_func(str(input_path), message, str(output_path))
            decoded_msg, dec_time = dec_func(str(encoded_path))
            ssim_val, psnr_val = evaluate_images(str(input_path), str(encoded_path))

            results.append({
                "method": method_name,
                "encoded_url": url_for("output_file", filename=Path(encoded_path).name),
                "download_url": url_for("download_output", filename=Path(encoded_path).name),
                "encode_time": round(enc_time, 4),
                "decode_time": round(dec_time, 4),
                "ssim": None if ssim_val is None else round(ssim_val, 4),
                "psnr": None if psnr_val is None else round(psnr_val, 2),
            })
        except Exception as e:
            results.append({
                "method": method_name,
                "error": str(e),
            })

    # Build plots using matplotlib
    try:
        import matplotlib
        matplotlib.use("Agg")  # non-GUI backend
        import matplotlib.pyplot as plt
        import pandas as pd

        df = pd.DataFrame([r for r in results if "error" not in r])
        plot_files = {}
        if not df.empty:
            # SSIM/PSNR bar chart
            fig, ax = plt.subplots(figsize=(8, 5))
            df.plot(x="method", y=["ssim", "psnr"], kind="bar", ax=ax, title="SSIM & PSNR Comparison")
            plt.xticks(rotation=0)
            plt.tight_layout()
            plot1 = f"metrics_{int(time.time())}_{uuid.uuid4().hex[:6]}.png"
            plt.savefig(PLOTS_DIR / plot1)
            plt.close(fig)
            plot_files["metrics"] = url_for("plot_file", filename=plot1)

            # Time line chart
            fig, ax = plt.subplots(figsize=(8, 5))
            df.plot(x="method", y=["encode_time", "decode_time"], kind="line", marker="o", ax=ax, title="Encoding/Decoding Time")
            plt.xticks(rotation=0)
            plt.tight_layout()
            plot2 = f"times_{int(time.time())}_{uuid.uuid4().hex[:6]}.png"
            plt.savefig(PLOTS_DIR / plot2)
            plt.close(fig)
            plot_files["times"] = url_for("plot_file", filename=plot2)
        else:
            plot_files = {}
    except Exception as e:
        plot_files = {"error": str(e)}

    return render_template(
        "auto.html",
        input_image_url=url_for("uploaded_file", filename=input_path.name),
        message=message,
        results=results,
        plots=plot_files,
    )


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/outputs/<path:filename>")
def output_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)


@app.route("/plots/<path:filename>")
def plot_file(filename):
    return send_from_directory(PLOTS_DIR, filename)


@app.route("/download/<path:filename>")
def download_output(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

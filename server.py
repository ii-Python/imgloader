# Copyright 2022 iiPython
# ROBLOX Image Loader v2

# Modules
import os
import zlib
import requests
from PIL import Image
from io import BytesIO
from flask import Flask, abort, request, render_template

# Initialization
app = Flask("Image Loader v2")

# Image loader
def load_image(url: str) -> bytes | None:
    try:
        req = requests.get(url, timeout = 2)
        if req.status_code != 200:
            return None

    except requests.Timeout:
        return None

    # Handle image processing
    image, image_data = Image.open(BytesIO(req.content)).convert("RGBA"), ""
    image.thumbnail((500, 500), Image.ANTIALIAS)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            c = image.getpixel((x, y))
            image_data += f"{x};{y};{c[0]};{c[1]};{c[2]};{c[3]}:"

    return zlib.compress(image_data[:-1].encode("utf-8"), 5)

# Routes
@app.route("/")
def index() -> None:
    return render_template("index.html"), 200

@app.route("/status")
def status() -> None:
    return "200 OK", 200

@app.route("/load", methods = ["POST"])
def process_image() -> None:
    try:
        url = request.data.decode("utf-8")

    except Exception:
        return abort(400)

    image_data = load_image(url)
    if image_data is None:
        return abort(400)

    return image_data

# Launch server
app.run(host = os.getenv("HOST", "0.0.0.0"), port = os.getenv("PORT", 8080))

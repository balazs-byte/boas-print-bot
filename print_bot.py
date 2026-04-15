import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

def print_sku_label(sku):
    label_path = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "sku_label.txt")
    with open(label_path, "w") as f:
        f.write(sku)
    
    dymo_path = "C:\\Program Files\\DYMO\\DYMO Connect\\DYMOConnect.exe"
    subprocess.run([dymo_path, "/print", label_path])
    print(f"Printed label for SKU: {sku}")

@app.route("/webhook/product-created", methods=["POST"])
def product_created():
    data = request.get_json(force=True, silent=True)
    try:
        sku = data["variants"][0]["sku"]
        if sku:
            print_sku_label(sku)
        else:
            print("No SKU found, skipping print")
    except Exception as e:
        print(f"Error: {e}")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

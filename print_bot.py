import os
import socket
from flask import Flask, request, jsonify

app = Flask(__name__)

PRINTER_IP = os.environ.get("PRINTER_IP", "192.168.1.100")
PRINTER_PORT = 9100

def print_sku_label(sku):
    zpl = (
        "^XA"
        f"^FO50,50^BY3^BCN,100,Y,N,N^FD{sku}^FS"
        f"^FO50,180^A0N,40,40^FD{sku}^FS"
        "^XZ"
    )
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((PRINTER_IP, PRINTER_PORT))
        s.sendall(zpl.encode())

@app.route("/webhook/product-created", methods=["POST"])
def product_created():
    data = request.get_json()
    try:
        sku = data["variants"][0]["sku"]
        if sku:
            print_sku_label(sku)
            print(f"Printed label for SKU: {sku}")
        else:
            print("No SKU found, skipping print")
    except Exception as e:
        print(f"Error: {e}")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

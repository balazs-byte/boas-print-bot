import requests
from datetime import datetime
from flask import Flask, request, jsonify
import urllib3
urllib3.disable_warnings()

app = Flask(__name__)

DYMO_API = "https://localhost:41951/DYMO/DLS/Printing"

def print_sku_label(sku):
    date_str = datetime.now().strftime("%d-%m-%Y")

    with open("label.xml", "r") as f:
        label_xml = f.read()
    
    label_xml = label_xml.replace("Label_Test", sku)
    label_xml = label_xml.replace("Date", date_str)

    payload = {
        "printerName": "DYMO LabelWriter 4XL",
        "labelXml": label_xml,
        "labelSetXml": ""
    }
    response = requests.post(f"{DYMO_API}/PrintLabel", data=payload, verify=False)
    print(f"Print response: {response.status_code} - {response.text}")

@app.route("/webhook/product-created", methods=["POST"])
def product_created():
    data = request.get_json(force=True, silent=True)
    print(f"Received data: {data}")
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

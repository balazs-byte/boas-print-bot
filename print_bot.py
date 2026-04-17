import requests
from datetime import datetime
from flask import Flask, request, jsonify
import urllib3
urllib3.disable_warnings()

app = Flask(__name__)

DYMO_API = "https://localhost:41951/DYMO/DLS/Printing"

def print_sku_label(sku):
    date_str = datetime.now().strftime("%d-%m-%Y")
    label_text = f"{sku} | {date_str}"

    label_xml = """<?xml version="1.0" encoding="utf-8"?>
<DieCutLabel Version="8.0" Units="twips" MediaType="Default">
  <PaperOrientation>Landscape</PaperOrientation>
  <Id>shipping</Id>
  <IsOutlined>False</IsOutlined>
  <PaperName>30256 Shipping</PaperName>
  <DrawCommands>
    <RoundRectangle X="0" Y="0" Width="3331" Height="5765" Rx="270" Ry="270"/>
  </DrawCommands>
  <ObjectInfo>
    <TextObject>
      <Name>Text</Name>
      <ForeColor Alpha="255" Red="0" Green="0" Blue="0"/>
      <BackColor Alpha="0" Red="255" Green="255" Blue="255"/>
      <LinkedObjectName/>
      <Rotation>Rotation0</Rotation>
      <IsMirrored>False</IsMirrored>
      <IsVariable>False</IsVariable>
      <HorizontalAlignment>Center</HorizontalAlignment>
      <VerticalAlignment>Middle</VerticalAlignment>
      <TextFitMode>ShrinkToFit</TextFitMode>
      <UseFullFontHeight>True</UseFullFontHeight>
      <Verticalized>False</Verticalized>
      <StyledText>
        <Element>
          <String>""" + label_text + """</String>
          <Attributes>
            <Font Family="Helvetica" Size="36" Bold="True" Italic="False" Underline="False" StrikeOut="False"/>
            <ForeColor Alpha="255" Red="0" Green="0" Blue="0"/>
          </Attributes>
        </Element>
      </StyledText>
    </TextObject>
    <ObjectLayout>
      <DYMOPoint><X>100</X><Y>100</Y></DYMOPoint>
      <Size><Width>5565</Width><Height>3131</Height></Size>
    </ObjectLayout>
  </ObjectInfo>
</DieCutLabel>"""

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

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
<DesktopLabel Version="1">
  <DYMOLabel Version="4">
    <Description>DYMO Label</Description>
    <Orientation>Landscape</Orientation>
    <LabelName>S0722540 multipurpose</LabelName>
    <InitialLength>0</InitialLength>
    <BorderStyle>SolidLine</BorderStyle>
    <DYMORect>
      <DYMOPoint>
        <X>0.039999966</X>
        <Y>0.060000002</Y>
      </DYMOPoint>
      <Size>
        <Width>2.17</Width>
        <Height>1.13</Height>
      </Size>
    </DYMORect>
    <BorderColor>
      <SolidColorBrush>
        <Color A="1" R="0" G="0" B="0"></Color>
      </SolidColorBrush>
    </BorderColor>
    <BorderThickness>1</BorderThickness>

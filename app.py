from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes, Details
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json

with open('secret.json') as f:
    secret = json.load(f)

KEY = secret['KEY']
ENDPOINT = secret['ENDPOINT']

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

filepath = "photo.jpg"

def get_tags(filepath):
    local_image = open(filepath, "rb")
    tags_result_local = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result_local.tags
    print(tags)
    tags_name =[]
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name

def detect_objects(filepath):
    local_image = open(filepath, "rb")
    detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results_local.objects
    return objects


import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont


st.title('物体検出アプリ')
uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'png'])
if uploaded_file != None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_objects(img_path)

    draw = ImageDraw.Draw(img)
    for object in objects:
        x =object.rectangle.x
        y =object.rectangle.y
        w =object.rectangle.w
        h =object.rectangle.h
        caption = object.object_property

        font = ImageFont.truetype(font = './PlaypenSans-VariableFont_wght.ttf', size=20)
        # text_w, text_h = draw.textsize(caption, font=font)

        draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline='green', width=5)
        # draw.rectangle([(x, y), (x+text_w, y+text_h)], fill='Green', width=5)
        
        tl = (x, y)
        a, b, c, d= draw.textbbox(tl, caption, font=font)
        draw.rectangle([(x, y), (c, d)], fill='Green', width=5)
        draw.text((x, y), caption, fill='white', font = font)
        
    st.image(img)




    tags_name = get_tags(img_path)
    tags_name = ', '.join(tags_name)
    st.markdown('**認識されたコンテンツタグ**')
    st.markdown(f'> {tags_name}')
import streamlit as st
import re
import numpy as np
import pandas as pd
import cv2
from google.cloud import firestore
from time import time
from datetime import datetime
from PIL import Image
import io
from google.oauth2 import service_account
import json
import glob

def report(region, img, result_time):
    # Authenticate to Firestore with the JSON account key.
    key_dict = json.loads(st.secrets['textkey'])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds)
    result_time = f"{time() - start:.4f}"
    data = {
        'region': region,
        'img': img,
        'datetime': datetime.now(),
        'time' : result_time
        }
    
    # Create a reference to the Google post.
    doc_ref = db.collection('test_img').add(data)

    return doc_ref[1].id, db, result_time


def retrieve(id, db):
    doc_ref = db.collection('test_img').document(id)
    doc = doc_ref.get().to_dict()
    image_bytes = doc['img']
    return image_bytes

@st.cache
def is_valid_email(email):
    # Regular expression to validate email format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

@st.cache(suppress_st_warning=True)
def load_img_data():
    # Load the Excel data and create the DataFrame
    guide_img_paths = [Image.open(file) for file in glob.glob('./data/guide/*.png')]

    return guide_img_paths

@st.cache(suppress_st_warning=True)
def load_img_data():
    # Load the Excel data and create the DataFrame
    guide_img_paths = [Image.open(file) for file in glob.glob('./data/guide/*.png')]

    return guide_img_paths

st.title("Ai_profile")
st.write("사진을 보내주시면, 이메일로 사진 세트를 보내드립니다! 아래는 받아보실 사진의 샘플입니다.")
st.write("")
guide_img_paths = load_img_data()
st.image(guide_img_paths[0],caption='보정이 많이된 사진')
col1, col2 = st.columns(2)
with col1:
    st.image(guide_img_paths[0],caption='보정이 많이된 사진')
with col2:
    st.image(guide_img_paths[1],caption='과한 표정으로 이목구비가 왜곡된 사진')
col1, col2 = st.columns(2)
with col1:
    st.image(guide_img_paths[2],caption='이목구비가 다 안 보이는 사진')
with col2:
    st.image(guide_img_paths[3],caption='이목구비가 틀어진 사진')

    
    
email_input = st.text_input("이메일을 입력해주세요。")
st.write("") 
if email_input:
    if is_valid_email(email_input):
        st.success("성공!")
    else:
        st.warning("잘못된 이메일 형식입니다. 유효한 이메일 주소를 입력하세요.")

uploaded_file = st.file_uploader("이목구비가 잘 들어나는 셀카 사진을 입력해주세요。", type=["jpg", "jpeg", "png"])



if uploaded_file is not None and email_input is not None:
    start = time()
    # assume `uploaded_file` is the image uploaded from Streamlit
    image = Image.open(uploaded_file)

    # convert the image to byte type
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    byte_image = buffered.getvalue()


    
    if st.button("Send"):
        id, db, result_time = report(email_input, byte_image, start)
        result_img = retrieve(id, db)
        st.image(result_img, channels="BGR")
        st.write(result_time + "秒かかりました。")

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

def is_valid_email(email):
    # Regular expression to validate email format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


st.title("Ai_profile")
st.write("사진을 보내주시면, 이메일로 사진 세트를 보내드립니다! 아래는 받아보실 사진의 샘플입니다.")
st.write("")

email_input = st.text_input("이메일을 입력해주세요。")
st.write("") 
if email_input:
    if is_valid_email(email_input):
        st.success("성공!")
    else:
        st.warning("잘못된 이메일 형식입니다. 유효한 이메일 주소를 입력하세요.")

uploaded_file = st.file_uploader("이목구비가 잘 들어나는 셀카 사진을 입력해주세요。", type=["jpg", "jpeg", "png"])
guide_img_paths = [Image.open(file) for file in glob.glob('./data/guide/*.png')]


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


if uploaded_file is not None:
    start = time()
    # assume `uploaded_file` is the image uploaded from Streamlit
    image = Image.open(uploaded_file)

    # resize the image to (1862, 4032)
    resized_image = image.resize((1862, 4032))

    # convert the image to byte type
    buffered = io.BytesIO()
    resized_image.save(buffered, format="JPEG")
    byte_image = buffered.getvalue()


    # img = retrieve(id, db)
    # f1 = FireStore(region, uploaded_file.read())
    # img = f1.retrieve()

    # file_bytes = np.asarray(bytearray(resized_image), dtype=np.uint8)
    np_image = np.array(resized_image)

    # convert the NumPy array to an OpenCV image format
    image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

    # st.image(wrinkle_combined, channels="BGR")

    
    
    id, db, result_time = report(email_input, byte_image, start)
    
    st.write(result_time + "秒かかりました。")

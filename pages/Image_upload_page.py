import streamlit as st
import re
from google.cloud import firestore
from time import time
from datetime import datetime
from PIL import Image
import io
from google.oauth2 import service_account
import json


def report(e_mail, img_lst, start):
    # Authenticate to Firestore with the JSON account key.
    key_dict = json.loads(st.secrets['textkey'])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds)
    result_time = f"{time() - start:.4f}"
    data = {
        'e_mail': e_mail,
        'selfie_img_1': img_lst[0],
        'selfie_img_2': img_lst[1],
        'selfie_img_3': img_lst[2],
        'datetime': datetime.now()
        }
    
    # Create a reference to the Google post.
    doc_ref = db.collection('test_img').add(data)

    return doc_ref[1].id, db, result_time


def retrieve_lst(id, db):
    doc_ref = db.collection('test_img').document(id)
    doc = doc_ref.get().to_dict()
    image_bytes_lst = [doc[f'selfie_img_{idx}'] for idx in range(1,4) ]
    return image_bytes_lst


def to_byte_img(uploaded_file):
    image = Image.open(uploaded_file)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    byte_image = buffered.getvalue()
    
    return byte_image

@st.cache
def is_valid_email(email):
    # Regular expression to validate email format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def main():
    st.set_page_config(page_title="Image Upload", page_icon="📈")

    st.markdown("# Image Upload")
    st.write("")

    email_input = st.text_input("이메일을 입력해주세요。")
    st.write("") 
    if email_input:
        if is_valid_email(email_input):
            st.success("성공!")
        else:
            st.warning("잘못된 이메일 형식입니다. 유효한 이메일 주소를 입력하세요.")
    st.write("## 가이드에 맞는 셀카 사진을 입력해주세요。")
    uploaded_file_1 = st.file_uploader("첫번째", type=["jpg", "jpeg", "png"])
    uploaded_file_2 = st.file_uploader("두번째", type=["jpg", "jpeg", "png"])
    uploaded_file_3 = st.file_uploader("세번째", type=["jpg", "jpeg", "png"])

    if uploaded_file_1 and uploaded_file_2 and uploaded_file_3 and email_input:
        start_time = time()
        byte_imgs = [to_byte_img(file) for file in [uploaded_file_1, uploaded_file_2, uploaded_file_3]]
        

        if st.button("Send"):
            id, db, result_time = report(email_input, byte_imgs, start_time)
            result_imgs = retrieve_lst(id, db)
            st.success("성공!")
            st.image(result_imgs[0], channels="BGR")
            st.image(result_imgs[1], channels="BGR")
            st.image(result_imgs[2], channels="BGR")
            st.write(result_time + " 업로드 소요시간")
               

if __name__ == "__main__":
    main()

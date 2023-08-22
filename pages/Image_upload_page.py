import streamlit as st
import re
from google.cloud import firestore
from time import time
from datetime import datetime
from PIL import Image
import io
from google.oauth2 import service_account
import json


def report(region, img, start):
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

     uploaded_file = st.file_uploader("가이드에 맞는 셀카 사진을 입력해주세요。", type=["jpg", "jpeg", "png"])

     if uploaded_file is not None and email_input is not None:
          start_time = time.time()
          image = Image.open(uploaded_file)

          buffered = io.BytesIO()
          image.save(buffered, format="JPEG")
          byte_image = buffered.getvalue()

          if st.button("Send"):
               id, db, result_time = report(email_input, byte_image, start_time)
               result_img = retrieve(id, db)
               st.image(result_img, channels="BGR")
               st.write(result_time + " seconds elapsed.")

if __name__ == "__main__":
    main()

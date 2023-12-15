import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import re
# from google.cloud import firestore
from firebase_admin import credentials, initialize_app, firestore
from time import time
from datetime import datetime
from PIL import Image
import io
import json


def report(e_mail, img_lst, selected_palette, start, firebase_app):    
    # creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.client(app=firebase_app)
    
    
    result_time = f"{time() - start:.4f}"
    data = {
        'e_mail': e_mail,
        "selected_palette" : selected_palette,
        'selfie_img_1': img_lst[0],
        'selfie_img_2': img_lst[1],
        'selfie_img_3': img_lst[2],
        'createdAt': datetime.now(),
        'finishedAt': None,  # Represent finishedAt as null
        'pickedAt': None,    # Represent pickedAt as null
        'region' : 'kr'
        }
    
    # Create a reference to the Google post.
    doc_ref = db.collection('ai_snap_night').add(data)

    return doc_ref[1].id, db, result_time


def retrieve_lst(id, db):
    doc_ref = db.collection('ai_snap_night').document(id)
    doc = doc_ref.get().to_dict()
    image_bytes_lst = [doc[f'selfie_img_{idx}'] for idx in range(1,4) ]
    return image_bytes_lst


def to_byte_img(uploaded_file, target_width=960):
    image = Image.open(uploaded_file)
     # Get the original width and height
    original_width, original_height = image.size
    
    # Calculate the new height while maintaining the aspect ratio
    new_height = int((target_width / original_width) * original_height)
    
    # Resize the image
    resized_img = image.resize((target_width, new_height), Image.ANTIALIAS)
    
    
    buffered = io.BytesIO()
    # Determine the format based on the image mode (PNG or JPEG)
    image_mode = resized_img.mode
    if image_mode == "RGBA" or image_mode == "P":
        save_format = "PNG"
    else:
        save_format = "JPEG"

    # Save the resized image in the determined format
    resized_img.save(buffered, format=save_format)
    byte_image = buffered.getvalue()
    
    return byte_image

@st.cache(allow_output_mutation=True)
def load_app(key_dict):
    # file_path = '/Users/seongrok.kim/Github/Ai_snap/ai-snap-ff5fb-firebase-adminsdk-1nb7f-114b10efad.json'
    creds = credentials.Certificate(key_dict)
    firebase_app = initialize_app(creds, name='learningnRunning')
    return firebase_app

@st.cache
def is_valid_email(email):
    # Regular expression to validate email format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def main():
    st.set_page_config(page_title="Image Upload", page_icon="🧞‍♂️")
    # secret_door = st.text_input("Alohomora🚪")
    # if secret_door == st.secrets['secrets_keys']:
    #     st.success("Merlin's beard!")
    #     st.markdown("# Image Upload")
    #     st.write("")
    key_dict = json.loads(st.secrets['firebase_auth_token'])
    firebase_app = load_app(key_dict)
    
    
    email_input = st.text_input("결과를 받아 볼 이메일을 입력해주세요。")
    st.write("") 
    if email_input:
        if is_valid_email(email_input):
            st.success("이메일 입력완료")
        else:
            st.warning("잘못된 이메일 형식입니다. 유효한 이메일 주소를 입력하세요.")
    st.write("## 가이드에 맞는 셀카 사진을 입력해주세요。")
    want_to_home = st.button("가이드 다시 확인하러 가기!")
    st.caption("이거 누르면 입력한 내용이 없어집니다! (소노주의)")
    if want_to_home:
        switch_page("Introduction_page")
        
    uploaded_file_1 = st.file_uploader("첫번째 사진", type=["jpg", "jpeg", "png"])
    uploaded_file_2 = st.file_uploader("두번째 사진", type=["jpg", "jpeg", "png"])
    uploaded_file_3 = st.file_uploader("세번째 사진", type=["jpg", "jpeg", "png"])

    if uploaded_file_1 and uploaded_file_2 and uploaded_file_3 and email_input:
        start_time = time()
        byte_imgs = [to_byte_img(file) for file in [uploaded_file_1, uploaded_file_2, uploaded_file_3]]
        # Create a radio button for gender selection
        gender = st.radio("성별을 골라주세요!", ("여성", "남성"))

        # Display a warning message if gender is "Man"
        if gender == "남성":
            st.warning("🥲아쉽게도, 남성 버전은 아직 준비가 안 되었습니다. ")
            st.caption("여자로 태어났다면? 궁금하다면 해도 됩니다.")
        else:
            selected_palette = st.selectbox("받아보실 팔레트를 선택해주세요.", ["night_snap", "christmas_snap", "tennis_snap"])
            if selected_palette:
                selected_palette_path = f'./data/guide/palette_ex_img/{selected_palette}_ex.png'
                st.image(selected_palette_path, channels="BGR", width=500)
            if st.button("사진 업로드📬"):
                with st.spinner('Wait for it...'):
                    id, db, result_time = report(email_input, byte_imgs, selected_palette, start_time, firebase_app)
                    result_imgs = retrieve_lst(id, db)
                st.success("성공!")
                
                # Row 1: Display 3 images side by side
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(result_imgs[0], channels="BGR")
                with col2:
                    st.image(result_imgs[1], channels="BGR")
                with col3:
                    st.image(result_imgs[2], channels="BGR")
                            

                st.write(result_time + " 업로드 소요시간")
                
                st.write(f"### 업로드 완료되었습니다! \n #### 작업이 완료되는 대로 빠르게 보내주신 메일({email_input})로 보내드리겠습니다.")
                st.caption("만약 24시간이 경과 되었는데도 메일이 오지 않았다면 다시 한번 시도해주시길 바랍니다!")
                st.caption("결과 사진을 메일로 보내드릴 때 구글 폼 링크도 보내드립니다..! 피드백이 저희에게  많은 도움이 됩니다.")
    # elif secret_door:
    #     st.warning("No muggles allowed🚷")

if __name__ == "__main__":
    main()

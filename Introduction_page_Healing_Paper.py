import streamlit as st
import random
# from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import glob
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

# Define a custom hash function for re.Match
def my_hash_func(match_obj):
    return hash((match_obj.span(), match_obj.group()))

@st.cache(hash_funcs={re.Match: my_hash_func})
def is_valid_email(email):
    # Regular expression to validate email format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def center_image(image_path):
    st.markdown(
        f'<div style="display: flex; justify-content: center;"><img src="{image_path}" style="width: auto; max-width: 100%;" alt="Centered Image"></div>',
        unsafe_allow_html=True
    )


def load_img_data():
    # Load the Excel data and create the DataFrame
    guide_img_paths = glob.glob('./data/guide/*.png')
    guide_img_paths = sorted(guide_img_paths)
#     st.text(guide_img_paths)
    guide_imgs = [Image.open(file) for file in guide_img_paths]
    
    return guide_imgs



def main():

    
    
    

    
    word_txt = """
    ### 안녕하세요 :)
    연애 프로그램 속 내 모습을 AI 사진으로 만들어보세요!
    """
    # guide_img_paths = load_img_data()
    st.empty()
    
    st.markdown("# 내가 연애 프로그램 출연자라면?")
    # Example usage
    gif_img_paths = [['lee_hyori_27', "거꾸로해도 이효리"], ['solo_seugi_27', "솔로지옥2 슬기"], ['imsolo_youngsuk_27', "나는SOLO 16기 영숙"]]

    # Randomly select an item from the list
    gif_img_path = random.choice(gif_img_paths)

    # Construct the full path to the selected GIF image
    gif_selected_img_path = f"./data/guide/{gif_img_path[0]}.gif"

    st.image(gif_selected_img_path, caption=gif_img_path[1])
    # center_image(gif_img_path)
    # st.sidebar.header("Ai Snap Demo")
    st.markdown(word_txt)
    # st.write("사진을 보내주시면, 이메일로 사진 세트를 보내드립니다! 아래는 받아보실 사진의 샘플입니다.")
    # st.text("보내주신 원본 사진은 사용 후 완전 삭제됨을 알려드립니다.")
    # st.write("")
    
    
    
    # st.image(guide_img_paths[1])
    st.write("")
    st.write("#### 📢 사진 업로드 가이드")
    st.write("정면에 홀로 나온 사진을 입력해주세요! (증명사진이 제일 좋아요!)")
    guide_img_path = "./data/guide/no_photo.jpg"
    st.image(guide_img_path, width= 500)
    

    st.write("")
    st.write("")
    st.write("")
    
    st.write("##### 아래의 정보를 입력해주시면 AI 로맨스 사진을 보내드리겠습니다.")
    
    email_input = st.text_input("결과를 받아 볼 이메일을 입력해주세요。")
    st.write("") 
    if email_input:
        if is_valid_email(email_input):
            st.success("이메일 입력 완료")
        else:
            st.warning("잘못된 이메일 형식입니다. 유효한 이메일 주소를 입력하세요.")

        
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
            selected_palette = st.selectbox("받아보실 팔레트를 선택해주세요.", ["dating_program_snap", "night_snap", "christmas_snap", "tennis_snap"])
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
                
                st.write(f"""
                         ### 업로드 완료되었습니다! \n #### 작업이 완료되는 대로 빠르게 보내주신 메일({email_input})로 보내드리겠습니다.
                             \n그외 문의사항이 있다면 아래로 연락주세요,\n\nmax_sungrok@naver.com \n \n 성록 올림""")
                st.caption("만약 24시간이 경과 되었는데도 메일이 오지 않았다면 다시 한번 시도해주시길 바랍니다!")
                

if __name__ == "__main__":
    
    st.set_page_config(
        page_title="AI ROMANCE", 
        page_icon="📸"
        )
    
    key_dict = json.loads(st.secrets['firebase_auth_token'])
    firebase_app = load_app(key_dict)
    
    
    main()
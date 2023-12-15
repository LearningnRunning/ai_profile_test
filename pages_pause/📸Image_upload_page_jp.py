import streamlit as st
from streamlit_extras.switch_page_button import switch_page
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
        'datetime': datetime.now(),
        'processing_completed' : False,
        'in_progress' : False,
        'region' : 'jp'
        }
    
    # Create a reference to the Google post.
    doc_ref = db.collection('test_img').add(data)

    return doc_ref[1].id, db, result_time


def retrieve_lst(id, db):
    doc_ref = db.collection('test_img').document(id)
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

@st.cache
def is_valid_email(email):
    # Regular expression to validate email format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def main():
    st.set_page_config(page_title="Image_Upload_jp", page_icon="🧞‍♂️")

    # st.markdown("# Image Upload")
    # st.write("")

    # email_input = st.text_input("結果を受け取るメールアドレスを入力してください。")
    # st.write("") 
    # if email_input:
    #     if is_valid_email(email_input):
    #         st.success("成功!")
    #     else:
    #         st.warning("メールアドレスの形式が正しくありません。有効なメールアドレスを入力してください。")
    # st.write("## ガイドに合った自撮り写真を入力してください。")
    # want_to_home = st.button("ガイドを再確認しに行こう")
    # st.caption("これを押すと、入力した内容が消えてしまいます！（注意）")
    # if want_to_home:
    #     switch_page("Introduction_page_jp")
    
    # st.write("")
    # st.write("### デモに参加するには必ず3枚の写真とメールアドレスを入力してください。 写真が3枚未満の場合、参加ができかねます。")
    # uploaded_file_1 = st.file_uploader("最初の", type=["jpg", "jpeg", "png"])
    # uploaded_file_2 = st.file_uploader("二番目", type=["jpg", "jpeg", "png"])
    # uploaded_file_3 = st.file_uploader("三番目", type=["jpg", "jpeg", "png"])

    # if uploaded_file_1 and uploaded_file_2 and uploaded_file_3 and email_input:
    #     start_time = time()
    #     byte_imgs = [to_byte_img(file) for file in [uploaded_file_1, uploaded_file_2, uploaded_file_3]]
    #     # Create a radio button for gender selection
    #     gender = st.radio("性別を選んでください!", ("女性", "男性"))

    #     # Display a warning message if gender is "Man"
    #     if gender == "男性":
    #         st.warning("🥲残念ながら、男性用はまだ準備ができていません。")
    #         st.caption("女の子として生まれたらどんな姿になるのかが気になる方はどうぞ。")
    #     else:
    #         if st.button("Ai photo デモを申し込む"):
    #             with st.spinner('Wait for it...'):
    #                 id, db, result_time = report(email_input, byte_imgs, start_time)
    #                 result_imgs = retrieve_lst(id, db)
    #             st.success("成功!")
                
    #             # Row 1: Display 3 images side by side
    #             col1, col2, col3 = st.columns(3)
    #             with col1:
    #                 st.image(result_imgs[0], channels="BGR")
    #             with col2:
    #                 st.image(result_imgs[1], channels="BGR")
    #             with col3:
    #                 st.image(result_imgs[2], channels="BGR")
                            

    #             st.write(result_time + " 업로드 소요시간")
                
    #             st.write(f"### アップロードが完了しました! \n #### 作業が完了次第、すぐにお送りいただいたメール({email_input})にお送りします。")
    #             st.caption("もし24時間経過してもメールが届かない場合は、もう一度お試しください！")
    #             st.caption("結果写真をメールでお送りする際に、Googleフォームのリンクもお送りします...！？フィードバックは私たちにとって大きな助けになります。")
                

if __name__ == "__main__":
    main()

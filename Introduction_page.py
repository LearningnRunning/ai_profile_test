import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import glob


def load_img_data():
    # Load the Excel data and create the DataFrame
    guide_img_paths = glob.glob('./data/guide/*.png')
    guide_img_paths = sorted(guide_img_paths)
#     st.text(guide_img_paths)
    guide_imgs = [Image.open(file) for file in guide_img_paths]
    
    return guide_imgs



def main():
     
     st.set_page_config(
          page_title="Ai Snap Demo", 
          page_icon="📸"
          )

     st.markdown("# Ai Snap Demo")
     # st.sidebar.header("Ai Snap Demo")

     st.write("사진을 보내주시면, 이메일로 사진 세트를 보내드립니다! 아래는 받아보실 사진의 샘플입니다.")
     st.text("보내주신 원본 사진은 사용 후 완전 삭제됨을 알려드립니다.")
     st.write("")
     guide_img_paths = load_img_data()
     st.image(guide_img_paths[1])

     st.write("## 셀카 사진 업로드 가이드")

     st.image(guide_img_paths[0],caption='보정이 많이된 사진')

     want_to_img_upload = st.button("이미지 업로드하러 가기!")
     if want_to_img_upload:
          switch_page("Image_upload_page")

if __name__ == "__main__":
    main()
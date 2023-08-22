import streamlit as st
from PIL import Image
import glob

@st.cache(suppress_st_warning=True)
def load_img_data():
    # Load the Excel data and create the DataFrame
    guide_img_paths = [Image.open(file) for file in glob.glob('./data/guide/*.png')]

    return guide_img_paths



def main():
     
     st.set_page_config(
          page_title="Ai Snap Demo", 
          page_icon="📸"
          )

     st.markdown("# Ai Snap Demo")
     # st.sidebar.header("Ai Snap Demo")

     st.write("사진을 보내주시면, 이메일로 사진 세트를 보내드립니다! 아래는 받아보실 사진의 샘플입니다.")
     st.write("")
     guide_img_paths = load_img_data()
     st.image(guide_img_paths[4])

     st.write("## 사진 업로드 가이드")
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


if __name__ == "__main__":
    main()
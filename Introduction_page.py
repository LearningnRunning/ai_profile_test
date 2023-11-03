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
        page_title="AI_snap_night_ver", 
        page_icon="📸"
        )
    word_txt = """
    ### 안녕하세요,
    지난 번에 이어 야간 버전으로 [Ai Snap]이 돌아왔습니다. \n
    \n
    아래 사진 가이드 확인하시고 신청해주시면 빠른 시일 내에 이메일로 보내드립니다. \n
    피드백을 위한 데모 기간에 제공하는 서비스입니다. 이메일과 함께 보내드리는 피드백 폼 작성부탁드립니다. \n 
    
    혹시 피드백 참여를 깜빡하신 분은 [피드백 참여하기](https://forms.gle/CUwG5NuyGPQyEtJr9) 작성 부탁드립니다!
    \n
    그외 문의사항이 있다면 아래로 연락주세요,\n
    김성록 매니저 올림\n
    seongrok.kim@elinha.net \n
    ELINHA Co., Ltd
    """
    guide_img_paths = load_img_data()
    st.empty()
    
    st.markdown("# Ai Snap MOONLIGHT")
    st.image(guide_img_paths[0])
    # st.sidebar.header("Ai Snap Demo")
    st.markdown(word_txt)
    # st.write("사진을 보내주시면, 이메일로 사진 세트를 보내드립니다! 아래는 받아보실 사진의 샘플입니다.")
    # st.text("보내주신 원본 사진은 사용 후 완전 삭제됨을 알려드립니다.")
    # st.write("")
    
    
    
    st.image(guide_img_paths[1])

    # st.write("## 셀카 사진 업로드 가이드")

    # st.image(guide_img_paths[0])

    want_to_img_upload = st.button("😀😀😀😀😀😀신청하기😀😀😀😀🤓😀")
    if want_to_img_upload:
        switch_page("Image_upload_page_kr")

if __name__ == "__main__":
    main()
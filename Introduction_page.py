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
        page_title="Ai 사진 서비스 Demo", 
        page_icon="📸"
        )
    word_txt = """
    ### 안녕하세요,
    지난 한 주 동안 시간을 내어 서비스 데모에 신청해주시고 피드백을 보내주신 모든 분들께 진심으로 감사의 말씀을 드립니다. \n
    여러분의 의견과 인사이트는 저희에게 큰 힘이 되었습니다. 압도적인 호응을 보내주신 덕분에 여러분의 요구와 기대에 대해 더 깊이 이해할 수 있었습니다. \n\n
    보내주신 피드백은 여러분의 기대에 부응하고 그 이상을 충족할 수 있도록 서비스를 개선하고 향상시키는 데 중요한 역할을 할 것입니다.
    실제 서비스 배포를 위한 마지막 준비 단계를 진행하고 있다는 소식을 알려드리게 되어 기쁩니다. 출시가 얼마 남지 않았으며, 하루빨리 정식 버전을 여러분께 공유할 수 있기를 기대합니다. \n
    여러분의 참여가 큰 힘이 되었으며, 여러분의 성원에 진심으로 감사드립니다.
    \n
    혹시 피드백 참여를 깜빡하신 분은 [피드백 참여하기](https://forms.gle/CUwG5NuyGPQyEtJr9) 작성 부탁드립니다!
    \n
    그외 문의사항이 있다면 아래로 연락주세요,\n
    김성록 매니저 올림\n
    seongrok.kim@elinha.net \n
    ELINHA Co., Ltd
    """
    st.markdown("# 귀중한 참여에 감사드립니다🥹")
    # st.sidebar.header("Ai Snap Demo")
    st.markdown(word_txt)
    # st.write("사진을 보내주시면, 이메일로 사진 세트를 보내드립니다! 아래는 받아보실 사진의 샘플입니다.")
    # st.text("보내주신 원본 사진은 사용 후 완전 삭제됨을 알려드립니다.")
    # st.write("")
    guide_img_paths = load_img_data()
    st.image(guide_img_paths[1])

    # st.write("## 셀카 사진 업로드 가이드")

    # st.image(guide_img_paths[0])

    # want_to_img_upload = st.button("이미지 업로드하러 가기!")
    # if want_to_img_upload:
    #     switch_page("Image_upload_page_kr")

if __name__ == "__main__":
    main()
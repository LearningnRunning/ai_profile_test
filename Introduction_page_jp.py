import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import glob


def load_img_data():
    # Load the Excel data and create the DataFrame
    guide_img_paths = glob.glob('./data/guide_jp/*.png')
    guide_img_paths = sorted(guide_img_paths)
#     st.text(guide_img_paths)
    guide_imgs = [Image.open(file) for file in guide_img_paths]
    
    return guide_imgs



def main():
     
     st.set_page_config(
          page_title="AI写真サービス", 
          page_icon="📸"
          )

     st.markdown("# AI写真サービス")
     # st.sidebar.header("Ai Snap Demo")

     st.write("写真を送っていただければ、メールで写真セットをお送りします！以下は、お送りする写真のサンプルです。")
     st.text("お送りいただいたオリジナル写真は、使用後に完全に削除されることをお知らせします。")
     st.write("")
     guide_img_paths = load_img_data()
     st.image(guide_img_paths[1])

     st.write("## 自撮り写真アップロードガイド")

     st.image(guide_img_paths[0])

     want_to_img_upload = st.button("画像アップロードへ!")
     if want_to_img_upload:
          switch_page("Image_upload_page_jp")

if __name__ == "__main__":
    main()
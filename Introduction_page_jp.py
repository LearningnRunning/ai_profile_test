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
    word_txt = """
    ### こんにちは、
    この一週間、サービスデモにお申し込みいただき、フィードバックを送ってくださった皆様、誠にありがとうございました。\n
    皆様のご意見は、私たちにとって大きな励みとなりました。大きな反響があったおかげで、皆様のニーズと期待をより深く理解することができました。n\n\n
    いただいたフィードバックは、皆様の期待に応え、それを超えることができるようなサービスに改善していく上で、重要な役割を担うと思います。
    実際のサービス展開に向けた最終段階に入ることができ嬉しく思っています。 リリースまであとわずかですが、早く正式版を皆様にお届けできることを楽しみにしています。\n
    皆様の参加が大きな力になりました。ご協力誠にありがとうございました。
    \n
    もしフィードバックに参加するのを忘れた方は、[[フィードバックに参加する](https://forms.gle/vjJSKZ3tXfp1KSnt8)] を作成してください!
    \n
    その他ご不明な点がございましたら、下記までご連絡ください,\n
    キム・ソンロク マネージャー \n
    seongrok.kim@elinha.net \n
    ELINHA Co., Ltd
    """
    st.markdown("# 貴重なご参加ありがとうございました🥹。")
    # st.sidebar.header("Ai Snap Demo")
    st.markdown(word_txt)
    
    # st.write("写真を送っていただければ、メールで写真セットをお送りします！以下は、お送りする写真のサンプルです。")
    # st.text("お送りいただいたオリジナル写真は、使用後に完全に削除されることをお知らせします。")
    # st.write("")
    guide_img_paths = load_img_data()
    st.image(guide_img_paths[1])

    # st.write("## 自撮り写真アップロードガイド")

    # st.image(guide_img_paths[0])

    # want_to_img_upload = st.button("画像アップロードへ!")
    # if want_to_img_upload:
    #     switch_page("Image_upload_page_jp")

if __name__ == "__main__":
    main()
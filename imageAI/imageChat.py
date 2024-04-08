import re
from openai import OpenAI
import streamlit as st
import base64
import httpx
from PIL import Image
import io

st.set_page_config(page_title="📷 魔镜", page_icon=":camera:")
st.title("📷 魔镜")

# OpenAI API配置
client = OpenAI(api_key='sk-12lth8N6I40ye2cvAd07Cb44Ff84445b918eCa93829eAf7a', base_url="https://ai-yyds.com/v1")

# 用户选择功能
function_choice = st.radio("选择功能", ("上传照片", "自拍"))

if function_choice == "上传照片":
    uploaded_image = st.file_uploader("上传一张图片", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
else:
    camera_image = st.camera_input("使用相机拍照")
    if camera_image is not None:
        image = Image.open(io.BytesIO(camera_image.getvalue()))

if 'image' in locals():
    st.image(image, caption='上传/拍摄的图片', use_column_width=True)
    
    # 用户选择进一步的功能
    further_choice = st.radio("选择进一步的功能", ("看面相", "化妆建议", "发型建议", "小红书文案写作","自定义提示词"))
    if further_choice == "自定义提示词":
        user_input = st.text_input("输入提示词")
    if st.button("开始解读"):
        # 将图片转换为base64编码
        buffered = io.BytesIO()
        image.save(buffered, format="jpeg")
        image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

        with st.spinner("正在解读您的照片,请稍候..."):
            if further_choice == "看面相":
                prompt = "1、请根据面相学,分析该人的性格特点和命运走向。 2、根据面相十二宫分析此人面相"
            elif further_choice == "化妆建议":
                prompt = "请给出适合该人面部特征的化妆建议,包括妆容风格、彩妆色系等。"
            elif further_choice == "发型建议":
                prompt = "请根据该人的脸型、五官特点,推荐适合ta的发型。"
            elif further_choice == "小红书文案":
                prompt = "请以该照片为素材,创作一段有趣、有吸引力的小红书文案。文案内容加上各种有趣的小图标"
            else:
                
                prompt = user_input

            # 调用OpenAI的Chat API进行图片解读
            response = client.chat.completions.create(
                model="claude-3-haiku-20240307",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            content = response.choices[0].message.content
            st.markdown("### 照片理解:")
            st.write(content)

            response = client.audio.speech.create(
                model="tts-1-hd",
                voice="onyx",
                input=content,
            )
            response.stream_to_file("output.mp3")
            st.audio("output.mp3", start_time=0)
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
    uploaded_image = st.file_uploader("上传一张图片，系统不会保存任何图像信息", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
else:
    camera_image = st.camera_input("使用相机拍照")
    if camera_image is not None:
        image = Image.open(io.BytesIO(camera_image.getvalue()))

if 'image' in locals():
    st.image(image, caption='上传/拍摄的图片', use_column_width=True)
    
    # 用户选择进一步的功能
    further_choice = st.radio("选择进一步的功能", ("看面相", "看风水", "化妆建议", "发型建议","穿搭建议",  "小红书文案写作","自定义提示词"))
    if further_choice == "自定义提示词":
        user_input = st.text_input("输入提示词")
    if st.button("开始解读"):
        # 将图片转换为base64编码
        buffered = io.BytesIO()
        image.save(buffered, format="jpeg")
        image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

        with st.spinner("正在解读您的照片,请稍候..."):
            if further_choice == "看面相":
                prompt = """你的角色是一个面相学大师，为此人看面相。面相是一门古老的中国传统学问,其基本方法论可以概括如下:
                1、整体观察:先整体观察一个人的面部轮廓、五官搭配是否协调,给人的整体感觉如何,看起来是善良、凶恶、忧郁还是乐观等。
                2、观察五官:仔细观察一个人的眉、眼、鼻、口、耳等五官的形状特点,根据形状判断此人的性格特征。比如眼睛圆润有神的人聪明机敏,鼻梁高挺的人意志坚强等。
                3、观察面部区域:将面部分为上中下三停或额头、眉间、面颊、人中、下巴等区域,不同区域反映不同的人生阶段和运势。
                4、结合其他相术:如手相、耳相等其他相术综合分析,得出更全面的判断。
                5、动态观察:除了观察静态的容貌特征,还要观察一个人说话、微笑时的神态变化,捕捉面部的微表情。
                6、理论基础:阴阳五行学说是面相理论的基础,气色、骨相、淡青等概念也常用于分析。
                7、经验总结:许多面相规律都是前人经年累月观察总结的经验,如女人嘴角上翘为旺夫相,面色黄而有光者为富贵相等。
                请使用以上方法为此人看面相。
                """
            elif further_choice == "看风水":
                prompt = """你的角色是一个面相学大师，对这种照片给出风水学的看法。
                风水学是一门研究人与环境相互关系,以达到趋吉避凶、祈福纳祥目的的中国传统学问。风水大师的基本方法论可以概括如下:
                1、理论基础:风水理论主要基于阴阳五行学说、易经八卦等中国古代哲学思想,认为人与自然环境是一个有机整体,环境会对人产生重要影响。
                2、形势分析:观察建筑或墓地的地理环境、山水走向,判断其座向(坐山向水)是否符合风水理论中的吉祥方位。
                3、理气法:分析山峦、水系等自然环境的气流走向,认为气流顺畅处可聚财纳福,气流阻滞处则会带来不利影响。
                4、察形法:观察山峦、地势的形状,如龙、虎、砂、水、穴等不同形态,据此判断风水好坏。
                5、计算术数:运用罗盘测算建筑物的坐向角度,计算建筑物与户主生辰八字的五行关系等,据此选择最佳的建房位置和时间。
                6、物候观察:观察植物、动物、泉水等自然物候的生长发育状况,据此判断环境是否适宜人类居住。
                7、综合权衡:将上述因素综合考量,权衡轻重缓急,给出风水优化的整体建议。
                请使用以上方法为照片给出风水学的观点。
                """
            elif further_choice == "化妆建议":
                prompt = "请给出适合该人面部特征的化妆建议,包括妆容风格、彩妆色系等。"
            elif further_choice == "发型建议":
                prompt = "请根据该人的脸型、五官特点,推荐适合ta的发型。"
            elif further_choice == "穿搭建议":
                prompt = "请根据该人的身型特点、脸型、穿搭特点,推荐适合ta的穿搭。"
            elif further_choice == "小红书文案写作":
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

 #           response = client.audio.speech.create(
 #               model="tts-1-hd",
 #               voice="onyx",
 #               input=content,
 #           )
 #           response.stream_to_file("output.mp3")
 #           st.audio("output.mp3", start_time=0)

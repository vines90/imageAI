import re
from openai import OpenAI
import streamlit as st

import base64
import httpx



image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
image2_media_type = "image/jpeg"
image2_data = base64.b64encode(httpx.get(image2_url).content).decode("utf-8")

client = OpenAI(api_key='sk-12lth8N6I40ye2cvAd07Cb44Ff84445b918eCa93829eAf7a',base_url="https://ai-yyds.com/v1")

response = client.chat.completions.create(
  model="claude-3-haiku-20240307",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "描述图片",
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{image2_data}",
          },
        },

      ],
    }
  ],
  max_tokens=300,
)
content = response.choices[0].message.content
print(content)

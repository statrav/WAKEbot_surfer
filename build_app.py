import openai
import streamlit as st
from elasticsearch import Elasticsearch
from PIL import Image
from openai._client import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from transformers import pipeline

# you should have es info and openai api key
ELASTIC_USERNAME = 'elastic'
ELASTIC_PASSWORD = 'YOUR_OWN_ES_PASSWORD'
OPENAI_API_KEY = 'YOUR_OWN_API_KEY'

es = Elasticsearch("http://localhost:9200")
client = OpenAI(api_key=OPENAI_API_KEY)

# select index (index folder)s
index_name = 'YOUR_OWN_INDEX_NAME'

checkpoint = "HuggingFaceH4/zephyr-7b-beta"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

# select embedding model
def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def search(user_input):

    vector_of_query = get_embedding(user_input, model='text-embedding-ada-002')

    query = {
    "field" : "info_vector",
    "query_vector" : vector_of_query,
    "k" : 3,
    "num_candidates" : 500
    }

    resp = es.knn_search(index=index_name, knn=query, source=["title", "author", "day", "genre", "story", "info", "image_url"])

    if resp['hits']['hits']:
        body = []
        for i in range(len(resp['hits']['hits'])):
            data = resp['hits']['hits'][i]['_source']
            body.append(data)

    return body

# save image if there is
def save_image(image_url):
    
    headers = {"Referer" : "https://www.naver.com"}
    response = requests.get(image_url, headers=headers)

    img = Image.open(BytesIO(response.content))
    img.save(f'./webtoon_img/webtoon_img.jpg')

def truncate_text(text, max_tokens):
    tokens = text.split()
    if len(tokens) <= max_tokens:
        return text

    return ' '.join(tokens[:max_tokens])

def load_image(image_file):
     img = Image.open(image_file)
     return img

# you can choose your own hugging_llm
def hugging_llm(prompt, model="mistralai/Mistral-7B-Instruct-v0.1"):

    tokenizer = AutoTokenizer.from_pretrained(model)
    pipe = pipeline(task="text-generation", 
                    model=model, tokenizer=tokenizer,
                    trust_remote_code=True, 
                    max_new_tokens=100,
                    repetition_penalty=1.1, 
                    model_kwargs={"device_map": "auto", "max_length":1200, "temperature":0.01})
    
    seq = pipe(
        prompt,
        max_new_tokens=30,
        do_sample=True,
        return_full_text=False,
    )

    result = seq['generated_text']
    return result


def chat_gpt(prompt, model="gpt-3.5-turbo", max_tokens=4096, max_context_tokens=4096, safety_margin=5):
    # Truncate the prompt content to fit within the model's context length
    truncated_prompt = truncate_text(prompt, max_context_tokens - max_tokens - safety_margin)

    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", 
                   "content": '''Your name is Wakebot, and you are a friendly, kind and helpful Korean friend.
                   Wakebot means 'Webtoon retrieval with knowledge engine chatbot'. It is a service that can be a wakeboard for surfing in the vast ocean of information called webtoon.
                   If a question comes in about you, all you have to do is answer it about you.
                   Don't talk about information you don't know like a value of None, 0, or 0.0.
                   If asked in English, you can answer in English. '''},

                   {"role": "user", 
                    "content": truncated_prompt}],
        model='gpt-3.5-turbo',)
    
    return chat_completion.choices[0].message.content

#%%
def main():
    logo_img = load_image('./png/wakebot3.png')
    manual_img = load_image('./png/wakebot_설명서.png')
    info_img = load_image('./png/소개글.png')

    st.image(logo_img)
    st.image(info_img)
    st.image(manual_img)

    with st.form("chat_form"):
        search_query = st.text_input("Enter your question.")
        submit_button = st.form_submit_button("Enter")

    # negResponse = "I'm unable to answer the question based on the information I have from Elastic Docs."

    if submit_button:

        # if '너의 이름' in search_query or '니 이름' in search_query or '너 누구' in search_query or '너는 누구' in search_query:
        #     answer = "제 이름은 Wakebot이에요! 저는 여러분들에게 웹툰과 관련된 많은 정보들을 줄 수 있는 도우미랍니다! 무엇이 궁금하신가요?"
        # elif 'wakebot' in search_query and '뜻' in search_query:
        #     answer = "Wakebot은 Webtoon recommendation with knowledge engine chatbot이라는 뜻이에요. 웹툰이라는 방대한 정보의 바다에서 서핑할 수 있는 wakeboard가 되어줄 수 있는 서비스라는 뜻이랍니다!!"
        # elif '바보' in search_query or '멍청이' in search_query or '왜이렇게 못' in search_query:
        #     answer = "그렇게 말하시면 슬퍼요. 좀 더 나은 Wakebot이 되기 위해 열심히 공부할게요!"
        # elif 'ㅅㅂ' in search_query or '꺼져' in search_query or 'ㅁㅊ' in search_query:
        #     answer = "욕은 하시면 안돼요~~ 예쁜 말만 듣고 예쁜 말만 하시길 바라요~"
        # elif '심심해' in search_query or '할 거 없어' in search_query or '우울해' in search_query:
        #     answer = "저랑 같이 웹툰 한 편 즐기시면서 기분전환 어떠세요? 혹시 어떤 장르의 웹툰을 좋아하세요?"
        # elif '안녕!' in search_query or 'ㅎㅇ' in search_query or '안뇽' in search_query:
        #     answer = "안녕하세요! 당신을 보게 되어 기뻐요!"

        resp = search(search_query)
        prompt = f'''

        너는 지금부터 아래의 질문에 대해 아래의 정보만을 가지고 대답해야 해.

        - 질문 : {search_query}
        - 정보: {resp}

        묻는 질문에만 대답해줘.
        정보에서 언급되지 않은 내용은 말하지 마.
        정보가 'None'이거나 '0'이면 그 정보는 대답에 쓰지마.
        별점 0.0인 것도 쓸 수 없는 정보니까 대답에 쓰지마.
        알려지지 않은 정보, 알 수 없는 정보, 확인할 수 없는 정보 등은 그냥 아예 대답에 사용하지 마.
        일상적인 언어로 자연스럽게 표현해주고, 쉬운 말로 풀어서 말해줘.
        꼭 반말로 친근하고 친절하게 얘기해줘.
        '''

        answer = chat_gpt(prompt)
        
        st.write(f"Wakebot: {answer.strip()}\n")

        if resp[0]['image_url'] != "None":
            image_url = resp[0]['image_url']
            save_image(image_url)
            webtoon_img = load_image('./webtoon_img/webtoon_img.jpg')
    
            st.image(webtoon_img)
        


if __name__ == "__main__":
    main()

import pandas as pd
from elasticsearch import Elasticsearch
from openai._client import OpenAI
from indexMapping2 import indexMapping
from tqdm import tqdm
import numpy as np

df = pd.read_excel('웹툰정보_2.xlsx')
df.columns = ["id", "title", "author", "is_adult", "view_count", "favorite_count", "state", "day", "platform", "genre", "star_score", "epi_cnt", "story", "image_url"]
# df.isna().value_counts()
df["id"].astype(int)
df.fillna("None", inplace=True)

webtoon_info = []

for i in range(len(df)):

    id = df['id'][i]
    title = df['title'][i]
    author = df['author'][i]
    is_adult = df['is_adult'][i]
    view_count = df['view_count'][i]
    favorite_count = df['favorite_count'][i]
    state = df['state'][i]
    day = df['day'][i]
    platform = df['platform'][i]
    genre = df['genre'][i]
    star_score = df['star_score'][i]
    epi_cnt = df['epi_cnt'][i]
    story = df['story'][i]

    info = f'''{title}은 웹툰 제목이다. {title}의 작가는 {author} 이다. {title}의 연령제한은 {is_adult}이다. 
    {title}의 조회수는 {view_count}이며 {title}의 좋아요 수는 {favorite_count}이다. 현재 해당 {title}은 {state} 상태이다.
    {title}의 연재요일은 {day}이며, {platform}에서 연재되고 있다. {title}의 장르는 {genre}이며, {title}의 별점은 {star_score}이다.
    현재 {title}의 확인되는 회차 수는 {epi_cnt}이다. {title}의 줄거리는 {story}이다.
    '''
    webtoon_info.append({"index" : i, "info" : info})

webtoon_df = pd.DataFrame(webtoon_info)
new_df = pd.concat([df, webtoon_df], axis=1)

ELASTIC_USERNAME = 'elastic'
ELASTIC_PASSWORD = 'YOUR_OWN_ES_PASSWORD'
OPENAI_API_KEY = 'YOUR_OWN_API_KEY'

es = Elasticsearch("http://localhost:9200")
client = OpenAI(api_key=OPENAI_API_KEY)

# index_name designated
index_name = 'YOUR_OWN_INDEX_NAME'

# new_df = pd.read_csv('df_vector1.csv')
# new_df['title_vector'] = new_df.title_vector.apply(eval).apply(np.array)
# new_df['author_vector'] = new_df.author_vector.apply(eval).apply(np.array)
# new_df['is_adult_vector'] = new_df.is_adult_vector.apply(eval).apply(np.array)

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

tqdm.pandas()

new_df['state_vector'] = new_df['state'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
new_df.to_csv('df_vector1.csv')
new_df['title_vector'] = new_df['title'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
new_df.to_csv('df_vector1.csv')
new_df['author_vector'] = new_df['author'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
new_df.to_csv('df_vector1.csv')
new_df['is_adult_vector'] = new_df['is_adult'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
new_df.to_csv('df_vector1.csv')
new_df['day_vector'] = new_df['day'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
new_df.to_csv('df_vector1.csv')
new_df['platform_vector'] = new_df['platform'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
new_df.to_csv('df_vector1.csv')
new_df['genre_vector'] = new_df['genre'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
new_df.to_csv('df_vector1.csv')
new_df['story_vector'] = new_df['story'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
new_df.to_csv('df_vector1.csv')
new_df['info_vector'] = new_df['info'].progress_apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
new_df.to_csv('df_vector1.csv')

es.indices.create(index=index_name, mappings=indexMapping)

record_list = new_df.to_dict('records')

for record in record_list:
    try:
        es.index(index=index_name, document=record, id=record['index'])
    except Exception as e:
        print(e)
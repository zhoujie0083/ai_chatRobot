import os.path

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

DB_DIR = 'faiss_db/'
EMBEDDINGS = OpenAIEmbeddings()

def save_vectors_db():
    """ ベクターデータベースの構築 """

    if os.path.exists(DB_DIR):
        print('ベクトルデータベースは既に存在します。')
    else:
        with open('datas.txt',encoding = 'utf8') as f:
            content = f.read()

    #
    txt_splitter = CharacterTextSplitter(
        separator=r'\d+.',
        is_separator_regex= True,
        chunk_size=100,
        chunk_overlap=0,
        length_function=len
    )

    docs = txt_splitter.create_documents([content])
    db = FAISS.from_documents(docs,EMBEDDINGS)
    db.save_local(DB_DIR)

    # 質問動作テスト
    # result = db.similarity_search('')
    # print(result)


def init_chain():

    # 1
    db = FAISS.load_local(DB_DIR,EMBEDDINGS,allow_dangerous_deserialization= True)
    # 2


if __name__ == '__main__':
    save_vectors_db()

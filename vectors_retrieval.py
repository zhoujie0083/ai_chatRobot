import os.path

from langchain_text_splitters import CharacterTextSplitter

DB_DIR = 'faiss_db/'

def save_vectors_db():
    """ ベクターデータベースの構築 """

    if os.path.exists(DB_DIR):
        print('')
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

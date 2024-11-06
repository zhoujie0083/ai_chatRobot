import os.path
from platform import system

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from openai import models

DB_DIR = 'faiss_db/'
EMBEDDINGS = OpenAIEmbeddings()

def save_vectors_db():
    """ ベクターデータベースの構築 """

    if os.path.exists(DB_DIR):
        print('ベクトルデータベースは既に存在します。再構築不要！')
    else:
        with open('datas.txt',encoding = 'utf8') as f:
            contents = f.read()

    #
    txt_splitter = CharacterTextSplitter(
        separator=r'\d+\.\n',
        is_separator_regex= True,
        chunk_size=100,
        chunk_overlap=0,
        length_function=len
    )

    docs = txt_splitter.create_documents([contents])
    db = FAISS.from_documents(docs,EMBEDDINGS)
    db.save_local(DB_DIR)

    # 質問動作テスト
    # result = db.similarity_search('')
    # print(result)


def init_chain():

    # step_1 Loadベクターデータベース
    db = FAISS.load_local(DB_DIR,EMBEDDINGS,allow_dangerous_deserialization= True)
    # step_2 プロンプトテンプレートの作成
    system_prompt= """  
    {context}
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ('system',system_prompt),
            ('human','{input}')
        ]
    )

    # step_3 chain作成
    # 検索
    retriever = db.as_retriever(search_type='similarity_score_threshold', search_kwargs={"score_threshold": 0.7})


    model = ChatOpenAI(model_name='gpt-4o', temperature = 0.2)
    chain_1 = create_stuff_documents_chain(llm=model, prompt=prompt_template)
    return create_retrieval_chain(retriever= retriever, combine_docs_chain= chain_1)


if __name__ == '__main__':
    save_vectors_db()
    chain = init_chain()
    res = chain.invoke({'input':''})

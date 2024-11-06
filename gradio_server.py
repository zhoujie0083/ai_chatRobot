import random
import time

import gradio as gr

from vectors_retrieval import save_vectors_db, init_chain


def do_user(user_message, history):
    history.append((user_message, None))
    return '', history


def do_it(history):
    print(history)
    question = history[-1][0]
    res = robot.invoke({'input': question})
    resp = res['answer']

    if not resp:
        resp = 'すみません。この問題は回答出来ません、スタッフに聞いてください。'



    #ソース動作疎通
    # responses = [
    #     "メッセージありがとうございます！",
    #     "とても興味深いです！",
    #     "どう答えればいいのかわかりません。",
    #     "他にご質問はありますか？",
    #     "できるだけ早くご連絡させていただきます。",
    #     "あなたとコミュニケーションを取ることができて嬉しいです！",
    # ]
    #
    # resp = random.choice(responses)

    history[-1][1] = ''


    for char in resp:
        history[-1][1] += char
        time.sleep(0.1)
        yield history

def run_gradio():

    css = """
    #bgc {background-color: #7FFFD4}
    .feedback textarea {font-size: 24px !important}
    """

    # Blocks：
    with gr.Blocks(title='日本の税金AI_ChatRobot', css=css) as instance:
        gr.Label('日本の税金AI_ChatRobot', container=False)
        chatbot = gr.Chatbot(label='AI Robotの回答',height=550, placeholder='<strong>AI ChatRobot</strong><br> こんにちは、何かお手伝いできますか?')
        msg = gr.Textbox(label='質問を入力してください',placeholder='質問を入力してください！', elem_classes='feedback', elem_id='bgc')
        clear = gr.ClearButton(value='会話の記録をクリア', components=[msg, chatbot])


        msg.submit(do_user, [msg, chatbot], [msg, chatbot], queue=False).then(do_it, chatbot, chatbot)


    instance.queue()
    instance.launch(server_name='127.0.0.1', server_port=8008)


def init():
    # 初期化AI Robot
    save_vectors_db()
    global robot
    robot = init_chain()


if __name__ == '__main__':
    # 初期化AI Robot
    init()
    run_gradio()

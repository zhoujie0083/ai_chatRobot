import random
import time

import gradio as gr


def do_user(user_message, history):
    history.append((user_message, None))
    return '', history


def do_it(history):
    print(history)
    responses = [
        "メッセージありがとうございます！",
        "とても興味深いです！",
        "どう答えればいいのかわかりません。",
        "他にご質問はありますか？",
        "できるだけ早くご連絡させていただきます。",
        "あなたとコミュニケーションを取ることができて嬉しいです！",
    ]

    resp = random.choice(responses)


    history[-1][1] = ''


    for char in resp:
        history[-1][1] += char
        time.sleep(0.1)
        yield history

css = """
#bgc {background-color: #7FFFD4}
.feedback textarea {font-size: 24px !important}
"""

# Blocks：
with gr.Blocks(title='日本の税金AI_ChatRobot', css=css) as instance:
    gr.Label('日本の税金AI_ChatRobot', container=False)
    chatbot = gr.Chatbot(height=550, placeholder='<strong>AI ChatRobot</strong><br> こんにちは、何かお手伝いできますか?',type='messages')
    msg = gr.Textbox(placeholder='質問を入力してください！', elem_classes='feedback', elem_id='bgc')
    clear = gr.ClearButton(value='会話の記録をクリア', components=[msg, chatbot])


    msg.submit(do_user, [msg, chatbot], [msg, chatbot], queue=False).then(do_it, chatbot, chatbot)


instance.queue()
instance.launch(server_name='127.0.0.1', server_port=8008,share=True)

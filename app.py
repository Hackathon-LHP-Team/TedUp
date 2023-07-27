'''
Structure of the web
Homepage
    - Navbar:
        - Logo + Virtual Therapist
        - Developer docs:
            - Documentations (how to clone this website and run code)
            - Github (Deep learning notebook, resources)
            - Research paper
        - About us
        - Experience app
        - Account
    - Main theme:
        - Motion image 
        - "explore now" button
    - Our Story / Introduction (With Virtual Therapist, you've got someone in your corner) -> 4 main features
    - Demo (two options: video or gif image with options bar) -> Small conversation, meaningful progress
    - Core/key features (images needed):
        - Chatbot as virtual therapist
        - Artificial Intelligence using Deep Neural Network 
        - Syetem for Mental health quality assessment
    - Team members
        - Name + task (leader: Idea pitching, AI engineer, Backend developer)
        - Name + task (frontend developers)
        - Name + Task (Persona + Design)
    
App page:
    - Sidebar:
        - Your conversations
        - Your history record
        - System messages
        - Blogs (optional)
'''

'''
cookies = json.loads(open("cookies.json", encoding="utf-8").read()) 



async def main(res):
    for _ in range(1):
        bot = await Chatbot.create(cookies=cookies) 
        input_text = input("Talk something...")
        response = await bot.ask(prompt=input_text, conversation_style=ConversationStyle.creative, simplify_response=True)
        bot_response = response["text"]
        output_response = re.sub('\[\^\d+\^\]', '', bot_response)
        res = output_response
        await bot.close()
    return res

if __name__ == "__main__":
    res = ""
    res = asyncio.run(main(res))
    print(res)
'''


from flask import Flask, render_template, request, jsonify
import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import re


cookies = json.loads(open("cookies.json", encoding="utf-8").read()) 
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/app_experience")
def app_experience():
    return render_template('app_experience.html')


async def main(res):
    for _ in range(1):
        bot = await Chatbot.create(cookies=cookies) 
        input_text = input("Talk something...")
        response = await bot.ask(prompt=input_text, conversation_style=ConversationStyle.creative, simplify_response=True)
        bot_response = response["text"]
        output_response = re.sub('\[\^\d+\^\]', '', bot_response)
        res = output_response
        await bot.close()
    return res

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        text = request.form.get('floatingTextarea2')
        print(text)
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(main(res))
        print(res)
        return render_template('app_experience.html', res=res)
    else:
        return render_template('app_experience.html')

if __name__ == '__main__':
    app.run()

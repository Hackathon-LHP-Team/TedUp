import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import re

cookies = json.loads(open("cookies.json", encoding="utf-8").read()) 
output_response = ""

async def main():
    for _ in range(5):
        bot = await Chatbot.create(cookies=cookies) 
        input_text = input("Talk something...")
        response = await bot.ask(prompt=input_text, conversation_style=ConversationStyle.creative, simplify_response=True)
        bot_response = response["text"]
        output_response = re.sub('\[\^\d+\^\]', '', bot_response)
        print("Bot Response: ", output_response)
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
    
    
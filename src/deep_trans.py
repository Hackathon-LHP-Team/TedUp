from deep_translator import GoogleTranslator

def translate(list_Chats):
    translated_list_chats = []
    for chat in list_Chats:
        translated_chat = GoogleTranslator(source='vi', target='en').translate(chat)
        translated_list_chats.append(translated_chat)
    return translated_list_chats

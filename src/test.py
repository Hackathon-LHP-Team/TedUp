from score import score
import numpy as np

# chat data retrieved from streamlit 
Chats = [
    "",
    "I feel very dejected today. I got a very low score in my math exam, everybody in class made a joke on me. The rest of my day, I do not feel like doing anything, the sadness, the sorrow just seem to fill in me",
    "But when coming home (today has been really tough), my parents even depress me more, they scolded me, they made me more disheartened. I feel so hopeless",
    "it's kind of good. But I am rather confused whether their method coud be applied in my case. Anyway let me try",
    "Oh I have tried on that method. Things start getting positive. My parents can sympathize with me now. I feel really pleased and happy that they can understand me. Hopefully, everything can get better because I really want to be joyful at school. Anyway just maintain my optimistic outlook",
]

# Create an object of the class
score_obj = score(Chats)

# Call the methods on the object
tokenizer = score_obj.generate_token()
padded_chat_seq = score_obj.tokenize_text(tokenizer)
padded_text_seq = score_obj.tokenize_text_test(tokenizer, Chats[1])
# print(padded_chat_seq)

s = [0]
print(padded_chat_seq[1])
print(padded_text_seq)
print(Chats[1])
print(score_obj.predict(padded_text_seq))
# for i in range(1, len(padded_chat_seq)):
#     y_i = score_obj.predict(padded_chat_seq[i])
#     y_i = np.argsort(y_i)[0][-3:]

#     s_i = 0
#     for j in range(len(y_i)):
#         s_i += y_i[j]
#         s_i /= 3
#     s.append(s_i)
    
# print(s)

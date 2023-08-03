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
Q_res, s_res = score_obj.Q_value(padded_chat_seq)
print(s_res)
print(Q_res)

'''
results

1/1 [==============================] - 2s 2s/step
1/1 [==============================] - 0s 68ms/step
1/1 [==============================] - 0s 94ms/step
1/1 [==============================] - 0s 85ms/step
[0, 1.5, 3.8000000000000003, 3.8000000000000003, 3.633333333333333]
2.806208333333333
'''
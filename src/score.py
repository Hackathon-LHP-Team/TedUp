# Array and Dataframe
import numpy as np
import pandas as pd

# Text preprocessing
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


class score:
    def __init__(self, Chats):
        self.vocab_size = 10000
        self.embedding_dim = 64
        self.max_length = 200
        self.df = pd.read_csv('assets/emotion_classification_dataset_v1.1.csv')
        self.model = tf.keras.models.load_model('assets/12_classes_emotions_classifications.h5')
        self.model2 = tf.keras.models.load_model('assets/model_3_classes_v1.1.h5')
        self.classes = ["anger", "sadness", "remorse", "fear", "depression", "lonely", "joy", "love", "optimism", "gratitude", "pride", "confusion"]
        self.classes2 = ["Negative Emotions", "Positive Emotions", "Neutral Emotions"]
        self.Chats = Chats
        self.N = len(Chats) - 1
        self.f = [1.5, 1.8, 2.0, 2.2, 1.2, 1.9, 4.8, 4.9, 4.5, 4.6, 4.2, 2.5]
        
    def generate_token(self):
        sentences = self.df["text"].values
        tokenizer = Tokenizer(num_words=self.vocab_size, oov_token="<OOV>")
        tokenizer.fit_on_texts(sentences)
        return tokenizer

    def tokenize_text(self, tokenizer):
        chat_seq = tokenizer.texts_to_sequences(self.Chats)
        padded_chat_seq = pad_sequences(chat_seq, maxlen=self.max_length, truncating="post", padding="post")
        return padded_chat_seq
            
    def predict(self, padded_text_seq):
        prediction = self.model.predict(padded_text_seq)
        return prediction
    
    def predict2(self, padded_text_seq):
        prediction = np.argmax(self.model2.predict(padded_text_seq))
        return self.classes2[prediction]
    
    def Q_value(self, chats, gamma = 0.9):
        s = [0]
        for i in range(1, len(chats)):
            y_i= self.model.predict([chats[i].tolist()])
            y_i = np.argsort(y_i)[0][-3:]

            s_i = 0
            for j in range(len(y_i)):
                s_i += self.f[y_i[j]]
            s_i /= 3
            s.append(s_i)
           
        Q = 0
        for i in range(1, self.N + 1):
            Q = Q + gamma**(self.N - i) * s[i]
        Q /= self.N
        return Q,s
            



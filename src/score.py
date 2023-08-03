# # Array and Dataframe
# import numpy as np
# import pandas as pd

# # Text preprocessing
# import re
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences

# # Training
# from sklearn.model_selection import train_test_split
# import tensorflow as tf
# from tensorflow.keras.layers import Input, Embedding, Bidirectional, LSTM, GlobalAveragePooling1D, Dense, Dropout
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.utils import to_categorical
# from sklearn.model_selection import train_test_split

# df = pd.read_csv('emotion_classification_dataset_v1.1.csv')
# sentences, labels = df["text"].values, df["index_label"].values

# x_train, x_test, y_train_2, y_test_2 = train_test_split(
#     sentences,
#     labels,
#     test_size=0.2,
#     shuffle=True,
#     random_state=42,
#     stratify=labels
# )

# vocab_size = 10000
# embedding_dim = 64
# max_length = 200

# tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
# tokenizer.fit_on_texts(sentences)
# word_index = tokenizer.word_index

# train_sequences = tokenizer.texts_to_sequences(x_train)
# padded_train_sequences = pad_sequences(train_sequences, maxlen=max_length, truncating="post", padding="post")

# test_sequences = tokenizer.texts_to_sequences(x_test)
# padded_test_sequences = pad_sequences(test_sequences, maxlen=max_length, truncating="post", padding="post")

# infer_text = ["I feel deeply disappointed today because my parents scolded me too much. They do not understand me. Very downmood to know that they only judge me on my scores. What a despondent life"]

# text_seq = tokenizer.texts_to_sequences(infer_text)
# padded_text_seq = pad_sequences(text_seq, maxlen=max_length, truncating="post", padding="post")
# padded_text_seq
# print(padded_text_seq)

# model_path = 'model_12_classes_v1.1.h5'
# model = tf.keras.models.load_model(model_path)

# prediction = np.argmax(model.predict(padded_text_seq))
# classes = ["anger", "sadness", "remorse", "fear", "depression", "lonely", "joy", "love", "optimism", "gratitude", "pride", "confusion"]

# print(classes[prediction])


# Array and Dataframe
import numpy as np
import pandas as pd

# Text preprocessing
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Training
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Bidirectional, LSTM, GlobalAveragePooling1D, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

class score:
    def __init__(self, Chats):
        self.vocab_size = 10000
        self.embedding_dim = 64
        self.max_length = 200
        self.df = pd.read_csv('emotion_classification_dataset_v1.1.csv')
        self.model = tf.keras.models.load_model('model_12_classes_v1.1.h5')
        self.classes = ["anger", "sadness", "remorse", "fear", "depression", "lonely", "joy", "love", "optimism", "gratitude", "pride", "confusion"]
        self.Chats = Chats
        self.N = len(Chats) - 1
        
    def generate_token(self):
        sentences = self.df["text"].values
        tokenizer = Tokenizer(num_words=self.vocab_size, oov_token="<OOV>")
        tokenizer.fit_on_texts(sentences)
        return tokenizer

    def tokenize_text(self, tokenizer):
        chat_seq = tokenizer.texts_to_sequences(self.Chats)
        padded_chat_seq = pad_sequences(chat_seq, maxlen=self.max_length, truncating="post", padding="post")
        return padded_chat_seq
    
    def tokenize_text_test(self, tokenizer, infer):
        text_seq = tokenizer.texts_to_sequences([infer])
        padded_text_seq = pad_sequences(text_seq, maxlen=self.max_length, truncating="post", padding="post")
        return padded_text_seq
        
    def predict(self, padded_text_seq):
        prediction = self.model.predict(padded_text_seq)
        return prediction
    
    def Q_value(self, chats, gamma = 0.9):
        s = [0]
        for i in range(1, len(chats)):
            y_i= self.model.predict(chats[i])
            y_i = np.argsort(y_i)[0][-3:]

            s_i = 0
            for j in range(len(y_i)):
                s_i += y_i[j]
            s_i /= 3
            s.append(s_i)
            
        print(s)
                
        Q = 0
        for i in range(1, self.N + 1):
            Q = Q + gamma**(self.N - i) * s[i]
            Q /= self.N
        return Q
            



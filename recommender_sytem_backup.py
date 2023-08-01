import pandas as pd
import numpy as np

def cosine(a, b):
  # add the epsilon to avoid denominator being 0
  return a.dot(b) / ((np.linalg.norm(a) * np.linalg.norm(b)) + np.finfo(np.float64).eps)

def recys():
    df = pd.read_csv('utility_matrix.csv')
    mean = df.mean()
    df = df.sub(mean, axis=1)
    COLS = df.columns.values.tolist().copy()

    # Compute cosine similarity
    utility_matrix = df.values
    num_user = utility_matrix.shape[1]
    user_to_user_similarity_matrix = np.zeros((num_user, num_user))

    for i in range(num_user):
        for j in range(num_user):
            # lấy ra 1 cặp item
            user_1 = df[COLS[i]]
            user_2 = df[COLS[j]]

            index_not_zero = (user_1 > 0) & (user_2 > 0)
            user_to_user_similarity_matrix[i,j] = cosine(user_1[index_not_zero], user_2[index_not_zero])
            
    # Fill back in
    zero_rating_indices = np.where(utility_matrix == 0)
    for blog, user in zip(zero_rating_indices[0], zero_rating_indices[1]):
        similar_users = user_to_user_similarity_matrix[2]
        blog_time_spent = utility_matrix[blog]
        index = blog_time_spent > 0
        blog_time_spent = blog_time_spent[index]
        similar_users = similar_users[index]
        utility_matrix[blog, user] = np.sum(blog_time_spent * similar_users) / (np.sum(similar_users) + np.finfo(np.float64).eps)
        utility_matrix.to_csv("utility_matrix.csv")


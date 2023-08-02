import pandas as pd
import numpy as np

class recys:
  def cosine(self, a, b):
    # add the epsilon to avoid denominator being 0
    return a.dot(b) / ((np.linalg.norm(a) * np.linalg.norm(b)) + np.finfo(np.float64).eps)

  # function in flask backend
  def compute(self, current_user_logined_id):
    utility_matrix = pd.read_csv("utility_matrix.csv")
    utility_matrix.replace(0, np.nan, inplace=True)
    mean = utility_matrix.mean(skipna=True)
    utility_matrix = utility_matrix.sub(mean, axis=1)
    utility_matrix = utility_matrix.fillna(0)
    utility_matrix = utility_matrix.values

    num_user = utility_matrix.shape[1]
    user_to_user_similarity_matrix = np.zeros((num_user, num_user))

    for i in range(num_user):
      for j in range(num_user):
        user_i = utility_matrix[:,i]
        user_j = utility_matrix[:,j]
        index_not_zero = (user_i > 0) & (user_j > 0)
        user_to_user_similarity_matrix[i,j] = self.cosine(user_i[index_not_zero], user_j[index_not_zero])
      
    zero_rating_indices = np.where(utility_matrix == 0)
    for blog, user in zip(zero_rating_indices[0], zero_rating_indices[1]):
      similar_users = user_to_user_similarity_matrix[user]
      blog_time_spent = utility_matrix[blog]
      index = blog_time_spent > 0
      blog_time_spent = blog_time_spent[index]
      similar_users = similar_users[index]
      utility_matrix[blog, user] = np.sum(blog_time_spent * similar_users) / (np.sum(similar_users) + np.finfo(np.float64).eps)

    mean = mean.values
    utility_matrix = utility_matrix + mean
    utility_matrix = pd.DataFrame(utility_matrix)
    utility_matrix.to_csv("filled_utility_matrix.csv", index=False) 

    utility_matrix = pd.read_csv("utility_matrix.csv")
    utility_matrix_filled = pd.read_csv("filled_utility_matrix.csv")

    zero_rating_indices = np.where(utility_matrix == 0)
    dictionary = {}
    for blog, user in zip(zero_rating_indices[0], zero_rating_indices[1]):
        if user == current_user_logined_id - 1:
          dictionary[blog + 1] = utility_matrix_filled.iloc[blog, user]
        
    dictionary = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
    threshold = mean[current_user_logined_id - 1]
    result = [i for i, j in dictionary if j >= threshold]
    return result[:3]

result = recys()
print(result.compute(current_user_logined_id=4))
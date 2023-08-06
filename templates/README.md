# README
## Recommender System

View [colab notebook](https://github.com/Hackathon-LHP-Team/Virtual-Therapist/blob/main/Deep%20Learning%20training/model_v1.1/Recommender_System.ipynb) for more explanation

See [video demo](https://youtu.be/iaAHY0NucaI) to see how it actually works on wesite

Update utility matrix when new user register, new blog is created, user read a blog, user delete a blog

```python
class utility_matrix_management:
  def __init__(self, csv_path):
    self.csv_path = csv_path
    
  def init_or_update_csv(self, Users_query, Blogs_query):
      df = pd.read_csv(self.csv_path)
      num_cols = len(df.columns)
      num_rows = len(df.index)
      
      num_users = Users_query
      num_blogs = Blogs_query
          
      # if new user registers
      if num_users > num_cols:
          temp_col = [0] * num_rows
          temp_col = pd.DataFrame(temp_col)
          df = pd.concat([df, temp_col], axis=1)
          df = df.to_numpy()
          df = pd.DataFrame(df)
          df.to_csv(self.csv_path, index=False)

      # if new blog is created
      if num_blogs > num_rows:
          df = df.T
          df.to_csv(self.csv_path, index=False)
          df = pd.read_csv(self.csv_path)
          num_rows = len(df.index)
          
          temp_col = [0] * num_rows
          temp_col = pd.DataFrame(temp_col)
          df = pd.concat([df, temp_col], axis=1)
          df = df.T.to_numpy()
          df = pd.DataFrame(df)
          df.to_csv(self.csv_path, index=False)
       
  # fill the value of utility matrix with time a user spends reading a particular blog
  def fill_uitlity_matrix(self, blog_id, user_id, duration):
      df = pd.read_csv(self.csv_path)
      if duration > df.iloc[blog_id - 1][user_id - 1]:
        df.iloc[blog_id - 1][user_id - 1] = duration
        df.to_csv(self.csv_path, index=False)

  # Delete row when a user deletes a blog 
  def delete_row_utility_matrix(self, blog_id):
      df = pd.read_csv(self.csv_path)
      df = df.drop([blog_id-1])
      df.to_csv(self.csv_path, index=False)
```

This blog recommeneder system uses user-to-user collaborative filtering to suggest blogs for user. The value in the utility matrix is the actual time user spend on a particular blog. Then the class recsys in the `recommender_sytem_backup.py` file will predict the zero values in the matrix (the blogs that one particular user has not read). Finally the function `compute` will return the descending probability vector showing which blogs user might like and spend much time reading

```python
class recys:
  # function to compute similarity between users
  def cosine(self, a, b):
    # add the epsilon to avoid denominator being 0
    return a.dot(b) / ((np.linalg.norm(a) * np.linalg.norm(b)) + np.finfo(np.float64).eps)

  # function in flask backend
  def compute(self, current_user_logined_id):
    
    # preprocessing the utility matrix 
    utility_matrix = pd.read_csv("utility_matrix.csv")
    utility_matrix.replace(0, np.nan, inplace=True)
    mean = utility_matrix.mean(skipna=True)
    utility_matrix = utility_matrix.sub(mean, axis=1)
    utility_matrix = utility_matrix.fillna(0)
    utility_matrix = utility_matrix.values

    # Create the user-to-user similarity matrix
    num_user = utility_matrix.shape[1]
    user_to_user_similarity_matrix = np.zeros((num_user, num_user))

    for i in range(num_user):
      for j in range(num_user):
        user_i = utility_matrix[:,i]
        user_j = utility_matrix[:,j]
        index_not_zero = (user_i > 0) & (user_j > 0)
        user_to_user_similarity_matrix[i,j] = self.cosine(user_i[index_not_zero], user_j[index_not_zero])
      
    # Fill back into the original utility matrix with the neighborhood colloborative filtering formula
    # Open colab notebook to see the image describing the math formula
    zero_rating_indices = np.where(utility_matrix == 0)
    for blog, user in zip(zero_rating_indices[0], zero_rating_indices[1]):
      similar_users = user_to_user_similarity_matrix[user]
      blog_time_spent = utility_matrix[blog]
      index = blog_time_spent > 0
      blog_time_spent = blog_time_spent[index]
      similar_users = similar_users[index]
      utility_matrix[blog, user] = np.sum(blog_time_spent * similar_users) / (np.sum(similar_users) + np.finfo(np.float64).eps)

    # Return back to the original scale value by adding the mean value
    mean = mean.values
    utility_matrix = utility_matrix + mean
    utility_matrix = pd.DataFrame(utility_matrix)
    utility_matrix.to_csv("filled_utility_matrix.csv", index=False) 

    utility_matrix = pd.read_csv("utility_matrix.csv")
    utility_matrix_filled = pd.read_csv("filled_utility_matrix.csv")

    # Compute the probability vector with dictionary
    zero_rating_indices = np.where(utility_matrix == 0)
    dictionary = {}
    for blog, user in zip(zero_rating_indices[0], zero_rating_indices[1]):
        if user == current_user_logined_id - 1:
          dictionary[blog + 1] = utility_matrix_filled.iloc[blog, user]
        
    # dictionar{'key', 'value'} : 'key' is blog_id and 'value' is the estimated time user spend on that blog
    dictionary = sorted(dictionary.items(), key=lambda item: item[1], reverse=True) 
    
    # Define the threshold (the mean value)
    threshold = mean[current_user_logined_id - 1]
    result = [i for i, j in dictionary if j >= threshold]
    
    if len(result) > 3:
      return result[:3]
    return result
```

This class receive the current_user.id from flask database. Let's check the result with this command

```python
result = recys()
print(result.compute(current_user_logined_id=4))
```
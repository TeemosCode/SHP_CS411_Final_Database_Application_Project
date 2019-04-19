# Import Pandas
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import sys
import csv




# Function that takes in movie title as input and outputs most similar movies
def get_recommendations_post(rows, post_id):
    # get blogpost data
    metadata = pd.DataFrame(rows)
    print(metadata)
    content = metadata['content']
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(content)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    # Construct a reverse map of indices and post_id
    indices = pd.Series(
        metadata.index, index=metadata['postid']).drop_duplicates()
    # Get the index of the post given post_id
    idx = indices[post_id]
    # Get the pairwsie similarity scores of all activity with that activity
    sim_scores = list(enumerate(cosine_sim[idx]))
    # print("sim_scores", sim_scores, "post_id", post_id)
    updated_sim_scores = [(metadata['postid'][pair[0]].item(), pair[1].item()) for pair in sim_scores]
    # Sort the movies based on the similarity scores
    updated_sim_scores = sorted(updated_sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 3 most similar movies except itself
    updated_sim_scores = updated_sim_scores[1:4]
    # Return the top 3 most similar movies
    print(updated_sim_scores)
    return updated_sim_scores


# print("__name__", __name__)

if __name__ == "__main__":
    res = get_recommendations_post(3)
    print(res)

# Import Pandas
import pandas as pd
import sys
import csv

from .tf_idf import tf_idf_process, getIDFs
from .metrics import Metrics

def getSimScores(rows, post_id):
    # get blogpost data
    metadata = pd.DataFrame(rows)

    docs = list(metadata['content'])
    target = metadata[metadata['postid'] == post_id]['content'].values[0]
    idfs = getIDFs(docs)
    res = []
    for doc in docs:
        tfidf1, tfidf2 = tf_idf_process(str(doc), str(target),idfs)

        keys = tfidf1.keys()
        lst1 = [tfidf1[k] for k in keys]
        lst2 = [tfidf2[k] for k in keys]
        res.append(Metrics.customized(lst1, lst2))
        print(Metrics.customized(lst1,lst2))
    return list(enumerate(res))


# def getSimScores2(rows, post_id):
#     metadata = pd.DataFrame(rows)
#
#     content = metadata['content']
#     tfidf = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = tfidf.fit_transform(content)
#     cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
#     # Construct a reverse map of indices and post_id
#     indices = pd.Series(
#         metadata.index, index=metadata['postid']).drop_duplicates()
#     # Get the index of the post given post_id
#     idx = indices[post_id]
#     # Get the pairwsie similarity scores of all activity with that activity
#     sim_scores = list(enumerate(cosine_sim[idx]))
#     return sim_scores


# Function that takes in movie title as input and outputs most similar movies
def get_recommendations_post(rows, post_id):
    # get blogpost data
    metadata = pd.DataFrame(rows)
    sim_scores = getSimScores(rows,post_id)
    updated_sim_scores = [(metadata['postid'][pair[0]].item(), pair[1] if type(pair[1])==int or type(pair[1])==float else pair[1].item()) for pair in sim_scores]
    # Sort the movies based on the similarity scores
    updated_sim_scores = sorted(updated_sim_scores, key=lambda x: x[1])
    # Get the scores of the 4 most similar movies except itself
    updated_sim_scores = updated_sim_scores[:4]
    # Return the top 4 most similar movies
    return updated_sim_scores



if __name__ == "__main__":
    res = get_recommendations_post(3)

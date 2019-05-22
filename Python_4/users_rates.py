import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
from sklearn.preprocessing import LabelEncoder
from scipy.sparse import coo_matrix, csr_matrix


def cosine_similarity_pair_users(u, v):
    if (u).multiply(v).nnz <= 2:
        return 0.0

    user_rated = (u.todense() != 0) & (v.todense() != 0)

    u = u[user_rated]
    v = v[user_rated]

    return u.dot(v.T)[0, 0] / ((u.dot(u.T)[0, 0] ** 0.5) * (v.dot(v.T)[0, 0] ** 0.5))


def get_top5(ind, M, n_neighbours):
    users_dict = {}

    for i in range(M.shape[0]):
        if i != ind:
            users_dict[i] = cosine_similarity_pair_users(M[ind], M[i])

    top_neighbours = sorted(users_dict, key=users_dict.get, reverse=True)[: n_neighbours]

    rates_dict = {}

    for i in range(R.toarray().shape[1]):
        if R[ind].toarray()[0][i] == 0.0:
            num_sum = 0.0
            den_sum = 0.0

            for j in top_neighbours:
                num_sum += users_dict[j] * R[j].toarray()[0][i]
                den_sum += users_dict[j]

            rates_dict[i] = num_sum / den_sum

    return sorted(rates_dict, key=rates_dict.get, reverse=True)[: 5]


if __name__ == '__main__':
    filepath = './data/user_ratedmovies.dat'
    df_rates = pd.read_csv(filepath, sep='\t')

    filepath = './data/movies.dat'
    df_movies = pd.read_csv(filepath, sep='\t', encoding='iso-8859-1')

    enc_user = LabelEncoder()
    enc_mov = LabelEncoder()

    enc_user = enc_user.fit(df_rates.userID.values)
    enc_mov = enc_mov.fit(df_rates.movieID.values)

    idx = df_movies.loc[:, 'id'].isin(df_rates.movieID)
    df_movies = df_movies.loc[idx]

    df_rates.loc[:, 'userID'] = enc_user.transform(df_rates.loc[:, 'userID'].values)
    df_rates.loc[:, 'movieID'] = enc_mov.transform(df_rates.loc[:, 'movieID'].values)
    df_movies.loc[:, 'id'] = enc_mov.transform(df_movies.loc[:, 'id'].values)

    R = coo_matrix((df_rates.rating.values, (df_rates.userID.values, df_rates.movieID.values)))
    R = R.tocsr()

    top5 = get_top5(20, R, 30)

    print(', '.join(str(i) for i in top5))


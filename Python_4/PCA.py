import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import numpy as np


if __name__ == '__main__':
    filepath = 'tsfresh_features_filt.csv'
    sign_features_filtered = pd.read_csv(filepath)

    #df_database = pd.read_csv('sign_database.csv')

    sign_classes = pd.read_csv('sign_classes.csv', index_col=0, header=0, names=['id', 'class'])

    X = sign_features_filtered.values

    del sign_features_filtered

    enc = LabelEncoder()
    enc.fit(sign_classes.loc[:, 'class'])
    sign_classes.loc[:, 'target'] = enc.transform(sign_classes.loc[:, 'class'])
    y = sign_classes.target.values

    del sign_classes

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=123)

    X = StandardScaler().fit_transform(X)

    pca = PCA(n_components=27, svd_solver='randomized', random_state=123)
    pca.fit(X)
    print(pca.explained_variance_ratio_.sum())

    """
    base_model = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('pca', pca),
        ('clf', KNeighborsClassifier(n_neighbors=9))
    ])

    base_cv_scores = cross_val_score(base_model, X, y, cv=cv, scoring='accuracy')

    print(base_cv_scores.mean())
    print(np.var(pca.transform(X), axis=0).sum())
    """

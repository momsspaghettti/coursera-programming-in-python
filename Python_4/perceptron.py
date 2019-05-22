import numpy as np
from sklearn.datasets import load_iris
import random
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class Perceptron:

    def __init__(self, nu, t_max):
        self.nu = nu
        self.t_max = t_max

        self.w = [0, 0, 0, 0]
        self.b = 0

    def fit(self, X, y):
        random.seed(42)
        n = len(X)

        t = 0
        while t < self.t_max:
            rnd_index = random.randint(0, n - 1)

            tmp_X = X[rnd_index]
            tmp_y = y[rnd_index]

            if tmp_y * (np.dot(tmp_X, self.w) + self.b) <= 0:
                self.b += self.nu * tmp_y

                for i in range(len(self.w)):
                    self.w[i] += self.nu * tmp_y * tmp_X[i]

            t += 1

    def predict(self, X):
        out_y = []

        for x in X:
            if np.dot(x, self.w) + self.b >= 0:
                out_y.append(1)
            else:
                out_y.append(-1)

        return out_y


if __name__ == '__main__':
    X, y = load_iris(return_X_y=True)
    X, y = X[:100], y[:100]
    num_features = X.shape[1]
    y = np.array([1 if y_i == 1 else -1 for y_i in y])

    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.25, random_state=10)

    perceptron = Perceptron(0.1, 40)

    perceptron.fit(train_X, train_y)

    score = accuracy_score(test_y, perceptron.predict(test_X))

    print("score {0:.2f}".format(score))

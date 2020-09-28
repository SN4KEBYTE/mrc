from pathlib import Path

import numpy as np
from pyprind import ProgBar
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier

from mrc.docstream import DocStream
from mrc.preprocessing import preprocessor
from mrc.tokenization import tokenize, stop
from mrc.utils import dump, load

objects_dir = Path(__file__).parent.parent / 'data' / 'pkl_objects'
vect_path = objects_dir / 'vect.pkl'
clf_path = objects_dir / 'clf.pkl'
stopwords_path = objects_dir / 'stop.pkl'


def check_vectorizer() -> HashingVectorizer:
    if not vect_path.is_file():
        print('Hashing vectorizer was not found, creating...')

        vect = HashingVectorizer(decode_error='ignore', n_features=2 ** 21, preprocessor=preprocessor,
                                 tokenizer=tokenize)
        dump(vect, vect_path, protocol=4)
    else:
        vect = load(vect_path)

    return vect


def check_classifier(vect: HashingVectorizer) -> None:
    if not clf_path.is_file():
        print('Classifier was not found, creating...')

        clf = SGDClassifier(loss='log', random_state=1)
        ds = DocStream('./movie_data.csv')
        pbar = ProgBar(45)

        classes = np.array([0, 1])

        for _ in range(45):
            x_train, y_train = ds.get_minibatch(1000)

            if not x_train:
                break

            x_train = vect.transform(x_train)
            clf.partial_fit(x_train, y_train, classes)
            pbar.update()

        print('Training completed...')

        x_test, y_test = ds.get_minibatch(5000)
        x_test = vect.transform(x_test)

        print(f'Score: {clf.score(x_test, y_test)}')

        clf = clf.partial_fit(x_test, y_test)

        dump(clf, clf_path, protocol=4)


def check_stopwords() -> None:
    if not stopwords_path.is_file():
        print('Stopwords were not found, creating...')

        dump(stop, stopwords_path, protocol=4)


if __name__ == '__main__':
    v = check_vectorizer()
    check_classifier(v)
    check_stopwords()

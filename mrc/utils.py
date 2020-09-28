import pickle
from typing import Any


def dump(obj: Any, path, protocol: int = None, fix_imports: bool = True, buffer_callback: bool = None) -> None:
    with open(path, 'wb') as out:
        pickle.dump(obj, out, protocol=protocol, fix_imports=fix_imports, buffer_callback=buffer_callback)


def load(path, fix_imports=True, encoding="ASCII", errors="strict", buffers=None) -> Any:
    with open(path, 'rb') as inp:
        return pickle.load(inp, fix_imports=fix_imports, encoding=encoding, errors=errors, buffers=buffers)


def classify(clf, vect, document):
    labels = {0: 'negative', 1: 'positive'}

    x = vect.transform([document])
    y = clf.predict(x)[0]
    proba = clf.predict_proba(x).max()

    return labels[y], proba


def partial_fit(clf, vect, document, label):
    clf.partial_fit(vect.transform(document), [label])

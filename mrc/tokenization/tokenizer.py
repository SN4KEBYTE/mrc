from typing import List

from nltk.corpus import stopwords

stop = stopwords.words('english')


def tokenize(text: str) -> List[str]:
    return [word for word in text.split() if word not in stop]

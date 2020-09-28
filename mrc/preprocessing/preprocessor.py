import re
from typing import List


def _remove_html(text: str) -> str:
    return re.sub('<[^>]*>', '', text)


def _find_emoticons(text) -> List[str]:
    return re.findall(r'(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)


def _remove_non_alpha(text: str) -> str:
    return re.sub(r'[\W]+', ' ', text.lower())


def preprocessor(text: str) -> str:
    t: str = _remove_html(text)
    emoticons = _find_emoticons(t)
    t = _remove_non_alpha(t) + ' '.join(emoticons).replace('-', '')

    return t

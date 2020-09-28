from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from pyprind import ProgBar

DOCS_NUM: int = 50000


def main():
    labels: Dict[str, int] = {'neg': 0, 'pos': 1}
    dataset_path: Path = Path(__file__).parent.parent / 'data' / 'movie_data.csv'

    np.random.seed(0)

    pbar: ProgBar = ProgBar(DOCS_NUM)
    df: pd.DataFrame = pd.DataFrame()

    for subset in ('test', 'train'):
        for label in ('pos', 'neg'):
            path: Path = Path(__file__).parent / 'aclImdb' / subset / label

            for file in path.iterdir():
                with open(path / file, 'r', encoding='utf-8') as inp:
                    txt: str = inp.read()

                df = df.append([[txt, labels[label]]], ignore_index=True)
                pbar.update()

    df.columns = ['review', 'sentiment']

    df = df.reindex(np.random.permutation(df.index))
    df.to_csv(dataset_path, index=False)


if __name__ == '__main__':
    main()

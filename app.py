from flask import Flask, render_template, request

from mrc.utils import classify, load, partial_fit
from mrc.review_db import ReviewDB
from mrc.review_form import ReviewForm

from pathlib import Path


app = Flask(__name__)
cur_dir = Path(__file__).parent

clf = load(cur_dir / 'data' / 'pkl_objects' / 'clf.pkl')
db = ReviewDB(cur_dir / 'data' / 'reviews.sqlite')


@app.route('/')
def index():
    form = ReviewForm(request.form)

    return render_template('review_form.html', form=form)


@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)

    if request.method == 'POST' and form.validate():
        review = request.form['movie_review']

        label, proba = classify(clf, None, review)

        return render_template('results.html', content=review, prediction=label, probability=round(proba * 100, 2))

    return render_template('review_form.html', form=form)


@app.route('/thanks', methods=['POST'])
def feedback():
    fb = request.form['feedback_button']
    review = request.form['review']
    prediction = request.form['prediction']

    inv_labels = {'negative': 0, 'positive': 1}
    y = inv_labels[prediction]

    if fb == 'Неправильно':
        y = int(not(y))

    partial_fit(clf, None, review, y)
    db.insert_entry(review, y)

    return render_template('thanks.html')


if __name__ == '__main__':
    app.run(debug=True)

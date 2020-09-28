from wtforms import Form, TextAreaField, validators


class ReviewForm(Form):
    movie_review: TextAreaField = TextAreaField('', [validators.DataRequired(), validators.length(min=15)])

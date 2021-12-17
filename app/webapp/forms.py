from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import ValidationError

class MainForm(FlaskForm):
    content = TextAreaField('Enter text', validators=[]) #DataRequired()


    file = FileField('Or insert txt/pdf file', validators = [FileAllowed(['pdf','txt'])])
    submit = SubmitField('Start search', render_kw={"onclick": "$('#loading').show();$('#content').hide();"})

    keyword = StringField('Keywords for searching')
    pdf_only = BooleanField('Only search for PDF files')

    default_slider_val = 6
    num_files = IntegerRangeField('How many search results do you want to compare your document with?', default = default_slider_val)

    def validate_keyword(self, keyword):
        if len(keyword.data) ==0:
            raise ValidationError("This field cannot be empty!")
        elif len(keyword.data.split()) > 32:
            raise ValidationError("Maximum word count for Google Search is 32!")
        else:
            for item in keyword.data.split():
                if len(item) >128:
                    raise ValidationError("Maximum characters in a word for Google Search is 128!")

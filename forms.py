from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, SubmitField


class BatchForm(FlaskForm):
  csv_file = FileField(
      'Upload CSV',
      validators=[
          FileRequired(message='Please select a CSV file to upload.'),
          FileAllowed(['csv'], message='Only CSV files are allowed!'),
      ],
  )
  submit = SubmitField('Process Batch CSV')
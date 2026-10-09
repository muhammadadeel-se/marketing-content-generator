import io
import os
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
import pandas as pd

from forms import BatchForm
from generate_copy import generate_copy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY', 'default-dev-secret-key-12345'
)

# In-memory storage for batch results (for review and export)
batch_storage = []


@app.route('/', methods=['GET', 'POST'])
def index():
  copy_result = None
  error = None

  if request.method == 'POST':
    product_name = request.form.get('product_name', '').strip()
    key_features = request.form.get('key_features', '').strip()
    target_audience = request.form.get('target_audience', '').strip()

    if not product_name or not key_features or not target_audience:
      error = 'Please fill out all fields before generating content.'
    else:
      try:
        copy_result = generate_copy(product_name, key_features, target_audience)
      except Exception as e:
        error = f'Error generating copy: {str(e)}'

  return render_template('index.html', copy_result=copy_result, error=error)


@app.route('/batch', methods=['GET', 'POST'])
def batch():
  global batch_storage
  form = BatchForm()

  if form.validate_on_submit():
    csv_file = form.csv_file.data

    try:
      # Read uploaded CSV file directly using Pandas
      df = pd.read_csv(csv_file)

      # Validate required columns
      required_cols = {'Product Name', 'Key Features', 'Target Audience'}
      if not required_cols.issubset(df.columns):
        flash(
            'CSV missing required columns: Product Name, Key Features, Target'
            ' Audience',
            'danger',
        )
        return render_template('batch.html', form=form)

      results = []
      for idx, row in df.iterrows():
        product_name = str(row.get('Product Name', '')).strip()
        key_features = str(row.get('Key Features', '')).strip()
        target_audience = str(row.get('Target Audience', '')).strip()

        # Generate AI copy for each row
        generated = generate_copy(product_name, key_features, target_audience)

        results.append({
            'id': idx,
            'product_name': product_name,
            'headline': generated.get('headline', ''),
            'tagline': generated.get('tagline', ''),
            'body': generated.get('body', ''),
            'approved_headline': True,
            'approved_tagline': True,
            'approved_body': True,
        })

      # Update global batch storage for export
      batch_storage = results
      return render_template('batch_results.html', results=results)

    except Exception as e:
      flash(f'Error processing CSV: {str(e)}', 'danger')
      return render_template('batch.html', form=form)

  return render_template('batch.html', form=form)


@app.route('/export', methods=['POST'])
def export():
  global batch_storage

  if not batch_storage:
    flash('No batch results available to export.', 'warning')
    return redirect(url_for('batch'))

  # Capture checkbox approval statuses from form submission
  for item in batch_storage:
    item_id = str(item['id'])
    item['approved_headline'] = (
        request.form.get(f'approved_headline_{item_id}') == 'on'
    )
    item['approved_tagline'] = (
        request.form.get(f'approved_tagline_{item_id}') == 'on'
    )
    item['approved_body'] = request.form.get(f'approved_body_{item_id}') == 'on'

  # Build DataFrame for export
  export_data = []
  for item in batch_storage:
    export_data.append({
        'Product Name': item['product_name'],
        'Headline': item['headline'],
        'Headline Approved': item['approved_headline'],
        'Tagline': item['tagline'],
        'Tagline Approved': item['approved_tagline'],
        'Body Copy': item['body'],
        'Body Approved': item['approved_body'],
    })

  export_df = pd.DataFrame(export_data)

  # Save to buffer stream for direct browser download
  buffer = io.BytesIO()
  export_df.to_csv(buffer, index=False)
  buffer.seek(0)

  return send_file(
      buffer,
      mimetype='text/csv',
      as_attachment=True,
      download_name='reviewed_marketing_copy.csv',
  )


if __name__ == '__main__':
  app.run(debug=True)
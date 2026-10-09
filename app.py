import io
import pandas as pd
from flask import Flask, render_template, request, Response
from generate_copy import generate_marketing_copy

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    copy_result = None
    error_message = None

    if request.method == "POST":
        product_name = request.form.get("product_name", "").strip()
        key_features = request.form.get("key_features", "").strip()
        target_audience = request.form.get("target_audience", "").strip()

        if not product_name or not key_features or not target_audience:
            error_message = "Please fill in all required fields."
        else:
            combined = f"Product Name: {product_name}. Key Features: {key_features}. Target Audience: {target_audience}."
            try:
                copy_result = generate_marketing_copy(combined)
            except Exception as e:
                error_message = f"Error generating copy: {str(e)}"

    return render_template("index.html", copy_result=copy_result, error_message=error_message)

@app.route("/batch", methods=["GET", "POST"])
def batch():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename.endswith(".csv"):
            return render_template("batch.html", error="Please upload a valid CSV file.")

        try:
            df = pd.read_csv(file)
            results = []
            for _, row in df.iterrows():
                p_name = row.get("Product Name", "N/A")
                features = row.get("Key Features", "N/A")
                audience = row.get("Target Audience", "N/A")

                combined = f"Product Name: {p_name}. Key Features: {features}. Target Audience: {audience}."
                generated = generate_marketing_copy(combined)
                
                results.append({
                    "product_name": p_name,
                    "headline": generated.get("headline", ""),
                    "tagline": generated.get("tagline", ""),
                    "body": generated.get("body", "")
                })

            return render_template("batch_results.html", results=results)
        except Exception as e:
            return render_template("batch.html", error=f"Error processing CSV: {str(e)}")

    return render_template("batch.html")

@app.route("/export", methods=["POST"])
def export():
    total_rows = int(request.form.get("total_rows", 0))
    exported_data = []

    for i in range(total_rows):
        exported_data.append({
            "Product Name": request.form.get(f"product_name_{i}"),
            "Headline": request.form.get(f"headline_{i}"),
            "Tagline": request.form.get(f"tagline_{i}"),
            "Body Copy": request.form.get(f"body_{i}"),
            "Approved Status": "Approved" if request.form.get(f"approved_{i}") == "Yes" else "Pending"
        })

    out_df = pd.DataFrame(exported_data)
    output = io.StringIO()
    out_df.to_csv(output, index=False)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=reviewed_marketing_copy.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True)
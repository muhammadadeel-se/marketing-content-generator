from flask import Flask, render_template, request
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

        # Validation
        if not product_name or not key_features or not target_audience:
            error_message = "Please fill in all required fields (Product Name, Key Features, Target Audience)."
        else:
            combined_description = (
                f"Product Name: {product_name}. "
                f"Key Features: {key_features}. "
                f"Target Audience: {target_audience}."
            )

            try:
                copy_result = generate_marketing_copy(combined_description)
            except Exception as e:
                error_message = f"Error generating copy: {str(e)}"

    return render_template("index.html", copy_result=copy_result, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
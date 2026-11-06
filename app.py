
from flask import Flask, render_template, request
import pandas as pd
from io import StringIO

application = Flask(__name__)


@application.route("/", methods=["GET"])
def dashboard():
    return render_template("index.html")


@application.route("/analyze", methods=["POST"])
def process_csv():

    stock_name = request.form.get("symbol", "").strip()
    expiration_date = request.form.get("expiry", "").strip()
    csv_file = request.files.get("file")

    if not csv_file or csv_file.filename == "":
        return "Please select a CSV file before submitting."

    try:
        # Read uploaded CSV information
        csv_content = csv_file.read().decode("latin1")
        dataset = pd.read_csv(StringIO(csv_content))

        # Prepare dataset information
        total_rows = len(dataset)
        total_columns = len(dataset.columns)
        column_names = dataset.columns.tolist()

        # Convert dataset into HTML format
        table_content = dataset.to_html(
            classes="table table-striped",
            index=False,
            border=0
        )

        return render_template(
            "result.html",
            stock=stock_name,
            expiration=expiration_date,
            table=table_content,
            rows=total_rows,
            columns=total_columns,
            headers=column_names
        )

    except Exception as error:
        return f"Unable to process the uploaded file: {error}"


if __name__ == "__main__":
    application.run(debug=True)
  

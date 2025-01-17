from flask import Flask, render_template, request
import requests
import pandas as pd

app = Flask(__name__)

PRODUCTION = "http://backend:8000/api/v1/processing/"  # FastAPI URL

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        year = request.form.get("year")

        if not year:
            return render_template("form.html", error="Year is required")
        
        # Make a POST request to FastAPI
        try:
            response = requests.post(f"{PRODUCTION}{year}")
            response.raise_for_status()  # Raise HTTPError for bad responses
            # Convert JSON to pandas DataFrame
            df = pd.DataFrame(response.json())
            # Convert DataFrame to HTML table
            table_html = df.to_html(classes='table table-striped', index=False)
        except requests.exceptions.RequestException as e:
            return render_template("form.html", error=f"Error: {e}")
        
        # Render the response
        return render_template("response.html", table_html=table_html)
    
    # Render the form for GET requests
    return render_template("form.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

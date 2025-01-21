from flask import Flask, render_template, request
import requests
import pandas as pd

app = Flask(__name__)

PRODUCTION = "http://backend:8000/api/v1/"  # FastAPI URL

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        year = request.form.get("year")
        category = request.form.get("category")

        # if not year:
        #     return render_template("form.html", error="Year is required")
        
        # Make a POST request to FastAPI
        try:
            response = requests.post(f"{PRODUCTION}{category}/{year}")
            response.raise_for_status()  # Raise HTTPError for bad responses
            # Convert JSON to pandas DataFrame
            df = pd.DataFrame(response.json())
            # Convert DataFrame to HTML table
            table_html = df.to_html(classes='table table-striped', index=False)
        except requests.exceptions.RequestException as e:
            return render_template("form.html", error=f"Error: {e}")
        
        # Render the response
        return render_template("response.html", table_html=table_html, category=category)
    
    # Render the form for GET requests
    return render_template("form.html")

@app.route("/predict", methods=["GET"])
def predict():
    try:
        # Send a GET request to the prediction API
        response = requests.get(f"{PRODUCTION}predict/commercialization")
        response.raise_for_status()  # Raise HTTPError for bad responses
        
        # Extract JSON data from the response
        json_data = response.json()
        data = json_data.get('data', [])  # Get the 'data' key from the JSON

        # Convert JSON data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Convert DataFrame to an HTML table
        table_html = df.to_html(classes='table table-striped', index=False)

    except requests.exceptions.RequestException as e:
        # Handle request errors
        return render_template("predict.html", error=f"Request Error: {e}")

    except ValueError as e:
        # Handle JSON parsing errors
        return render_template("predict.html", error=f"JSON Error: {e}")

    except Exception as e:
        # Handle unexpected errors
        return render_template("predict.html", error=f"Unexpected Error: {e}")

    # Render the template with the HTML table
    return render_template("predict.html", table_html=table_html)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

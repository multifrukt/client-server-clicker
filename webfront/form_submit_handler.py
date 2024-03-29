from flask import Flask, request, render_template_string
import os
import requests
from datetime import datetime

app = Flask(__name__)

# URL of the external API
ENV_VAR_API_URL = 'API_URL'
api_url = os.environ.get(ENV_VAR_API_URL)  # Read the environment variable once
print(f"Got Environment variable {ENV_VAR_API_URL}: {api_url}")


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@app.route('/form_submit', methods=['POST'])
def form_submit():
    form_data = request.form
    json_data = form_data.to_dict()

    try:
        # Send JSON data to the external API
        response = requests.post(api_url, json=json_data)
        response_data = response.json()

        # Display the API's response
        return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>API Response</title>
            </head>
            <body>
                <p>API Response:</p>
                <h1>{{ message }}</h1>
                <p>
                    <button onclick="window.history.back();">Back to the form</button>
                </p>
            </body>
            </html>
        """, message=response_data.get("message"))

    except requests.exceptions.RequestException as e:
        error_message = f"[{timestamp()}] Connection to apiserver at {api_url} failed: {e}"
        print(error_message)

        # Display the error on the web page
        return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Error</title>
            </head>
            <body>
                <p>Error:</p>
                <p style="color:red;">{{ message }}</p>
                <p>
                    <button onclick="window.history.back();">Back to the form</button>
                </p>
            </body>
            </html>
        """, message=error_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

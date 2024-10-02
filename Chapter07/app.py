from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Get color from environment variable, default to 'white' if not set
    color = os.getenv('COLOR', 'white')

    # Get name from query parameters, default to 'Guest' if not provided
    name = request.args.get('name', 'Guest')

    # Generate HTML response with dynamic color and name
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Welcome</title>
      <style>
        body {{
          background-color: {color};
          text-align: center;
        }}
        h1 {{
          margin-top: 40vh;  /* Center text vertically */
        }}
      </style>
    </head>
    <body>
      <h1>Welcome, {name}!</h1>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

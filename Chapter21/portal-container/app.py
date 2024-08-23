from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Get color and portal details from environment variables
    color = os.getenv('COLOR', 'white')
    portal = os.getenv('PORTAL', 'Main')

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
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}
        h1 {{
          margin-top: 40vh;  /* Center text vertically */
        }}
      </style>
    </head>
    <body>
      <h1>Welcome to {portal} Portal!</h1>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

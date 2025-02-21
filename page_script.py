from flask import Flask, render_template_string
import threading

# Initialize Flask app
app = Flask(__name__)

# Global variable to store user-added text
page_text = "Welcome to the page!"

# HTML Template with a placeholder for the text
template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Text Page</title>
</head>
<body>
    <h1>Page Content</h1>
    <p>{{ content }}</p>
</body>
</html>
'''

# Flask route for homepage
@app.route('/')
def index():
    return render_template_string(template, content=page_text)

# Function to run the Flask server http://0.0.0.0:5000
def run_server():
    app.run(host='0.0.0.0', port=5000)

# Function to handle text input from command line
def add_text():
    global page_text
    while True:
        new_text = input("Enter text to add to the page: ")
        page_text = new_text
        print(f"Updated page content: {page_text}")

if __name__ == '__main__':
    # Run the server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True  # This ensures the server will close when the main program exits
    server_thread.start()

    # Handle command-line interface
    add_text()

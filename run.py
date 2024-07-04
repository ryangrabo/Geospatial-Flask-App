# Import the create_app function from the app package
from app import create_app

# Create the Flask application instance
app = create_app()

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # You can change to any other available port

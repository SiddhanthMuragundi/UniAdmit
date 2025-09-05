from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Temporarily enable debug to see error details
    app.run(debug=True, host='0.0.0.0', port=5000)

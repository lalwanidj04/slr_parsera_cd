import sys
sys.path.append("backend")

from backend.app import app

if __name__ == '__main__':
    app.run(debug=True)

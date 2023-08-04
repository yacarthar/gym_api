"""app
"""

from flask import Flask
from api import blue_print

app = Flask(__name__)

app.register_blueprint(blue_print)

if __name__ == "__main__":
    app.run(debug=True)

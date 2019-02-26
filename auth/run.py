import os
from app import APP
host=os.environ.get("FLASK_HOST", "0.0.0.0")
port=os.environ.get("FLASK_PORT", 5000)
APP.run(host=host, port=port, debug=False, threaded=True)

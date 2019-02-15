import sys
sys.path.append('/var/www/ISTS16-Backend')
from app import APP as application
application.secret_key = "thedoshboi"

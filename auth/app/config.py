"""
Configuration settings.
"""
import os


# MYSQL settings, pulled from the environment, matches up with the mysql docker
# image on dockerhub
mysql_user = os.environ.get("MYSQL_USER", "root")
if mysql_user == "root":
    mysql_pass = os.environ.get("MYSQL_ROOT_PASSWORD", "youwontguess23")
else:
    mysql_pass = os.environ.get("MYSQL_PASSWORD", "youwontguess23")

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    mysql_user,
    mysql_pass,
    os.environ.get("MYSQL_SERVER", "0.0.0.0"),
    os.environ.get("MYSQL_DATABASE", "ists"))

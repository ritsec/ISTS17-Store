"""
    Create our database and fill it with the team
"""
import yaml
from app import DB
from app.models.teams import Team
from app.models.session import Session

DB.create_all()


with open("../users.yml") as fil:
    config = yaml.load(fil)


# ADD WHITE TEAM ACCOUNT
wt = config.get("accounts", {}).get("whiteteam", {})
white_team = Team(pub_key=None, private_key=None, **wt)
white_team_session = Session(uuid=wt.get("uuid", 1337))

DB.session.add(white_team)
DB.session.add(white_team_session)
print("Added whiteteam account: {}".format(wt))


# ADD RED TEAM ACCOUNT
rt = config.get("accounts", {}).get("redteam", {})
new_team = Team(pub_key=None, private_key=None, **rt)
new_session = Session(uuid=rt.get("uuid", 99))

DB.session.add(new_team)
DB.session.add(new_session)
print("Added redteam account: {}".format(rt))


sc = config.get("accounts", {}).get("scoring", {})
# ADD SCORING USER
new_team = Team(pub_key=None, private_key=None, **sc)
new_session = Session(uuid=sc.get("uuid", 47))

DB.session.add(new_team)
DB.session.add(new_session)
print("Added scoring account: {}".format(sc))


# add team accounts
bt = config.get("accounts", {}).get("blueteam", {})
passwords = bt.get("passwords", [])
for team in range(1, len(passwords)+1):
    new_team = Team(uuid=team, username='team{}'.format(team),
                    password=passwords[team-1], balance=bt.get("balance", 0),
                    pub_key=None, 
                    private_key=None)
    new_session = Session(uuid=team)

    DB.session.add(new_team)
    DB.session.add(new_session)
print("Added {} blueteams".format(len(passwords)))
DB.session.commit()

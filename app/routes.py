from app import app
from flask import jsonify, request
from app.models import *
from app.utils import *


@app.route('/list/<int:id>', methods=['GET'])
def watch_list_get():
    """
    Obtain watch list of user with given id.

    Author: Jérémie Dierickx
    """
    pass


@app.route('/list/<int:id>', methods=['POST'])
def watch_list_post():
    """
    Obtain watch list of user with given id.

    Author: Jérémie Dierickx
    """
    pass


@app.route('/shows/<int:id>', methods=['POST'])
def show_create():
    """
    Create a new show.

    Author: Antoine Mouchet
    """
    pass


@app.route('/shows/', methods=['GET'])
def show_all():
    """
    Get every existing show.

    Author: Antoine Mouchet
    """
    pass


@app.route('/shows/<int:id>', methods=['GET'])
def show_get():
    """
    Get information about a specific show.

    Author: Jérémie Dierickx
    """
    pass


@app.route('/recommendations/<int:id>', methods=['GET'])
def recommendations_get():
    """
    Get recommendations for a specific user.

    Author: Antoine Mouchet
    """
    pass


@app.route('/login/', methods=['POST'])
def login_post():
    """
    Connect a user.

    Author: Sémy Drif
    """
    pass


@app.route('/login/', methods=['POST'])
def logout_post():
    """
    Disconnect a user.

    Author: Sémy Drif
    """
    pass


@app.route('/users/', methods=['POST'])
def users_create():
    """
    Create a new user.

    Author: Sémy Drif
    """
    pass


@app.route('/users/', methods=['GET'])
def users_get():
    """
    Get all users.

    Author: Sémy Drif
    """
    pass


@app.route('/session/<tag>', methods=['GET'])
def session_sync(tag):
    """
    Get information about watchparty.

    Author: Vincent Higginson
    """
    watchparty = session.query(WatchParty).filter_by(id=tag).first()

    if watchparty == None:
        return jsonify({
            "msg": "Couldn't find a watch party."
        }), 404
    else:
        state = "play"
        if not watchparty.state:
            state = "pause"
        return jsonify({
            "time": watchparty.time,
            "state": state,
        })


@app.route('/session/<tag>', methods=['PATCH'])
def session_update(tag):
    """
    Update information about a watchparty.

    Author: Vincent Higginson
    """
    watchparty = session.query(WatchParty).filter_by(id=tag).first()

    if watchparty == None:
        return jsonify({
            "msg": "Couldn't find a watch party."
        }), 404
    else:
        data = request.json
        if data["state"] == "pause":
            data["state"] = False
        else:
            data["state"] = True
        watchparty.time = data["time"]
        watchparty.state = data["state"]
        session.commit()
        return jsonify({
            "msg": "ok."
        })


@app.route('/session/', methods=['POST'])
def session_create():
    """
    Create a new watchparty.

    Author: Vincent Higginson
    """
    # Get parameters
    try:
        watch_party_type = request.json["type"]
        given_users = request.json["users"]
    except KeyError as e:
        return jsonify({
            "msg": "KEY=%s manquant. Mauvais JSON." % e
        })
    if watch_party_type == "public":
        watch_party_type = True
    else:
        watch_party_type = False

    # Let's create the watch party
    watch_party = WatchParty(id=get_random_word(), state=False, time=0)
    session.add(watch_party)

    # Let's define parameters
    parameters = WatchPartyParameters(id=watch_party.id, type=watch_party_type)
    session.add(parameters)

    # Create a watch party black list entry
    # For each given users
    for user in given_users:
        entry = WatchPartyBlackList(
            parameters, parameters=parameters.id, user=user)
        session.add(entry)
    session.commit()
    return jsonify({
        "id": watch_party.id,
    })

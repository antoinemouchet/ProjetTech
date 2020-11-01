from app import app
from flask import jsonify


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


@app.route('/session/<id>', methods=['GET'])
def session_sync():
    """
    Get information about watch session.

    Author: Vincent Higginson
    """
    pass


@app.route('/session/<id>', methods=['PATCH'])
def session_update():
    """
    Update information about a session.

    Author: Vincent Higginson
    """
    pass


@app.route('/session/', methods=['POST'])
def session_create():
    """
    Create a new session.

    Author: Vincent Higginson
    """
    pass
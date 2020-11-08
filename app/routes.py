from app import app
from flask import jsonify, redirect, request
from app.models import Show, session
from app.utils import generate_file_path


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


@app.route('/new_show/', methods=['POST'])
def show_create():
    """
    Create a new show.

    Author: Antoine Mouchet
    """
    new_show_data = request.json

    # Store image and video in static/img and static/video respectively
    # Get the file from the request then store it?

    new_show = Show(name=new_show_data["name"], description=new_show_data["desc"], tags=new_show_data["tags"])

    # Get id and name of show just created
    new_show_id = new_show.get_id()
    new_show_name = new_show.get_name()

    # Generate path to files (img + videos to store them) based on show_id
    path_to_show_img = generate_file_path(new_show_id, new_show_name, new_show_data["img"])
    path_to_show_vid = generate_file_path(new_show_id, new_show_name, new_show_data["video"], "video")

    # Check that each path exists (therefore each content exists)
    if path_to_show_img:
        new_show.img_path = path_to_show_img
    if path_to_show_vid:
        new_show.file_path = path_to_show_img

    session.add(new_show)
    session.commit()
    return "sucess"


@app.route('/shows/', methods=['GET'])
def show_all():
    """
    Get every existing show.

    Author: Antoine Mouchet
    """
    shows = session.query(Show).all()
    print(shows)
    return jsonify(shows)


@app.route('/shows/<int:id>', methods=['GET'])
def show_get(show_id):
    """
    Get information about a specific show.

    Parameters
    ----------
    show_id: id of the show of which we want to retrieve the info

    Author: Antoine Mouchet
    """
    show_info = session.query(Show).filter_by(id=show_id).first()

    # Show exists
    if show_info:
        return jsonify(show_info)

    # Reaction when show doesn't exist
    else:
        return redirect("/shows")




@app.route('/recommendations/<int:id>', methods=['GET'])
def recommendations_get():
    """
    Get recommendations for a specific user.

    Author: Jérémie Dierickx
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
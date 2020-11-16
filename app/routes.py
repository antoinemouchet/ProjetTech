from app import app
from flask import jsonify, redirect, request
from app.models import Show, session
import uuid, os

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


@app.route('/shows/', methods=['POST'])
def show_create():
    """
    Create a new show.

    Author: Antoine Mouchet
    """
    new_show_data = request.form
    new_show_file = request.files

    # Store image and video in static/img and static/video respectively
    # Get the file from the request then store it?

    new_show = Show(
        name=new_show_data["name"], desc=new_show_data["desc"],
        tags=new_show_data["tags"])

    # Generate random files names for file of the show
    path_to_show_img = str(uuid.uuid4())
    path_to_show_video = str(uuid.uuid4())

    img_extension = new_show_file["img"].filename.split('.')[1]
    video_extension = new_show_file["video"].filename.split('.')[1]

    # Check that each path exists (therefore each content exists)
    if new_show_file["img"]:
        new_show.img = os.path.join(os.getcwd(), "static", "img", path_to_show_img + "." + img_extension)
        new_show_file["img"].save(os.path.join(os.getcwd(), "static", "img", path_to_show_img + "." +  img_extension))

    if new_show_file["video"]:
        new_show.video = os.path.join(os.getcwd(), "static", "video", path_to_show_video + "." + video_extension)
        new_show_file["video"].save(os.path.join(os.getcwd(), "static", "video", path_to_show_video + "." +  video_extension))

    session.add(new_show)
    session.commit()
    return "success"


@app.route('/shows/', methods=['GET'])
def show_all():
    """
    Get every existing show.

    Author: Antoine Mouchet
    """
    shows = session.query(Show).all()

    data = []
    for show in shows:
        data.append({
            "name": show.name,
            "desc": show.desc,
            "img": show.img,
            "tags": show.tags
        })

    return jsonify(data)


@app.route('/shows/<int:show_id>', methods=['GET'])
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
        return jsonify({
            "name": show_info.name,
            "desc": show_info.desc,
            "img": show_info.img,
            "video": show_info.video,
            "tags": show_info.tags
        })
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

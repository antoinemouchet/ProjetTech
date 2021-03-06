from flask_login import login_user, current_user, login_required, logout_user
from flask import render_template, redirect, request, flash, jsonify
from jinja2 import Template, Environment, PackageLoader, select_autoescape

from sqlalchemy.sql.expression import func
import sqlalchemy.sql

import uuid
import os

from app import app
from app.models import *
from app.forms import *
from app.utils import *

# Prepare stuff for rendering templates
env = Environment(
    # 'app' is the name of the current python module
    # 'templates' is the directory containing templates
    loader=PackageLoader("app", "templates"),
    # automatically select html file (and nothing else)
    autoescape=select_autoescape(["html"])
)


@login_manager.unauthorized_handler
def unauthorized():
    """
    A not connected user tries to use login_required view.
    Redirect him to login page.

    Author: Vincent Higginson
    """
    return redirect('/login/', 302)


def header(page_name):
    """
    Render heading. Load header from file system and render it.

    Author: Vincent Higginson
    """
    header = env.get_template("header.html")

    return header.render(page_name=page_name, current_user=current_user)


def footer():
    """
    Render footer. Load footer from file system and render it.

    Author: Vincent Higginson
    """
    footer = env.get_template("footer.html")

    return footer.render()


@app.route('/list/<int:id>', methods=['GET'])
@login_required
def watch_list_get(id):
    """
    Obtain watch list of user with given id.

    Author: Jérémie Dierickx
    """
    # Get watch list from current user
    watchlist = session.query(WatchList).filter_by(user_id=id).first()

    # User may not have a watch list at the moment
    if not watchlist:
        # The actual user may not be the user who asked for the watch list
        if id == current_user.id:
            watchlist = WatchList(user_id=current_user.id)
            session.add(watchlist)
            session.commit()
        else:
            # Watch list does not exist
            return jsonify({'error': 'watchlist not found.'}, 404)

    # Query all shows linked to this watch list
    shows = session.query(ShowList).filter_by(watchlist_id=watchlist.id).all()

    # Build a data structure with them
    showsList = []
    for show in shows:
        show = session.query(Show).filter_by(id=show.show_id).first()
        showsList.append({'id': show.id, 'name': show.name, 'desc': show.desc,
                          'img': show.img, 'video': show.video, 'tags': show.tags})

    # Return this structure using json
    return jsonify({'data': showsList, 'status' : watchlist.status})


@app.route('/list/<int:id>', methods=['POST'])
@login_required
def watch_list_post(id):
    """
    Modify watch list of user with given id.

    Author: Jérémie Dierickx
    """
    # Get watch list from current user
    watchlist = session.query(WatchList).filter_by(user_id=id).first()

    # Check if watchlist isn't None
    # AND
    # Check if current user is the user who wants to modify the list
    if watchlist and watchlist.user_id == current_user.id:
        # JSON containing all modifications
        # {
        #   delete: [id1, id2, ...],
        #   add: [id1, id2, ...]
        # }
        data = request.json
        # Shows to delete from watchlist
        delete = data['delete']
        # Shows to add to watchlist
        add = data['add']
        # Status of the watchlist
        status = data['status']

        # Delete ShowList elements
        for show_id in delete:
            show = session.query(ShowList).filter_by(
                watchlist_id=watchlist.id, show_id=show_id).first()
            if show:
                session.delete(show)
                session.commit()

        # Create ShowList elements
        for show_id in add:
            show = session.query(Show).filter_by(id=show_id).first()
            if show and not session.query(ShowList).filter_by(watchlist_id=watchlist.id, show_id=show_id).first():
                session.add(
                    ShowList(watchlist_id=watchlist.id, show_id=show_id))
                session.commit()

        # Modify the watchlist status
        if status >= 0 and status < 3:
            watchlist.status = status
            session.add(watchlist)
            session.commit()


    return "success"


@app.route('/list/', methods=['GET'])
@login_required
def watch_list_main_get():
    """
    Render watch list page.

    Author: Jérémie Dierickx
    """
    watchlist = env.get_template('watchlists.html')
    return header("Watch List") + watchlist.render(user_name=current_user.pseudo) + footer()


@app.route('/comparison/', methods=['GET'])
@login_required
def comparison_main_get():
    """
    Render comparison page.

    Author: Jérémie Dierickx
    """
    comparison = env.get_template('compare.html')
    return header("Compare Watch List") + comparison.render(user_id=current_user.id) + footer()


@app.route('/new-show/', methods=['POST'])
@login_required
def show_create():
    """
    Create a new show from form data.

    Author: Antoine Mouchet
    """
    new_show_data = request.form
    new_show_file = request.files

    # Store image and video in static/img and static/video respectively
    # Get the file from the request then store it?
    new_show = Show(
        name=new_show_data["name"],
        desc=new_show_data["desc"],
        tags=new_show_data["tags"]
    )

    # Generate random files names for file of the show
    path_to_show_img = str(uuid.uuid4())
    path_to_show_video = str(uuid.uuid4())

    # Check that each path exists (therefore each content exists)
    if new_show_file["img"]:
        img_extension = new_show_file["img"].filename.split('.')[1]
        new_show.img = os.path.join(
            "static", "img", path_to_show_img + "." + img_extension)
        new_show_file["img"].save(os.path.join(
            "static", "img", path_to_show_img + "." + img_extension))

    if new_show_file["video"]:
        video_extension = new_show_file["video"].filename.split('.')[1]
        new_show.video = os.path.join(
            "static", "video", path_to_show_video + "." + video_extension)
        new_show_file["video"].save(os.path.join(
            "static", "video", path_to_show_video + "." + video_extension))

    session.add(new_show)
    session.commit()

    return redirect("/show-list/", 302)


@app.route('/new-show/', methods=['GET'])
@login_required
def show_form_render():
    """
    Render form to add a show.

    Author: Antoine Mouchet
    """
    newShow = env.get_template('show-form.html')
    return header("Add a show") + newShow.render() + footer()


@app.route('/shows/', methods=['GET'])
@login_required
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
            "tags": show.tags,
            "id": show.id,
        })

    return jsonify(data)


@app.route('/show-list/', methods=["GET"])
@login_required
def display_shows():
    """
    Render all shows page. Shows are fetched by the page itself.

    Author: Antoine Mouchet
    """
    shows = env.get_template('shows.html')
    return header("Shows") + shows.render() + footer()


@app.route('/show/<int:show_id>', methods=['GET'])
@login_required
def show_get(show_id):
    """
    Get information about a specific show.

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
        return redirect("/shows/")


@app.route('/show-detail/<int:show_id>', methods=["GET"])
@login_required
def show_view(show_id):
    """
    Render page information about a specific show.

    Author: Antoine Mouchet
    """
    show = env.get_template('show-detail.html')
    return header("Details") + show.render(show=show_id) + footer()


@app.route('/recommendations/<int:id>', methods=['GET'])
@login_required
def recommendations_get(id):
    """
    Get recommendations for a specific user.

    Author: Jérémie Dierickx
    """
    # Check if the given user id correspond to an existing user
    user = session.query(User).filter_by(id=id).first()

    # Check if watchlist isn't None
    if user and user.id == current_user.get_id():
        tags_frequencies = {}

        # Get watch list of user
        watchlist = session.query(WatchList).filter_by(
            user_id=current_user.get_id()).first()

        # He doesn't have one
        if not watchlist:
            # Return an empty recommendations list
            return {'recommendations': []}

        # Compute statistics based on shows present in watch list
        watchlist_showlists = session.query(ShowList).filter_by(
            watchlist_id=watchlist.id).all()

        # Iterate through all watchlist's showlists
        for showlist in watchlist_showlists:
            # Get show
            show = session.query(Show).filter_by(
                id=showlist.show_id).first()

            # Analyze tags
            if show:
                tag_list = show.tags.split(';')

                # Update tag frequencies
                for tag in tag_list:
                    if tag != "":
                        if tag in tags_frequencies:
                            tags_frequencies[tag] += 1
                        else:
                            tags_frequencies[tag] = 0

        # Get show corresponding to tags frequencies
        if len(tags_frequencies) > 0:
            # Sort by frequencies
            sorted_3_tags = sorted(tags_frequencies.keys(), key=lambda key: tags_frequencies[key])[
                :4]
            recommendationsList = {}
            # Max 10 recommendation for the most common tag.
            for show in session.query(Show).filter(Show.tags.contains(sorted_3_tags[0])).order_by(func.random()).limit(10):
                recommendationsList[show.id] = {
                    'id': show.id,
                    'name': show.name,
                    'desc': show.desc,
                    'img': show.img,
                    'video': show.video,
                    'tags': show.tags
                }
            index = 1
            while index < len(sorted_3_tags):
                # Max 4 for others.
                for show in session.query(Show).filter(Show.tags.contains(sorted_3_tags[index])).order_by(func.random()).limit(4):
                    recommendationsList[show.id] = {
                        'id': show.id,
                        'name': show.name,
                        'desc': show.desc,
                        'img': show.img,
                        'video': show.video,
                        'tags': show.tags
                    }
                index += 1

            return jsonify({'recommendations': recommendationsList})

    return jsonify({'error': 'user not exist'})


@app.route('/recommendations-list/', methods=['GET'])
@login_required
def recommendations_main_get():
    """
    Render recommendations page. Recommendations are fetched by the page itself.

    Author: Jérémie Dierickx
    """
    recommendations = env.get_template('recommendations.html')
    return header("Recommendations") + recommendations.render(user_id=current_user.id) + footer()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    """
    Show connect form and connect a user.

    Author: Sémy Drif
    """
    # Prepare form
    form = LoginForm()

    # POST and user submitted the form
    if form.validate_on_submit():
        user = session.query(User).filter_by(pseudo=form.username.data).first()
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/friends/', 302)

        elif user == None:
            flash('Wrong username', 'danger')
            return redirect('/login/', 302)
        elif not check_password_hash(user.password, form.password.data):
            flash('Wrong password', 'danger')  # error message plus category
            return redirect('/login/', 302)

    # User didn't submit anything
    # So render form
    else:
        return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET'])
@login_required
def logout_post():
    """
    Disconnect a user.

    Author: Sémy Drif
    """
    logout_user()
    return redirect('/', 302)


@app.route('/users/', methods=['POST'])
def users_create():
    """
    Create a new user.

    Author: Sémy Drif
    """
    form = Register()
    # Get user with this pseudo
    user_found = session.query(User).filter_by(
        pseudo=form.username.data).first()
    if form.validate_on_submit():
        # If a user with this pseudo exist
        # We cannot allow the creation
        if user_found:
            flash("This pseudo is already used.", "danger")
            return render_template("register.html", form=form)
        else:
            # Create the user
            new_user = User(pseudo=form.username.data, password=generate_password_hash(form.password.data),
                            enabled=False)
            session.add(new_user)
            session.commit()
            return redirect('/login/', 302)
    # User didn't submit anything
    # Just render form
    else:
        return render_template('register.html', form=form)


@app.route('/register/', methods=['GET'])
def register_form():
    """
    Show register form.
    Author: Sémy Drif
    """
    form = Register()
    return render_template('register.html', form=form)


@app.route('/users/', methods=['GET'])
@login_required
def users_get():
    """
    Get all users.

    Author: Sémy Drif
    """
    users = session.query(User).all()
    data = []
    for u in users:
        data.append({
            "id": u.id,
            "pseudo": u.pseudo,
        })
    return jsonify(data)


@app.route('/friends/<int:tag>', methods=["GET"])
@login_required
def friends_get(tag):
    """
    Get all friends of user

    Author: Vincent Higginson
    """
    friends_by_a = session.query(FriendShip).filter_by(user_a=tag)
    friends_by_b = session.query(FriendShip).filter_by(user_b=tag)

    friends_id = []

    for friend in friends_by_a:
        if friend.user_b not in friends_id:
            friends_id.append({
                "id": friend.user_b,
                "pseudo": session.query(User).filter_by(id=friend.user_b).first().pseudo
            })

    for friend in friends_by_b:
        if friend.user_a not in friends_id:
            friends_id.append({
                "id": friend.user_a,
                "pseudo": session.query(User).filter_by(id=friend.user_a).first().pseudo
            })
    return jsonify({
        "friends": friends_id
    })


@app.route('/friends/<int:tag>', methods=["DELETE"])
@login_required
def friends_delete(tag):
    """
    Delete a specific friends for a user.

    Author: Vincent Higginson
    """
    # Get user to remove
    friend = request.json['friend']
    # Get related friendship
    friends_by_a = session.query(FriendShip).filter_by(
        user_a=tag, user_b=friend).first()
    if friends_by_a != None:
        session.delete(friends_by_a)
    friends_by_b = session.query(FriendShip).filter_by(
        user_a=friend, user_b=tag).first()
    if friends_by_b != None:
        session.delete(friends_by_b)
    session.commit()

    return jsonify({
        "msg": "okay"
    })


@app.route('/friends/<int:tag>', methods=["POST"])
@login_required
def friends_add(tag):
    print("Salut salut")
    """
    Add a new friend to a user.

    Author: Vincent Higginson
    """
    # Get user with this pseudo
    user = session.query(User).filter_by(pseudo=request.json['friend']).first()
    if user == None:
        return jsonify({
            "msg": "Does not exist."
        })
    if user.id == current_user.get_id():
        return jsonify({
            "msg": "You cannot be friend with yourself."
        })
    user_id = user.id
    # Check if a friendship of this type doesn't exist
    f_by_a = session.query(FriendShip).filter_by(
        user_a=tag, user_b=user_id).first()
    f_by_b = session.query(FriendShip).filter_by(
        user_b=tag, user_a=user_id).first()
    if f_by_a == None and f_by_b == None:
        # Create friendship
        friend_ship = FriendShip(user_a=tag, user_b=user_id)
        session.add(friend_ship)
        session.commit()

        return jsonify({
            "msg": "okay"
        })
    else:
        return jsonify({
            "msg": "already friends"
        })


@app.route('/friends/', methods=['GET'])
@login_required
def friends_form():
    friends = env.get_template('friends.html')
    return header("My Friends") + friends.render(user_id=current_user.get_id()) + footer()


@app.route('/session/<tag>', methods=['GET'])
@login_required
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
        state = "played"
        if not watchparty.state:
            state = "paused"
        return jsonify({
            "time": watchparty.time,
            "state": state,
        })


@app.route('/session/<tag>/', methods=['PATCH'])
@login_required
def session_update(tag):
    """
    Update information about a watchparty.

    Author: Vincent Higginson
    """
    # Get current watch party
    watchparty = session.query(WatchParty).filter_by(id=tag).first()

    # Does it exist ?
    if watchparty == None:
        return jsonify({
            "msg": "Couldn't find a watch party."
        }), 404
    else:
        # Update state in database
        data = request.json
        if data["state"] == "paused":
            data["state"] = False
        else:
            data["state"] = True
        watchparty.time = data["time"]
        watchparty.state = data["state"]
        print(data["time"])
        print(data["state"])
        session.commit()
        return jsonify({
            "msg": "ok."
        })


@app.route('/session/', methods=['POST'])
# @login_required
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


@app.route('/session/<int:media>', methods=['POST'])
@login_required
def session_create_from_file(media):
    """
    Create a watch party with default parameters and given media.

    Author: Vincent Higginson
    """
    # Get path to media
    media = session.query(Show).filter_by(id=media).first()
    if not media:
        pass
    media = media.video

    # Set default parameters
    # PUBLIC watch party
    watch_party_type = True

    # Let's create the watch party
    watch_party = WatchParty(id=get_random_word(),
                             state=False, time=0, media=media)
    session.add(watch_party)

    # Let's define parameters
    parameters = WatchPartyParameters(id=watch_party.id, type=watch_party_type)
    session.add(parameters)

    session.commit()

    # And directly redirect to watch party
    return jsonify({'id': watch_party.id})


@app.route('/watch/<tag>', methods=['GET'])
@login_required
def watch(tag):
    """
    Render watch page.

    Author: Vincent Higginson
    """
    # Check permission and existence of watch party
    watch_party = session.query(WatchParty).filter_by(id=tag).first()
    if not watch_party:
        pass
    media = watch_party.media
    form = env.get_template('watch.html')
    return header("Watch Party") + form.render(watch_party_tag=tag, media='/'+media) + footer()


@app.route('/watch-party/', methods=['GET'])
@login_required
def watch_party_form():
    """
    Render watch form.

    Author: Vincent Higginson
    """
    form = env.get_template('watch-party.html')
    return header("Find a Watch Party") + form.render() + footer()


@app.route('/', methods=['GET'])
def front_page():
    """
    Render front page.

    Author: Antoine Mouchet
    """
    page = env.get_template('front-page.html')
    return page.render() + footer()

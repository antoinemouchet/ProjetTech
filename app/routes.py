from flask_login import login_user, current_user, login_required, logout_user
from flask import render_template, redirect, url_for, request, flash, jsonify, request
from jinja2 import Template, Environment, PackageLoader, select_autoescape
from flask import jsonify, redirect, request

from sqlalchemy.sql.expression import func

import uuid, os

from app import app
from app.models import *
from app.forms import *
from app.utils import *

env = Environment(
    loader=PackageLoader("app", "templates"),
    autoescape=select_autoescape(["html"])
)


@login_manager.unauthorized_handler
def unauthorized():
    """
    A not connected user tries to use login_required view.
    """
    return redirect('/login/', 302)


def header(page_name):
    """
    Render heading.
    """
    header = env.get_template("header.html")

    return header.render(page_name=page_name, current_user=current_user)


def footer():
    """
    Render footer.
    """
    footer = env.get_template("footer.html")

    return footer.render()

@app.route('/list/<int:id>', methods=['GET'])
def watch_list_get(id):
    """
    Obtain watch list of user with user id.

    Author: Jérémie Dierickx
    """
    watchlist = session.query(WatchList).filter_by(id=id).first()
    if not watchlist or watchlist.user_id != current_user.id:
        return redirect('/shows')  # no access
    else:
        shows = session.query(ShowList).filter_by(watchlist_id=id).all()
        # [{id:,nom:,description:,img:,file:,tags:,}, ...]
        return jsonify(shows)


@app.route('/list/<int:id>', methods=['POST'])
def watch_list_post(id):
    """
    Modify watch list of user with user id.

    Author: Jérémie Dierickx
    """
    watchlist = session.query(WatchList).filter_by(id=id).first()
    if not watchlist or watchlist.user_id != current_user.id:
        return redirect('/shows')  # no access
    else:
        data = request.json  # {delete:[id1,id2,...], add:[id1,id2,...]}
        delete = data['delete']  # shows to delete from watchlist
        add = data['add']  # shows to add to watchlist
        if delete:
            for show_id in delete:
                show = session.query(ShowList).filter_by(
                    watchlist_id=id, show_id=show_id).first()
                if show:
                    session.delete(show)
        if add:
            for show_id in add:
                show = session.query(Show).filter_by(show_id=show_id).exist()
                if show:
                    session.add(ShowList(watchlist_id=id, show_id=show_id))
        session.commit()

        return redirect('/list/%d' % id)


@app.route('/new-show/', methods=['GET', 'POST'])
def show_create():
    """
    Create a new show.

    Author: Antoine Mouchet
    """
    if request.method == "POST":
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

        # Check that each path exists (therefore each content exists)
        if new_show_file["img"]:
            img_extension = new_show_file["img"].filename.split('.')[1]
            new_show.img = os.path.join( "static", "img", path_to_show_img + "." + img_extension)
            new_show_file["img"].save(os.path.join("static", "img", path_to_show_img + "." +  img_extension))

        if new_show_file["video"]:
            video_extension = new_show_file["video"].filename.split('.')[1]
            new_show.video = os.path.join("static", "video", path_to_show_video + "." + video_extension)
            new_show_file["video"].save(os.path.join("static", "video", path_to_show_video + "." +  video_extension))

        session.add(new_show)
        session.commit()

        return redirect("/show-list/")

    else:
        newShow = env.get_template('show-form.html')
        return header("Add a show") + newShow.render() + footer()


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
            "tags": show.tags,
            "id": show.id,
        })

    return jsonify(data)

@app.route('/show-list/', methods=["GET"])
def display_shows():
    shows = env.get_template('shows.html')
    return header("Shows") + shows.render() + footer()

@app.route('/show/<int:show_id>', methods=['GET'])
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
def show_view(show_id):
    show = env.get_template('show-detail.html')
    return header("Details") + show.render(show=show_id) + footer()

@app.route('/recommendations/<int:id>', methods=['GET'])
def recommendations_get(id):
    """
    Get recommendations for a specific user.

    Author: Jérémie Dierickx
    """
    user = User.query.filter_by(id=id).first()
    if user:
        tags_frequencies = {}
        user_watchlists = WatchList.query.filter_by(user_id=id).all()

        for watchlist in user_watchlists:  # iterate through all user's watchlists
            watchlist_showlists = ShowList.query.filter_by(
                watchlist_id=watchlist.id).all()

            for showlist in watchlist_showlists:  # iterate through all watchlist's showlists
                show = Show.query.filter_by(
                    id=showlist.show_id).first()  # get show
                if show:
                    tag_list = show.tags.split(';')

                    for tag in tag_list:
                        if tag in tags_frequencies:
                            tags_frequencies[tag] += 1
                        else:
                            tags_frequencies[tag] = 0

        # do something with frequencies
        if len(tags_frequencies) > 0:
            sorted_3_tags = sorted(tags_frequencies.keys(), key=lambda key: tags_frequencies[key])[
                :4]  # maybe needs optimization ?
            recommendations = Show.query.filter(Show.tags.ilike(sorted_3_tags[0])).order_by(
                func.random()).limit(10)  # max 10 recommendation for the most common tag.
            index = 1
            while index < len(sorted_3_tags):
                recommendations = recommendations.union(Show.query.filter(Show.tags.ilike(
                    sorted_3_tags[index])).order_by(func.random()).limit(4))  # max 4 for others.
                index += 1
            return jsonify(recommendations)

    return redirect('/shows')  # user not exist


@app.route('/login/', methods=['POST', 'GET'])
def login():
    """
    Connect a user.

    Author: Sémy Drif
    """
    print("Salut")
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(pseudo=form.username.data).first()
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/friends/', 302)

        elif user == None:
            flash('Wrong username', 'danger')
            return redirect(url_for('login_post'))
        elif not check_password_hash(user.password, form.password.data):
            flash('Wrong password', 'danger')  # error message plus category
            return redirect(url_for('login_post'))

    else:
        return render_template('login.html', form=form)


@app.route('/login/', methods=['POST'])
@login_required
def logout_post():
    """
    Disconnect a user.

    Author: Sémy Drif
    """
    logout_user()
    return redirect(url_for('login_post'))


@app.route('/users/', methods=['POST'])
def users_create():
    """
    Create a new user.

    Author: Sémy Drif
    """
    form = Register()
    user_found = session.query(User).filter_by(
        pseudo=form.username.data).first()
    # Permert d'avoir tout les utilisateurs de la base de donée
    if form.validate_on_submit():
        if user_found:
            flash("there is already an user called like that", "danger")
            return render_template("register.html", form=form)
        else:

            new_user = User(pseudo=form.username.data, password=generate_password_hash(form.password.data),
                            enabled=False)
            session.add(new_user)
            session.commit()
            return redirect(url_for('login_post'))

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
def users_get():
    """
    Get all users.

    Author: Sémy Drif
    """
    form = Register()
    users = session.query(User).all()
    data = []
    for u in users:
        data.append({
            "id": u.id,
            "pseudo": u.pseudo,
        })
    return jsonify(data)


@app.route('/friends/<int:tag>', methods=["GET"])
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
def friends_add(tag):
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


@ app.route('/friends/', methods=['GET'])
@ login_required
def friends_form():
    friends = env.get_template('friends.html')
    return header("My Friends") + friends.render(user_id=current_user.get_id()) + footer()


@ app.route('/session/<tag>', methods=['GET'])
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


@ app.route('/session/<tag>/', methods=['PATCH'])
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


@ app.route('/session/', methods=['POST'])
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


@app.route('/watch/<tag>', methods=['GET'])
def watch(tag):
    form = env.get_template('watch.html')
    return header("Watch Party") + form.render(watch_party_tag=tag) + footer()


@app.route('/watch-party/', methods=['GET'])
def watch_party_form():
    form = env.get_template('watch-party.html')
    return header("Find a Watch Party") + form.render() + footer()

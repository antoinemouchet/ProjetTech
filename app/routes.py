# -*- coding: cp1252 -*-
from app import app
from flask import jsonify, redirect
from models import ShowList , WatchList, Show


@app.route('/list/<int:id>', methods=['GET'])
def watch_list_get(id):
    """
    Obtain watch list of user with given id.

    Author: Jérémie Dierickx
    """
    watchlist = WatchList.query.filter_by(id=id).first()
    if not watchlist or watchlist.user_id != current_user.id:
        pass #no access
    else:
        shows = ShowList.query.filter_by(watchlist_id=id).all()
        return jsonify(shows) # [{id:,nom:,description:,img:,file:,tags:,}, ...]
    


@app.route('/list/<int:id>', methods=['POST'])
def watch_list_post(id):
    """
    Modify watch list of user with given id.

    Author: Jérémie Dierickx
    """
    watchlist = WatchList.query.filter_by(id=id).first()
    if not watchlist or watchlist.user_id != current_user.id:
        pass #no access
    else:
        data = request.json # {delete:[id1,id2,...], add:[id1,id2,...]}
        delete = data['delete'] # shows to delete from watchlist
        add = data['add'] # shows to add to watchlist
        if delete:
            for show_id in delete:
                show = ShowList.query.filter_by(watchlist_id=id, show_id=show_id).first()
                if show:
                    db.session.delete(show)
        if add:
            for show_id in add:
                show = Show.query.filter_by(show_id=show_id).exist()
                if show:
                    db.session.add(ShowList(watchlist_id=id, show_id=show_id))
        db.session.commit()
        
        return redirect('/list/%d' % id) 


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
def show_get(id):
    """
    Get information about a specific show.

    Author: Antoine Mouchet
    """
    pass


@app.route('/recommendations/<int:id>', methods=['GET'])
def recommendations_get(id):
    """
    Get recommendations for a specific user.

    Author: Jérémie Dierickx
    """
    user = Utilisateur.query.filter_by(id=id).first()
    if user:
        tags_frequencies = {}
        user_watchlists = WatchList.query.filter_by(user_id=id).all()
       
        for watchlist in user_watchlists:  #iterate through all user's watchlists
            watchlist_showlists = ShowList.query.filter_by(watchlist_id=watchlist.id).all()
           
            for showlist in watchlist_showlists: #iterate through all watchlist's showlists
                show = Show.query.filter_by(id=showlist.show_id).first() #get show
                tag_list = show.tags.split(';')
               
                for tag in tag_list:
                    if tag in tags_frequencies:
                        tags_frequencies[tag] += 1
                    else:
                        tags_frequencies[tag] = 0
        
        #do something with frequencies
    else:
        pass #user not exist



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
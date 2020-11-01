from app import app
from app import routes
from app import models

# Todo should be an array and in db lol
# watch_session = {
#     "time": 0,
#     "state": "paused"
# }


# @app.route('/sync/', methods=['POST'])
# def video_sync_post():
#     """
#     Update watch session data.
#     """
#     new_watch_session = request.json
#     # Should do some integrity check
#     watch_session["time"] = new_watch_session["time"]
#     watch_session["state"] = new_watch_session["state"]
#     print(watch_session)
#     return "ok"

# @app.route('/users/', methods=['GET'])
# def users_get():
#     return jsonify([
#         {
#             "name": "Antoine",
#         },
#         {
#             "name": "Sémy",
#         },
#         {
#             "name": "Jérémy",
#         }
#     ])


# @app.route('/sync/', methods=['GET'])
# def video_sync_get():
#     """
#     Fetch watch session data.
#     """
#     return jsonify(watch_session)

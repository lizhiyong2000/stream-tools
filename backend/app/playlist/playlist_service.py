import traceback
from datetime import datetime

import bson
from bson import ObjectId
from flask import Blueprint, request, json, jsonify
from flask_login import login_required, current_user

from common import todict
from playlist.playlist import Playlist
from result import Result

playlist_blueprint = Blueprint('playlist', __name__)


@playlist_blueprint.route('/', methods=['GET'])
# @login_required
def my_playlist():

    uid = 1

    playlists = Playlist.objects(uid=uid)

    return Result.gen_success(playlists)


@playlist_blueprint.route('/custom', methods=['GET'])
def custom_jsonencoder():
    now = datetime.now()
    return jsonify({'now': now})


@playlist_blueprint.route('/', methods=['POST'])
def create_playlist():

    uid = current_user.get_id()
    if not request.json \
            or not 'name' in request.json :
        return Result.gen_fail(None, 'Request not Json or miss name')
    elif Playlist.objects(uid=uid, name=request.json['name']).first():

        return Result.gen_fail(None, 'Name is already existed.')
    else:
        playlist = Playlist(
            uid=uid,
            name=request.json['name'],
            create_time=datetime.now()
        )
        try:
            playlist.save()
        except Exception as ex:
            traceback.print_exc()
            return Result.gen_fail(None, 'Create playlist error.')

    return Result.gen_success(playlist, 'Create playlist success.')


@playlist_blueprint.route('/<playlist_id>', methods=['GET'])
def get_playlist_item(playlist_id):

    # playlist = Playlist.objects(uid=uid, id=request.json['item']).first()

    playlist = Playlist.objects.get(id=bson.objectid.ObjectId(playlist_id))

    return Result.gen_success(playlist, 'get playlist success.')


@playlist_blueprint.route('/<playlist_id>/item', methods=['PUT'])
def toggle_playlist_item(playlist_id):
    uid = 1
    if not request.json \
            or not 'item' in request.json  or not 'checked' in request.json:
        return Result.gen_fail(None, 'Request not Json or invalid')

    # playlist = Playlist.objects(uid=uid, id=request.json['item']).first()

    playlist = Playlist.objects.get(id=bson.objectid.ObjectId(playlist_id))

    item = request.json['item']

    checked = request.json['checked']

    if checked:
        playlist.items.append(bson.objectid.ObjectId(item))
    else:

        if bson.objectid.ObjectId(item) in playlist.items:
            playlist.items.remove(bson.objectid.ObjectId(item))

    playlist.save()

    return Result.gen_success(playlist, 'toggle_playlist_item success.')
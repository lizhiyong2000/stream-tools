import { combineReducers } from 'redux'
import { connectRouter } from 'connected-react-router'

import playitems from './playitems'
import channels from './channels'
import channel from './channel'
import users from  './user'
import playlists from './playlists'

export default (history) => combineReducers({
    router: connectRouter(history),
    playitems,
    channels,
    channel,
    users,
    playlists,
})
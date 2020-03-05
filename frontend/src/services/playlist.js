
import {client} from './common'


export const playlistService = {
    fetchPlaylists,
    createPlaylist,
    editPlaylist,
    deletePlaylist,
    togglePlaylistItem,

};



function fetchPlaylists() {

    return client.get('/playlists/');
}


function createPlaylist(params) {
    return client.post('/playlists/', params);
}

function editPlaylist(id, params) {
    return client.put(`/playlists/${id}`, params);
}


function deletePlaylist(id, params) {
    return client.delete(`/playlists/${id}`);
}


function togglePlaylistItem(id, item, checked) {

    const params = {
        item,
        checked,
    }
    return client.put(`/playlists/${id}/item`, params);
}

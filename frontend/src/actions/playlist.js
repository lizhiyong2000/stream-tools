import {playlistService} from "../services";
import {playlistConstants} from "../constants";

export const playlistActions = {
    fetchPlaylists,
    createPlaylist,
    editPlaylist,
    deletePlaylist,
    togglePlaylistItem,
};


function fetchPlaylists() {
    return dispatch => {

        dispatch(request());

        playlistService
        .fetchPlaylists()
        .then(resp => {
            dispatch(success(resp.data));
        })
        .catch(err => {
            dispatch(failure(err.message));
        });
    };


    function request() {
        return {
            type: playlistConstants.FETCH_PLAYLISTS_REQUEST,
        };
    }
    function success(result) {

        if(result.success)
        {
             return {
                type: playlistConstants.FETCH_PLAYLISTS_SUCCESS,
                payload: {
                    playlists:result.data
                },
             };
        }
  
        return {
            type: playlistConstants.FETCH_PLAYLISTS_FAILURE,
            payload: {
                error:result.message,
            },
        };

       
    }
    function failure(error) {
        return {
            type: playlistConstants.FETCH_PLAYLISTS_FAILURE,
            payload: {
                error,
            },
        };
    }


}


function createPlaylist({title, description, status = 'Unstarted'}) {
    return dispatch => {

        dispatch(request());

        playlistService.createPlaylist({
            title,
            description,
            status
        }).then(resp => {
            dispatch(success(resp.data));
        });
    };



    function request() {
        return {
            type: 'CREATE_PLAYLIST_REQUEST',
        };
    }
    function success(Playlist) {
        return {
            type: 'CREATE_PLAYLIST_SUCCESS',
            payload: {
                Playlist,
            },
        };
    }
    function failure(error) {
        return {
            type: 'FETCH_PLAYLISTS_FAILURE',
            payload: {
                error,
            },
        };
    }
}


function editPlaylist(id, params = {}) {

    return (dispatch, getState) => {

        dispatch(request());

        const Playlist = getPlaylistById(getState().Playlists.Playlists, id);
        const updatedPlaylist = Object.assign({}, Playlist, params);
        playlistService.editPlaylist(id, updatedPlaylist).then(resp => {
            dispatch(success(resp.data));
        });

    };


    function request() {
        return {
            type: 'EDIT_PLAYLIST_REQUEST',
        };
    }
    function success(result) {
        return {
            type: 'EDIT_PLAYLIST_SUCCESS',
            payload: {
                result,
            },
        };
    }
    function failure(error) {
        return {
            type: 'EDIT_PLAYLIST_FAILURE',
            payload: {
                error,
            },
        };
    }
}


function deletePlaylist(id) {

    return (dispatch) => {

        dispatch(request());

        playlistService.deletePlaylist(id).then(resp => {
            dispatch(success(resp.data));
        });

    };


    function request() {
        return {
            type: 'DELETE_PLAYLIST_REQUEST',
        };
    }
    function success(result) {
        return {
            type: 'DELETE_PLAYLIST_SUCCESS',
            payload: {
                result,
            },
        };
    }
    function failure(error) {
        return {
            type: 'DELETE_PLAYLIST_FAILURE',
            payload: {
                error,
            },
        };
    }
}


function togglePlaylistItem(id, itemId, checked) {

    return (dispatch) => {

        dispatch(request());

        playlistService.togglePlaylistItem(id, itemId, checked)
        .then(resp => {
            dispatch(success(resp.data));
        });

    };


    function request() {
        return {
            type: 'TOGGLE_PLAYLIST_REQUEST',
        };
    }
    function success(result) {
        return {
            type: 'TOGGLE_PLAYLIST_SUCCESS',
        };
    }
    function failure(error) {
        return {
            type: 'TOGGLE_PLAYLIST_FAILURE',
            payload: {
                error,
            },
        };
    }
}



function getPlaylistById(Playlists, id) {
    return Playlists.find(Playlist => Playlist.id === id);
}
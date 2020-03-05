import {playlistConstants} from "../constants";

const initialState = {
    playlists: [],
    isLoading: false,
    error: null,
};

export default function playlists(state = initialState, action) {

    switch (action.type) {
    case playlistConstants.FETCH_PLAYLISTS_REQUEST: {
        return {
            ...state,
            isLoading: true,
        };
    }
    case playlistConstants.FETCH_PLAYLISTS_SUCCESS: {

        return {
            ...state,
            playlists: action.payload.playlists,
            isLoading: false,
        };
    }
    case playlistConstants.FETCH_PLAYLISTS_FAILURE: {
        return {
            ...state,
            isLoading: false,
            error: action.payload.error,
        };
    }
    case playlistConstants.CREATE_PLAYLIST_SUCCESS: {
        return {
            ...state,
            playlists: state.playlists.concat(action.payload.playlist),
        };
    }
    case playlistConstants.EDIT_PLAYLIST_SUCCESS: {
        const {payload} = action;
        const nextPlayItems = state.playlists.map(playlist => {
            if (playlist.id === payload.playlist.id) {
                return payload.playlist;
            }

            return playlist;
        });
        return {
            ...state,
            playlists: nextPlayItems,
        };
    }
    default: {
        return state;
    }
    }
}

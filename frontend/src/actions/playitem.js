import {playitemService} from "../services";
import {playitemConstants} from "../constants";

export const playitemActions = {
    fetchPlayItems,

    createPlayItem,

    editPlayItem
};


function fetchPlayItems(filters) {
    return dispatch => {
        dispatch(request());

        playitemService
        .fetchPlayItems(filters)
        .then(resp => {
            dispatch(success(resp.data));
        })
        .catch(err => {
            dispatch(failure(err.message));
        });
    };


    function request() {
        return {
            type: playitemConstants.FETCH_PLAYITEMS_REQUEST,
        };
    }
    function success(result) {
        return {
            type: playitemConstants.FETCH_PLAYITEMS_SUCCESS,
            payload: {
                playitems:result.data,
                pagination:result.pagination
            },
        };
    }
    function failure(error) {
        return {
            type: playitemConstants.FETCH_PLAYITEMS_FAILURE,
            payload: {
                error,
            },
        };
    }


}


function createPlayItem({title, description, status = 'Unstarted'}) {
    return dispatch => {

        dispatch(request());

        playitemService.createPlayItem({
            title,
            description,
            status
        }).then(resp => {
            dispatch(success(resp.data));
        });
    };



    function request() {
        return {
            type: 'CREATE_PLAYITEM_REQUEST',
        };
    }
    function success(PlayItem) {
        return {
            type: 'CREATE_PLAYITEM_SUCCESS',
            payload: {
                PlayItem,
            },
        };
    }
    function failure(error) {
        return {
            type: 'FETCH_PLAYITEMS_FAILURE',
            payload: {
                error,
            },
        };
    }
}


function editPlayItem(id, params = {}) {

    return (dispatch, getState) => {

        dispatch(request());

        const PlayItem = getPlayItemById(getState().PlayItems.PlayItems, id);
        const updatedPlayItem = Object.assign({}, PlayItem, params);
        playitemService.editPlayItem(id, updatedPlayItem).then(resp => {
            dispatch(success(resp.data));
        });

    };


    function request() {
        return {
            type: 'EDIT_PLAYITEM_REQUEST',
        };
    }
    function success(result) {
        return {
            type: 'EDIT_PLAYITEM_SUCCESS',
            payload: {
                result,
            },
        };
    }
    function failure(error) {
        return {
            type: 'EDIT_PLAYITEM_FAILURE',
            payload: {
                error,
            },
        };
    }
}

function getPlayItemById(PlayItems, id) {
    return PlayItems.find(PlayItem => PlayItem.id === id);
}
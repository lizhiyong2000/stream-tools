import {channelsService} from "../services";
import {channelsConstants} from "../constants";


export const channelsActions = {
    fetchChannels
};

export function fetchChannels(filters) {
    return dispatch => {
        dispatch(request());

        channelsService
            .fetchChannels(filters)
            .then(resp => {
                dispatch(success(resp.data));
            })
            .catch(err => {
                dispatch(failure(err.message));
            });
    };


    function request() {
        return {
            type: channelsConstants.FETCH_CHANNELS_REQUEST,
        };
    }
    function success(result) {
        return {
            type: channelsConstants.FETCH_CHANNELS_SUCCESS,
            payload: {
                channels: result.data,
                pagination: result.pagination
            },
        };
    }
    function failure(error) {
        return {
            type: channelsConstants.FETCH_CHANNELS_FAILURE,
            payload: {
                error,
            },
        };
    }
}

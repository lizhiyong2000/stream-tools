import {channelsConstants} from "../constants";

const initialState = {
    pagination:{
        total_count:-1,
        current_page:1,
        page_size:30

    },
    channels: [],
    isLoading: false,
    error: null,
};

export default function channels(state = initialState, action) {
    switch (action.type) {
    case channelsConstants.FETCH_CHANNELS_REQUEST: {
        return {
            ...state,
            isLoading: true,
        };
    }
    case channelsConstants.FETCH_CHANNELS_SUCCESS: {


        var items = action.payload.channels;

        return {
            ...state,
            channels: action.payload.channels,
            pagination: action.payload.pagination,
            isLoading: false,
        };
    }
    case channelsConstants.FETCH_CHANNELS_FAILURE: {
        return {
            ...state,
            isLoading: false,
            error: action.payload.error,
        };
    }
    case channelsConstants.CREATE_CHANNEL_SUCCESS: {
        return {
            ...state,
            channels: state.channels.concat(action.payload.channel),
        };
    }
    case channelsConstants.EDIT_CHANNEL_SUCCESS: {
        const {payload} = action;
        const nextChannels = state.channels.map(channel => {
            if (channel._id === payload.channel._id) {
                return payload.channel;
            }

            return channel;
        });
        return {
            ...state,
            channels: nextChannels,
        };
    }
    default: {
        return state;
    }
    }
}

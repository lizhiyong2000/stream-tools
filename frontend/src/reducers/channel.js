import { playitemConstants } from "../constants";

const initialState = {
    channel: null,
    playitems: [],
    isLoading: false,
    error: null,
};

export default function channel(state = initialState, action) {
    switch (action.type) {
    case playitemConstants.FETCH_PLAYITEMS_REQUEST: {
        return {
            ...state,
            isLoading: true,
        };
    }
    case playitemConstants.FETCH_PLAYITEMS_SUCCESS: {


        var items = action.payload.playitems;

        var i;
        for (i in items) {
            items[i].status = "IN_CHANNEL";
        }

        return {
            ...state,
            playitems: action.payload.playitems,
            isLoading: false,
        };
    }
    case playitemConstants.FETCH_PLAYITEMS_FAILURE: {
        return {
            ...state,
            isLoading: false,
            error: action.payload.error,
        };
    }
    case playitemConstants.CREATE_PLAYITEM_SUCCESS: {
        return {
            ...state,
            playitems: state.playitems.concat(action.payload.playitem),
        };
    }
    case playitemConstants.EDIT_PLAYITEM_SUCCESS: {
        const {payload} = action;
        const nextPlayItems = state.playitems.map(playitem => {
            if (playitem.id === payload.playitem.id) {
                return payload.playitem;
            }

            return playitem;
        });
        return {
            ...state,
            playitems: nextPlayItems,
        };
    }
    default: {
        return state;
    }
    }
}


import {client} from './common'

export const channelsService = {
    fetchChannels,

};


function fetchChannels(filters) {

    var params = {};

    if (filters)
    {
        params.keyword = filters.keyword;
        params.type  =filters.type;

        params.pageSize = filters.pageSize;

        params.pageNum = filters.pageNum;
    }

    console.log(params)
    return client.get('/channels', {params});

}
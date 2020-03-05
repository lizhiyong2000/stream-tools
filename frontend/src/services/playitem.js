
import {client} from './common'


export const playitemService = {
    fetchPlayItems,
    createPlayItem,
    editPlayItem,

};



function fetchPlayItems(filters) {

    var params = {};

    if (filters)
    {
        params.keyword = filters.keyword;

        params.pageSize = filters.pageSize;

        params.pageNum = filters.pageNum;
    }

    return client.get('/playitems', {params});
}


function createPlayItem(params) {
    return client.post('/playitems', params);
}

function editPlayItem(id, params) {
    return client.put(`/playitems/${id}`, params);
}

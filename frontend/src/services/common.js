import axios from 'axios';
import https from 'https';

//const API_BASE_URL = 'http://freeiptv.cn/backend';
const API_BASE_URL = 'http://localhost:5000';

const agent = new https.Agent({
    rejectUnauthorized: false
});

export const client = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"

    },
    httpsAgent: agent
});

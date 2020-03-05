
import {client} from './common'


export const userService = {
    login,
    logout,
    register,
    update,
};

function login(username, password) {

    var params = {
        name:username,
        password:password
    };

    console.log(params)
    return client.post('/users/login', params)
    .then(resp => {
        var result = resp.data

        if(result.success){
            return result.data;
        }

        else{
            return Promise.reject(result.message);
        }
    })
    .catch(err => {
        return Promise.reject(err);
    });



}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}



function register(user) {
    var params = {
        name:user.username,
        password:user.password,
        email:user.email
    };

    console.log(params)
    return client.post('/users/register', params)
    .then(resp => {
        var result = resp.data

        if(result.success){
            return result.data;
        }

        else{
            return Promise.reject(result.message);
        }
    })
    .catch(err => {
        return Promise.reject(err);
    });
}

function update(user) {
    var params = {
        name:user.username,
        password:user.password
    };

    console.log(params)
    return client.post('/users/login', params);
}


//function handleResponse(response) {
//    return response.text().then(text => {
//        const data = text && JSON.parse(text);
//        if (!response.ok) {
//            if (response.status !== 401) {
//            }
//            else {
//                // auto logout if 401 response returned from api
//                logout();
//                location.reload(true);
//            }
//
//            const error = (data && data.message) || response.statusText;
//            return Promise.reject(error);
//        }
//
//        return data;
//    });
//}
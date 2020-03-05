// import serviceWorker from './serviceWorker';
// import * as serviceWorker from './serviceWorker';

import React from 'react';
import ReactDOM from 'react-dom';


import { Provider } from 'react-redux'
import { Route, Switch } from 'react-router' // react-router v4/v5
import { ConnectedRouter } from 'connected-react-router'
import configureStore, { history } from './configureStore'

// import App from './App';
import Home from './views/home';

import Channels from './views/channels';

import Contact from './views/contact';
import Legal from './views/legal';
import About from './views/about';
import ChannelPage from './views/channel';

import Login from './views/login';
import Register from './views/register';
const store = configureStore()

ReactDOM.render(
    <Provider store={ store }>
        <ConnectedRouter history={ history }>
            <Switch>
                    <Route exact path="/" component={ Home } />
                    <Route exact path='/channels' component={ Channels } />
                    <Route exact path='/contact' component={ Contact } />
                    <Route exact path='/about' component={ About } />
                    <Route exact path='/legal' component={ Legal } />

                    <Route exact path='/login' component={ Login } />

                    <Route exact path='/register' component={ Register } />

                    <Route path='/channels/:channelId' component={ ChannelPage } />
            </Switch>
        </ConnectedRouter>
    </Provider>,
    document.getElementById('root')
)


// if (module.hot) {
//   module.hot.accept('./App', () => {
//     const NextApp = require('./App').default;
//     ReactDOM.render(
//       <Provider store={store}><NextApp /></Provider>,
//       document.getElementById('root')
//     );
//   });

//   module.hot.accept('./reducers', () => {
//     const nextRootReducer = require('./reducers').default;
//     store.replaceReducer(nextRootReducer);
//   });
// }

// serviceWorker.unregister();





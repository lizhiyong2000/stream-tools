import React from 'react';
import Channel from './Channel';

const ChannelList = props => {
    return (

            <ul>
            { props.channels.map(channel => (
                 <li>
                  <Channel key={ channel._id } channel={ channel } />
                 </li>
              )) }
            </ul>

        );
};

export default ChannelList;

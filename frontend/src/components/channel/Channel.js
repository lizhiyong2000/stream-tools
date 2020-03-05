import React from 'react';

import {Link} from 'react-router-dom'


const Channel = props => {

    const thumb_path =  '/images/channels/' + props.channel.thumb

    return (



        <div className="channel-item">
            <Link to={{pathname: "/channels/" + props.channel._id , state:{channel:props.channel} }} className="image"
               target="_self"
               title= { props.channel.name } >

                <img src="/images/loading.gif" data-echo={ thumb_path } />

            </Link>

            <p className="title">
                { props.channel.name }
            </p>
        </div>


        );


};

export default Channel;

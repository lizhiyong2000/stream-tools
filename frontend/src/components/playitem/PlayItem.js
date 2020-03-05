import React from 'react';
import { Link } from 'react-router-dom'

import { PLAYITEM_STATUSES } from '../../constants';

import PlaylistDropdown from './PlaylistDropdown'

import "../../stylesheets/PlayItem.css"


const PlayItem = props => {


    
    const thumb_path = '/images/thumbs/' + props.playitem.thumb


    return (
        <div className="playitem">
            <div className="playitem-header">
                <div>
                    { props.playitem.name }
                </div>
                <div className="position-button">


                    <PlaylistDropdown playlists={ props.playlists } playitem= {props.playitem} ></PlaylistDropdown>
                </div>


                 
            </div>
            <div className="playitem-body">
                { /*<Link to={ { pathname: "/player", state: { url: props.playitem.url } } }>*/ }
                { props.playitem.url }
                { /*</Link>*/ }
            </div>
            <img src="/images/loading.gif" data-echo={ thumb_path } />
            { props.playitem.thumb && <div>
                                          <div>
                                              { props.playitem.thumb_resolution }
                                          </div>
                                          <div>
                                              { props.playitem.thumb_time}
                                          </div>
                                      </div> }
            <hr />
        </div>
        );

    function onStatusChange(e) {
        props.onStatusChange(props.playitem.id, e.target.value);
    }



};

export default PlayItem;


import React, { Component } from "react";
import ReactPlayer from 'react-player'

import Header from '../components/Header'
import Footer from '../components/Footer'


export default class Player extends Component {
    render() {

        console.log(this.props.location.state)
        return (

            <div>
                <Header />
                <div className='player-wrapper'>
                    <ReactPlayer url={this.props.location.state.url}
                        className='react-player'
                        controls
                        width='100%'
                        height='100%' />
                </div>
                <Footer />
            </div>




            );
    }
}


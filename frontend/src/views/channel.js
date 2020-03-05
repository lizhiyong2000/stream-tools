import React, { Component } from 'react';
import { connect } from 'react-redux';

import PlayItemsPage from '../components/playitem/PlayItemsPage';
import FlashMessage from '../components/FlashMessage';

import Header from '../components/Header'
import Footer from '../components/Footer'

import Filters from '../components/filter/Filters';
import InputFilter from '../components/filter/InputFilter';

import { playitemActions } from '../actions';

class ChannelPage extends Component {

    state = {
        filters: { keyword: '' },
    }

    onFilterChange = (filters) => {
        console.log(filters)
        this.setState({ filters });
    }


    componentDidMount() {

        const filters =  { keyword: this.props.location.state.channel.name };

        this.props.dispatch(playitemActions.fetchPlayItems(filters));
    }


    render() {
        const { filters } = this.state;

        const {channel} = this.props.location.state;

        return (

            <div>
                <Header />
                { this.props.error && <FlashMessage message={ this.props.error } /> }

                <div className='channel-player flexbox'>
                    <div class="title fl">
                        <span>
                            <img src={ channel.thumb } alt={ channel.name } title={ channel.name } />
                        </span>
                        <h1 class="channel-title">{ channel.name }</h1>
                    </div>
                </div>

                <Filters onChange={this.onFilterChange}>
                    <InputFilter filterName="keyword" />
                </Filters>

                <div className="main-content">
                    <PlayItemsPage playitems={ this.props.playitems }
                        onCreatePlayItem={ this.onCreatePlayItem }
                        onStatusChange={ this.onStatusChange }
                        isLoading={ this.props.isLoading } />
                </div>
                <Footer />
            </div>
            );
    }
}

function mapStateToProps(state) {
    const {channel, playitems, isLoading, error} = state.channel;
    return {
        channel,
        playitems,
        isLoading,
        error
    };
}

export default connect(mapStateToProps)(ChannelPage);
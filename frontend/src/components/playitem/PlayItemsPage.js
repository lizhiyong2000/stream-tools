import React, { Component } from 'react';
import PlayItemList from './PlayItemList';

import { PLAYITEM_STATUSES } from '../../constants';

class PlayItemsPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showNewPlayItemForm: false,
            name: '',
            url: '',
        };
    }

    onNameChange = e => {
        this.setState({
            name: e.target.value
        });
    };

    onUrlChange = e => {
        this.setState({
            url: e.target.value
        });
    };

    resetForm() {
        this.setState({
            showNewPlayItemForm: false,
            name: '',
            url: '',
        });
    }

    onCreatePlayItem = e => {
        e.preventDefault();
        this.props.onCreatePlayItem({
            name: this.state.name,
            url: this.state.url,
        });
        this.resetForm();
    };

    toggleForm = () => {
        this.setState({
            showNewPlayItemForm: !this.state.showNewPlayItemForm
        });
    };

    render() {
        if (this.props.isLoading) {
            return (
                <div className="playitems-loading">
                    Loading...
                </div>
                );
        }

        return (
            <div className="playitems">
                <div className="playitems-header">
                    <button className="button button-default" onClick={ this.toggleForm }>
                        + New PlayItem
                    </button>
                </div>
                { this.state.showNewPlayItemForm &&
                  <form className="new-playitem-form" onSubmit={ this.onCreatePlayItem }>
                      <input className="full-width-input"
                          onChange={ this.onNameChange }
                          value={ this.state.name }
                          type="text"
                          placeholder="name" />
                      <input className="full-width-input"
                          onChange={ this.onUrlChange }
                          value={ this.state.url }
                          type="text"
                          placeholder="url" />
                      <button className="button" type="submit">
                          Save
                      </button>
                  </form> }
                <div className="playitem-lists">
                    <PlayItemList playitems={ this.props.playitems } onStatusChange={ this.props.onStatusChange } />
                </div>
            </div>
            );
    }
}

export default PlayItemsPage;

import React, {Component} from 'react';
import ChannelList from './ChannelList';


class ChannelsPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showNewChannelForm: false,
            name: '',
            thumb: '',
            keyword:'',
        };
    }

    onNameChange = e => {
        this.setState({
            name: e.target.value
        });
    };

    onThumbChange = e => {
        this.setState({
            thumb: e.target.value
        });
    };

    resetForm() {
        this.setState({
            showNewChannelForm: false,
            name: '',
            thumb: '',
        });
    }

    onCreatePlayItem = e => {
        e.preventDefault();
        this.props.onCreatePlayItem({
            name: this.state.name,
            thumb: this.state.thumb,
        });
        this.resetForm();
    };

    toggleForm = () => {
        this.setState({
            showNewChannelForm: !this.state.showNewChannelForm
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
                { this.state.showNewChannelForm &&
                  <form className="new-playitem-form" onSubmit={ this.onCreatePlayItem }>
                      <input className="full-width-input"
                          onChange={ this.onNameChange }
                          value={ this.state.name }
                          type="text"
                          placeholder="name" />
                      <input className="full-width-input"
                          onChange={ this.onThumbChange }
                          value={ this.state.thumb }
                          type="text"
                          placeholder="thumb" />
                      <button className="button" type="submit">
                          Save
                      </button>
                  </form> }
                <div className="list-image clear">
                     <ChannelList channels={ this.props.channels} />

                </div>
            </div>
            );
    }
}

export default ChannelsPage;

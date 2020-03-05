import React, { Component} from 'react';


import PropTypes from 'prop-types'


import filter from './filter';

const { func, string } = PropTypes;

class ChannelFilter extends Component {
    static propTypes = {
        updateFilter: func.isRequired,
        filterItems: PropTypes.array.isRequired
    }

    onChange = (event) => {
        event.preventDefault();

        var value = event.currentTarget.attributes['href'].value;
        //console.log("ChannelFilter onchange:" + value)
        this.props.updateFilter(value);

    }

    render() {

        return (
            <div className="filter-list">

                { this.props.filterItems.map(item => (

                    <li key={item.value}>
                        <a href = {item.value} onClick={this.onChange}>{ item.text}</a>
                    </li>
                )) }
            </div>
        );


        //return <input onChange={this.onChange} />
    }
}

export default filter(ChannelFilter);
import React, { Component} from 'react';


import PropTypes from 'prop-types'


import filter from './filter';

const { func, string } = PropTypes;

class InputFilters extends Component {
    static propTypes = {
        updateFilter: func.isRequired,
    }

    onChange = ({ target: { value } }) => {
        console.log("onchange:" + value)
        this.props.updateFilter(value);
    }

    render() {
        return <input onChange={this.onChange} />
    }
}

export default filter(InputFilters);
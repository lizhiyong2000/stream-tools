import React, { Component } from 'react';

import PropTypes from 'prop-types'

const { func } = PropTypes;

class Filters extends Component {
    static propTypes = {
        onChange: func.isRequired,
    }

    static childContextTypes = {
        updateFilter: func,
    }

    state = { filters: {} };

    notifyChange = () => {
        console.log('notifyChange:' + JSON.stringify(this.state.filters));

        this.props.onChange(this.state.filters);
    }

    updateFilter = (name, value) => {

        console.log('updateFilter:' + name + ',' +value)


        //var result = {
        //    filters: { ...this.state.filters, [name]: value },
        //}
        //
        //console.log('result:' + JSON.stringify(result.filters));

        this.setState({
            filters: { ...this.state.filters, [name]: value },
        }, this.notifyChange);
    }

    getChildContext() {
        return {
            updateFilter: this.updateFilter,
        }
    }

    render() {
        return <div>{this.props.children}</div>;
    }
}

export default Filters;
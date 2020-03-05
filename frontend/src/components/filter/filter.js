
import React, { Component } from 'react';

import PropTypes from 'prop-types'

const { func, string } = PropTypes;

export default function filter(ComposedComponent) {
    return class Filter extends Component {
        static contextTypes = {
            updateFilter: func.isRequired,
        }

        static propTypes = {
            filterName: string.isRequired,
        }

        updateFilter = (value) => {

            console.log("this.context.updateFilter:" + value)
            this.context.updateFilter(this.props.filterName, value);
        }

        render() {
            const props = { ...this.props, updateFilter: this.updateFilter };
            return <ComposedComponent {...props} />;
        }
    }
}
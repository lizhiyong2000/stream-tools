import React, { Component } from 'react';

import PropTypes from 'prop-types'

class Checkbox extends Component {
    state = {
        isChecked: this.props.isChecked,
    }

    toggleCheckboxChange = () => {
        const {handleCheckboxChange, value} = this.props;

        const state = this.state.isChecked

        this.setState(({isChecked}) => (
        {
            isChecked: !isChecked,
        }
        ));

        handleCheckboxChange(value, !state);
    }

    render() {

        const {label, value} = this.props;

        const {isChecked} = this.state;

        return (
            <div className="checkbox">
                <label>
                { label }
                    
                    
                </label>

                <input type="checkbox"
                        value={ value }
                        checked={ isChecked }
                        onChange={ this.toggleCheckboxChange } />
            </div>
            );
    }
}

Checkbox.propTypes = {
    label: PropTypes.string.isRequired,
    value: PropTypes.string.isRequired,
    handleCheckboxChange: PropTypes.func.isRequired,
    isChecked: PropTypes.bool.isRequired,
};

export default Checkbox;
import React from 'react'
import ReactDOM from 'react-dom'
import PropTypes from 'prop-types'
import AbstractListChild from '../AbstractListChild'

export default class AbstractListItem extends AbstractListChild {
  static get propTypes () {
    return {
      listItemId: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.number
      ]).isRequired,
      isSelected: PropTypes.bool
    }
  }

  static get defaultProps () {
    return {
      listItemId: null,
      isSelected: false
    }
  }
}
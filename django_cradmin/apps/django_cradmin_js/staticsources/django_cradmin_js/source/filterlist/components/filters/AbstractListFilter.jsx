import React from 'react'
import PropTypes from 'prop-types'
import AbstractListChild from '../AbstractListChild'

export default class AbstractListFilter extends AbstractListChild {
  static get propTypes () {
    return Object.assign(super.propTypes, {
      name: PropTypes.string.isRequired,

      // The filter does not control where it is rendered,
      // but it may want to be rendered a bit differently depending
      // on the location where the list places it.
      location: PropTypes.string.isRequired,

      // If this is ``true``, the filter is not rendered,
      // but the API requests is always filtered by the
      // value specified for the filter.
      //
      // This means that {@link filterHttpRequest} is used,
      // but render is not used.
      isStatic: PropTypes.bool,

      // The value of the filter.
      // This is changed using {@link AbstractListFilter#setFilterValue},
      // which uses the setFilterValueCallback prop to update the filter
      // value in the {@link AbstractList} state, which will lead to
      // a re-render of the filter with new value prop.
      value: PropTypes.any
    })
  }

  static get defaultProps () {
    return Object.assign(super.defaultProps, {
      isStatic: false,
      value: null
    })
  }

  static filterHttpRequest (httpRequest, name, value) {
    httpRequest.urlParser.queryString.set(name, value)
  }

  constructor (props) {
    super(props)
    this.state = this.getInitialState()
  }

  getInitialState () {
    return {}
  }

  setupBoundMethods () {
    super.setupBoundMethods()
    this.setFilterValue = this.setFilterValue.bind(this)
  }

  setFilterValue (value) {
    this.props.childExposedApi.setFilterValue(this.props.name, value)
  }
}
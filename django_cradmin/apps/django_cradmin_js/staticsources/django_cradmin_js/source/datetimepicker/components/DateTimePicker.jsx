import React from 'react'
import DatePicker from './DatePicker'
import TimePicker from './TimePicker'
import PropTypes from 'prop-types'
import BemUtilities from '../../utilities/BemUtilities'
import { gettext } from 'ievv_jsbase/lib/gettext'
import moment from 'moment/moment'

export default class DateTimePicker extends React.Component {
  static get defaultProps () {
    return {
      momentObject: null,
      initialFocusMomentObject: moment(),
      locale: null,
      showSeconds: false,
      dateIconClassName: 'cricon cricon--calendar-grid',
      timeIconClassName: 'cricon cricon--clock',
      dateButtonLabel: gettext('Date'),
      timeButtonLabel: gettext('Time')
    }
  }

  static get propTypes () {
    return {
      momentObject: PropTypes.any,
      initialFocusMomentObject: PropTypes.any.isRequired,
      locale: PropTypes.string,
      showSeconds: PropTypes.bool.isRequired,
      dateIconClassName: PropTypes.string.isRequired,
      timeIconClassName: PropTypes.string.isRequired,
      dateButtonLabel: PropTypes.string.isRequired,
      timeButtonLabel: PropTypes.string.isRequired
    }
  }

  constructor (props) {
    super(props)
    this.state = {
      tabName: 'date'
    }
  }

  get tabsClassName () {
    return BemUtilities.addVariants('buttonbar', ['stretch', 'tinymargin'])
  }

  makeTabButtonClassName (tabName) {
    const bemVariants = []
    if (tabName === this.state.tabName) {
      bemVariants.push('secondary-fill')
    } else {
      bemVariants.push('secondary')
    }
    return BemUtilities.buildBemElement('buttonbar', 'button', bemVariants)
  }

  renderDatePicker () {
    return <DatePicker
      key={'datePicker'}
      momentObject={this.props.momentObject}
      initialFocusMomentObject={this.props.initialFocusMomentObject}
      locale={this.props.locale}
      onChange={this.props.onChange}
    />
  }

  renderTimePicker () {
    return <TimePicker
      key={'timePicker'}
      momentObject={this.props.momentObject}
      initialFocusMomentObject={this.props.initialFocusMomentObject}
      showSeconds={this.props.showSeconds}
      locale={this.props.locale}
      onChange={this.props.onChange}
    />
  }

  renderPicker () {
    if (this.state.tabName === 'date') {
      return this.renderDatePicker()
    } else {
      return this.renderTimePicker()
    }
  }

  renderTabButton (tabName, label, iconClassName) {
    return <button
      className={this.makeTabButtonClassName(tabName)}
      onClick={this.handleClickTab.bind(this, tabName)}
    >
      <span className={iconClassName} aria-hidden='true' />
      {' '}{label}
    </button>
  }

  renderTabs () {
    return <div key={'tabs'} className={this.tabsClassName}>
      {this.renderTabButton('date', this.props.dateButtonLabel, this.props.dateIconClassName)}
      {this.renderTabButton('time', this.props.timeButtonLabel, this.props.timeIconClassName)}
    </div>
  }

  render () {
    return [
      this.renderTabs(),
      this.renderPicker()
    ]
  }

  handleClickTab (tabName, e) {
    e.preventDefault()
    this.setState({tabName: tabName})
  }
}

import React from 'react'
import PropTypes from 'prop-types'
import TimeDisplay from './TimeDisplay'
import RangeSlider from '../../components/RangeSlider'
import { gettext } from 'ievv_jsbase/lib/gettext'
import moment from 'moment/moment'
import BemUtilities from '../../utilities/BemUtilities'

export default class TimePicker extends React.Component {
  static get defaultProps () {
    return {
      moment: null,
      locale: null,
      showSeconds: false,
      onChange: null,
      includeShortcuts: true
    }
  }

  static get propTypes () {
    return {
      moment: PropTypes.any,
      locale: PropTypes.string,
      showSeconds: PropTypes.bool.isRequired,
      onChange: PropTypes.func.isRequired,
      includeShortcuts: PropTypes.bool
    }
  }

  get timeDisplayComponentProps () {
    return {
      moment: this.props.moment,
      showSeconds: this.props.showSeconds,
      bemVariants: ['xlarge']
    }
  }

  renderTimeDisplay () {
    return <TimeDisplay {...this.timeDisplayComponentProps} />
  }

  renderTimeDisplayWrapper () {
    return <p className={'text-center'} key={'time-display-wrapper'}>
      {this.renderTimeDisplay()}
    </p>
  }

  renderHourPicker () {
    return <label className='label' key={'hour'}>
      {gettext('Hours')}:
      <RangeSlider
        value={this.props.moment.hour()}
        min={0}
        max={23}
        onChange={this.changeHours.bind(this)}
      />
    </label>
  }

  renderMinutePicker () {
    return <label className='label' key={'minute'}>
      {gettext('Minutes')}:
      <RangeSlider
        value={this.props.moment.minute()}
        min={0}
        max={59}
        onChange={this.changeMinutes.bind(this)}
      />
    </label>
  }

  renderSecondPicker () {
    if (!this.props.showSeconds) {
      return null
    }
    return <label className='label' key={'second'}>
      {gettext('Seconds')}:
      <RangeSlider
        value={this.props.moment.second()}
        min={0}
        max={59}
        onChange={this.changeSeconds.bind(this)}
      />
    </label>
  }

  renderTimePickers () {
    return [
      this.renderHourPicker(),
      this.renderMinutePicker(),
      this.renderSecondPicker()
    ]
  }

  makeShortcutButtonClassName (bemVariants = []) {
    return BemUtilities.buildBemElement('buttonbar', 'button', [bemVariants, ...['compact']])
  }

  renderNowButtonLabel () {
    return gettext('Now')
  }

  renderNowButton () {
    return <button
      type={'button'}
      key={'nowButton'}
      className={this.makeShortcutButtonClassName()}
      onClick={this.onClickNowButton.bind(this)}
    >
      {this.renderNowButtonLabel()}
    </button>
  }

  renderShortcutButtons () {
    return [
      this.renderNowButton()
    ]
  }

  renderShortcutButtonBar () {
    return <div key={'shortcutButtonBar'} className={'buttonbar buttonbar--center'}>
      {this.renderShortcutButtons()}
    </div>
  }

  render () {
    return [
      this.renderTimeDisplayWrapper(),
      this.renderTimePickers(),
      this.props.includeShortcuts ? this.renderShortcutButtonBar() : null
    ]
  }

  _cleanMoment (momentObject) {
    momentObject.millisecond(0)
    if (!this.showSeconds) {
      momentObject.second(0)
    }
    return momentObject
  }

  onClickNowButton () {
    const today = moment()
    let momentObject = this.props.moment.clone()
    momentObject.hour(today.hour())
    momentObject.minute(today.minute())
    momentObject.second(today.second())
    momentObject.millisecond(0)
    this.props.onChange(this._cleanMoment(momentObject))
  }

  changeHours (hours) {
    let moment = this.props.moment.clone()
    moment.hours(hours)
    this.props.onChange(this._cleanMoment(moment))
  }

  changeMinutes (minutes) {
    let moment = this.props.moment.clone()
    moment.minutes(minutes)
    this.props.onChange(this._cleanMoment(moment))
  }

  changeSeconds (seconds) {
    let moment = this.props.moment.clone()
    moment.seconds(seconds)
    this.props.onChange(this._cleanMoment(moment))
  }
}

import AbstractDateOrDateTimeSelect from './AbstractDateOrDateTimeSelect'

export default class AbstractEmbeddedDateOrDateTimeSelect extends AbstractDateOrDateTimeSelect {
  static get defaultProps () {
    return Object.assign({}, super.defaultProps, {
      bemVariants: ['sane-max-width'],
      bodyBemVariants: ['outlined']
    })
  }

  setSelectedMoment (selectedMoment) {
    this.triggerOnChange(selectedMoment)
  }

  renderContent () {
    return [
      ...super.renderContent(),
      this.renderHiddenField()
    ]
  }
}

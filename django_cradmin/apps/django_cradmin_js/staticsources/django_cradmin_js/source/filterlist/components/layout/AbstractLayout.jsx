import React from 'react'
import PropTypes from 'prop-types'
import 'ievv_jsbase/lib/utils/i18nFallbacks'
import AbstractListChild from '../AbstractListChild'
import LoadingIndicator from '../../../components/LoadingIndicator'
import AbstractListFilter from '../filters/AbstractListFilter'
import AbstractList from '../lists/AbstractList'
import AbstractPaginator from '../paginators/AbstractPaginator'

export default class AbstractLayout extends AbstractListChild {
  static get propTypes () {
    return Object.assign(super.propTypes, {
      layout: PropTypes.object.isRequired,
      listItemsDataArray: PropTypes.array.isRequired,
      listItemsDataMap: PropTypes.instanceOf(Map).isRequired,
      selectedListItemsMap: PropTypes.instanceOf(Map).isRequired,
      isLoadingNewItemsFromApi: PropTypes.bool.isRequired,
      isLoadingMoreItemsFromApi: PropTypes.bool.isRequired
    })
  }

  static get defaultProps () {
    return Object.assign(super.defaultProps, {
      layout: null,
      listItemsDataArray: null,
      listItemsDataMap: new Map(),
      selectedListItemsMap: new Map(),
      isLoadingNewItemsFromApi: false,
      isLoadingMoreItemsFromApi: false
    })
  }

  //
  //
  // Rendering
  //
  //

  renderLoadingIndicator () {
    return <LoadingIndicator key={`loadingIndicator`}/>
  }

  /**
   * Used by {@link AbstractLayout#shouldRenderComponent} when
   * the provided componentSpec.componentClass is a subclass
   * of {@link AbstractListFilter}.
   *
   * By default this returns `true`.
   *
   * @param componentSpec
   * @returns {boolean}
   */
  shouldRenderFilterComponent (componentSpec) {
    return true
  }

  /**
   * Used by {@link AbstractLayout#shouldRenderComponent} when
   * the provided componentSpec.componentClass is a subclass
   * of {@link AbstractList}.
   *
   * By default this returns `true`.
   *
   * @param componentSpec The component we want to determine if should be rendered.
   * @returns {boolean} `true` to render the component, and `false` to not render
   *    the component.
   */
  shouldRenderListComponent (componentSpec) {
    return true
  }

  /**
   * Used by {@link AbstractLayout#shouldRenderComponent} when
   * the provided componentSpec.componentClass is a subclass
   * of {@link AbstractPaginator}.
   *
   * By default this returns `true` unless we are loading a new list
   * of items from the API (which typically happens when a filter is changed).
   *
   * @param componentSpec The component we want to determine if should be rendered.
   * @returns {boolean} `true` to render the component, and `false` to not render
   *    the component.
   */
  shouldRenderPaginatorComponent (componentSpec) {
    return !this.props.isLoadingNewItemsFromApi
  }

  /**
   * Determine if a component should be rendered.
   *
   * Perfect place to hook in things like "show advanced" filters etc.
   * in subclasses, but you will normally want to override one of
   * {@link AbstractLayout#shouldRenderFilterComponent},
   * {@link AbstractLayout#shouldRenderListComponent} or
   * {@link AbstractLayout#shouldRenderPaginatorComponent} instead
   * of this method.
   *
   * @param componentSpec The component we want to determine if should be rendered.
   * @returns {boolean} `true` to render the component, and `false` to not render
   *    the component.
   */
  shouldRenderComponent (componentSpec) {
    if (componentSpec.componentClass.prototype instanceof AbstractListFilter) {
      return this.shouldRenderFilterComponent(componentSpec)
    } else if (componentSpec.componentClass.prototype instanceof AbstractList) {
      return this.shouldRenderListComponent(componentSpec)
    } else if (componentSpec.componentClass.prototype instanceof AbstractPaginator) {
      return this.shouldRenderPaginatorComponent(componentSpec)
    }
    return true
  }

  getFilterComponentProps (componentSpec) {
    return {
      value: this.props.childExposedApi.getFilterValue(componentSpec.props.name)
    }
  }

  getListComponentProps (componentSpec) {
    return {
      listItemsDataArray: this.props.listItemsDataArray,
      selectedListItemsMap: this.props.selectedListItemsMap
    }
  }

  getPaginatorComponentProps (componentSpec) {
    return {
      listItemsDataArray: this.props.listItemsDataArray
    }
  }

  getComponentProps (componentSpec) {
    let extraProps = {}
    if (componentSpec.componentClass.prototype instanceof AbstractListFilter) {
      extraProps = this.getFilterComponentProps(componentSpec)
    } else if (componentSpec.componentClass.prototype instanceof AbstractList) {
      extraProps = this.getListComponentProps(componentSpec)
    } else if (componentSpec.componentClass.prototype instanceof AbstractPaginator) {
      extraProps = this.getPaginatorComponentProps(componentSpec)
    }
    return this.makeChildComponentProps(Object.assign(componentSpec.props, {
      key: componentSpec.props.uniqueComponentKey
    }, extraProps))
  }

  renderComponent (componentSpec) {
    return React.createElement(
      componentSpec.componentClass,
      this.getComponentProps(componentSpec))
  }

  renderComponentsAtLocation (location, fallback=null) {
    const renderedComponents = []
    for (let componentSpec of this.props.layout.getComponentsAtLocation(location)) {
      if (this.shouldRenderComponent(componentSpec)) {
        renderedComponents.push(this.renderComponent(componentSpec))
      }
    }
    if(renderedComponents.length === 0) {
      return fallback
    }
    return renderedComponents
  }
}

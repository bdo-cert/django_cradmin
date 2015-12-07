angular.module('djangoCradmin.listfilter.directives', [])


.directive('djangoCradminListfilter', [
  '$window', '$timeout', 'djangoCradminBgReplaceElement',
  ($window, $timeout, djangoCradminBgReplaceElement) ->
    return {
      restrict: 'A'
      scope: {
        options: '=djangoCradminListfilter'
      }

      controller: ($scope, $element) ->
        filterListDomId = $element.attr('id')
        filterScopes = []
        loadInProgress = false
        $messageElement = null
        showMessageTimer = null

        @loadIsInProgress = ->
          return loadInProgress

        setLoadInProgress = (options) ->
          loadInProgress = true
          $scope.targetElement.addClass('django-cradmin-listfilter-target-loading')
          for filterScope in filterScopes
            filterScope.onLoadInProgress(options.filterDomId)

        setLoadFinished = (options) ->
          loadInProgress = false
          $scope.targetElement.removeClass('django-cradmin-listfilter-target-loading')
          for filterScope in filterScopes
            filterScope.onLoadFinished(options.filterDomId)
#          $scope.targetElement.removeAttr('aria-describedby', 'myprogress')
          $scope.targetElement.attr('aria-busy', 'false')

        onLoadSuccess = ($remoteHtmlDocument, remoteUrl) =>
          $remoteFilterList = $remoteHtmlDocument.find('#' + filterListDomId)
          title = $window.document.title
          $window.history.pushState("list filter change", title, remoteUrl)
          for filterScope in filterScopes
            filterScope.syncWithRemoteFilterList($remoteFilterList)

        showMessage = (variant, message) ->
          hideMessage()
          loadspinner = ""
          if $scope.options.loadspinner_css_class?
            loadspinner = "<span class='django-cradmin-listfilter-message-loadspinner " +
              "#{$scope.options.loadspinner_css_class}' aria-hidden='true'></span>"
          $messageElement = angular.element(
            "<div aria-role='progressbar' " +
            "class='django-cradmin-listfilter-message django-cradmin-listfilter-message-#{variant}'>" +
            "#{loadspinner}" +
            "<span class='django-cradmin-listfilter-message-text'>#{message}</span></div>")
          $messageElement.prependTo($scope.targetElement)
          $scope.targetElement.attr('aria-busy', 'true')

        queueMessage = (variant, message) ->
          if showMessageTimer?
            $timeout.cancel(showMessageTimer)
          showMessageTimer = $timeout(->
            showMessage(variant, message)
          , $scope.options.loadingmessage_delay_milliseconds)

        hideMessage = ->
          if showMessageTimer?
            $timeout.cancel(showMessageTimer)
          if $messageElement
            $messageElement.remove()
            $messageElement = null

        @load = (options) ->
          setLoadInProgress(options)
          queueMessage('loading', options.loadingmessage)
          djangoCradminBgReplaceElement.load({
            parameters: {
              method: 'GET'
              url: options.remoteUrl
            },
            remoteElementSelector: '#' + $scope.options.target_dom_id
            targetElement: $scope.targetElement
            $scope: $scope
            replace: true
            onHttpError: (response) ->
              console?.error? 'Error while filtering', response
              showMessage('error', $scope.options.loaderror_message)
            onSuccess: ($remoteHtmlDocument) ->
              onLoadSuccess($remoteHtmlDocument, options.remoteUrl)
              if options.onLoadSuccess?
                options.onLoadSuccess(options.onLoadSuccessData)
            onFinish: ->
              setLoadFinished(options)
              hideMessage()
          })

        @addFilterScope = (filterScope) ->
          filterScopes.push(filterScope)

        return

      link: ($scope, $element, attributes) ->
        $scope.targetElement = angular.element('#' + $scope.options.target_dom_id)
        return
    }
])


.directive('djangoCradminListfilterSelect', [
  ->
    return {
      restrict: 'A',
      require: '^djangoCradminListfilter'
      scope: {
        options: '=djangoCradminListfilterSelect'
      }

      controller: ($scope, $element) ->

        ###
        Replace all <option>-elements with new <option>-elements from the server.
        ###
        $scope.syncWithRemoteFilterList = ($remoteFilterList) ->
          domId = $element.attr('id')
          $remoteElement = $remoteFilterList.find('#' + domId)
          $element.empty()
          $element.append(angular.element($remoteElement.html()))

        $scope.onLoadInProgress = (filterDomId) ->
          $element.prop('disabled', true)

        $scope.onLoadFinished = (filterDomId) ->
          $element.prop('disabled', false)

        return

      link: ($scope, $element, attributes, listfilterCtrl) ->
        listfilterCtrl.addFilterScope($scope)

        getValue = ->
          $element.find("option:selected").attr('value')

        $element.on 'change', ->
          remoteUrl = getValue()
          listfilterCtrl.load({
            remoteUrl: remoteUrl
            filterDomId: $element.attr('id')
            loadingmessage: $scope.options.loadingmessage
            onLoadSuccess: ->
              $element.focus()
          })
        return
    }
])


.directive('djangoCradminListfilterTextinput', [
  '$timeout'
  ($timeout) ->
    urlpatternAttribute = 'django-cradmin-listfilter-urlpattern'
    urlpatternReplaceText = '_-_TEXTINPUT_-_VALUE_-_'

    return {
      restrict: 'A',
      require: '^djangoCradminListfilter'
      scope: {
        options: '=djangoCradminListfilterTextinput'
      }

      controller: ($scope, $element) ->

        ###
        Update the "django-cradmin-listfilter-urlpattern"-attribute with
        the one from the server.
        ###
        $scope.syncWithRemoteFilterList = ($remoteFilterList) ->
          domId = $element.attr('id')
          $remoteElement = $remoteFilterList.find('#' + domId)
          $element.attr(urlpatternAttribute,
            $remoteElement.attr(urlpatternAttribute))

        $scope.onLoadInProgress = (filterDomId) ->
          if filterDomId != $element.attr('id')
            $element.prop('disabled', true)

        $scope.onLoadFinished = (filterDomId) ->
          $element.prop('disabled', false)

        return

      link: ($scope, $element, attributes, listfilterCtrl) ->
        listfilterCtrl.addFilterScope($scope)
        applySearchTimer = null
        loadedValue = $element.val()
        timeoutMilliseconds = $scope.options.timeout_milliseconds
        if not timeoutMilliseconds?
          timeoutMilliseconds = 500

        buildUrl = (value) ->
          urlpattern = $element.attr(urlpatternAttribute)
          return urlpattern.replace(urlpatternReplaceText, value)

        onLoadSearchSuccess = (data) ->
          currentValue = $element.val()
          if data.value != currentValue
            onValueChange(true)
          loadedValue = data.value

        loadSearch = ->
          if listfilterCtrl.loadIsInProgress()
            return

          value = $element.val()
          if loadedValue == value
            return

#          console.log 'Search for', value
          remoteUrl = buildUrl(value)
          loadedValue = value
          listfilterCtrl.load({
            remoteUrl: remoteUrl
            onLoadSuccess: onLoadSearchSuccess
            onLoadSuccessData: {
              value: value
            }
            filterDomId: $element.attr('id')
            loadingmessage: $scope.options.loadingmessage
          })

        onValueChange = (useTimeout) ->
          if applySearchTimer?
            $timeout.cancel(applySearchTimer)
          if not listfilterCtrl.loadIsInProgress()
            if useTimeout
              applySearchTimer = $timeout(loadSearch, timeoutMilliseconds)
            else
              loadSearch()

        $element.on 'change', ->
          onValueChange(false)

        $element.on 'keydown', (e) ->
          if e.which == 13
            # ENTER/RETURN was pressed, load search instantly
            onValueChange(false)
          else
            onValueChange(true)
        return
    }
])


.directive('djangoCradminListfilterCheckboxlist', [
  ->
    return {
      restrict: 'A',
      require: '^djangoCradminListfilter'
      scope: {
        options: '=djangoCradminListfilterCheckboxlist'
      }

      controller: ($scope, $element) ->

        ###
        Replace all contents with new elements from the server.
        ###
        $scope.syncWithRemoteFilterList = ($remoteFilterList) ->
          domId = $element.attr('id')
          $remoteElement = $remoteFilterList.find('#' + domId)
          $element.empty()
          $element.append(angular.element($remoteElement.html()))
          $scope.registerCheckboxChangeListeners(true)

        $scope.onLoadInProgress = (filterDomId) ->
          $element.find('input').prop('disabled', true)

        $scope.onLoadFinished = (filterDomId) ->
          $element.find('input').prop('disabled', false)

        return

      link: ($scope, $element, attributes, listfilterCtrl) ->
        listfilterCtrl.addFilterScope($scope)

        getUrl = ($inputElement) ->
          $inputElement.attr('data-url')

        $scope.onCheckboxChange = (e) ->
          console.log 'Change'
          remoteUrl = getUrl(angular.element(e.target))
          listfilterCtrl.load({
            remoteUrl: remoteUrl
            filterDomId: $element.attr('id')
            loadingmessage: $scope.options.loadingmessage
            onLoadSuccess: ->
              $element.focus()
          })

        $scope.registerCheckboxChangeListeners = (removeFirst) ->
          if removeFirst
            $element.find('input').off 'change', $scope.onCheckboxChange
          $element.find('input').on 'change', $scope.onCheckboxChange

        $scope.registerCheckboxChangeListeners(false)

        return
    }
])

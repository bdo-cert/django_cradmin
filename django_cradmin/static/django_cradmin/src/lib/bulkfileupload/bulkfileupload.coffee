
angular.module('djangoCradmin.bulkfileupload', [
  'angularFileUpload', 'ngCookies'
])


.provider 'cradminBulkfileuploadCoordinator', ->
  class FileUploadCoordinator
    constructor: ($window) ->
      @hiddenfieldnameToScopeMap = {}
      @window = $window

    register: (hiddenfieldname, scope) ->
      existingScope = @hiddenfieldnameToScopeMap[hiddenfieldname]
      if existingScope?
        console.error(
          'Trying to register a fieldname that is already registered with ' +
          'cradminBulkfileuploadCoordinator. Fieldname:', hiddenfieldname)
        return
      @hiddenfieldnameToScopeMap[hiddenfieldname] = scope

    unregister: (hiddenfieldname) ->
      scope = @hiddenfieldnameToScopeMap[hiddenfieldname]
      if not scope?
        console.error(
          'Trying to unregister a field that is not registered with ' +
          'cradminBulkfileuploadCoordinator. Fieldname:', hiddenfieldname)
      @hiddenfieldnameToScopeMap[hiddenfieldname] = undefined

    _getScope: (hiddenfieldname) ->
      scope = @hiddenfieldnameToScopeMap[hiddenfieldname]
      if not scope?
        console.error(
          'Trying to get a field that is not registered with ' +
          'cradminBulkfileuploadCoordinator. Fieldname:', hiddenfieldname)
      return scope

    showOverlayForm: (hiddenfieldname) ->
      scope = @_getScope(hiddenfieldname)
      scope.formController.showOverlay()

#    hideOverlayForm: (hiddenfieldname) ->
#      scope = @_getScope(hiddenfieldname)
#      scope.formController.hideOverlay()

  @$get = (['$window', ($window) ->
    return new FileUploadCoordinator($window)
  ])

  return @


.factory 'cradminBulkfileupload', ->
  class FileInfo
    constructor: (options) ->
      @file = options.file
      @temporaryfileid = options.temporaryfileid
      if @file?
        @name = @file.name
      else
        @name = options.name
      @isRemoving = false

      @percent = options.percent
      if options.finished
        @finished = true
      else
        @finished = false
      if options.hasErrors
        @hasErrors = true
      else
        @hasErrors = false
#      @rawFiles = options.files
#      @files = []
#      for file in options.files
#        @files.push(new FileInfo({
#          temporaryfileid: null
#          name: file.name
#          file: file
#        }))
      @errors = options.errors

    markAsIsRemoving: ->
      @isRemoving = true

    markAsIsNotRemoving: ->
      @isRemoving = false

    updatePercent: (percent) ->
      @percent = percent

    finish: (temporaryfile, singlemode) ->
      @finished = true

      # Update the client provided filenames with the filename from the server
      index = 0
      @file = undefined
      @temporaryfileid = temporaryfile.id
      @name = temporaryfile.filename

    setErrors: (errors) ->
      @hasErrors = true
      @errors = errors

    indexOf: (fileInfo) ->
      return @files.indexOf(fileInfo)

    remove: (index) ->
      return @files.splice(index, 1)

#  class FileInfoList
  return {
#    createFileInfoList: (options) ->
#      new FileInfoList(options)
    createFileInfo: (options) ->
      return new FileInfo(options)
  }


.directive('djangoCradminBulkfileuploadForm', [
  ->
    ###
    A form containing ``django-cradmin-bulkfileupload`` fields
    must use this directive.
    ###
    return {
      restrict: 'AE'
      scope: {}

      controller: ($scope) ->
        $scope._inProgressCounter = 0

        # Simple submit buttons are simply disabled when files are beeing uploaded.
        $scope._submitButtonScopes = []

        $scope._setSubmitButtonsInProgress = ->
          for buttonScope in $scope._submitButtonScopes
            buttonScope.setNotInProgress()

        $scope._setSubmitButtonsNotInProgress = ->
          for buttonScope in $scope._submitButtonScopes
            buttonScope.setInProgress()

        @addInProgress = ->
          $scope._inProgressCounter += 1
          if $scope._inProgressCounter == 1
            $scope._setSubmitButtonsInProgress()

        @removeInProgress = ->
          if $scope._inProgressCounter == 0
            throw new Error("It should not be possible to get _inProgressCounter below 0")
          $scope._inProgressCounter -= 1
          if $scope._inProgressCounter == 0
            $scope._setSubmitButtonsNotInProgress()

        @addSubmitButtonScope = (submitButtonScope) ->
          $scope._submitButtonScopes.push(submitButtonScope)

        @addSubmitButtonScope = (submitButtonScope) ->
          $scope._submitButtonScopes.push(submitButtonScope)

        @registerOverlayControls = (overlayControlsScope) ->
          $scope._overlayControlsScope = overlayControlsScope

        @showOverlay = ->
          if $scope.overlay
            $scope.wrapperElement.addClass('django-cradmin-bulkfileupload-overlaywrapper-show')
          else
            throw new Error('Can only show the overlay if the form has the ' +
              'django-cradmin-bulkfileupload-form-overlay="true" attribute.')

        @hideOverlay = ->
          if $scope.overlay
            $scope.wrapperElement.removeClass('django-cradmin-bulkfileupload-overlaywrapper-show')
          else
            throw new Error('Can only hide the overlay if the form has the ' +
              'django-cradmin-bulkfileupload-form-overlay="true" attribute.')

        return

      link: ($scope, element, attr, uploadController) ->
        $scope.overlay = attr.djangoCradminBulkfileuploadFormOverlay == 'true'
        $scope.element = element
        if $scope.overlay
          # NOTE: If you do not want the form to be visible until the angularjs adds this class,
          #       simply add the class to your form.
          element.addClass('django-cradmin-bulkfileupload-form-overlay')

          body = angular.element('body')
          $scope.wrapperElement = angular.element('<div></div>')
          $scope.wrapperElement.addClass('django-cradmin-bulkfileupload-overlaywrapper')
          $scope.wrapperElement.appendTo(body)
          element.appendTo($scope.wrapperElement)
          $scope._overlayControlsScope.element.appendTo($scope.wrapperElement)
        element.on 'submit', (evt) ->
          if $scope._inProgressCounter != 0
            evt.preventDefault()
        return
    }
])


.directive('djangoCradminBulkfileuploadSubmit', [
  ->
    return {
      require: '^djangoCradminBulkfileuploadForm'
      restrict: 'A'
      scope: true

      controller: ($scope) ->
        $scope.inProgress = false

        $scope.setInProgress = ->
          $scope.element.prop('disabled', false)
          $scope.inProgress = false

        $scope.setNotInProgress = ->
          $scope.element.prop('disabled', true)
          $scope.inProgress = true

      link: (scope, element, attr, formController) ->
        scope.element = element
        formController.addSubmitButtonScope(scope)
        return
    }
])


.directive('djangoCradminBulkfileupload', [
  '$upload', '$cookies', 'cradminDetectize', 'cradminBulkfileuploadCoordinator'
  ($upload, $cookies, cradminDetectize, cradminBulkfileuploadCoordinator) ->
    return {
      require: '^djangoCradminBulkfileuploadForm'
      restrict: 'AE'
      scope: true

      controller: ($scope) ->
        $scope.collectionid = null

        # The scope variable changed when users add files
        $scope.cradminLastFilesSelectedByUser = []

        # Queue of files waiting for upload. Each time $scope.cradminLastFilesSelectedByUser
        # is changed, we add files here and clear $scope.cradminLastFilesSelectedByUser.
        $scope.fileUploadQueue = []

        # This is set to ``true`` when the first upload is in progress.
        # While this is ``true``, we just add files to the $scope.fileUploadQueue
        # but we do not upload the files until it becomes ``false``.
        $scope.firstUploadInProgress = false

        $scope.simpleWidgetScope = null
        $scope.advancedWidgetScope = null
        $scope.rejectedFilesScope = null

        @setInProgressOrFinishedScope = (inProgressOrFinishedScope) ->
          $scope.inProgressOrFinishedScope = inProgressOrFinishedScope

        @setFileUploadFieldScope = (fileUploadFieldScope, fieldname) ->
          $scope.fileUploadFieldScope = fileUploadFieldScope
          cradminBulkfileuploadCoordinator.register(fileUploadFieldScope.fieldname, $scope)

        @setSimpleWidgetScope = (simpleWidgetScope) ->
          $scope.simpleWidgetScope = simpleWidgetScope
          $scope._showAppropriateWidget()

        @setAdvancedWidgetScope = (advancedWidgetScope) ->
          $scope.advancedWidgetScope = advancedWidgetScope
          $scope._showAppropriateWidget()

        @setRejectFilesScope = (rejectedFilesScope) ->
          $scope.rejectedFilesScope = rejectedFilesScope

        @getUploadUrl = ->
          return $scope.uploadUrl

        @getCollectionId = ->
          return $scope.collectionid

        $scope._showAppropriateWidget = ->
          if $scope.advancedWidgetScope and $scope.simpleWidgetScope
            if cradminDetectize.device.type == 'desktop'
              $scope.simpleWidgetScope.hide()
            else
              $scope.advancedWidgetScope.hide()

        $scope.filesDropped = (files, evt, rejectedFiles) ->
          ###
          Callend when a file is draggen&dropped into the widget.
          ###
          if rejectedFiles.length > 0
            $scope.rejectedFilesScope.setRejectedFiles(rejectedFiles)

        $scope.$watch 'cradminLastFilesSelectedByUser', ->
          if $scope.cradminLastFilesSelectedByUser.length > 0
            for file in $scope.cradminLastFilesSelectedByUser
              $scope._addFileToQueue(file)
              if $scope.apiparameters.singlemode
                # Single mode only allows upload of a single file,
                # so it makes no sense to process more than one file.
                break
            $scope.cradminLastFilesSelectedByUser = []

        $scope._addFileToQueue = (file) ->
          if $scope.apiparameters.singlemode
            $scope.inProgressOrFinishedScope.clear()
          progressFileInfo = $scope.inProgressOrFinishedScope.addFileInfo({
            percent: 0
            file: file
          })
          $scope.fileUploadQueue.push(progressFileInfo)
          if $scope.firstUploadInProgress
            # If the first upload is in progress, we need to postpone subsequent
            # uploads until we get the response from the first upload containing
            # the collectionid.
            return
          if $scope.collectionid == null
            $scope.firstUploadInProgress = true
          $scope._processFileUploadQueue()

        $scope._onFileUploadComplete = ->
          ###
          Called both on file upload success and error
          ###
          $scope.firstUploadInProgress = false
          $scope.formController.removeInProgress()
          if $scope.fileUploadQueue.length > 0
            $scope._processFileUploadQueue()

        $scope._processFileUploadQueue = () ->
          progressFileInfo = $scope.fileUploadQueue.shift()  # Pop the first element from the queue
          apidata = angular.extend({}, $scope.apiparameters, {collectionid: $scope.collectionid})
          $scope.formController.addInProgress()

          $scope.upload = $upload.upload({
            url: $scope.uploadUrl
            method: 'POST'
            data: apidata
            file: progressFileInfo.file
            fileFormDataName: 'file'  # The form field name
            headers: {
              'X-CSRFToken': $cookies.get('csrftoken')
              'Content-Type': 'multipart/form-data'
            }
          }).progress((evt) ->
            progressFileInfo.updatePercent(parseInt(100.0 * evt.loaded / evt.total))
          ).success((data, status, headers, config) ->
            progressFileInfo.finish(data.temporaryfiles[0], $scope.apiparameters.singlemode)
            $scope._setCollectionId(data.collectionid)
            $scope._onFileUploadComplete()
          ).error((data, status) ->
            if status == 503
              progressFileInfo.setErrors({
                file: [{
                  message: $scope.errormessage503
                }]
              })
            else
              progressFileInfo.setErrors(data)
            $scope._onFileUploadComplete()
          )

        $scope._setCollectionId = (collectionid) ->
          $scope.collectionid = collectionid
          $scope.fileUploadFieldScope.setCollectionId(collectionid)

        return

      link: ($scope, element, attributes, formController) ->
        $scope.uploadUrl = attributes.djangoCradminBulkfileupload
        $scope.errormessage503 = attributes.djangoCradminBulkfileuploadErrormessage503
        if attributes.djangoCradminBulkfileuploadApiparameters?
          $scope.apiparameters = $scope.$parent.$eval(attributes.djangoCradminBulkfileuploadApiparameters)
          if not angular.isObject($scope.apiparameters)
            throw new Error('django-cradmin-bulkfileupload-apiparameters must be a javascript object.')
        else
          $scope.apiparameters = {}
        $scope.formController = formController
        $scope.$on '$destroy', ->
          if $scope.fileUploadFieldScope?
            cradminBulkfileuploadCoordinator.unregister $scope.fileUploadFieldScope.fieldname

        return
    }
])


.directive('djangoCradminBulkfileuploadRejectedFiles', [
  ->
    ###
    This directive is used to show files that are rejected on drop because
    of wrong mimetype. Each time a user drops one or more file with invalid
    mimetype, this template is re-rendered and displayed.
    ###
    return {
      restrict: 'A'
      require: '^djangoCradminBulkfileupload'
      templateUrl: 'bulkfileupload/rejectedfiles.tpl.html'
      transclude: true
      scope: {
        rejectedFileErrorMessage: '@djangoCradminBulkfileuploadRejectedFiles'
      }

      controller: ($scope) ->
        $scope.rejectedFiles = []
        $scope.setRejectedFiles = (rejectedFiles) ->
          $scope.rejectedFiles = rejectedFiles

        $scope.closeMessage = (rejectedFile) ->
          index = $scope.rejectedFiles.indexOf(rejectedFile)
          if index != -1
            $scope.rejectedFiles.splice(index, 1)

      link: (scope, element, attr, bulkfileuploadController) ->
        bulkfileuploadController.setRejectFilesScope(scope)
        return
    }
])


.directive('djangoCradminBulkfileuploadProgress', [
  'cradminBulkfileupload', '$http', '$cookies'
  (cradminBulkfileupload, $http, $cookies) ->
    return {
      restrict: 'AE'
      require: '^djangoCradminBulkfileupload'
      templateUrl: 'bulkfileupload/progress.tpl.html'
      scope: {}

      controller: ($scope) ->
        $scope.fileInfoArray = []

        $scope._findFileInfo = (fileInfo) ->
          if not fileInfo.temporaryfileid?
            throw new Error("Can not remove files without a temporaryfileid")
          for fileInfo in $scope.fileInfoArray
            fileInfoIndex = fileInfoArray.indexOf(fileInfo)
            if fileInfoIndex != -1
              return {
                fileInfo: fileInfo
                index: fileInfoIndex
              }
          throw new Error("Could not find requested fileInfo with temporaryfileid=#{fileInfo.temporaryfileid}.")

        @removeFile = (fileInfo) ->
          fileInfoLocation = $scope._findFileInfo(fileInfo)
          fileInfo.markAsIsRemoving()
          $scope.$apply()

          $http({
              url: $scope.uploadController.getUploadUrl()
              method: 'DELETE'
              headers:
                'X-CSRFToken': $cookies.get('csrftoken')
              data:
                collectionid: $scope.uploadController.getCollectionId()
                temporaryfileid: fileInfo.temporaryfileid
            })
            .success((data, status, headers, config) ->
              fileInfoLocation.fileInfoArray.remove(fileInfoLocation.index)
            ).
            error((data, status, headers, config) ->
              console?.error? 'ERROR', data
              alert('An error occurred while removing the file. Please try again.')
              fileInfo.markAsIsNotRemoving()
            )

        $scope.addFileInfo = (options) ->
          fileInfo = cradminBulkfileupload.createFileInfo(options)
          $scope.fileInfoArray.push(fileInfo)
          return fileInfo

        $scope.clear = (options) ->
          $scope.fileInfoArray = []


#        $scope.addFileInfo({
#          percent: 10
#          name: 'test.txt'
#        })
#        $scope.addFileInfo({
#            percent: 100
#            finished: true
#            name: 'Some kind of test.txt'
#        })
#        $scope.addFileInfo({
#          percent: 90
#          finished: true
#          name: 'mybigfile.txt'
#          hasErrors: true
#          errors: {
#            files: [{
#              message: 'File is too big'
#            }]
#          }
#        })

        return

      link: (scope, element, attr, uploadController) ->
        scope.uploadController = uploadController
        uploadController.setInProgressOrFinishedScope(scope)
        return
    }
])

.directive('djangoCradminBulkFileInfo', [
  ->
    ###*
    Renders a single file info with progress info, errors, etc.

    Used both the djangoCradminBulkfileuploadProgress directive.
    ###
    return {
      restrict: 'AE'
      scope: {
        fileInfo: '=djangoCradminBulkFileInfo'
      }
      templateUrl: 'bulkfileupload/fileinfo.tpl.html'
      transclude: true

      controller: ($scope) ->
        @close = ->
          $scope.element.remove()
        return

      link: (scope, element, attr) ->
        scope.element = element
        return
    }
])


.directive('djangoCradminBulkfileuploadErrorCloseButton', [
  ->
    return {
      restrict: 'A'
      require: '^djangoCradminBulkFileInfo'
      scope: {}

      link: (scope, element, attr, fileInfoController) ->
        element.on 'click', (evt) ->
          evt.preventDefault()
          fileInfoController.close()
        return
    }
])


.directive('djangoCradminBulkfileuploadRemoveFileButton', [
  ->
    return {
      restrict: 'A'
      require: '^djangoCradminBulkfileuploadProgress'
      scope: {
        'fileInfo': '=djangoCradminBulkfileuploadRemoveFileButton'
      }

      link: (scope, element, attr, progressController) ->
        element.on 'click', (evt) ->
          evt.preventDefault()
          progressController.removeFile(scope.fileInfo)
        return
    }
])


.directive('djangoCradminBulkfileuploadCollectionidField', [
  ->
    return {
      require: '^djangoCradminBulkfileupload'
      restrict: 'AE'
      scope: {}

      controller: ($scope) ->
        $scope.setCollectionId = (collectionid) ->
          $scope.element.val("#{collectionid}")
        return

      link: (scope, element, attr, uploadController) ->
        scope.element = element
        scope.fieldname = attr.name
        uploadController.setFileUploadFieldScope(scope)
        return
    }
])


.directive('djangoCradminBulkfileuploadAdvancedWidget', [
  ->
    return {
      require: '^djangoCradminBulkfileupload'
      restrict: 'AE'
      scope: {}

      link: (scope, element, attr, uploadController) ->
        scope.hide = ->
          element.css('display', 'none')

        uploadController.setAdvancedWidgetScope(scope)
        return
    }
])


.directive('djangoCradminBulkfileuploadSimpleWidget', [
  ->
    return {
      require: '^djangoCradminBulkfileupload'
      restrict: 'AE'
      scope: {}

      link: (scope, element, attr, uploadController) ->
        scope.hide = ->
          element.css('display', 'none')

        uploadController.setSimpleWidgetScope(scope)

        return
    }
])


.directive('djangoCradminBulkfileuploadShowOverlay', [
  'cradminBulkfileuploadCoordinator'
  (cradminBulkfileuploadCoordinator) ->
    return {
      restrict: 'AE'
      scope: {
        hiddenfieldname: '@djangoCradminBulkfileuploadShowOverlay'
      }

      link: ($scope, element, attr) ->
        element.on 'click', ->
          cradminBulkfileuploadCoordinator.showOverlayForm($scope.hiddenfieldname)
        return
    }
])

.directive('djangoCradminBulkfileuploadHideOverlay', [
  ->
    return {
      restrict: 'AE'
      require: '^djangoCradminBulkfileuploadForm'
      scope: {
        hiddenfieldname: '@djangoCradminBulkfileuploadHideOverlay'
      }

      link: ($scope, element, attr, uploadFormController) ->
        element.on 'click', ->
          uploadFormController.hideOverlay()
        return
    }
])

.directive('djangoCradminBulkfileuploadOverlayControls', [
  ->
    return {
      restrict: 'AE'
      require: '^djangoCradminBulkfileuploadForm'
      scope: {}

      link: ($scope, element, attr, uploadFormController) ->
        $scope.element = element
        uploadFormController.registerOverlayControls($scope)
        return
    }
])

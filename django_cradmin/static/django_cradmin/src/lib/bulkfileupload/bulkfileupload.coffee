
angular.module('djangoCradmin.bulkfileupload', [
  'angularFileUpload', 'ngCookies'
])


.factory 'cradminBulkfileupload', ->
  class FileInfoList
    constructor: (options) ->
      @percent = options.percent
      @finished = false
      @files = options.files

    updatePercent: (percent) ->
      @percent = percent

    finish: ->
      console.log 'Finished!'
      @finished = true

  return {
    createFileInfoList: (options) ->
      new FileInfoList(options)
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
        return

      link: (scope, element, attr, uploadController) ->
        scope.element = element
        return
    }
])


.directive('djangoCradminBulkfileupload', [
  '$upload', '$cookies', 'cradminDetectize'
  ($upload, $cookies, cradminDetectize) ->
    return {
      require: '^djangoCradminBulkfileuploadForm'
      restrict: 'AE'
      scope: true

      controller: ($scope) ->
        $scope.collectionid = null
        $scope.cradminBulkFileUploadFiles = []
        $scope.simpleWidgetScope = null
        $scope.advancedWidgetScope = null

        @setInProgressOrFinishedScope = (inProgressOrFinishedScope) ->
          $scope.inProgressOrFinishedScope = inProgressOrFinishedScope


        @setFileUploadFieldScope = (fileUploadFieldScope) ->
          $scope.fileUploadFieldScope = fileUploadFieldScope

        @setSimpleWidgetScope = (simpleWidgetScope) ->
          $scope.simpleWidgetScope = simpleWidgetScope
          $scope._showAppropriateWidget()

        @setAdvancedWidgetScope = (advancedWidgetScope) ->
          $scope.advancedWidgetScope = advancedWidgetScope
          $scope._showAppropriateWidget()

        $scope._addFileInfoList = (fileInfoList) ->
          $scope.inProgressOrFinishedScope.addFileInfoList(fileInfoList)

        $scope._showAppropriateWidget = ->
          if $scope.advancedWidgetScope and $scope.simpleWidgetScope
            if cradminDetectize.device.type == 'desktop'
              $scope.simpleWidgetScope.hide()
            else
              $scope.advancedWidgetScope.hide()


        $scope.$watch 'cradminBulkFileUploadFiles', ->
          if $scope.cradminBulkFileUploadFiles.length > 0
            $scope._uploadFiles()

        $scope._uploadFiles = () ->
          progressInfo = $scope.inProgressOrFinishedScope.addFileInfoList({
            percent: 0
            files: $scope.cradminBulkFileUploadFiles.slice()
          })

          $scope.upload = $upload.upload({
            url: $scope.uploadUrl
            method: 'POST'
            data: {
              collectionid: $scope.collectionid
            }
            file: $scope.cradminBulkFileUploadFiles  # single file or a list of files. list is only for html5
            fileFormDataName: 'file'  # The form field name
            headers: {
              'X-CSRFToken': $cookies.csrftoken
              'Content-Type': 'multipart/form-data'
            }
          }).progress((evt) ->
#            files = ''
#            for file in evt.config.file
#              files += "#{file.name} "
#            console.log('progress: ' + parseInt(100.0 * evt.loaded / evt.total) + '% file :'+ files)
            progressInfo.updatePercent(parseInt(100.0 * evt.loaded / evt.total))
          ).success((data, status, headers, config) ->
            # file is uploaded successfully
#            files = ''
#            for file in config.file
#              files += "#{file.name} "
#            console.log('file ' + files + ' is uploaded successfully. Response: ')
#            console.log data
            progressInfo.finish()
            $scope._setCollectionId(data.collectionid)
          )

        $scope._setCollectionId = (collectionid) ->
          $scope.collectionid = collectionid
          $scope.fileUploadFieldScope.setCollectionId(collectionid)

        return

      link: (scope, element, attr, formController) ->
        scope.uploadUrl = attr.djangoCradminBulkfileupload
        return
    }
])


.directive('djangoCradminBulkProgress', [
  'cradminBulkfileupload'
  (cradminBulkfileupload) ->
    return {
      restrict: 'AE'
      require: '^djangoCradminBulkfileupload'
      templateUrl: 'bulkfileupload/progress.tpl.html'
      scope: {}

      controller: ($scope) ->
        $scope.fileInfoLists = [
#          new cradminBulkfileupload.createFileInfoList({
#            percent: 10
#            files: [{
#              name: 'test.txt'
#            }, {
#              name: 'test2.txt'
#            }]
#          }),
#          new cradminBulkfileupload.createFileInfoList({
#            percent: 100
#            finished: true
#            files: [{
#              name: 'Some kind of test.txt'
#            }]
#          })
        ]

        $scope.addFileInfoList = (options) ->
          fileInfoList = cradminBulkfileupload.createFileInfoList(options)
          $scope.fileInfoLists.push(fileInfoList)
          return fileInfoList

        return

      link: (scope, element, attr, uploadController) ->
        uploadController.setInProgressOrFinishedScope(scope)
        return
    }
])


.directive('djangoCradminBulkFileInfoList', [
  ->
    return {
      restrict: 'AE'
      scope: {
        fileInfoList: '=djangoCradminBulkFileInfoList'
      }
      templateUrl: 'bulkfileupload/fileinfolist.tpl.html'
      transclude: true

#      controller: ($scope) ->
#        return
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

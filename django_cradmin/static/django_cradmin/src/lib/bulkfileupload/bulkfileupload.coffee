
class DjangoCradminFileInfo
  constructor: (@file) ->

  getName: ->
    return @file.name


class DjangoCradminFileFieldWrapper
  constructor: (@fileFieldElement) ->
    @fileInfoList = []
    for file in @fileFieldElement[0].files
      @fileInfoList.push(new DjangoCradminFileInfo(file))


angular.module('djangoCradmin.bulkfileupload', [])

.directive 'djangoCradminBulkfileupload', ->
  return {
    restrict: 'A'
    scope: {
      config: '=djangoCradminBulkfileupload'
    }

    controller: ($scope) ->
      $scope._updateTotalForms = ->
        $scope.totalFormsElement.val("#{$scope.fileInfoListScope.fileFieldWrappers.length}")

      @setFileInfoListScope = (fileInfoListScope) ->
        $scope.fileInfoListScope = fileInfoListScope

      @setAddedFileFieldElementListScope = (addedFileFieldElementListScope) ->
        $scope.addedFileFieldElementListScope = addedFileFieldElementListScope

      @setFileFieldScope = (fileFieldScope) ->
        $scope.fileFieldScope = fileFieldScope
        formsetPrefix = fileFieldScope.formsetPrefix
        $scope.totalFormsElement = angular.element(
          document.getElementById("id_#{formsetPrefix}-TOTAL_FORMS"))

      @onFileAdded = (fileFieldElement) ->
        $scope.fileInfoListScope.addFileToList(fileFieldElement)
        $scope.addedFileFieldElementListScope.addFileFieldElement(fileFieldElement)
        $scope._updateTotalForms()

      @debugIsEnabled = ->
        return $scope.config?.debug?

      @getFileCount = ->
        return $scope.fileInfoListScope.fileFieldWrappers.length

      return

  }


.directive 'djangoCradminBulkfileuploadFileInfoList', ->
  return {
    require: '^djangoCradminBulkfileupload'
    restrict: 'A'
    scope: {}
    templateUrl: 'bulkfileupload/bulkfileupload-files.tpl.html'

    controller: ($scope) ->
      # List of DjangoCradminFileFieldWrapper objects
      $scope.fileFieldWrappers = []

      $scope.addFileToList = (fileFieldElement) ->
        fileFieldWrapper = new DjangoCradminFileFieldWrapper(fileFieldElement)
        $scope.fileFieldWrappers.push(fileFieldWrapper)
        $scope.$apply()

      $scope.getFlatFileInfoArray = ->
        flatFileInfoArray = []
        for fileFieldWrapper in $scope.fileFieldWrappers
          for fileInfo in fileFieldWrapper.fileInfoList
            flatFileInfoArray.push(fileInfo)
        return flatFileInfoArray

      return

    link: (scope, element, attr, bulkfileuploadController) ->
      bulkfileuploadController.setFileInfoListScope(scope)
      return
  }


.directive 'djangoCradminBulkfileuploadAddedFileFieldElementList', ->
  return {
    require: '^djangoCradminBulkfileupload'
    restrict: 'A'
    scope: {}

    controller: ($scope) ->
      $scope.addFileFieldElement = (fileFieldElement) ->
        console.log 'Add file element'
#        fileFieldElement.detach()
        $scope.element.append(fileFieldElement)
      return

    link: (scope, element, attr, bulkfileuploadController) ->
      scope.element = element
      bulkfileuploadController.setAddedFileFieldElementListScope(scope)
      if not bulkfileuploadController.debugIsEnabled()
        scope.element.addClass('ng-hide')

      return
  }


.directive 'djangoCradminBulkfileuploadFileField', ->
  return {
    require: '^djangoCradminBulkfileupload'
    restrict: 'A'
    scope: {
      formsetPrefix: '@formsetPrefix'
      filesfieldName: '@filesfieldName'
    }
    templateUrl: 'bulkfileupload/bulkfileupload-filefield.tpl.html'

    link: (scope, element, attr, bulkfileuploadController) ->
      bulkfileuploadController.setFileFieldScope(scope)
      scope.element = element

      scope._onFileFieldChange = (fileFieldElement) ->
        bulkfileuploadController.onFileAdded(fileFieldElement)
        scope._resetElement()

      scope._resetElement = ->
        fileCount = bulkfileuploadController.getFileCount()
        console.log fileCount
        scope.fileFieldElement = angular.element(
          "<input name='#{scope.formsetPrefix}-#{fileCount}-#{scope.filesfieldName}' type='file' multiple>")
        scope.element.append(scope.fileFieldElement)
        scope.fileFieldElement.on 'change', ->
          scope._onFileFieldChange(scope.fileFieldElement)

      scope._init = ->
        scope._resetElement()

      scope._init()
      return
  }

app.controller('FileUploadCtrl', ['$scope', 'Upload', '$timeout', function ($scope, Upload, $timeout) {

    $scope.$watch('files', function () {
        $scope.upload($scope.files);
    });

    $scope.$watch('file', function () {
        if ($scope.file != null) {
            $scope.files = [$scope.file]; 
        }
    });
    $scope.log = '';

    $scope.prc = {}
    $scope.matches = {}


    $scope.upload = function (files) {
        if (files && files.length) {
            for (var i = 0; i < files.length; i++) {
              var file = files[i];
              if (!file.$error) {
                Upload.upload({
                    url: 'files/submit',
                    data: {
                      username: $scope.username,
                      docfile: file  
                    }
                }).then(function (resp) {
                    $timeout(function() {
                        // console.log('RESPONSE 1 : ',resp)
                        $scope.log = 'file: ' +
                        resp.config.data.docfile.name +
                        ', Response: ' + JSON.stringify(resp.data) +
                        '\n';

                        $scope.matches[resp.data.name] = resp.data.match

                    });
                }, null, function (evt) {
                        // console.log('RESPONSE 2 : ',evt)

                    var progressPercentage = parseInt(100.0 *
                            evt.loaded / evt.total);
                    $scope.log = 'progress: ' + progressPercentage + 
                        '% ' + evt.config.data.docfile.name + '\n';

                    $scope.prc[evt.config.data.docfile.name] = progressPercentage
                });
              }
            }
        }
    };
}]);
// //inject directives and services.
// // var app = angular.module('fileUpload', ['ngFileUpload']);

// app.controller('FileUploadCtrl', ['$scope', 'Upload', function ($scope, Upload) {
//     // upload later on form submit or something similar
//     $scope.submit = function() {

//       console.log('FILES ',$scope.file)
//       console.log('UPLOAD ',Upload)

//       if ($scope.form.file.$valid && $scope.file) {
//         $scope.upload($scope.file);
//       }
//     };

//     // upload on file select or drop
//     $scope.upload = function (file) {
//         Upload.upload({
//             url: 'upload/url',
//             data: {file: file, 'username': $scope.username}
//         }).then(function (resp) {
//             console.log('Success ' + resp.config.data.file.name + 'uploaded. Response: ' + resp.data);
//         }, function (resp) {
//             console.log('Error status: ' + resp.status);
//         }, function (evt) {
//             var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
//             console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file.name);
//         });
//     };
//     // for multiple files:
//     $scope.uploadFiles = function (files) {
//       console.log('FILES ',files)
//       console.log('UPLOAD ',Upload)

//       if (files && files.length) {
//         // for (var i = 0; i < files.length; i++) {
//         //   Upload.upload({..., data: {file: files[i]}, ...})...;
//         // }
//         // or send them all together for HTML5 browsers:
//         // Upload.upload({data: {file: files},});
//         console.log('N FILES ',files.length)
//       }
//     }
// }]);
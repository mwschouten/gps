
var app = angular.module('nlogproduction', 
    ['ngCookies','ngRoute','ui.bootstrap','ngFileUpload','highcharts-ng'])


// var app = angular.module('fileUpload', ['ngFileUpload']);

app.config([
    '$httpProvider',
    '$interpolateProvider',
    function($httpProvider, $interpolateProvider) {
        $interpolateProvider.startSymbol('{{');
        $interpolateProvider.endSymbol('}}');
    }]);

app.run([
    '$http',
    '$cookies',
    function($http, $cookies) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    }]);

// set routing
app.config(function ($routeProvider) {

    $routeProvider
        .when('/',{ redirectTo: '/index'})
        .when('/index',
            {controller: 'TestCtrl',
             templateUrl: 'static/base/partials/entry.html'
            })
        .when('/submit',
            {controller: 'FileUploadCtrl',
             templateUrl: 'static/upload/partials/submit.html'
            })

        // .when('/view',
        //     {controller: 'ViewCtrl',
        //      templateUrl: 'static/base/partials/view.html'
        //     })
        // .otherwise({ redirectTo: '/'});
});

// app.filter('unique', function() {
//   return function (items) {
//     itemsnew = new Object(items)
//     var msgs = []
//     var counts = {}
//     var key = new Object()
//     for ( key in itemsnew){
        
//         var msg = itemsnew[key]
//         if (msg.indexOf("Ok,") === 0) msg = "Download OK"
//         if (msgs.indexOf( msg ) == -1){
//             msgs.push( msg )
//             counts[ msg ] = 0
//         }
//         counts[ msg ] += 1
//     }
//     return counts
//   };
// })

console.log('klaar')

/* global angular */


var app = angular.module(
    'scool',
    [
        'ngResource',
        'ngCookies',
        'ui.router',
        'ui.bootstrap',
        'ui.select2'
    ]
);


app.controller('IndexCtrl', function ($scope, $log, $rootScope, $location, $state, AUTH_EVENTS, Auth) {
    'use strict';



    $scope.go = function (path) {
        $location.path(path);
    };

    console.log('IndexCtrl');

    $rootScope.$on('unauthorized', function () {
        $state.go('public.login');
    });

    $rootScope.$on('loginFailure', function () {
        console.error('Login failed');
    });

    $rootScope.$on('loginSuccess', function () {
        $state.go('user.home');
    });

    $rootScope.$on('logoutSuccess', function () {
        $state.go('public.login');
    });


    $scope.logout = function () {
        $log.info('Logging out');

        Auth.logout();
    };

    $scope.current_user = Auth.getCurrentUser();
    if ($scope.current_user === undefined) {
        var x = $state.go('public.login').then(function () { console.log('good'); }, function (x) {console.log(x)});
    }

    console.log($scope.current_user);
    $rootScope.$on('$stateChangeStart',function(event, toState, toParams, fromState, fromParams){
        console.log(toState);
        console.log(toParams);

        console.log('$stateChangeStart to '+toState.to+'- fired when the transition begins. toState,toParams : \n',toState, toParams);
    });
     $rootScope.$on('$stateChangeError',
    function (event, toState, toParams, fromState, fromParams, error) {
        $log.debug(error);
        $state.go('login');
    });


});


app.controller('ErrorCtrl', function () {
});

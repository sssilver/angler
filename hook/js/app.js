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
        $state.go('public.login');  // TODO: This fails :(
    }

});


app.controller('ErrorCtrl', function () {
});

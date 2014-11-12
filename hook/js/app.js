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

    $scope.loginFailure = false;

    $scope.go = function (path) {
        $location.path(path);
    };

    $scope.closeLoginFailure = function () {
        $scope.loginFailure = false;
    };

    $rootScope.$on('unauthorized', function () {
        $state.go('public.login');
    });

    $rootScope.$on('loginFailure', function () {
        $scope.loginFailure = true;
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
    Auth.verify();  // Verify that the user is actually logged in

    if ($scope.current_user === undefined) {
        $state.go('public.login');  // TODO: This fails :(
    }

    $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
        if (toState.data.access.indexOf('public') == -1)
            Auth.verify();
    });

    $rootScope.closeAlert = function (index) {
        $rootScope.alerts.splice(index, 1);
    };

});


app.controller('ErrorCtrl', function () {
});

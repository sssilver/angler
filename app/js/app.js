/* global angular */


var app = angular.module(
    'scool',
    [
        'ngResource',
        'ui.router',
        'ui.bootstrap',
        'ui.select2'
    ]
);


app.controller('IndexCtrl',
    ['$scope', '$log', '$rootScope', '$location', '$state', 'AUTH_EVENTS', 'Auth', 'ROLES',
        function ($scope, $log, $rootScope, $location, $state, AUTH_EVENTS, Auth, ROLES) {

    'use strict';

    $scope.current_user = {role: 'public'};
    $scope.is_authorized = Auth.is_authorized;


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


    /*
    $rootScope.$on('$stateChangeStart',
        function (event, toState, toParams, fromState, fromParams) {
            console.log(fromState);
            console.log(toState);
            if (toState.data !== undefined && !Auth.is_authorized(toState.data.access)) {
                $rootScope.error = 'Access denied';
                event.preventDefault();

                if (fromState.url === '^') {
                    if (Auth.is_authenticated()) {
                        console.log('Authenticated. Going home.');
                        $state.go('user.home');
                    } else {
                        console.log('NOT Authenticated. Going to login.');
                        $rootScope.error = null;
                        $state.go('public.login');
                    }
                }
            }
        }
    );

    console.log('Broadcasting a $stateChangeStart');
    $rootScope.$broadcast('$stateChangeStart', $state, null, $state, null);
    */

}]);


app.controller('ErrorCtrl',
    ['$scope', '$rootScope', '$location', '$state', 'AUTH_EVENTS', 'Auth', 'ROLES',
        function ($scope, $rootScope, $location, $state, AUTH_EVENTS, Auth, ROLES) {
    console.log('error controller');
}]);

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
    ['$scope', '$rootScope', '$location', '$state', 'AUTH_EVENTS', 'Auth', 'ROLES',
        function($scope, $rootScope, $location, $state, AUTH_EVENTS, Auth, ROLES) {

    $scope.current_user = {role: 'public'};
    $scope.is_authorized = Auth.is_authorized;


    $scope.go = function(path) {
        $location.path(path);
    };

    $rootScope.$on('$stateChangeStart',
        function(event, toState, toParams, fromState, fromParams) {
            if (!Auth.is_authorized(toState.data.access)) {
                $rootScope.error = 'Access denied';
                event.preventDefault();

                if (fromState.url === '^') {
                    if (Auth.is_authenticated())
                        $state.go('user.home');
                    else {
                        $rootScope.error = null;
                        $state.go('public.login');
                    }
                }
            }
        }
    );

}]);

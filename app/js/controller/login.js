app.controller(
    'LoginCtrl',
        ['$scope', '$log', '$modal', 'Model', 'Auth',
            function($scope, $log, $modal, Model, Auth) {

    $scope.login = function(email, password) {
        $log.info('Logging in ' + email);

        Auth.login({
            email: email,
            password: password
        }).then(function () {
            $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
        }, function () {
            $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
        });
    };

}]);
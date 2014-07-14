app.controller(
    'LoginCtrl',
        ['$scope', '$log', '$rootScope', '$modal', 'Model', 'Auth',
            function ($scope, $log, $rootScope, $modal, Model, Auth) {

    // TODO: Remove these
    $scope.email = 'sssilver@gmail.com';
    $scope.password = 'aoeu';

    $scope.login = function (email, password) {
        $log.info('Logging in ' + email);

        Auth.login({email: email, password: password});
    };
}]);
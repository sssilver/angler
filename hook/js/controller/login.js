app.controller('LoginCtrl', function ($scope, $log, $rootScope, $modal, Model, Auth) {
    $scope.login = function () {
        $log.info('Logging in ' + $scope.email);

        console.log($scope.email);
        Auth.login({email: $scope.email, password: $scope.password});
    };
});
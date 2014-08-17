app.controller('LoginCtrl', function ($scope, $log, $rootScope, $modal, Model, Auth) {
    $scope.login = function (email, password) {
        $log.info('Logging in ' + email);

        Auth.login({email: email, password: password});
    };
});
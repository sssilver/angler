app.controller(
    'LoginCtrl',
        ['$scope', '$log', '$modal', 'Model',
            function($scope, $log, $modal, Model) {

    $scope.login = function() {
        alert('boom');
    }

}]);
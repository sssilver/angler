var app = angular.module('scool', ['ngRoute', 'ngResource', 'ui.bootstrap']);

app.controller('IndexCtrl', ['$scope', '$location', function($scope, $location) {
    $scope.go = function(path) {
        $location.path(path);
    };
}]);
var app = angular.module(
    'scool',
    [
        'ngResource',
        'ui.router',
        'ui.bootstrap',
        'ui.select2'
    ]
);

app.controller('IndexCtrl', ['$scope', '$location', function($scope, $location) {
    $scope.go = function(path) {
        $location.path(path);
    };

    $scope.tests = [
        {id: 1, name: 'one'},
        {id: 2, name: 'two'},
        {id: 3, name: 'three'}
    ];

}]);

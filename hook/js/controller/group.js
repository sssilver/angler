app.controller(
    'GroupsCtrl',
        ['$scope', '$log', '$modal', 'Model',
            function ($scope, $log, $modal, Model) {

    $scope.refresh = function () {
        groups = Model.query({'model': 'group'}, function () {
            $scope.groups = groups;
        });
    };

    $scope.remove = function (id) {
        if (confirm('Are you sure?')) {
            Model.remove({'model': 'group', 'id': id}, function () {
                $scope.refresh();
            });
        }
    };

    $scope.refresh();
}]);

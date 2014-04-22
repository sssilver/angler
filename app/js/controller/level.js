app.controller(
    'LevelsCtrl',
        ['$scope', '$log', '$modal', 'Model', 'TIMES', 'DAYS',
            function($scope, $log, $modal, Model, TIMES, DAYS) {

    $scope.dlgLevel = function(level) {

        if (level)
            $scope.level = level;
        else
            $scope.level = {};

        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-level.html',
            controller: 'LevelFormCtrl',
            resolve: {
                level: function() {
                    return $scope.level;
                }
            }
        });

        modalInstance.result.then(function(level) {
            level_service = new Level(level);

            if (level.id) {
                level_service.$save({'id': level.id}, function() {
                    $scope.refresh();
                });
            } else {
                level_service.$post(function() {
                    $scope.refresh();
                });
            }
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function() {
        levels = Model.query({'model': 'level'}, function() {
            $scope.levels = levels;
        });
    }

    $scope.remove = function(id) {
        if (confirm('Are you sure?')) {
            Level.remove({'id': id}, function() {
                $scope.refresh();
            });
        }
    }

    $scope.refresh();
}]);


app.controller(
    'LevelFormCtrl',
        ['$scope', '$modalInstance', 'level',
            function($scope, $modalInstance, level) {

    $scope.level = level;

    $scope.ok = function() {
        $modalInstance.close($scope.level);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

}]);

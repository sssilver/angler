app.controller(
    'LevelsCtrl',
        ['$scope', '$log', '$modal', 'Level', 'TIMES', 'DAYS',
            function($scope, $log, $modal, Level, TIMES, DAYS) {

    $scope.dlgAddLevel = function() {
        var modalInstance = $modal.open({
            templateUrl: 'template/form-level.html',
            controller: 'LevelFormCtrl'
        });

        modalInstance.result.then(function(level) {
            level.$post(function() {
                $scope.refresh();
            });
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function() {
        levels = Level.query(function() {
            $scope.levels = levels;
            console.log($scope.levels);
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
        ['$scope', '$modalInstance', 'Level',
            function($scope, $modalInstance, Level) {


    $scope.level = new Level();

    $scope.ok = function() {
        $modalInstance.close($scope.level);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

}]);

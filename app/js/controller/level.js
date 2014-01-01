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
            level.$save();
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

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

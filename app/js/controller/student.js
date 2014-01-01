app.controller(
    'StudentsCtrl',
        ['$scope', '$log', 'Student', 'TIMES', 'DAYS', '$modal',
            function($scope, $log, Student, TIMES, DAYS, $modal) {

    $scope.open = function () {

        var modalInstance = $modal.open({
            templateUrl: 'template/form-student.html',
            controller: 'StudentFormCtrl',
            resolve: {
                items: function () {
                    return $scope.items;
                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };



    $scope.dlgAddStudent = function() {
        $scope.isShowDlgAddStudent = true;
        console.log('must show now');
    }

    $scope.registerStudent = function() {

        $scope.student.$save();
    }

}]);


app.controller(
    'StudentFormCtrl',
        ['$scope', 'Student', 'TIMES', 'DAYS',
            function($scope, Student, TIMES, DAYS) {


    $scope.times = TIMES;
    $scope.days = DAYS;
    $scope.student = new Student({'availabilities': []});

    for (var i in DAYS)
        $scope.student.availabilities[i] = [];

    //$scope.items = Students.query();

    $scope.addAvailability = function(day) {
        console.log('Adding availability for day ' + day.toString());
        $scope.student.availabilities[day].push([0, 0]);
    }

    $scope.removeAvailability = function(day, availability) {
        console.log('Removing availability #' + availability.toString() + ' from day ' + day.toString());
        $scope.student.availabilities[day].splice(availability, 1);
    }
}]);

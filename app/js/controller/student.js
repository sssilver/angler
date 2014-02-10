app.controller(
    'StudentsCtrl',
        ['$scope', '$log', 'Student', 'TIMES', 'DAYS', '$modal',
            function($scope, $log, Student, TIMES, DAYS, $modal) {

    $scope.dlgAddStudent = function() {
        var modalInstance = $modal.open({
            templateUrl: 'template/form-student.html',
            controller: 'StudentFormCtrl'
        });

        modalInstance.result.then(function(student) {
            student.$post(function() {
                $scope.refresh();
            });
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function() {
        students = Student.query(function() {
            $scope.students = students;
            console.log($scope.students);
        });
    }

    $scope.remove = function(id) {
        if (confirm('Are you sure?')) {
            Student.remove({'id': id}, function() {
                $scope.refresh();
            });
        }
    }

    $scope.refresh();
}]);


app.controller(
    'StudentFormCtrl',
        ['$scope', '$modalInstance', 'Student', 'TIMES', 'DAYS',
            function($scope, $modalInstance, Student, TIMES, DAYS) {


    $scope.times = TIMES;
    $scope.days = DAYS;
    $scope.student = new Student({'availabilities': []});

    for (var i in DAYS)
        $scope.student.availabilities[i] = [];

    $scope.addAvailability = function(day) {
        console.log('Adding availability for day ' + day.toString());
        $scope.student.availabilities[day].push([0, 0]);
    }

    $scope.removeAvailability = function(day, availability) {
        console.log('Removing availability #' + availability.toString() + ' from day ' + day.toString());
        $scope.student.availabilities[day].splice(availability, 1);
    }

    $scope.ok = function() {
        $modalInstance.close($scope.student);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

}]);

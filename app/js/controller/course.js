app.controller(
    'CoursesCtrl',
        ['$scope', '$log', '$modal', 'Model', 'TIMES', 'DAYS',
            function($scope, $log, $modal, Model, TIMES, DAYS) {

    $scope.dlgCourse = function(course) {

        if (course)
            $scope.course = course;
        else
            $scope.course = {};

        var modalInstance = $modal.open({
            templateUrl: 'template/form-course.html',
            controller: 'CourseFormCtrl',
            resolve: {
                course: function() {
                    return $scope.course;
                }
            }
        });

        modalInstance.result.then(function(course) {
            course_service = new Model(course);

            if (course.id) {
                course_service.$save({'model': 'course', 'id': course.id}, function() {
                    $scope.refresh();
                });
            } else {
                course_service.$post({'model': 'course'}, function() {
                    $scope.refresh();
                });
            }
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function() {
        courses = Model.query({'model': 'course'}, function() {
            $scope.courses = courses;
        });
    }

    $scope.remove = function(id) {
        if (confirm('Are you sure?')) {
            Model.remove({'model': 'course', 'id': id}, function() {
                $scope.refresh();
            });
        }
    }

    $scope.refresh();
}]);


app.controller(
    'CourseFormCtrl',
        ['$scope', '$modalInstance', 'course',
            function($scope, $modalInstance, course) {

    $scope.course = course;

    $scope.ok = function() {
        $modalInstance.close($scope.course);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

}]);

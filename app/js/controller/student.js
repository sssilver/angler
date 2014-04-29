app.controller(
    'StudentsCtrl',
        ['$scope', '$routeParams', '$log', 'Student', 'Model', 'TIMES', 'DAYS', '$modal',
            function($scope, $routeParams, $log, Student, Model, TIMES, DAYS, $modal) {

    if ($routeParams.student_id) {  // Detail view?
        $scope.refresh_student = function() {
            // Load the requested student
            student = Model.query(
                {
                    model: 'student',
                    id: $routeParams.student_id
                },
                function() {
                    $scope.student = student;
                    console.log(student);
                }
            );
        }

        $scope.refresh_student();
    }

    $scope.dlgAddStudent = function() {
        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-student.html',
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

    $scope.dlgEditStudent = function(student) {
        // TODO
        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-student.html',
            controller: 'StudentFormCtrl'
        });
    }

    $scope.dlgPayment = function(student) {
        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-payment.html',
            controller: 'StudentPaymentDialogCtrl',
            resolve: {
                student: function() {
                    return $scope.student;
                }
            }
        });

        modalInstance.result.then(function(transaction) {
            transaction_service = new Model(transaction);

            transaction_service.$post(
                {'model': 'student-transaction'},
                function() {
                    $scope.refresh_student();
                }
            );
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    }

    $scope.dlgRefund = function(student) {
        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-refund.html',
            controller: 'StudentRefundDialogCtrl',
            resolve: {
                student: function() {
                    return $scope.student;
                }
            }
        });

        modalInstance.result.then(function(transaction) {
            transaction_service = new Model(transaction);

            transaction_service.$post(
                {'model': 'student-transaction'},
                function() {
                    $scope.refresh_student();
                }
            );
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    }

    $scope.refresh();
}]);


app.controller(
    'StudentFormCtrl',
        ['$scope', '$modalInstance', 'Student', 'Level', 'TIMES', 'DAYS',
            function($scope, $modalInstance, Student, Level, TIMES, DAYS) {


    $scope.times = TIMES;
    $scope.days = DAYS;
    $scope.student = new Student({'availabilities': []});

    levels = Level.query(function() {
        $scope.levels = levels.objects;
    });


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


app.controller(
    'StudentPaymentDialogCtrl',
        ['$scope', '$log', '$modalInstance', '$modal', 'student', 'Model',
            function($scope, $log, $modalInstance, $modal, student, Model) {

    $scope.student = student;
    $scope.transaction = {
        student_id: student.id
    }

    $scope.ok = function() {
        $modalInstance.close($scope.transaction);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

}]);


app.controller(
    'StudentRefundDialogCtrl',
        ['$scope', '$log', '$modalInstance', '$modal', 'student', 'Model',
            function($scope, $log, $modalInstance, $modal, student, Model) {

    $scope.student = student;
    $scope.transaction = {
        student_id: student.id
    }

    $scope.ok = function() {
        $modalInstance.close($scope.transaction);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

}]);

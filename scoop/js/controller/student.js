app.controller(
    'StudentsCtrl',
        ['$scope', '$stateParams', '$log', '$location', 'Model', 'TIMES', 'DAYS', '$modal',
            function ($scope, $stateParams, $log, $location, Model, TIMES, DAYS, $modal) {

    if ($stateParams.student_id) {  // Detail view?
        $scope.refresh_student = function () {
            // Load the requested student
            student = Model.query(
                {
                    model: 'student',
                    id: $stateParams.student_id
                },
                function () {
                    $scope.student = student;
                    console.log(student);
                }
            );
        };

        $scope.refresh_student();
    }

    $scope.dlgAddStudent = function () {
        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-student.html',
            controller: 'StudentFormCtrl'
        });

        modalInstance.result.then(function (student) {
            student.$post(function () {
                $scope.refresh();
            });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.dlgGroups = function (students) {
        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-groups.html',
            controller: 'GroupsDialogCtrl',
            resolve: {
                students: function () {
                    return students;
                }
            }
        });

        modalInstance.result.then(function (group) {
            var filters = [];

            for (var i = 0; i < students.length; ++i) {
                var student = students[i];

                filters.push({
                    'name': 'id',
                    'op': '==',
                    'val': student.id
                });
            }

            students_data = {add_group_id: group.id};

            var student_service = new Model(students_data);

            student_service.$save({
                model: 'student',
                q: JSON.stringify({
                    filters: filters,
                    disjunction: true
                })
            });



        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function (query) {
        students = Model.query({model: 'student'}, function () {
            $scope.students = students;
            console.log($scope.students);
        });
    };

    $scope.viewStudent = function (studentID) {
        console.log($location);

        $location.path('/students/' + studentID);
    };

    $scope.selectStudent = function (student) {
        var index = $scope.selectedStudents.indexOf(student);

        if (index > -1)  // Deselect
          $scope.selectedStudents.splice(index, 1);
        else             // Select
          $scope.selectedStudents.push(student);
    };

    $scope.listAllStudents = function () {
        $scope.refresh();  // no query filter
    };

    $scope.listPendingStudents = function () {
        //[{"name":"computers__manufacturer","op":"any","val":"Apple"}]
        /*
        var query = [{
            'name': 'groups',
            'op': 'is_
        }]
        */
    };

    $scope.remove = function (id) {
        if (confirm('Are you sure?')) {
            Student.remove({'id': id}, function () {
                $scope.refresh();
            });
        }
    };

    $scope.dlgEditStudent = function (student) {
        // TODO
        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-student.html',
            controller: 'StudentFormCtrl'
        });
    };

    $scope.dlgPayment = function (student) {
        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-payment.html',
            controller: 'StudentPaymentDialogCtrl',
            resolve: {
                student: function () {
                    return $scope.student;
                }
            }
        });

        modalInstance.result.then(function (transaction) {
            transaction_service = new Model(transaction);

            transaction_service.$post(
                {'model': 'student-transaction'},
                function () {
                    $scope.refresh_student();
                }
            );
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.dlgRefund = function (student) {
        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-refund.html',
            controller: 'StudentRefundDialogCtrl',
            resolve: {
                student: function () {
                    return $scope.student;
                }
            }
        });

        modalInstance.result.then(function (transaction) {
            transaction_service = new Model(transaction);

            transaction_service.$post(
                {'model': 'student-transaction'},
                function () {
                    $scope.refresh_student();
                }
            );
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh();
    $scope.selectedStudents = [];
}]);


app.controller(
    'StudentFormCtrl',
        ['$scope', '$modalInstance', 'Student', 'Level', 'TIMES', 'DAYS',
            function ($scope, $modalInstance, Student, Level, TIMES, DAYS) {


    $scope.times = TIMES;
    $scope.days = DAYS;
    $scope.student = new Student({'availabilities': []});

    levels = Model.query({model: 'level'}, function () {
        $scope.levels = levels.objects;
    });


    for (var i in DAYS)
        $scope.student.availabilities[i] = [];

    $scope.addAvailability = function (day) {
        console.log('Adding availability for day ' + day.toString());
        $scope.student.availabilities[day].push([0, 0]);
    };

    $scope.removeAvailability = function (day, availability) {
        console.log('Removing availability #' + availability.toString() + ' from day ' + day.toString());
        $scope.student.availabilities[day].splice(availability, 1);
    };

    $scope.ok = function () {
        $modalInstance.close($scope.student);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);


app.controller(
    'StudentPaymentDialogCtrl',
        ['$scope', '$log', '$modalInstance', '$modal', 'student', 'Model',
            function ($scope, $log, $modalInstance, $modal, student, Model) {

    $scope.student = student;
    $scope.transaction = {
        student_id: student.id
    };

    $scope.ok = function () {
        $modalInstance.close($scope.transaction);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);


app.controller(
    'StudentRefundDialogCtrl',
        ['$scope', '$log', '$modalInstance', '$modal', 'student', 'Model',
            function ($scope, $log, $modalInstance, $modal, student, Model) {

    $scope.student = student;
    $scope.transaction = {
        student_id: student.id
    };

    $scope.ok = function () {
        $modalInstance.close($scope.transaction);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);


app.controller(
    'GroupsDialogCtrl',
        ['$scope', '$log', '$modalInstance', '$modal', 'students', 'Model',
            function ($scope, $log, $modalInstance, $modal, students, Model) {

    $scope.students = students;
    $scope.selected_group = {};

    courses = Model.query({model: 'course'}, function () {
        $scope.courses = courses.objects;
    });

    $scope.populateLevels = function (course) {
        levels = Model.query(
            {
                model: 'level',
                course_id: course.id
            },
            function () {
                $scope.levels = levels.objects;
            }
        );
    };

    $scope.populateGroups = function (level, teacher) {
        if (!level || !teacher) {
            $scope.groups = [];

            return;
        }

        groups = Model.query(
            {
                model: 'group',
                level_id: level.id,
                teacher_id: teacher.id
            },
            function () {
                $scope.groups = groups.objects;
            }
        );
    };

    $scope.createGroup = function (level, teacher) {
        var title;

        if (!(title = prompt('Level title')))
            return;

        group_service = new Model({
            title: title,
            level_id: level.id,
            teacher_id: teacher.id
        });

        group_service.$post({
            model: 'group'
        }, function () {
            $scope.populateGroups(level, teacher);
        });
    };

    $scope.ok = function () {
        $modalInstance.close($scope.selected_group.data);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);

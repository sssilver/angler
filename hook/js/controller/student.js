app.controller(
    'StudentsCtrl',
        ['$scope', '$q', '$state', '$stateParams', '$log', '$location', '$resource', 'Model', 'TIMES', 'DAYS', '$modal',
            function ($scope, $q, $state, $stateParams, $log, $location, $resource, Model, TIMES, DAYS, $modal) {

    if ($stateParams.student_id) {  // Detail view?
        $scope.refresh_student = function () {
            // Load the requested student
            var student = Model.query(
                {
                    model: 'student',
                    resource_id: $stateParams.student_id
                },
                function () {
                    $scope.student = student;
                    console.log(student);
                }
            );
        };

        $scope.refresh_student();
    }

    $scope.dlgStudent = function (student) {
        if (student)
            $scope.student = student;
        else
            $scope.student = {};

        console.log(student);

        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-student.html',
            controller: 'StudentFormCtrl',
            resolve: {
                student: function () {
                    return $scope.student;
                }
            }
        });

        modalInstance.result.then(function (student) {
            delete student.balance;  // Remove the hybrid property

            var student_service = new Model(student);

            if (student.id) {
                student_service.$save(
                    {model: 'student', resource_id: student.id},
                    function () {
                        $scope.refresh();
                    }
                );
            } else {
                student_service.$post(
                    {model: 'student'},
                    function () {
                        $scope.refresh();
                    }
                )
            }
            console.log(student);
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

        modalInstance.result.then(function (result) {
            // Add students
            // TODO: This currently being done one-by-one, due to a limitation
            // of flask-restless. Must fix this sometime in the future.
            var promises = [];

            for (var i = 0; i < students.length; ++i) {
                var student_group = {
                    student_id: students[i].id,
                    group_id: result.group.id,
                    tariff_id: result.tariff.id
                };

                student_group_service = new Model(student_group);

                promises.push(student_group_service.$post(
                    {'model': 'student_group'}
                ));
            }

            $q.all(promises).then(
                function () {
                    console.info('added all students to the group');
                }
            );

        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function () {
        var students = Model.query({model: 'student'}, function () {
            $scope.students = students;
            console.log($scope.students);
        });
    };

    $scope.viewStudent = function (student_id) {
        console.log($location);

        $state.go('.view', {student_id: student_id});
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
            Model.remove({model: 'student', resource_id: id}, function () {
                $scope.refresh();
            });
        }
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
            var transaction_service = new Model(transaction);

            transaction_service.$post(
                {model: 'student-transaction'},
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
        ['$scope', '$modalInstance', 'Model', 'student',
            function ($scope, $modalInstance, Model, student) {

    $scope.student = student;
    console.log(student);

    var levels = Model.query({model: 'level'}, function () {
        $scope.levels = levels.objects;
    });


    /*
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
    */

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
    $scope.selected_tariff = {};

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
        $modalInstance.close({
            group: $scope.selected_group.data,
            tariff: $scope.selected_tariff.data
        });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);

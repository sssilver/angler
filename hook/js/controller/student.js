app.controller(
    'StudentsCtrl',
        ['$scope', '$q', '$state', '$stateParams', '$log', '$location', '$resource', 'Model', 'TIMES', 'DAYS', '$modal', 'Credit',
            function ($scope, $q, $state, $stateParams, $log, $location, $resource, Model, TIMES, DAYS, $modal, Credit) {

    if ($stateParams.student_id) {  // Detail view?
        $scope.refreshStudent = function () {
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

        $scope.refreshStudent();
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
            // Add students to the group
            var members = [];

            for (var i = 0; i < students.length; ++i) {
                members.push({
                    student_id: students[i].id,
                    tariff_id: result.tariff.id
                });
            }

            var group_service = new Model({members: members});

            group_service.$post({model: 'group', resource_id: result.group.id}, function () {
                $scope.refresh();
            });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function () {
        var students = Model.query({model: 'student'}, function () {
            $scope.students = students.items;
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

    $scope.dlgCredit = function (student) {
        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-credit.html',
            controller: 'StudentCreditDialogCtrl',
            resolve: {
                student: function () {
                    return $scope.student;
                }
            }
        });

        modalInstance.result.then(function (transaction) {
            var creditService = new Credit(transaction);

            creditService.$post(
                {
                    type: 'student',
                    entity_id: $scope.student.id
                },
                function () {
                    $scope.refreshStudent();
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
            var transaction_service = new Model(transaction);

            transaction_service.$post(
                {'model': 'student-transaction'},
                function () {
                    $scope.refreshStudent();
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

    var teachers = Model.query({model: 'staff'}, function () {
        $scope.teachers = teachers.items;
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
    'StudentCreditDialogCtrl',
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

    var courses = Model.query({model: 'course'}, function () {
        $scope.courses = courses.items;
    });

    var teachers = Model.query({model: 'staff'}, function () {
        $scope.teachers = teachers.items;
    });

    $scope.populateTariffs = function (course) {
        var tariffs = Model.query(
            {
                model: 'tariff',
                course_id: course.id
            },
            function () {
                $scope.tariffs = tariffs.items;
            }
        );
    };

    $scope.populateLevels = function (course) {
        var levels = Model.query(
            {
                model: 'level',
                course_id: course.id
            },
            function () {
                $scope.levels = levels.items;
            }
        );
    };

    $scope.populateGroups = function (level, teacher) {
        if (!level || !teacher) {
            $scope.groups = [];
            return;
        }

        var groups = Model.query({
            model: 'group',
            teacher_id: teacher.id,
            level_id: level.id
        }, function () {
            $scope.groups = groups.items;

            console.log(groups);
        });
    };

    $scope.createGroup = function (level, teacher) {
        var title;
        $scope.selection = {};

        if (!(title = prompt('Group title')))
            return;

        var group_service = new Model({
            title: title,
            level: level.id,
            teacher: teacher.id
        });

        group_service.$post({
            model: 'group'
        }).then(function (response) {
            $scope.populateGroups(level, teacher);
            console.log(response);
            console.log($scope.selection.group);
            $scope.selection.group = response.data;
        });
    };

    $scope.ok = function () {
        $modalInstance.close($scope.selection);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);

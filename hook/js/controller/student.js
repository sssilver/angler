app.controller('StudentsCtrl', function ($scope, $q, $state, $stateParams, $log, $location, Restangular, TIMES, DAYS, $modal) {

    if ($stateParams.student_id) {  // Detail view?
        $scope.refreshStudent = function () {
            // Load the requested student
            var student_id = $stateParams.student_id;
            Restangular.one('student', student_id).get().then(function (student) {
                $scope.student = student;
            });

            Restangular.all('group').getList({student_id: student_id}).then(function (groups) {
                $scope.groups = groups;
            });
        };

        $scope.refreshStudent();
    }

    $scope.dlgStudent = function (student) {
        if (student)
            $scope.student = student;
        else
            $scope.student = Restangular.one('student');

        $modal.open({
            templateUrl: 'template/dlg-student.html',
            controller: 'StudentFormCtrl',
            resolve: {
                student: function () {
                    return $scope.student;
                }
            }
        }).result.then(function (student) {
            student.save().then(function () {
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
        Restangular.all('student').getList().then(function (students) {
            $scope.students = students;
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
        $modal.open({
            templateUrl: 'template/dlg-credit.html',
            controller: 'StudentCreditDialogCtrl',
            resolve: {
                student: function () {
                    return $scope.student;
                }
            }
        }).result.then(function (transaction) {
            var studentCredit = Restangular.all('credit').one('student', $scope.student.id);

            studentCredit.doPOST(transaction).then(function () {
                $scope.refreshStudent();
            });
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
});


app.controller('StudentFormCtrl', function ($scope, $modalInstance, student, Restangular) {

    $scope.student = student;

    Restangular.all('staff').getList().then(function (teachers) {
        $scope.teachers = teachers;
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
});


app.controller('StudentCreditDialogCtrl', function ($scope, $log, $modalInstance, $modal, student) {
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

});


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


app.controller('GroupsDialogCtrl', function ($scope, $log, $modalInstance, $modal, students, Restangular) {

    $scope.students = students;
    $scope.selected_group = {};
    $scope.selected_tariff = {};



    Restangular.all('course').getList().then(function (courses) {
        $scope.courses = courses;
    });

    Restangular.all('staff').getList().then(function (staffs) {
        $scope.teachers = staffs;
    });

    $scope.populateTariffs = function (course) {
        Restangular.all('tariff').getList({course_id: course.id}).then(function (tariffs) {
            $scope.tariffs = tariffs;
        });
    };

    $scope.populateLevels = function (course) {
        Restangular.all('level').getList({course_id: course.id}).then(function (levels) {
            $scope.levels = levels;
        });
    };

    $scope.populateGroups = function (level, teacher) {
        if (!level || !teacher) {
            $scope.groups = [];
            return;
        }

        Restangular.all('group').getList({teacher_id: teacher.id, level_id: level.id}).then(function (groups) {
            $scope.groups = groups;
        });
    };

    $scope.createGroup = function (level, teacher) {
        var title;

        if (!(title = prompt('Group title')))
            return;

        var group = Restangular.one('group');
        group.title = title;
        group.level = level.id;
        group.teacher = teacher.id;

        group.save().then(function (response) {
            $scope.populateGroups(level, teacher);
            console.log(response);
            console.log($scope.selection);
            console.log(response.data);
            $scope.selection.group = response;
            console.log($scope.selection);
        });
    };

    $scope.ok = function () {
        $modalInstance.close($scope.selection);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

});

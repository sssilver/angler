app.controller('GroupsCtrl', function ($scope, $log, $modal, Restangular) {

    $scope.dlgGroup = function (group) {
        if (group)
            $scope.group = group;
        else
            $scope.group = Restangular.one('group');

        $modal.open({
            templateUrl: 'template/dlg-group.html',
            controller: 'GroupDialogCtrl',
            resolve: {
                group: function () {
                    return $scope.group;
                }
            }
        }).result.then(function (group) {
            group.save().then(function () {
                $scope.refresh();
            });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.manageStudents = function (group) {
        $modal.open({
            templateUrl: 'template/dlg-group-students.html',
            controller: 'ManageStudentsDialogCtrl',
            resolve: {
                group: function () {
                    return group;
                }
            }
        }).result.then(function () {
            $scope.refresh();
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function () {
        Restangular.all('group').getList().then(function (groups) {
            $scope.groups = groups;
        });
    };

    $scope.remove = function (group) {
        if (confirm('Are you sure?')) {
            Restangular.one('group', group.id).remove().then(function () {
                $scope.refresh();
            });
        }
    };

    $scope.refresh();
});


app.controller('GroupDialogCtrl', function ($scope, $log, $modalInstance, $modal, Restangular, group) {
    $scope.group = group;
    $scope.selectedCourse = null;

    if ($scope.group.level_id) {  // Group level is set, we need to populate the courses accordingly
        Restangular.one('level', $scope.group.level_id).get().then(function (level) {
            $scope.selectedCourse = level.course_id;
            $scope.populateLevels();
        });
    }

    Restangular.all('staff').getList().then(function (staffs) {
        $scope.teachers = staffs;
    });

    Restangular.all('course').getList().then(function (courses) {
        $scope.courses = courses;
    });

    $scope.populateLevels = function () {
        Restangular.all('level').getList({course_id: $scope.selectedCourse}).then(function (levels) {
            $scope.levels = levels;
        });
    };

    $scope.ok = function () {
        $modalInstance.close($scope.group);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});


app.controller('ManageStudentsDialogCtrl', function ($scope, $log, $modalInstance, $modal, Restangular, group) {
    $scope.group = group;

    Restangular.one('level', group.level_id).get().then(function (level) {
        $scope.level = level;
        Restangular.all('tariff').getList({course_id: level.course_id}).then(function (tariffs) {
            $scope.tariffs = tariffs;
        });
    });

    Restangular.all('company').getList().then(function (companies) {
        $scope.companies = companies;
    });

    $scope.validateAdd = function () {
        if (!$scope.tariff) return false;

        return ($scope.tariff.type == 'student') || ($scope.tariff.type == 'company' && $scope.company);
    };

    $scope.addMember = function (student, group, tariff, company) {
        var membership = {
            student_id: student.id,
            tariff_id: tariff.id
        };

        if (company)  // For corporate tariff memberships
            membership.company_id = company.id;

        Restangular.one('group', group.id).all('memberships').post([membership]).then(function () {
            $scope.refresh();
        });
    };

    $scope.removeMember = function (group, membership) {
        if (confirm('Are you sure?')) {
            Restangular.one('group', group.id).one('memberships', membership.id).remove().then(function () {
                $scope.refresh();
            });
        }
    };

    $scope.refresh = function () {
        Restangular.all('student').getList().then(function (students) {
            $scope.allStudents = students;
        });

        Restangular.one('group', $scope.group.id).get().then(function (group) {
            $scope.group = group;
        });
    };

    $scope.close = function () {
        $modalInstance.close($scope.group);
    };

    $scope.refresh();
});


app.controller('GroupCtrl', function ($scope, $stateParams, Restangular) {
    $scope.refresh = function () {
        Restangular.one('group', $stateParams.group_id).get().then(function (group) {
            $scope.group = group;
        });
    };

    $scope.refresh();
});

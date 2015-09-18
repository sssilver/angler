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

    $scope.refresh = function () {
        Restangular.all('group').getList().then(function (groups) {
            $scope.groups = groups;
        });
    };

    $scope.remove = function (id) {
        if (confirm('Are you sure?')) {
            Model.remove({'model': 'group', 'id': id}, function () {
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

app.controller('GroupsCtrl', function ($scope, $log, $modal, Model) {

    $scope.dlgGroup = function (group) {
        if (group)
            $scope.group = group;
        else
            $scope.group = {};

        console.log(group);

        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-group.html',
            controller: 'GroupDialogCtrl',
            resolve: {
                group: function () {
                    return $scope.group;
                }
            }
        });

        modalInstance.result.then(function (group) {
            var group_service = new Model(group);

            if (group.id) {
                group_service.$save(
                    {'model': 'group', 'id': group.id},
                    function () {
                        $scope.refresh();
                    }
                );
            } else {
                group_service.$post(
                    {'model': 'group'},
                    function () {
                        $scope.refresh();
                    }
                )
            }
            console.log(group);
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function () {
        var groups = Model.query({'model': 'group'}, function () {
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

app.controller('GroupDialogCtrl', function ($scope, $log, $modalInstance, $modal, Model, group) {
    $scope.group = group;
    console.log(group);

    var courses = Model.query({model: 'course'}, function () {
        $scope.courses = courses.objects;
    });

    var levels = Model.query({model: 'level'}, function () {
        $scope.levels = levels;
    });

    $scope.ok = function () {
        $modalInstance.close($scope.group);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

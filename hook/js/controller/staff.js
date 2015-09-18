app.controller('StaffCtrl', function ($scope, $log, $modal, Restangular) {

    $scope.dlgStaff = function (staff) {
        if (staff)
            $scope.staff = staff;
        else
            $scope.staff = Restangular.one('staff');

        $modal.open({
            templateUrl: 'template/dlg-staff.html',
            controller: 'StaffDialogCtrl',
            resolve: {
                staff: function () {
                    return $scope.staff;
                }
            }
        }).result.then(function (staff) {
            staff.save().then(function () {
                $scope.refresh();
            });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function () {
        Restangular.all('staff').getList().then(function (staffs) {
            $scope.staffs = staffs;
        });
    };

    $scope.remove = function (id) {
        if (confirm('Are you sure?')) {
            Restangular.one('staff', id).remove().then(function () {
                $scope.refresh();
            });
        }
    };

    $scope.refresh();
});


app.controller('StaffDialogCtrl', function ($scope, $log, $modalInstance, $modal, staff) {

    $scope.staff = staff;

    $scope.ok = function () {
        $modalInstance.close($scope.staff);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

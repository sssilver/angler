app.controller(
    'StaffCtrl',
        ['$scope', '$log', '$modal', 'Model',
            function ($scope, $log, $modal, Model) {

    $scope.dlgStaff = function (staff) {
        if (staff)
            $scope.staff = staff;
        else
            $scope.staff = {};

        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-staff.html',
            controller: 'StaffDialogCtrl',
            resolve: {
                staff: function () {
                    return $scope.staff;
                }
            }
        });

        modalInstance.result.then(function (staff) {
            var staff_service = new Model(staff);

            if (staff.id) {
                staff_service.$save(
                    {'model': 'staff', 'id': staff.id},
                    function () {
                        $scope.refresh();
                    }
                );
            } else {
                staff_service.$post(
                    {'model': 'staff'},
                    function () {
                        $scope.refresh();
                    }
                )
            }
            console.log(staff);
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function () {
        var staffs = Model.query({'model': 'staff'}, function () {
            $scope.staffs = staffs;
        });
    };

    $scope.remove = function (id) {
        if (confirm('Are you sure?')) {
            Model.remove({'model': 'staff', 'id': id}, function () {
                $scope.refresh();
            });
        }
    };

    $scope.refresh();
}]);


app.controller(
    'StaffDialogCtrl',
    ['$scope', '$log', '$modalInstance', '$modal', 'staff',
        function ($scope, $log, $modalInstance, $modal, staff ) {

    $scope.staff = staff;

    $scope.ok = function () {
        $modalInstance.close($scope.staff);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);

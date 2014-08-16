app.controller(
    'StaffCtrl',
        ['$scope', '$log', '$modal', 'Model',
            function ($scope, $log, $modal, Model) {

    $scope.dlgStaff = function (staff) {
        if (staff)
            $scope.staff = staff;
        else
            $scope.staff = {};

        console.log(staff);


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
            staff_service = new Model(staff);

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
    }
}]);


app.controller(
    'StaffDialogCtrl',
    ['$scope', '$log', '$modalInstance', '$modal', 'staff',
        function ($scope, $log, $modalInstance, $modal, staff ) {

    $scope.staff = staff;
    console.log(staff);

    $scope.ok = function () {
        $modalInstance.close($scope.staff);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);

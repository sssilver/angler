app.controller(
    'CompaniesCtrl',
        ['$scope', '$log', '$modal', 'Model',
            function ($scope, $log, $modal, Model) {

    $scope.dlgCompany = function (company) {

        if (company)
            $scope.company = company;
        else
            $scope.company = {};

        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-company.html',
            controller: 'CompanyDialogCtrl',
            resolve: {
                company: function () {
                    return $scope.company;
                }
            }
        });

        modalInstance.result.then(function (company) {
            company_service = new Model(company);

            if (company.id) {
                company_service.$save(
                    {'model': 'company', 'id': company.id},
                    function () {
                        $scope.refresh();
                    }
                );
            } else {
                company_service.$post(
                    {'model': 'company'},
                    function () {
                        $scope.refresh();
                    }
                );
            }
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function () {
        companies = Model.query({'model': 'company'}, function () {
            $scope.companies = companies;
        });
    }

    $scope.remove = function (id) {
        if (confirm('Are you sure?')) {
            Model.remove({'model': 'company', 'id': id}, function () {
                $scope.refresh();
            });
        }
    }

    $scope.refresh();
}]);


app.controller(
    'CompanyDialogCtrl',
        ['$scope', '$log', '$modalInstance', '$modal', 'company', 'Model',
            function ($scope, $log, $modalInstance, $modal, company, Model) {

    $scope.company = company;
    console.log(company);

    $scope.ok = function () {
        $modalInstance.close($scope.company);
    }

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);


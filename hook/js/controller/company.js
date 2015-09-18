app.controller('CompaniesCtrl', function ($scope, $log, $modal, Restangular) {

    $scope.dlgCompany = function (company) {

        if (company)
            $scope.company = company;
        else
            $scope.company = Restangular.one('company');

        $modal.open({
            templateUrl: 'template/dlg-company.html',
            controller: 'CompanyDialogCtrl',
            resolve: {
                company: function () {
                    return $scope.company;
                }
            }
        }).result.then(function (company) {
            company.save().then(function () {
                $scope.refresh();
            });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function () {
        Restangular.all('company').getList().then(function (companies) {
            $scope.companies = companies;
        });
    };

    $scope.remove = function (id) {
        if (confirm('Are you sure?')) {
            Restangular.one('course', id).remove().then(function () {
                $scope.refresh();
            });
        }
    };

    $scope.refresh();
});


app.controller('CompanyDialogCtrl', function ($scope, $log, $modalInstance, $modal, company) {

    $scope.company = company;

    $scope.ok = function () {
        $modalInstance.close($scope.company);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

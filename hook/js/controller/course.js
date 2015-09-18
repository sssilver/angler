app.controller('CoursesCtrl', function ($scope, $log, $modal, Restangular) {

    $scope.dlgLevels = function (course) {
        $modal.open({
            templateUrl: 'template/levels.html',
            controller: 'LevelsDialogCtrl',
            resolve: {
                course: function () {
                    return course;
                }
            },
            scope: $scope
        });
    };

    $scope.dlgTariffs = function (course) {
        $modal.open({
            templateUrl: 'template/tariffs.html',
            controller: 'TariffsDialogCtrl',
            resolve: {
                course: function () {
                    return course;
                }
            },
            scope: $scope
        });
    };

    $scope.dlgCourse = function (course) {
        if (course)
            $scope.course = course;
        else
            $scope.course = Restangular.one('course');

        $modal.open({
            templateUrl: 'template/dlg-course.html',
            controller: 'CourseDialogCtrl',
            resolve: {
                course: function () {
                    return $scope.course;
                }
            }
        }).result.then(function (course) {
            course.save().then(function () {
                $scope.refresh();
            });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function () {
        Restangular.all('course').getList().then(function (courses) {
            $scope.courses = courses;
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


app.controller('CourseDialogCtrl', function ($scope, $log, $modalInstance, $modal, course) {
    $scope.course = course;

    $scope.ok = function () {
        $modalInstance.close($scope.course);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

});


app.controller('LevelsDialogCtrl', function ($scope, $log, $modalInstance, $modal, course, Restangular) {
    $scope.course = course;

    $scope.remove = function (levelID) {
        if (confirm('Are you sure?')) {
            Restangular.one('level', levelID).remove().then(function () {
                $scope.refresh();
            });
        }
    };

    $scope.dlgLevel = function (course, level) {
        if (level) {
            $scope.level = level;
        } else {
            $scope.level = Restangular.one('course', course.id).one('level');
        }

        $modal.open({
            templateUrl: 'template/dlg-level.html',
            controller: 'LevelDialogCtrl',
            resolve: {
                level: function () {
                    return $scope.level;
                }
            }
        }).result.then(function (level) {
            level.save().then(function () {
                $scope.refresh();
            });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.ok = function () {
        $modalInstance.close();
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.refresh = function () {
        Restangular.one('course', course.id).all('level').getList().then(function (levels) {
            $scope.levels = levels;
        });
    };

    $scope.refresh();
});


app.controller('LevelDialogCtrl', function ($scope, $modalInstance, level) {
    $scope.level = level;

    $scope.ok = function () {
        $modalInstance.close($scope.level);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

});


app.controller(
    'TariffsDialogCtrl',
        ['$scope', '$log', '$modalInstance', '$modal', 'course', 'Model',
            function ($scope, $log, $modalInstance, $modal, course, Model) {

    $scope.course = course;

    $scope.remove = function (tariff_id) {
        if (confirm('Are you sure?')) {
            Model.remove({'model': 'tariff', 'resource_id': tariff_id}, function () {
                $scope.refresh();
            });
        }
    };

    $scope.dlgTariff = function (course, tariff) {
        if (tariff) {
            $scope.tariff = tariff;
        } else {
            $scope.tariff = {course: course.id};
        }

        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-tariff.html',
            controller: 'TariffDialogCtrl',
            resolve: {
                tariff: function () {
                    return $scope.tariff;
                }
            }
        });

        modalInstance.result.then(function (tariff) {
            var tariff_service = new Model(tariff);

            if (tariff.id) {
                tariff_service.$save(
                    {'model': 'tariff', 'resource_id': tariff.id},
                    function () {
                        $scope.refresh();
                    }
                );
            } else {
                tariff_service.$post(
                    {'model': 'tariff'},
                    function () {
                        $scope.refresh();
                    }
                );
            }
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.ok = function () {
        $modalInstance.close();
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.refresh = function () {
        var tariffs = Model.query({model: 'tariff', course_id: course.id}, function () {
            $scope.tariffs = tariffs.items;
        })
    };

    $scope.refresh();
}]);


app.controller(
    'TariffDialogCtrl',
        ['$scope', '$modalInstance', 'tariff', 'Model',
            function ($scope, $modalInstance, tariff, Model) {

    $scope.tariff = angular.copy(tariff);

    $scope.ok = function () {
        $modalInstance.close($scope.tariff);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

}]);

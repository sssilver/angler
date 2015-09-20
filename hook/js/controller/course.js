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
            templateUrl: 'template/dlg-tariffs.html',
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


app.controller('TariffsDialogCtrl', function ($scope, $log, $modalInstance, $modal, course, Restangular) {

    $scope.course = course;

    $scope.remove = function (tariff_id) {
        if (confirm('Are you sure?')) {
            Restangular.one('tariff', tariff_id).remove().then(function () {
                $scope.refresh();
            });
        }
    };

    $scope.dlgTariff = function (course, tariff) {
        if (tariff) {
            $scope.tariff = tariff;
        } else {
            $scope.tariff = Restangular.one('course', course.id).one('tariff');
        }

        $modal.open({
            templateUrl: 'template/dlg-tariff.html',
            controller: 'TariffDialogCtrl',
            resolve: {
                tariff: function () {
                    return $scope.tariff;
                }
            }
        }).result.then(function (tariff) {
            console.log(tariff);
            tariff.save().then(function () {
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
        Restangular.one('course', course.id).all('tariff').getList().then(function (tariffs) {
            $scope.tariffs = tariffs;
        })
    };

    $scope.refresh();
});


app.controller('TariffDialogCtrl', function ($scope, $modalInstance, tariff) {
    $scope.tariff = tariff;

    $scope.ok = function () {
        $modalInstance.close($scope.tariff);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

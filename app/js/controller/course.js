app.controller(
    'CoursesCtrl',
        ['$scope', '$log', '$modal', 'Model', 'TIMES', 'DAYS',
            function($scope, $log, $modal, Model, TIMES, DAYS) {

    $scope.dlgLevels = function(course) {
        var modalInstance = $modal.open({
            templateUrl: 'template/levels.html',
            controller: 'LevelsDialogCtrl',
            resolve: {
                course: function() {
                    return course;
                }
            },
            scope: $scope
        });
    }

    $scope.dlgTariffs = function(course) {
        var modalInstance = $modal.open({
            templateUrl: 'template/tariffs.html',
            controller: 'TariffsDialogCtrl',
            resolve: {
                course: function() {
                    return course;
                }
            },
            scope: $scope
        });
    }

    $scope.dlgCourse = function(course) {

        if (course)
            $scope.course = course;
        else
            $scope.course = {};

        var modalInstance = $modal.open({
            templateUrl: 'template/form-course.html',
            controller: 'CourseDialogCtrl',
            resolve: {
                course: function() {
                    return $scope.course;
                }
            }
        });

        modalInstance.result.then(function(course) {
            course_service = new Model(course);

            if (course.id) {
                course_service.$save(
                    {'model': 'course', 'id': course.id},
                    function() {
                        $scope.refresh();
                    }
                );
            } else {
                course_service.$post(
                    {'model': 'course'},
                    function() {
                        $scope.refresh();
                    }
                );
            }
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function() {
        courses = Model.query({'model': 'course'}, function() {
            $scope.courses = courses;
        });
    }

    $scope.remove = function(id) {
        if (confirm('Are you sure?')) {
            Model.remove({'model': 'course', 'id': id}, function() {
                $scope.refresh();
            });
        }
    }

    $scope.refresh();
}]);


app.controller(
    'CourseDialogCtrl',
        ['$scope', '$log', '$modalInstance', '$modal', 'course', 'Model',
            function($scope, $log, $modalInstance, $modal, course, Model) {

    $scope.course = course;

    $scope.ok = function() {
        $modalInstance.close($scope.course);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

}]);

app.controller(
    'LevelsDialogCtrl',
        ['$scope', '$log', '$modalInstance', '$modal', 'course', 'Model',
            function($scope, $log, $modalInstance, $modal, course, Model) {

    $scope.course = course;

    $scope.remove = function(level_id) {
        if (confirm('Are you sure?')) {
            Model.remove({'model': 'level', 'id': level_id}, function() {
                $scope.$parent.refresh();
            });
        }
    }

    $scope.dlgLevel = function(course, level) {
        if (level) {
            $scope.level = level;
        } else {
            console.log('new level dialog');
            $scope.level = {};
            $scope.level.course = {id: course.id};
        }

        var modalInstance = $modal.open({
            templateUrl: 'template/form-level.html',
            controller: 'LevelDialogCtrl',
            resolve: {
                level: function() {
                    return $scope.level;
                }
            }
        });

        modalInstance.result.then(function(level) {
            // Transform level.teachers
            level.teachers = level.teachers.map(function(teacher) {
                return {id: teacher}
            });

            level_service = new Model(level);

            if (level.id) {
                level_service.$save(
                    {'model': 'level', 'id': level.id},
                    function() {
                        $scope.refresh();
                    }
                );
            } else {
                level_service.$post(
                    {'model': 'level'},
                    function() {
                        $scope.refresh();
                    }
                );
            }
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    }

    $scope.ok = function() {
        $modalInstance.close();
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

    $scope.refresh = function() {
        console.log('querying levels for ');
        console.log(course);

        levels = Model.query(
            {
                model: 'level',
                q: {
                    filters: [{
                        name: 'course_id',
                        op: 'eq',
                        val: course.id
                    }]
                }
            },
            function() {
                $scope.levels = levels.objects;
            }
        );
    }

    $scope.refresh();
}]);


app.controller(
    'LevelDialogCtrl',
        ['$scope', '$modalInstance', 'level', 'Model',
            function($scope, $modalInstance, level, Model) {

    $scope.level = angular.copy(level);

    if (level.teachers) {
        $scope.level.teachers = level.teachers.map(function(teacher) {
            return teacher.id
        });
    }

    teachers = Model.query(
        {model: 'staff'},
        function() {
            $scope.teachers = teachers.objects;
            console.log(teachers);
        }
    );

    $scope.ok = function() {
        $modalInstance.close($scope.level);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

}]);



app.controller(
    'TariffsDialogCtrl',
        ['$scope', '$log', '$modalInstance', '$modal', 'course', 'Model',
            function($scope, $log, $modalInstance, $modal, course, Model) {

    $scope.course = course;

    $scope.remove = function(tariff_id) {
        if (confirm('Are you sure?')) {
            Model.remove({'model': 'tariff', 'id': tariff_id}, function() {
                $scope.$parent.refresh();
            });
        }
    }

    $scope.dlgTariff = function(course, tariff) {
        if (tariff) {
            $scope.tariff = tariff;
        } else {
            $scope.tariff = {};
            $scope.tariff.course = {id: course.id};
        }

        var modalInstance = $modal.open({
            templateUrl: 'template/form-tariff.html',
            controller: 'TariffDialogCtrl',
            resolve: {
                tariff: function() {
                    return $scope.tariff;
                }
            }
        });

        modalInstance.result.then(function(tariff) {
            tariff_service = new Model(tariff);

            if (tariff.id) {
                tariff_service.$save(
                    {'model': 'tariff', 'id': tariff.id},
                    function() {
                        $scope.refresh();
                    }
                );
            } else {
                tariff_service.$post(
                    {'model': 'tariff'},
                    function() {
                        $scope.refresh();
                    }
                );
            }
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    }

    $scope.ok = function() {
        $modalInstance.close();
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

    $scope.refresh = function() {
        tariffs = Model.query(
            {
                model: 'tariff',
                q: {
                    filters: [{
                        name: 'course_id',
                        op: 'eq',
                        val: course.id
                    }]
                }
            },
            function() {
                $scope.tariffs = tariffs.objects;
            }
        );
    }

    $scope.refresh();
}]);


app.controller(
    'TariffDialogCtrl',
        ['$scope', '$modalInstance', 'tariff', 'Model',
            function($scope, $modalInstance, tariff, Model) {

    $scope.tariff = angular.copy(tariff);

    $scope.ok = function() {
        $modalInstance.close($scope.tariff);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

}]);
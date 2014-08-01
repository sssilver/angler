app.controller(
    'LessonsCtrl',
    ['$scope', '$q', '$state', '$stateParams', '$log', '$location', '$resource', 'Model', 'TIMES', 'DAYS', '$modal',
        function ($scope, $q, $state, $stateParams, $log, $location, $resource, Model, TIMES, DAYS, $modal) {


    $scope.dlgFile = function (lesson) {
        if (lesson)
            $scope.lesson = lesson;
        else
            $scope.lesson = {};

        console.log(lesson);


        var modalInstance = $modal.open({
            templateUrl: 'template/dlg-lesson.html',
            controller: 'FileLessonDialogCtrl',
            resolve: {
                lesson: function () {
                    return $scope.lesson;
                }
            }
        });

        modalInstance.result.then(function (lesson) {
            lesson_service = new Model(lesson);

            if (lesson.id) {
                lesson_service.$save(
                    {'model': 'lesson', 'id': lesson.id},
                    function () {
                        $scope.refresh();
                    }
                );
            } else {
                lesson_service.$post(
                    {'model': 'student'},
                    function () {
                        $scope.refresh();
                    }
                )
            }
            console.log(lesson);
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

}]);


app.controller(
    'FileLessonDialogCtrl',
    ['$scope', '$log', '$modalInstance', '$modal', 'lesson', 'Model',
        function ($scope, $log, $modalInstance, $modal, lesson, Model) {

    $scope.lesson = lesson;
    $scope.lesson.attendance = {};
    Model.query({'model': 'group'}, function (groups) {
        $scope.groups = groups.objects;
    });

    $scope.$watch('lesson.group.students', function (newValue, oldValue) {
        if (newValue !== oldValue)
            angular.forEach($scope.lesson.group.students, function (student) {
                $scope.lesson.attendance[student.id] = 0;
            })
    })


    $scope.ok = function () {
        $modalInstance.close($scope.lesson);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);


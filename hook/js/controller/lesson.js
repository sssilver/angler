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
                    {'model': 'lesson'},
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


    $scope.refresh = function () {
        Model.query({'model': 'lesson'}, function (lessons) {
            $scope.lessons = lessons.objects;
        });
    };


    $scope.refresh();

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
                if ($scope.isActive(student))
                    $scope.lesson.attendance[student.student_id] = 0;
            });
    });

    $scope.isActive = function (student) {
        return student.is_suspended ? false : true;
    }

    $scope.populateStudents = function (group) {
        Model.query(
            {
                model: 'student_group',
                group_id: group.id
            },
            function (students) {
                $scope.students = students.objects;
            }
        );
    };


    $scope.ok = function () {
        var datetime = new Date();

        if ($scope.lesson.date && $scope.lesson.time) {
            var date = $scope.lesson.date.split('-');
            var time = $scope.lesson.time.split(':');

            datetime = new Date(date[0], date[1], date[2], time[0], time[1]);
        }

        console.log(datetime);

        var lesson = {
            group_id: $scope.lesson.group.id,
            attendance: $scope.lesson.attendance,
            // TODO: This is the right thing to do, but flask-restless is dumb
            // date: datetime.getTime() / 1000  // Convert to UNIX timestamp
            date: datetime.toISOString()
        }

        console.log(lesson);
        $modalInstance.close(lesson);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);


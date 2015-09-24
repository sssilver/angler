app.controller('LessonsCtrl', function ($scope, $q, $state, $stateParams, $log, $location, TIMES, DAYS, $modal, Auth, Restangular) {

    // Get the current teacher's groups
    Restangular.all('group').getList({teacher_id: Auth.getCurrentUser().id}).then(function (groups) {
        $scope.groups = groups;
    });

    $scope.dlgFile = function (lesson) {
        $modal.open({
            templateUrl: 'template/dlg-lesson.html',
            controller: 'FileLessonDialogCtrl',
            resolve: {
                lesson: function () { return lesson || {} },
                groups: function () { return $scope.groups }
            }
        }).result.then(function (lessonData) {
            var restLesson;

            if (lesson)  // Amending an existing lesson
                restLesson = Restangular.one('group', lessonData.group.id).one('lessons', lesson.id);
            else  // Filing a new lesson
                restLesson = Restangular.one('group', lessonData.group.id).one('lessons');

            restLesson.attendance = lessonData.attendance;
            restLesson.datetime = lessonData.datetime.toISOString();

            restLesson.save().then(function () {
                $scope.refresh();
            });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.refresh = function () {
        Restangular.all('lesson').getList().then(function (lessons) {
            $scope.lessons = lessons;
        });
    };

    $scope.refresh();
});


app.controller('FileLessonDialogCtrl', function ($scope, $log, $modalInstance, $modal, lesson, groups, Restangular) {
    $scope.groups = groups;
    $scope.lesson = lesson;
    $scope.lesson.attendance = {};

    $scope.isActive = function (student) {
        return student.is_suspended ? false : true;
    };

    $scope.populateStudents = function (group) {
        Restangular.all('student').getList({group_id: group.id}).then(function (students) {
            $scope.students = students;

            // Reset attendance for all active students
            angular.forEach($scope.students, function (student) {
                if ($scope.isActive(student))
                    $scope.lesson.attendance[student.id] = 0;
            });
        });
    };

    $scope.ok = function () {
        $modalInstance.close($scope.lesson);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

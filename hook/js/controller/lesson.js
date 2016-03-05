app.controller('LessonsCtrl', function ($scope, $q, $state, $stateParams, $log, $location, TIMES, DAYS, $modal, Auth, Restangular) {
    // Get the current teacher's groups
    Restangular.all('group').getList({teacher_id: Auth.getCurrentUser().id}).then(function (groups) {
        $scope.groups = groups;
        console.log(typeof(groups[1].id));
    });

    $scope.dlgFile = function (lesson) {
        console.log(typeof(lesson.group_id));

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
            // Group lessons by date to display them in the UI
            // This is harder than what seems like a trivial problem
            var groupedLessons = {};
            angular.forEach(lessons, function (lesson) {
                lesson.time = new Date(lesson.time);  // Convert time from string to an actual Date object
                var date = new Date(lesson.time).toISOString().slice(0, 10);

                // Get every unique date to the granularity we want to group by with
                if (!(date in groupedLessons))
                    groupedLessons[date] = [];

                groupedLessons[date].push(lesson);
            });

            // Get the list of unique dates to group with and sort them separately
            $scope.dateGroups = Object.keys(groupedLessons).sort();
            $scope.groupedLessons = groupedLessons;
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

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {templateUrl: 'partial/index.html', controller: 'IndexCtrl'}).
        when('/login', {templateUrl: 'partial/login.html', controller: 'LoginCtrl'}).

        when('/lessons', {templateUrl: 'partial/lessons.html', controller: 'LessonsCtrl'}).
        when('/students', {templateUrl: 'partial/students.html', controller: 'StudentsCtrl'}).
        when('/students/new', {templateUrl: 'partial/new-student.html', controller: 'StudentsCtrl'}).
        when('/teachers', {templateUrl: 'partial/teachers.html', controller: 'TeachersCtrl'}).

        // Administration
        when('/administration/courses', {templateUrl: 'partial/courses.html', controller: 'CoursesCtrl'}).
        when('/administration/courses/new', {templateUrl: 'partial/new-course.html', controller: 'CoursesCtrl'}).

        when('/administration/levels', {templateUrl: 'partial/levels.html', controller: 'LevelsCtrl'}).
        when('/administration/levels/new', {templateUrl: 'partial/new-level.html', controller: 'LevelsCtrl'}).

        otherwise({redirectTo: '/'});
}]);

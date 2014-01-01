app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {templateUrl: 'partial/index.html', controller: 'IndexCtrl'}).
        when('/login', {templateUrl: 'partial/login.html', controller: 'LoginCtrl'}).

        when('/lessons', {templateUrl: 'partial/lessons.html', controller: 'LessonsCtrl'}).
        when('/students', {templateUrl: 'partial/students.html', controller: 'StudentsCtrl'}).
        when('/students/new', {templateUrl: 'partial/new-student.html', controller: 'StudentsCtrl'}).
        when('/teachers', {templateUrl: 'partial/teachers.html', controller: 'TeachersCtrl'}).

        when('/administration/levels', {templateUrl: 'partial/levels.html', controller: 'LevelsCtrl'}).
        when('/administration/levels/new', {templateUrl: 'partial/new-level.html', controller: 'LevelsCtrl'}).

        otherwise({redirectTo: '/'});
}]);

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {templateUrl: 'partial/index.html', controller: 'IndexCtrl'}).
        when('/login', {templateUrl: 'partial/login.html', controller: 'LoginCtrl'}).

        when('/groups', {templateUrl: 'partial/groups.html', controller: 'GroupsCtrl'}).

        when('/students', {templateUrl: 'partial/students.html', controller: 'StudentsCtrl'}).
        when('/students/:student_id', {templateUrl: 'partial/student.html', controller: 'StudentsCtrl'}).

        when('/companies', {templateUrl: 'partial/companies.html', controller: 'CompaniesCtrl'}).
        when('/companies/:company_id', {templateUrl: 'partial/company.html', controller: 'CompaniesCtrl'}).

        when('/teachers', {templateUrl: 'partial/teachers.html', controller: 'TeachersCtrl'}).

        // Administration
        when('/administration/courses', {templateUrl: 'partial/courses.html', controller: 'CoursesCtrl'}).
        when('/administration/courses/new', {templateUrl: 'partial/new-course.html', controller: 'CoursesCtrl'}).

        when('/administration/levels', {templateUrl: 'partial/levels.html', controller: 'LevelsCtrl'}).
        when('/administration/levels/new', {templateUrl: 'partial/new-level.html', controller: 'LevelsCtrl'}).

        otherwise({redirectTo: '/'});
}]);

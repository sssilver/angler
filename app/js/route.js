app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

    $stateProvider
        .state('index', {
            url: '/',
            templateUrl: 'partial/index.html',
            controller: 'IndexCtrl'
        })
        .state('login', {
            url: '/login',
            templateUrl: 'partial/login.html',
            controller: 'LoginCtrl'
        })

        .state('groups', {
            url: '/groups',
            templateUrl: 'partial/groups.html',
            controller: 'GroupsCtrl'
        })

        .state('students', {
            url: '/students',
            templateUrl: 'partial/students.html',
            controller: 'StudentsCtrl'
        })
        .state('student', {
            url: 'students/:student_id',
            templateUrl: 'partial/student.html',
            controller: 'StudentsCtrl'
        })

        .state('companies', {
            url: '/companies',
            templateUrl: 'partial/companies.html',
            controller: 'CompaniesCtrl'
        })
        .state('company', {
            url: '/companies/:company_id',
            templateUrl: 'partial/company.html',
            controller: 'CompaniesCtrl'
        })

        .state('teachers', {
            url: '/teachers',
            templateUrl: 'partial/teachers.html',
            controller: 'TeachersCtrl'
        })

        .state('administration', {
            abstract: true,
            url: '/administration',
            template: '<ui-view/>'
        })
        .state('administration.courses', {
            url: '/courses',
            templateUrl: 'partial/courses.html',
            controller: 'CoursesCtrl'
        })
        .state('administration.courses.new', {
            url: '/new',
            templateUrl: 'partial/new-course.html',
            controller: 'CoursesCtrl'
        })

}]);

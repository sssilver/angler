app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

    $stateProvider
        .state('public', {
            abstract: true,
            templateUrl: 'partial/public/index.html',
            data: {
                access: ['public']
            }
        })
        .state('public.login', {
            url: '/login/',
            templateUrl: 'partial/public/login.html',
            controller: 'LoginCtrl'
        })


        .state('user', {
            abstract: true,
            templateUrl: 'partial/user/index.html',
            data: {
                access: ['teacher', 'admin']
            }
        })

        .state('user.home', {
            url: '/',
            templateUrl: 'partial/index.html',
            controller: 'IndexCtrl'
        })

        .state('user.students', {
            url: '/students',
            templateUrl: 'partial/students.html',
            controller: 'StudentsCtrl'
        })
        .state('user.students.view', {
            url: '/:student_id',
            templateUrl: 'partial/student.html',
            controller: 'StudentsCtrl'
        })

        .state('user.companies', {
            url: '/companies',
            templateUrl: 'partial/companies.html',
            controller: 'CompaniesCtrl'
        })
        .state('user.companies.view', {
            url: '/:company_id',
            templateUrl: 'partial/company.html',
            controller: 'CompaniesCtrl'
        })

        .state('user.teachers', {
            url: '/teachers',
            templateUrl: 'partial/teachers.html',
            controller: 'TeachersCtrl'
        })

        .state('user.administration', {
            abstract: true,
            template: '<ui-view />',
            data: {
                access: 'access.admin'
            }
        })
        .state('user.administration.courses', {
            url: '/courses',
            templateUrl: 'partial/courses.html',
            controller: 'CoursesCtrl'
        })
        .state('user.administration.courses.new', {
            url: '/new',
            templateUrl: 'partial/new-course.html',
            controller: 'CoursesCtrl'
        });

}]);

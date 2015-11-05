app.config(function ($stateProvider, $httpProvider, RestangularProvider) {

    RestangularProvider.setBaseUrl(window.location.protocol + '//' + window.location.hostname + ':5000');

    // Add a response interceptor
    RestangularProvider.addResponseInterceptor(function(data, operation) {
        var extractedData;

        if (operation === 'getList') {
            extractedData = data.items;
            extractedData.meta = data.meta;
        } else {
            extractedData = data;
        }

        return extractedData;
    });

    RestangularProvider.setOnElemRestangularized(function(elem, isCollection, route) {
        if (!isCollection && route === 'credit') {
            // This will add a method called evaluate that will do a get to path evaluate with NO default
            // query params and with some default header
            // signature is (name, operation, path, params, headers, elementToPost)
            elem.addRestangularMethod('credit', 'post', 'credit', undefined);
        }
        return elem;
    });

    $httpProvider.defaults.withCredentials = true;

    $httpProvider.interceptors.push('RodInterceptor');

    $httpProvider.defaults.transformResponse.push(function (responseData) {
        convertDateStringsToDates(responseData);

        return responseData;
    });

    $stateProvider
        .state('public', {
            abstract: true,
            templateUrl: 'partial/outer.html',
            data: {
                access: ['public']
            }
        })
        .state('public.login', {
            url: '/login/',
            templateUrl: 'partial/login.html',
            controller: 'LoginCtrl'
        })


        .state('user', {
            abstract: true,
            templateUrl: 'partial/inner.html',
            data: {
                access: ['teacher', 'admin']
            }
        })

        .state('user.home', {
            url: '/',
            templateUrl: 'partial/home.html',
            controller: 'HomeCtrl'
        })

        .state('user.groups', {
            url: '/groups',
            templateUrl: 'partial/groups.html',
            controller: 'GroupsCtrl'
        })

        .state('user.group', {
            url: '/groups/:group_id',
            templateUrl: 'partial/group.html',
            controller: 'GroupCtrl'
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

        .state('user.staff', {
            url: '/staff',
            templateUrl: 'partial/staff.html',
            controller: 'StaffCtrl'
        })

        .state('user.lessons', {
            url: '/lessons',
            templateUrl: 'partial/lessons.html',
            controller: 'LessonsCtrl'
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
});

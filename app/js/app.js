var app = angular.module('scool', ['ngRoute', 'ngResource']);


app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {templateUrl: 'partials/index.html', controller: 'IndexCtrl'}).
        when('/login', {templateUrl: 'partials/login.html', controller: 'LoginCtrl'}).

        when('/lessons', {templateUrl: 'partials/lessons.html', controller: 'LessonsCtrl'}).
        when('/students', {templateUrl: 'partials/students.html', controller: 'StudentsCtrl'}).
        when('/students/new', {templateUrl: 'partials/new-student.html', controller: 'StudentsCtrl'}).
        when('/teachers', {templateUrl: 'partials/teachers.html', controller: 'TeachersCtrl'}).
        otherwise({redirectTo: '/'});
}]);


app.factory('Students', function($resource) {
    return $resource('http://localhost\\:8080/students/:student_id', {}, {
        query: {method: 'GET', params: {student_id: ''}, isArray: true},
        post: {method: 'POST'},
        update: {method: 'PUT'},
        remove: {method: 'DELETE'}
    });
});


app.controller('IndexCtrl', ['$scope', '$location', function($scope, $location) {
    $scope.go = function(path) {
        $location.path(path);
    };
}]);


app.controller('LoginCtrl', ['$scope', function($scope) {
    console.log('login');

    $scope.items = [
        "The first choice!",
        "And another choice for you.",
        "but wait! A third!"
    ];

}]);


app.controller('StudentsCtrl', ['$scope', 'Students', 'HOURS', 'DAYS', function($scope, Students, HOURS, DAYS) {
    $scope.hours = HOURS;
    $scope.days = DAYS;


    //$scope.items = Students.query();

    $scope.toggleRange = function(time, status) {
        $scope.student.availability[time] = !($scope.student.availability[time]);
        console.log(time);
    }
}]);
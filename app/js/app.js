var app = angular.module('scool', ['ngRoute']);


app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {templateUrl: 'partials/index.html', controller: 'IndexCtrl'}).
        when('/login', {templateUrl: 'partials/login.html',   controller: 'LoginCtrl'}).

        when('/lessons', {templateUrl: 'partials/lessons.html',   controller: 'LessonsCtrl'}).
        when('/students', {templateUrl: 'partials/students.html',   controller: 'StudentsCtrl'}).
        when('/students/new', {templateUrl: 'partials/new-student.html',   controller: 'StudentCtrl'}).
        when('/teachers', {templateUrl: 'partials/teachers.html',   controller: 'TeachersCtrl'}).
        otherwise({redirectTo: '/'});
}]);


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

app.controller('StudentsCtrl', ['$scope', function($scope) {
    console.log('students');

    $scope.items = [
        "The first choice!",
        "And another choice for you.",
        "but wait! A third!"
    ];

}]);


app.controller('StudentCtrl', ['$scope', function($scope) {
    console.log('student!!');

    $scope.items = [
        "The first choice!",
        "And another choice for you.",
        "but wait! A third!"
    ];

}]);
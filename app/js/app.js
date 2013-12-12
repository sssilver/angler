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


app.controller(
    'StudentsCtrl',
        ['$scope', 'Student', 'TIMES', 'DAYS',
            function($scope, Student, TIMES, DAYS) {

    $scope.times = TIMES;
    $scope.days = DAYS;
    $scope.student = new Student({'availability': []});

    for (var i in DAYS)
        $scope.student.availability[i] = [];

    //$scope.items = Students.query();

    $scope.addAvailability = function(day) {
        console.log('Adding availability for day ' + day.toString());
        $scope.student.availability[day].push([0, 0]);
    }

    $scope.removeAvailability = function(day, availability) {
        console.log('Removing availability #' + availability.toString() + ' from day ' + day.toString());
        $scope.student.availability[day].splice(availability, 1);
    }

    $scope.registerStudent = function() {
        $scope.student.$save();
    }


}]);
var SERVICE_ENDPOINT = window.location.protocol + '//' + window.location.hostname + ':8080/api';


app.constant('AUTH_EVENTS', {
    loginSuccess: 'auth-login-success',
    loginFailed: 'auth-login-failed',
    logoutSuccess: 'auth-logout-success',
    sessionTimeout: 'auth-session-timeout',
    notAuthenticated: 'auth-not-authenticated',
    notAuthorized: 'auth-not-authorized'
});


app.constant('ROLES', {
    public: '*',
    teacher: 'teacher',
    admin: 'admin'
});


app.factory('TIMES', [function (value) {
    var times = [];

    for (var i = 0; i < 1440; i+=30) {
        var hour = Math.floor(i / 60);
        var minute = i % 60;

        var str_hour = ('0' + String(hour)).slice(-2);
        var str_minute = ('0' + String(minute)).slice(-2);

        if (hour < 10 || hour > 19)
            continue;

        times.push({
            'minute': i,
            'time': str_hour + ':' + str_minute
        });
    }

    return times;
}]);


app.constant('DAYS', {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
});


app.factory('Model', function ($resource, $http) {
    return $resource(SERVICE_ENDPOINT + '/:model/:id', {}, {
        get: {
            method: 'GET',
            isArray: false
        },

        query: {
            method: 'GET',
            isArray: false,
            params: {
                q: {
                    filters: [{
                        name: 'is_deleted',
                        op: 'eq',
                        val: false
                    }]
                }
            }
        },

        post: {
            method: 'POST'
        },

        save: {
            method: 'PUT'
        },

        remove: {
            method: 'PUT',
            params: {
                model: '@model',
                id: '@id'
            },
            transformRequest: [
                function () {
                    return {is_deleted: true};
                }
            ].concat($http.defaults.transformRequest)
        }
    });
});


app.factory('Auth', function ($http, $rootScope, $cookieStore) {
    return {
        login: function (credentials) {
            return $http
                .post(SERVICE_ENDPOINT + '/login', credentials, {withCredentials: true})
                .success(function (data, status, headers, config) {
                    console.info('loginSuccess');
                    this.user = data;
                    $cookieStore.put('angler-user', data);
                    $rootScope.$broadcast('loginSuccess');
                }).
                error(function (data, status, headers, config) {
                    console.info('loginFailure');
                    $rootScope.$broadcast('loginFailure');
                });
        },

        logout: function () {
            console.log('Auth.logout');
            return $http
                .post(SERVICE_ENDPOINT + '/logout', {}, {withCredentials: true})
                .success(function () {
                    console.log('logoutSuccess');
                    $rootScope.$broadcast('logoutSuccess');
                });
        },

        verify: function () {
            return $http
                .get(SERVICE_ENDPOINT + '/verify', {withCredentials: true})
                .error(function () {
                    $rootScope.$broadcast('unauthorized');
                });
        },

        getCurrentUser: function () {
            // Get the currently logged in user from the cookie storage
            return $cookieStore.get('angler-user');
        }
    };
});


app.factory('RodInterceptor', function ($q, $rootScope) {
    $rootScope.isLoading = 0;
    $rootScope.alerts = [];

    return {
        'request': function(config) {
            $rootScope.isLoading += 1;
            return config || $q.when(config);
        },

        'response': function(response) {
            $rootScope.isLoading -= 1;
            return response || $q.when(response);
        },

        'responseError': function(rejection) {
            $rootScope.isLoading -= 1;
            console.log(rejection);

            $rootScope.alerts.push({
                'msg': rejection.data.message,
                'type': 'danger'
            });

            return $q.reject(rejection);
        }
    };
});

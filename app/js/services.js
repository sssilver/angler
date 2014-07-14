var SERVICE_ENDPOINT = 'http://localhost:5000/api';  //'192.168.1.95';


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
    times = [];

    for (i = 0; i < 1440; i+=30) {
        hour = Math.floor(i / 60);
        minute = i % 60;

        str_hour = ('0' + String(hour)).slice(-2);
        str_minute = ('0' + String(minute)).slice(-2);

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
                function (data, headers_getter) {
                    return {is_deleted: true};
                }
            ].concat($http.defaults.transformRequest)
        }
    });
});


app.factory('Auth', function ($http, $rootScope, Session) {
    return {
        login: function (credentials) {
            return $http
                .post(SERVICE_ENDPOINT + '/login', credentials, {withCredentials: true})
                .success(function (data, status, headers, config) {
                    console.info('loginSuccess');
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
                .success(function (data, status, headers, config) {
                    console.log('logoutSuccess');
                    $rootScope.$broadcast('logoutSuccess');
                });
        }
    };
});


app.service('Session', function () {
    this.create = function (session_id, user_id, user_role) {
        this.id = session_id;
        this.user_id = user_id;
        this.user_role = user_role;
    };

    this.destroy = function () {
        this.id = null;
        this.user_id = null;
        this.user_role = null;
    };

    return this;
});


app.factory('AuthHttpInterceptor', function ($q, $rootScope) {
    return {
        'responseError': function (rejection) {
            console.error(rejection.data.message);

            // 401 UNAUTHORIZED
            if (rejection.status == 401)
                $rootScope.$broadcast('unauthorized');

            // 403 FORBIDDEN
            if (rejection.status == 403)
                $rootScope.$broadcast('forbidden');
        }
    };
});

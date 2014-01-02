app.constant('DAYS', {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
});


app.factory('TIMES', [function(value) {
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


app.factory('Student', function($resource) {
    return $resource('http://localhost\\:5000/students/:student_id', {}, {
        query: {
            method: 'GET',
            params: {
                student_id: ''
            },
            isArray: true
        },

        post: {
            method: 'POST'
        },

        save: {
            method: 'PUT'
        },

        remove: {
            method: 'DELETE'
        }
    });
});


app.factory('Level', function($resource) {
    return $resource('http://localhost\\:5000/api/level/:id', {}, {
        query: {
            method: 'GET',
            params: {
                id: ''
            },
            isArray: false
        },

        post: {
            method: 'POST'
        },

        save: {
            method: 'PUT'
        },

        remove: {
            method: 'DELETE'
        }
    });
});


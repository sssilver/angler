app.constant('DAYS', {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
});


app.factory('HOURS', [function(value) {
    hours = {};

    for (i = 0; i < 1440; i+=30) {
        hour = Math.floor(i / 60);
        minute = i % 60;

        str_hour = ('0' + String(hour)).slice(-2);
        str_minute = ('0' + String(minute)).slice(-2);

        if (hour < 10 || hour > 19)
            continue;

        hours[i] = str_hour + ':' + str_minute;
    }

    return hours;
}]);

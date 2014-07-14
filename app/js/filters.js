app.filter('timeRangeFilter', function () {
    return function (input, from) {
        output = [];

        for (i = 0; i < input.length; ++i) {
            if (input[i].minute > from)
                output.push(input[i]);
        }

        return output;
    };
});
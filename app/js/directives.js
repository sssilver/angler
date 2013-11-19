app.directive('scDatepicker', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var startView = attrs.startView;

            if (!startView)
                startView = 2;

            $(element).datetimepicker({
                'startView': startView
            });
        }
    };
});

app.directive('scDatetimepicker', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var mode = attrs.scDatepicker;

            if (!mode)
                mode = 'days';

            $(element).datetimepicker({
                'viewMode': mode
            });
        }
    };
});

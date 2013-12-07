app.directive('scDatepicker', function() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelCtrl) {
            var startView = attrs.startView;

            if (!startView)
                startView = 'month';

            $(element).datetimepicker({
                'startView': startView,
                'autoclose': true
            }).on('changeDate', function(e) {
                var outputDate = new Date(e.date);

                var n = outputDate.getTime();

                ngModelCtrl.$setViewValue(n);
                scope.$apply();
            });;
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

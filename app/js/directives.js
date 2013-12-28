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

app.directive('scInteger', function() {
    return {
        require: 'ngModel',
        link: function(scope, elm, attrs, ctrl) {
            var INTEGER_REGEXP = /^\-?\d+$/;
            ctrl.$parsers.unshift(function(viewValue) {
                if (INTEGER_REGEXP.test(viewValue)) {
                    // it is valid
                    ctrl.$setValidity('integer', true);
                    return viewValue;
                } else {
                    // it is invalid, return undefined (no model update)
                    ctrl.$setValidity('integer', false);
                    return undefined;
                }
            });
        }
    };
});

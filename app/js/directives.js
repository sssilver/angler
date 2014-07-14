app.directive('scDatepicker', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, element, attrs, ngModelCtrl) {
            var startView = attrs.startView;

            if (!startView)
                startView = 'month';

            $(element).datetimepicker({
                'startView': startView,
                'autoclose': true
            }).on('changeDate', function (e) {
                var outputDate = +new Date(e.date);

                // Apparently, Javascript timestamps are in milliseconds
                var unix_timestamp = Math.round(outputDate / 1000);

                ngModelCtrl.$setViewValue(unix_timestamp);
                scope.$apply();
            });;
        }
    };
});

app.directive('scDatetimepicker', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var mode = attrs.scDatepicker;

            if (!mode)
                mode = 'days';

            $(element).datetimepicker({
                'viewMode': mode
            });
        }
    };
});

app.directive('scInteger', function () {
    return {
        require: 'ngModel',
        link: function (scope, element, attrs, ctrl) {
            var INTEGER_REGEXP = /^\-?\d+$/;
            ctrl.$parsers.unshift(function (viewValue) {
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

app.directive('scMultiselect', [function () {
    return {
        link: function (scope, element, attrs) {
            //element = $(element);
            //console.log(element);

            element.multiselect({
                enableFiltering: true,

                // Replicate the native functionality on the elements so
                // that Angular can handle the changes for us
                onChange: function (optionElement, checked) {
                    optionElement.prop('selected', false);

                    if (checked)
                        optionElement.prop('selected', true);

                    element.change();
                }
            });

            scope.$watch(function () {
                return element[0].length;
            }, function () {
                element.multiselect('rebuild');
            });

            scope.$watch(attrs.ngModel, function () {
                element.multiselect('refresh');
            });
        }
    };
}]);
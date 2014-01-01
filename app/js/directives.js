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
                var outputDate = +new Date(e.date);

                // Apparently, Javascript timestamps are in milliseconds
                var unix_timestamp = Math.round(outputDate / 1000);

                ngModelCtrl.$setViewValue(unix_timestamp);
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
        link: function(scope, element, attrs, ctrl) {
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


app.directive('bsModal', function() {
    var link = function(scope, element, attrs) {
        /*
        scope.toggleModal = function(show) {
            if (show)
                $(element).modal('show');
            else
                $(element).modal('hide');
        }

        scope.$watch(attrs.bsModalShow, function (newValue, oldValue) {
            scope.toggleModal(newValue, attrs.$$element);
        });
        */

        $(element).modal('show');

        // Update the visible value when the dialog is closed through UI actions (Ok, cancel, etc.)
        element.bind('hide.bs.modal', function () {
            $parse(attrs.bsModalShow).assign(scope, false);
            if (!scope.$$phase && !scope.$root.$$phase)
                scope.$apply();
        });
    };

    return {
        link: link,
        restrict: 'A',
        templateUrl: 'template/modal.html',
        transclude: true
    };
})

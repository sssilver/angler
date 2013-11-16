app.directive('scDatepicker', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var mode = attrs.scDatepicker;

            if (!mode)
                mode = 'days';

            $(element).datepicker({
                'viewMode': mode
            });
        }
    };
});

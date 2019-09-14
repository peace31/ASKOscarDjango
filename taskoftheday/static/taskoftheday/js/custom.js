$(document).ready(function () {
    $('#chartprogress').on('change', function () {
        if (this.value == 'revenue-opt')
        //.....................^.......
        {
            $("#revenue").show();
        }
        else {
            $("#revenue").hide();
        }
    });
    $('#chartprogress').on('change', function () {
        if (this.value == 'rpu-opt')
        //.....................^.......
        {
            $("#rpu").show();
        }
        else {
            $("#rpu").hide();
        }
    });
    $('#chartprogress').on('change', function () {
        if (this.value == 'aov-opt')
        //.....................^.......
        {
            $("#aov").show();
        }
        else {
            $("#aov").hide();
        }
    });
    $('#chartprogress').on('change', function () {
        if (this.value == 'cr-opt')
        //.....................^.......
        {
            $("#cr").show();
        }
        else {
            $("#cr").hide();
        }
    });
    $('#chartprogress').on('change', function () {
        if (this.value == 'br-opt')
        //.....................^.......
        {
            $("#br").show();
        }
        else {
            $("#br").hide();
        }
    });
    $('#chartprogress').on('change', function () {
        if (this.value == 'scar-opt')
        //.....................^.......
        {
            $("#scar").show();
        }
        else {
            $("#scar").hide();
        }
    });
    $('#chartprogress').on('change', function () {
        if (this.value == 'traffic-opt')
        //.....................^.......
        {
            $("#traffic").show();
        }
        else {
            $("#traffic").hide();
        }
    });
});


$(function () {
    $('.button-checkbox').each(function () {

        // Settings
        var $widget = $(this),
            $button = $widget.find('button'),
            $button = $widget.find('button'),
            $checkbox = $widget.find('input:checkbox'),
            color = $button.data('color'),
            settings = {
                on: {
                    icon: 'glyphicon glyphicon-check'
                },
                off: {
                    icon: 'glyphicon glyphicon-unchecked'
                }
            };

        // Event Handlers
        $button.on('click', function () {
            $checkbox.prop('checked', !$checkbox.is(':checked'));
            $checkbox.triggerHandler('change');
            updateDisplay();
        });
        $checkbox.on('change', function () {
            updateDisplay();
        });

        // Actions
        function updateDisplay() {
            var isChecked = $checkbox.is(':checked');

            // Set the button's state
            $button.data('state', (isChecked) ? "on" : "off");

            // Set the button's icon
            $button.find('.state-icon')
                .removeClass()
                .addClass('state-icon ' + settings[$button.data('state')].icon);

            // Update the button's color
            if (isChecked) {
                $button
                    .removeClass('btn-default')
                    .addClass('btn-' + color + ' active');
            }
            else {
                $button
                    .removeClass('btn-' + color + ' active')
                    .addClass('btn-default');
            }
        }

        // Initialization
        function init() {

            updateDisplay();

            // Inject the icon if applicable
            if ($button.find('.state-icon').length == 0) {
                $button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i> ');
            }
        }

        init();
    });
});


$(function () {
    $('form.referral').each(function (i, e) {
        var form = $(e);
        options = {
            dataType: "json",
            success: function (data) {
                form.html('<input type="text" value="' + data.url + '" />');
                form.find("input[type=text]").select();
            }
        }
        form.ajaxForm(options);
    });
});
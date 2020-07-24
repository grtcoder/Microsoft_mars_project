/**
 * The control panel.
 */
var Panel = {
    init: function () {
        var $algo = $('#algorithm_panel');

        $('.panel').draggable();
        $('.accordion').accordion({
            collapsible: false,
        });
        $('.option_label').click(function () {
            $(this).prev().click();
        });
        $('#hide_instructions').click(function () {
            $('#instructions_panel').slideUp();
        });
        $('#play_panel').css({
            top: $algo.offset().top + $algo.outerHeight() + 20
        });
        $('#button2').attr('disabled', 'disabled');
    },
    /**
     * Get the user selected path-finder.
     * TODO: clean up this messy code.
     */
    getFinder: function () {
        var allowDiagonal = -1, dontCrossCorners = -1, timeLimit = -1;
        query = {};
        allowDiagonal = typeof $('#tsp_section ' +
            '.allow_diagonal:checked').val() !== 'undefined';
        // biDirectional = typeof $('#astar_section ' +
        //     '.bi-directional:checked').val() !== 'undefined';
        dontCrossCorners = typeof $('#tsp_section ' +
            '.dont_cross_corners:checked').val() !== 'undefined';
        //mars project stuff div
        // query['selected_header'] = selected_header;
        // query['heuristic'] = heuristic;
        query['allowDiagonal'] = allowDiagonal;
        // query['biDirectional'] = biDirectional;
        query['dontCrossCorners'] = dontCrossCorners;
        // query['weight'] = weight;
        // query['trackRecursion'] = trackRecursion;
        timeLimit = parseInt($('#tsp_section input[name=time_limit]').val());

        // Any non-negative integer, indicates "forever".
        timeLimit = (timeLimit <= 0 || isNaN(timeLimit)) ? -1 : timeLimit;
        query['timeLimit'] = timeLimit;
        console.log(query);
        return query;
    }
};

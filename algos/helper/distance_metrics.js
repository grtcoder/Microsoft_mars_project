/**
 * @namespace PF.Heuristic
 * @description A collection of heuristic functions.
 */
module.exports = {

    /**
     * Manhattan distance.
     * @param {number} dx - Difference in x.
     * @param {number} dy - Difference in y.
     * @return {number} dx + dy
     */
    manhattan: function (start, end) {
        return Math.abs(start.x - end.x) + Math.abs(start.y - end.y);
    },

    /**
     * Euclidean distance.
     * @param {number} dx - Difference in x.
     * @param {number} dy - Difference in y.
     * @return {number} sqrt(dx * dx + dy * dy)
     */
    euclidean: function (start, end) {
        var dx = Math.abs(start.x - end.x);
        var dy = Math.abs(start.y - end.y);
        return Math.sqrt(dx * dx + dy * dy);
    },

    /**
     * Octile distance.
     * @param {number} dx - Difference in x.
     * @param {number} dy - Difference in y.
     * @return {number} sqrt(dx * dx + dy * dy) for grids
     */
    octile: function (start, end) {
        var F = Math.SQRT2 - 1;
        var dx = Math.abs(start.x - end.x);
        var dy = Math.abs(start.y - end.y);
        return (dx < dy) ? F * dx + dy : F * dy + dx;
    },

    /**
     * Chebyshev distance.
     * @param {number} dx - Difference in x.
     * @param {number} dy - Difference in y.
     * @return {number} max(dx, dy)
     */
    chebyshev: function (start, end) {
        var dx = Math.abs(start.x - end.x);
        var dy = Math.abs(start.y - end.y);
        return Math.max(dx, dy);
    }

};
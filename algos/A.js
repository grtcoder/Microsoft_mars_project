const point = require('./point');
const map = require('./map');
const heap = require('collections/heap');
class A_star_node {
    constructor(x, y, f) {
        this.x = x;
        this.y = y;
        this.f = f == undefined ? Infinity : f;
    }
};
class A_star_solver {
    constructor(graph, start, end) {
        this.graph = graph;
        this.start = start;
        this.end = end;
        this.parent = {};
    }
    isvalid(pt, value) {
        if (pt.x >= 0 && pt.y >= 0 && pt.x < graph.length && pt.y < graph.breadth && graph.matrix[pt.x][pt.y] != '4') {
            return true;
        }
        return false;
    }
    fval(pt) {
        return 1 + hval(pt, end);
    }
    hval(pt) {//add heuristics corresponding to each distance metric
        return 0;
    }
    ntc(num) {
        var y = num % graph.length;
        var x = Math.floor(num / graph.length);
        return new point.point(x, y);
    }
    ctn(pt) {
        return (graph.length * pt.x) + pt.y;
    }
    path() {
        var iter = this.ctn(end);
        // console.log(this.parent[iter]==iter);
        while (this.parent[iter] != iter) {
            var pt = this.ntc(iter);
            console.log(pt);
            graph.matrix[pt.x][pt.y] = 'x';
            iter = this.parent[iter];
        }
    }
    findpath() {
        var visited = new map.map(graph.length, graph.breadth);
        var openlist = new heap([], true, function (a, b) {
            return a.f <= b.f;
        });
        var possiblen = [[1, 0], [0, 1], [-1, 0], [0, -1]];
        start.f = 0;
        this.parent[0] = 0;
        openlist.push(start);
        while (openlist.length != 0) {
            var curr = openlist.pop();
            var dist = curr.f + 1;
            // console.log(curr);
            visited.matrix[curr.x][curr.y] = '1';
            if (end.x == curr.x && end.y == curr.y) {
                this.path();
                graph.print_map();
                visited.print_map();
                // console.log(this.parent);
                break;
            }
            for (let i = 0; i < possiblen.length; i++) {
                var pt = new A_star_node(curr.x + possiblen[i][0], curr.y + possiblen[i][1], dist);
                if (this.isvalid(pt) && visited.matrix[pt.x][pt.y] == '0') {
                    this.parent[this.ctn(pt)] = this.ctn(curr);
                    openlist.push(pt);
                }
            }
        }
    }
};
var graph = new map.map(10, 10);
var start = new A_star_node(0, 0);
var end = new A_star_node(5, 5);
graph.matrix[1][0] = '4';
graph.matrix[0][2] = '4';
graph.matrix[3][0] = '4';
graph.matrix[1][2] = '4';
// graph.matrix[2][1] = '4';
// graph.print_map();
var solver = new A_star_solver(graph, start, end);
solver.findpath();


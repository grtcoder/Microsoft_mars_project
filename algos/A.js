const point = require('./point');
const map = require('./map');
const heap = require('collections/heap');
// var adjacency_list=[]
// var pt=new point.point(1,2,3);
// console.log(pt);
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
    path() {
        // var iter = end;
        // while (this.parent[iter] != iter) {
        //     console.log(iter);
        //     // console.log(parent[iter]);
        //     iter = this.parent[iter];
        // }
    }
    findpath() {
        var visited = new map.map(graph.length, graph.breadth);
        var parent = {};
        var openlist = new heap([], true, function (a, b) {
            return a.f <= b.f;
        });
        var possiblen = [[1, 0], [0, 1], [-1, 0], [0, -1]];
        start.f = 0;
        // parent.push( new A_star_node(start.x, start.y, start.f));
        // console.log(parent.keys());
        openlist.push(start);
        while (openlist.length != 0) {
            var curr = openlist.pop();
            var dist = curr.f + 1;
            console.log(curr);
            visited.matrix[curr.x][curr.y] = '1';
            if (end.x == curr.x && end.y == curr.y) {
                // for (var key in parent) {
                //     console.log(key.x);
                // }
                break;
            }
            for (let i = 0; i < possiblen.length; i++) {
                var pt = new A_star_node(curr.x + possiblen[i][0], curr.y + possiblen[i][1], dist);
                if (this.isvalid(pt) && visited.matrix[pt.x][pt.y] == '0') {
                    // console.log(graph.matrix[curr.x][curr.y]);
                    // parent[pt] = new A_star_node(curr.x, curr.y, curr.f);
                    openlist.push(pt);
                }
            }
        }
        console.log(visited.print_map());
    }
};
var graph = new map.map(10, 10);
var start = new A_star_node(0, 0);
var end = new A_star_node(5, 5);
graph.matrix[1][1]='4';
// graph.print_map();
var solver = new A_star_solver(graph, start, end);
solver.findpath();


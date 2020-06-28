const point = require('./point');
const map = require('./map');
const heap = require('collections/heap');
// var adjacency_list=[]
// var pt=new point.point(1,2,3);
// console.log(pt);
class A_star_node {
    constructor(pt, parent) {
        this.pt = pt;
        this.f = Infinity;
        this.parent = parent;
    }
};
function minfind(openList) {
    var minimum = openlist[0];
    var ind = 0;
    for (let index = 1; index < openlist.length; index++) {
        if (minimum.f > openList[index].f) {
            minimum = openList[index];
            ind = index;
        }
    }
    return ind;
};
function isvalid(pt, length, breadth, value) {
    if (pt.x != length && pt.y != breadth && value != 4) {
        return true;
    }
    return false;
}
function fval(pt, end) {
    return 1 + hval(pt, end);
}
function hval(pt, end) {//add heuristics corresponding to each distance metric
    return 0;
}
function findpath(graph, start, end) {
    var visited = map.map(graph.length, graph.breadth);
    var openlist = new heap([], true, function (a, b) {
        return a.f <= b.f;
    });
    var possiblen = [[1, 0], [0, 1], [-1, 0], [0, -1]];
    for (let index = 0; index < 4; index++) {
        var pt = point.point(start.x + possiblen[index][0], start.y + possiblen[index][1]);
        if (isvalid(pt, graph.length, graph.breadth, graph[x][y])) {
            openlist.push(A_star_node(pt, fval(pt, end), start));
        }
    }
    while (openlist.length != 0) {
        var curr = openlist.pop();
        visited[curr.x][curr.y] = 1;
        for (let i = 0; i < possiblen.length; i++) {
            var pt = point.point(curr.x + possiblen[index][0], curr.y + possiblen[index][1]);
            if(end==pt){
                break;
            }
            if (isvalid(pt, graph.length, graph.breadth, graph[x][y]) && visited[pt.x][pt.y] != 1 && !issolved) {
                openlist.push(A_star_node(pt, fval(pt, end), curr));
            }

        }
    }
};


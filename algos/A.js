const point = require('./point');
const map = require('./map');
// var adjacency_list=[]
// var pt=new point.point(1,2,3);
// console.log(pt);
class A_star_node {
    constructor(x,y,parent) {
        this.x=x;
        this.y=y;
        this.f = Infinity;
        this.parent=point.point(parent.x,parent.y);
    }
};
function minfind(openList) {
    var minimum = openlist[0];
    var ind=0;
    for (let index = 1; index < openlist.length; index++) {
        if(minimum.f>openList[index].f){
            minimum=openList[index];
            ind=index;
        }
    }
    return ind;
};
function isvalid(x, y, value, length, breadth) {
    if (x != length && y != breadth && value != '4') {
        return true;
    }
    return false;
}
function findpath(map, start) {
    var openlist = [];
    var closedlist = [start];
    var possiblen = [[1, 0], [0, 1], [-1, 0], [0, -1]];
    for (let index = 0; index < 4; index++) {
        if (isvalid(start.x + possiblen[index][0], start.y + possiblen[index][1], map[start.x + possiblen[index][0]][start.y + possiblen[index][1]])) {
            openlist.push(map[start.x + possiblen[index][0]][start.y + possiblen[index][1]]);
        }
    }
    while (openlist.length != 0) {
        var curr=minfind(openlist);
        openlist.splice(curr,1);
        
    }
};


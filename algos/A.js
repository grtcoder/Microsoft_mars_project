var point=require('./point.js')
var adjacency_list=[]
var pt=new point.point(1,2,3);
console.log(pt);
function findpath(adjlist,start,end) {
    var open=[];
    var closed=[start];
};
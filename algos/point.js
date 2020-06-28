//a grid point on the map
class point{
    /* @params
        x :- x-coordinate
        y :- y-coordinate
        type represents what type of point is it
        type 1 :- plane point
        type 2 :- slightly rough patch
        type 3 :- medium rough patch
        type 4 :- blockage
    */ 
    constructor(x,y){
        this.x=x;
        this.y=y;
    }
};

class node{
    
}
//Setting up parameters for export
exports.point=point;

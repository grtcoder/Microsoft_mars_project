const point=require('./point');
class map {
    constructor(length, breadth) {
        this.length = length;
        this.breadth = breadth;
        this.matrix = [];
        const default_array = []
        for (let i = 0; i < breadth; i++) {
            var arr=[]
            for (let j = 0; j < length; j++) {
                // var val=new point.point(i,j);
                arr.push('0');
            }
            this.matrix.push(arr);
        }
        // console.log(this.matrix);
    }
    print_map() {
        for (let i = 0; i < this.breadth; i++) {
            for (let j = 0; j < this.length; j++) {
                process.stdout.write(this.matrix[i][j]+' ');
            }
            process.stdout.write('\n');
        }
    }
};
// var x = new map(5, 5);
// x.matrix[0][4] = '1';
// x.print_map();
exports.map = map;




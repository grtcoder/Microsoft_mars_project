class map {
    constructor(length, breadth) {
        this.length = length;
        this.breadth = breadth;
        this.matrix = [];
        const default_array = []
        for (let index = 0; index < length; index++) {
            default_array.push('0');
        }
        for (let index = 0; index < breadth; index++) {
            this.matrix.push(default_array);
        }
        // console.log(this.matrix);
    }
    print_map() {
        for (let i = 0; i < this.breadth; i++) {
            for (let j = 0; j < this.length; j++) {
                process.stdout.write(this.matrix[i][j]);
            }
            process.stdout.write('\n');
        }
    }
};
var x = new map(50, 50);
x.print_map();
exports.map = map;
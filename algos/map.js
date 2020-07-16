class map {
    constructor(length, breadth) {
        this.length = length;
        this.breadth = breadth;
        this.matrix = [];
        const default_array = []
        for (let i = 0; i < breadth; i++) {
            var arr = []
            for (let j = 0; j < length; j++) {
                arr.push(1);
            }
            this.matrix.push(arr);
        }
    }
    print_map() {
        for (let i = 0; i < this.breadth; i++) {
            for (let j = 0; j < this.length; j++) {
                process.stdout.write(this.matrix[i][j] + ' ');
            }
            process.stdout.write('\n');
        }
    }
    clone() {
        var newMap = new map(this.length, this.breadth);
        newMap.matrix = JSON.parse(JSON.stringify(this.matrix));
        return newMap;
    }
};

// var x = new map(5, 5);
// var y=x.clone();
// x.matrix[0][4] = 0;
// x.print_map();
// y.print_map();
// exports.map = map;




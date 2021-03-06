/**
 * The pathfinding visualization.
 * It uses raphael.js to show the grids.
 */
//Two types of coordinates, grid and page, u concern urself with only GRID
var View = {
    nodeSize: 30, // width and height of a single node, in pixel
    nodeStyle: {
        normal: {
            fill: 'white',
            'stroke-opacity': 0.2, // the border
        },
        conv: {
            fill: 'red',
            'stroke-opacity': 0.6
        },
        weighted: {
            fill: 'grey',
            'stroke-opacity': 0.2,
        },
        blocked: {
            fill: 'black',
            'stroke-opacity': 0.2,
        },
        start: {
            fill: '#0d0',
            'stroke-opacity': 0.2,
        },
        end: {
            fill: '#e40',
            'stroke-opacity': 0.2,
        },
        opened: {//openlist
            fill: '#98fb98',
            'stroke-opacity': 0.2,
        },
        closed: {//closedlist
            fill: '#afeeee',
            'stroke-opacity': 0.2,
        },
        failed: {
            fill: '#ff8888',
            'stroke-opacity': 0.2,
        },
        tested: {
            fill: '#e5e5e5',
            'stroke-opacity': 0.2,
        },

    },
    nodeColorizeEffect: {
        duration: 50,
    },
    nodeZoomEffect: {
        duration: 200,
        transform: 's1.2', // scale by 1.2x
        transformBack: 's1.0',
    },
    pathStyle: {
        stroke: 'yellow',
        'stroke-width': 3,
    },
    supportedOperations: ['opened', 'closed', 'tested'],
    init: function (opts) {
        this.numCols = opts.numCols;
        this.numRows = opts.numRows;
        this.paper = Raphael('draw_area');//paper object
        this.$stats = $('#stats');
    },
    /**
     * Generate the grid asynchronously.
     * This method will be a very expensive task.
     * Therefore, in order to not to block the rendering of browser ui,
     * I decomposed the task into smaller ones. Each will only generate a row.
     */
    generateGrid: function (callback) {
        var i, j, x, y,
            rect,
            normalStyle, nodeSize,
            createRowTask, sleep, tasks,
            nodeSize = this.nodeSize,
            normalStyle = this.nodeStyle.normal,
            numCols = this.numCols,
            numRows = this.numRows,
            paper = this.paper,
            rects = this.rects = [],
            $stats = this.$stats;

        paper.setSize(numCols * nodeSize, numRows * nodeSize);//div paper size set

        createRowTask = function (rowId) {
            return function (done) {
                rects[rowId] = [];
                for (j = 0; j < numCols; ++j) {
                    x = j * nodeSize;
                    y = rowId * nodeSize;
                    rect = paper.rect(x, y, nodeSize, nodeSize, 8);
                    rect.attr(normalStyle);
                    rects[rowId].push(rect);
                }
                $stats.text(
                    'generating grid ' +
                    Math.round((rowId + 1) / numRows * 100) + '%'
                );
                done(null);
            };
        };

        sleep = function (done) {
            setTimeout(function () {
                done(null);
            }, 0);
        };

        tasks = [];
        for (i = 0; i < numRows; ++i) {
            tasks.push(createRowTask(i));
            tasks.push(sleep);
        }

        async.series(tasks, function () {
            if (callback) {
                callback();
            }
        });
    },
    setStartPos: function (gridX, gridY) {
        var coord = this.toPageCoordinate(gridX, gridY);
        if (!this.startNode) {
            this.startNode = this.paper.rect(
                coord[0],
                coord[1],
                this.nodeSize,//div setting color to attribuite in start node
                this.nodeSize,
                8
            ).attr(this.nodeStyle.normal)
                .animate(this.nodeStyle.start, 1000);
        } else {
            this.startNode.attr({ x: coord[0], y: coord[1] }).toFront();
        }
    },
    setEndPos: function (gridX, gridY) {
        var coord = this.toPageCoordinate(gridX, gridY);
        if (!this.endNode) {
            this.endNode = this.paper.rect(
                coord[0],//div segments are taken as continuous chunks
                coord[1],
                this.nodeSize,
                this.nodeSize,
                8
            ).attr(this.nodeStyle.normal)
                .animate(this.nodeStyle.end, 1000);
        } else {
            this.endNode.attr({ x: coord[0], y: coord[1] }).toFront();
        }
    },
    /**
     * Set the attribute of the node at the given coordinate.
     */
    setAttributeAt: function (gridX, gridY, attr, value, weight) {//div here
        var color, nodeStyle = this.nodeStyle;
        switch (attr) {
            case 'walkable':
                // this.colorizeNode(this.rects[gridY][gridX],color);
                this.setWalkableAt(gridX, gridY, value, weight);
                console.log(value);
                break;
            case 'opened':
                this.colorizeNode(this.rects[gridY][gridX], nodeStyle.opened.fill);
                this.setCoordDirty(gridX, gridY, true);
                break;
            case 'closed':
                this.colorizeNode(this.rects[gridY][gridX], nodeStyle.closed.fill);
                this.setCoordDirty(gridX, gridY, true);
                break;
            case 'tested':
                color = (value === true) ? nodeStyle.tested.fill : nodeStyle.normal.fill;//div remember

                this.colorizeNode(this.rects[gridY][gridX], color);
                this.setCoordDirty(gridX, gridY, true);
                break;
            case 'parent':
                // XXX: Maybe draw a line from this node to its parent?
                // This would be expensive.
                break;
            default:
                console.error('unsupported operation: ' + attr + ':' + value);
                return;
        }
    },
    colorizeNode: function (node, color) {
        node.animate({
            fill: color
        }, this.nodeColorizeEffect.duration);
    },
    zoomNode: function (node) {
        node.toFront().attr({
            transform: this.nodeZoomEffect.transform,
        }).animate({
            transform: this.nodeZoomEffect.transformBack,
        }, this.nodeZoomEffect.duration);
    },
    setWalkableAt: function (gridX, gridY, value, weight) {
        var node, i, blockedNodes = this.blockedNodes, roughNodes = this.roughNodes, textsRough = this.textsRough, redNodes = this.redNodes;
        if (!blockedNodes) {
            blockedNodes = this.blockedNodes = new Array(this.numRows);
            for (i = 0; i < this.numRows; ++i) {
                blockedNodes[i] = [];
            }
        }
        if (!roughNodes) {
            roughNodes = this.roughNodes = new Array(this.numRows);
            textsRough = this.textsRough = new Array(this.numRows);
            roughWeights = this.roughWeights = new Array(this.numRows);
            for (i = 0; i < this.numRows; ++i) {
                roughNodes[i] = [];
                textsRough[i] = [];
            }
        }
        if (!redNodes) {
            redNodes = this.redNodes = new Array(this.numRows);
            for (i = 0; i < this.numRows; i++) {
                redNodes[i] = [];
            }
        }
        console.log('greyval is' + String(weight));
        var nodeBlock = blockedNodes[gridY][gridX];//div here changes
        var nodeRough = roughNodes[gridY][gridX];
        var nodeRed = redNodes[gridY][gridX];
        if (nodeBlock)
            node = nodeBlock;
        if (nodeRough)
            node = nodeRough;
        if (nodeRed)
            node = nodeRed;
        console.log(value);
        coord = this.toPageCoordinate(gridX, gridY);
        if (value == 0) {
            // clear blocked node
            if (node) {
                this.colorizeNode(node, this.nodeStyle.normal.fill);
                this.zoomNode(node);
                blockedNodes[gridY][gridX] = null;
                roughNodes[gridY][gridX] = null;
                redNodes[gridY][gridX] = null;
                if (nodeRough) {
                    nodeRough.remove();
                    textsRough[gridY][gridX].remove();
                    textsRough[gridY][gridX] = null;
                }
                if (nodeBlock)
                    nodeBlock.remove();
                if (nodeRed)
                    nodeRed.remove();
                return;
            }
        }
        if (value == 1) {
            //add rough node
            if (nodeRough) {
                return;
            }
            nodeRough = roughNodes[gridY][gridX] = this.rects[gridY][gridX].clone();
            this.colorizeNode(nodeRough, this.nodeStyle.weighted.fill);
            this.zoomNode(nodeRough);
            textsRough[gridY][gridX] = this.paper.text(coord[0] + this.nodeSize / 2, coord[1] + this.nodeSize / 2, String(weight));
            return;
        }
        if (value == 2) {
            // draw blocked node
            if (nodeBlock)
                return;
            nodeBlock = blockedNodes[gridY][gridX] = this.rects[gridY][gridX].clone();
            this.colorizeNode(nodeBlock, this.nodeStyle.blocked.fill);
            this.zoomNode(nodeBlock);
            return;
        }
        if (value == 3) {
            if (nodeRed)
                return;
            nodeRed = redNodes[gridY][gridX] = this.rects[gridY][gridX].clone();
            this.colorizeNode(nodeRed, this.nodeStyle.end.fill);
            this.zoomNode(nodeRed);
        }
    },
    clearFootprints: function () {
        var i, x, y, coord, coords = this.getDirtyCoords();
        for (i = 0; i < coords.length; ++i) {
            coord = coords[i];
            x = coord[0];
            y = coord[1];
            this.rects[y][x].attr(this.nodeStyle.normal);
            this.setCoordDirty(x, y, false);
        }
    },
    clearBlockedNodes: function () {
        var i, j, blockedNodes = this.blockedNodes, roughNodes = this.roughNodes, textsRough = this.textsRough, redNodes = this.redNodes;
        if (!blockedNodes) {
            return;
        }
        for (i = 0; i < this.numRows; ++i) {
            for (j = 0; j < this.numCols; ++j) {
                if (blockedNodes[i][j]) {
                    blockedNodes[i][j].remove();
                    blockedNodes[i][j] = null;
                }
                if (roughNodes[i][j]) {
                    roughNodes[i][j].remove();
                    roughNodes[i][j] = null;
                    textsRough[i][j].remove();
                    textsRough[i][j] = null;
                }
                if (redNodes[i][j]) {
                    redNodes[i][j].remove();
                    redNodes[i][j] = null;
                }
            }
        }
    },
    drawPath: function (path) {
        if (!path.length) {
            return;
        }
        var svgPath = this.buildSvgPath(path);
        console.log(svgPath);
        this.path = this.paper.path(svgPath).attr(this.pathStyle);
    },
    /**
     * Given a path, build its SVG represention.
     */
    buildSvgPath: function (path) {
        var i, strs = [], size = this.nodeSize;

        strs.push('M' + (path[0][0] * size + size / 2) + ' ' +
            (path[0][1] * size + size / 2));
        for (i = 1; i < path.length; ++i) {
            strs.push('L' + (path[i][0] * size + size / 2) + ' ' +
                (path[i][1] * size + size / 2));
        }
        return strs.join('');
    },
    clearPath: function () {
        if (this.path) {
            this.path.remove();
        }
    },
    /**
     * Helper function to convert the page coordinate to grid coordinate
     */
    toGridCoordinate: function (pageX, pageY) {
        return [
            Math.floor(pageX / this.nodeSize),
            Math.floor(pageY / this.nodeSize)
        ];
    },
    /**
     * helper function to convert the grid coordinate to page coordinate
     */
    toPageCoordinate: function (gridX, gridY) {
        return [
            gridX * this.nodeSize,
            gridY * this.nodeSize
        ];
    },
    showStats: function (opts) {
        var texts = [
            'length: ' + Math.round(opts.pathLength * 100) / 100,
            'time: ' + opts.timeSpent + 'ms',
            'operations: ' + opts.operationCount
        ];
        $('#stats').show().html(texts.join('<br>'));
    },
    setCoordDirty: function (gridX, gridY, isDirty) {
        var x, y,
            numRows = this.numRows,
            numCols = this.numCols,
            coordDirty;

        if (this.coordDirty === undefined) {
            coordDirty = this.coordDirty = [];
            for (y = 0; y < numRows; ++y) {
                coordDirty.push([]);
                for (x = 0; x < numCols; ++x) {
                    coordDirty[y].push(false);
                }
            }
        }

        this.coordDirty[gridY][gridX] = isDirty;
    },
    getDirtyCoords: function () {
        var x, y,
            numRows = this.numRows,
            numCols = this.numCols,
            coordDirty = this.coordDirty,
            coords = [];

        if (coordDirty === undefined) {
            return [];
        }

        for (y = 0; y < numRows; ++y) {
            for (x = 0; x < numCols; ++x) {
                if (coordDirty[y][x]) {
                    coords.push([x, y]);
                }
            }
        }
        return coords;
    },
};

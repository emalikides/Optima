var ThreeDraw = function (canvas) {
    var BGCOLOR = "rgb(8,50,59)";
    canvas.width = 350;
    canvas.height = 300;
    var ctx = canvas.getContext('2d');

    var camera = (function () {
        var camera = {};
        camera.pos = {r:1, p:0, t:Math.PI/10}
        return camera;
    })();

    var update = function (vertices) {
        ctx.fillStyle = BGCOLOR;
        ctx.fillRect( 0, 0, ctx.canvas.width, ctx.canvas.height)
        ctx.beginPath();

        // create axis
        var axisVertices = [
            [{x:0,y:0,z:0,w:1}, {x:100,y:0,z:0,w:1}],
            [{x:0,y:0,z:0,w:1}, {x:0,y:100,z:0,w:1}],
            [{x:0,y:0,z:0,w:1}, {x:0,y:0,z:100,w:1}]
        ];

        var verticeGroups = [];
        verticeGroups.push(vertices);
        verticeGroups.push(axisVertices[0]);
        verticeGroups.push(axisVertices[1]);
        verticeGroups.push(axisVertices[2]);

        for (var i=0; i<verticeGroups.length; i++) {
            ctx.beginPath();
            for (var j=0; j<verticeGroups[i].length; j++) {
                var vtx = verticeGroups[i][j];

                // Euler rotate to camera
                vtx = rotateEuler(vtx, 0,camera.pos.t,camera.pos.p);

                // Translate away from camera
                vtx = translate3D(vtx, {r:150, t:Math.PI/2, p:Math.PI/2});

                // Perspective
                /*
                vtx = perspectiveTransform(vtx);
                vtx.x = vtx.x/vtx.w;
                vtx.y = vtx.y/vtx.w;
                vtx.z = vtx.z/vtx.w;
                */

                // Map to canvas
                vtx = {x: ctx.canvas.width/2 + vtx.x, y: ctx.canvas.height-100 - vtx.z}

                // Draw
                if (j==0) {
                    ctx.moveTo(vtx.x, vtx.y);
                }
                else {
                    ctx.lineTo(vtx.x, vtx.y);
                    if (j == verticeGroups[i].length - 1) {
                        if (i==0) {//antenna
                            ctx.strokeStyle = 'rgb(159,187,77)';
                        }
                        else {//axis
                            ctx.strokeStyle = 'rgb(87,179,205)';
                        }
                        ctx.stroke();
                    }
                }
            }
        }
    };
    
    this.camera = camera;
    this.update = update;
}

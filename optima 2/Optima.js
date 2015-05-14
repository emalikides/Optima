function Antenna () {
    var antenna = this;

    var model = (function () {
        function Rod (o,v) {
            var rod = this;
            rod.origin = {
                r: o.r,
                t: o.t,
                p: o.p
            };
            rod.vec = {
                r: v.r,
                t: v.t,
                p: v.p,
                setP: function(p_) {
                    this.p = p_ % (2*Math.PI);
                    cols.p.val(p_ * RAD2DEG );
                    cols.p.trigger("change");
                }
            }

            var controls = $("<div>").addClass("row");
            var cols = {
                r: $("<input type='text' value='"+ rod.vec.r + "'>"),
                t: $("<input type='text' value='"+ Math.round(rod.vec.t * RAD2DEG) +"'>"),
                p: $("<input type='text' value='"+ Math.round(rod.vec.p * RAD2DEG) +"'>"),
            }
            controls.append(cols.r);
            controls.append(cols.t);
            controls.append(cols.p);
            cols.r.knob({
                'min': 0,
                'max': 200,

                'thickness': 0.1,
                'width': 40,
                'bgColor': '#666',

                'change': function (value) {
                    rod.vec.r = value;
                }
            });
            cols.t.knob({
                'min': 0,
                'max': 360,

                'thickness': 0.1,
                'width': 40,
                'bgColor': '#666',

                'change': function (value) {
                    rod.vec.t = value * Math.PI / 180;
                }
            });
            cols.p.knob({
                'min': 0,
                'max': 360,

                'thickness': 0.1,
                'width': 40,
                'bgColor': '#666',

                'change': function (value) {
                    rod.vec.p = value * Math.PI / 180;
                }
            });
            $("#controls").append(controls);

            function getEndPoint () {
                return vecSum(rod.origin, rod.vec);
            }

            rod.controls = controls;
            rod.getEndPoint = getEndPoint;
        }

        var rods = [];
        for (var i=0; i<5; i++) {
            var rodStart = i==0?{r:0, t:0, p:0}:rods[i-1].getEndPoint();
            rods[i] = new Rod(rodStart, {r:50, t:Math.PI/4, p:i*Math.PI/4});
            $("<div>").addClass("rowTitle").html(i).prependTo(rods[i].controls);
        }

        function update () {
            for (var i=1; i<rods.length; i++) {
                rods[i].origin = rods[i-1].getEndPoint();
            }
        }

        return {
            rods: rods,
            update: update
        }
    })();

    var canvas = document.getElementById("c1");
    var view = new ThreeDraw(canvas);

    setInterval(function rotate() {
        view.camera.pos.p += 0.005;
        model.update();

        // Array of N(rods)+1 vertices in cartesian
        var vertices = [];
        var r = changeCoords(model.rods[0].origin, "Cartesian");
        vertices[0] = {x:r.x, y:r.z, z:r.z, w:1};
        for (var i=1; i<model.rods.length+1; i++) {
            r = changeCoords(model.rods[i-1].getEndPoint(), "Cartesian");
            vertices[i] = {x:r.x, y:r.y, z:r.z, w:1};
        }

        view.update(vertices);

        for (var i=0; i<model.rods.length; i++) {
            model.rods[i].vec.setP(model.rods[i].vec.p + 0.005*(i+1));
        }
    }, 30);
}

var antenna = new Antenna();

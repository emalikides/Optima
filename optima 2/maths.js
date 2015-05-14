var DEG2RAD = Math.PI / 180;
var RAD2DEG = 1/DEG2RAD;

function matMult (m1, m2) {
    // make sure lists are treated as matrices
    if (arguments.length != 2) { throw "can only handle 2 matrices" }
    for (var i=0; i<2; i++) {
        if (arguments[i][0].constructor !== Array) {
            for (var j=0; j<arguments[i].length; j++) {
                arguments[i][j]=[arguments[i][j]];
            }
        }
    }
    var result = [];
    for (var i = 0; i < m1.length; i++) {
        result[i] = [];
        for (var j = 0; j < m2[0].length; j++) {
            var sum = 0;
            for (var k = 0; k < m1[0].length; k++) {
                sum += m1[i][k] * m2[k][j];
            }
            result[i][j] = sum;
        }
    }
    return result;
}

function perspectiveTransform (v) {
    var n = 160;
    var f = 170;
    var r = 6;
    var t = 1;
    var perspMat = 
        [[n/r,0,0,0],
         [0,n/t,0,0],
         [0,0,-(f+n)/(f-n),-2*f*n/(f-n)],
         [0,0,1,0]];
    var perspMat =
        [[1,0,0,0],
         [0,1,0,0],
         [0,0,1,0],
         [0,0,0,1]];
    var A = matMult(perspMat, [[v.x], [v.y], [v.z], [v.w]]);
    return {x:A[0][0], y:A[1][0], z:A[2][0], w:A[3][0]};
}

function translate3D (vertice, vec_) {
    vec = changeCoords(vec_, "Cartesian");
    return vecSum(vertice, vec);
}

function rotateEuler (v, a,b,g) {
    var c1 = Math.cos(a);
    var c2 = Math.cos(b);
    var c3 = Math.cos(g);
    var s1 = Math.sin(a);
    var s2 = Math.sin(b);
    var s3 = Math.sin(g);
    var rot =
        [[c1*c3, -c1*s3-c2*c3*s1,  s1*s2],
         [c3*s1+c1*c2*s3,  c1*c2*c3-s1*s3, -c1*s2],
         [s2*s3,   c3*s2,     c2]];
    var n = matMult(rot, [[v.x], [v.y], [v.z]]);
    return {x:n[0][0], y:n[1][0], z:n[2][0], w:v.w};
}

function getCoordSystem (x) {
    if (x.hasOwnProperty("r")) {
        return "Spherical";
    }
    else {
        return "Cartesian";
    }
}
function changeCoords(a,sys) {
    if (getCoordSystem(a) == sys) {
        return a;
    }
    var b = {};
    if (sys == "Cartesian") {
        // change to cartesian
        b.x = a.r * Math.sin(a.t) * Math.cos(a.p);
        b.y = a.r * Math.sin(a.t) * Math.sin(a.p);
        b.z = a.r * Math.cos(a.t);
    }
    else {
        // change to spherical
        b.r = Math.sqrt(a.x*a.x + a.y*a.y + a.z*a.z);
        if (b.r == 0) {
            b.t = 0;
            b.p = 0;
            return b;
        }
        b.t = Math.acos(a.z / b.r);
        if (a.x != 0) {
            b.p = Math.atan2(a.y, a.x)
        }
        else if (a.x == 0 && a.z > 0) {
            b.p = 0;
        }
        else {
            b.p = Math.PI;
        }
    }
    b.w = a.w;
    return b;
}

function vecSum(a_,b_) {
    var sys = getCoordSystem(a_);
    if (getCoordSystem(a_) != getCoordSystem(b_)) {
        throw "Vectors in different coordinate systems";
    }
    if (sys != "Cartesian") {
        var a = changeCoords(a_, "Cartesian");
        var b = changeCoords(b_, "Cartesian");
    }
    else {
        var a = a_;
        var b = b_;
    }
    var sum = {x: a.x + b.x,
               y: a.y + b.y,
               z: a.z + b.z};
    if (sys != "Cartesian") {
        sum = changeCoords(sum, sys);
    }
    sum.w = a_.w;
    return sum;
}

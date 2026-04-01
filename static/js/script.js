const canvas = document.getElementById('shader-bg');
const gl = canvas.getContext('webgl');

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    gl.viewport(0, 0, canvas.width, canvas.height);
}
window.addEventListener('resize', resize);
resize();

const vertexShaderSrc = `
    attribute vec2 position;
    void main() {
        gl_Position = vec4(position, 0.0, 1.0);
    }
`;

const fragmentShaderSrc = `
    precision mediump float;
    uniform vec2 iResolution;
    uniform float iTime;

    void main() {
        vec2 fragCoord = gl_FragCoord.xy;
        float mr = min(iResolution.x, iResolution.y);
        vec2 uv = (fragCoord * 2.0 - iResolution.xy) / mr;

        float d = -iTime * 0.5;
        float a = 0.0;
        for (float i = 0.0; i < 8.0; ++i) {
            a += cos(i - d - a * uv.x);
            d += sin(uv.y * i + a);
        }
        d += iTime * 0.5;

        vec3 col = vec3(cos(uv * vec2(d, a)) * 0.6 + 0.4, cos(a + d) * 0.5 + 0.5);
        col = cos(col * cos(vec3(d, a, 2.5)) * 0.5 + 0.5);

        // Palette argentée : #EAEAEA, #DBDBDB, #F2F2F2, #ADA996
        vec3 silver1 = vec3(0.918, 0.918, 0.918); // #EAEAEA
        vec3 silver2 = vec3(0.859, 0.859, 0.859); // #DBDBDB
        vec3 silver3 = vec3(0.949, 0.949, 0.949); // #F2F2F2
        vec3 silver4 = vec3(0.678, 0.663, 0.588); // #ADA996

        // Mélange les couleurs argentées avec le shader
        float t = col.r * 0.5 + col.g * 0.3 + col.b * 0.2;
        vec3 finalColor = mix(
            mix(silver4, silver2, t),
            mix(silver1, silver3, t),
            col.g
        );

        gl_FragColor = vec4(finalColor, 1.0);
    }
`;

function compileShader(gl, type, src) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, src);
    gl.compileShader(shader);
    return shader;
}

const vertShader = compileShader(gl, gl.VERTEX_SHADER, vertexShaderSrc);
const fragShader = compileShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSrc);

const program = gl.createProgram();
gl.attachShader(program, vertShader);
gl.attachShader(program, fragShader);
gl.linkProgram(program);
gl.useProgram(program);

const vertices = new Float32Array([-1,-1, 1,-1, -1,1, 1,1]);
const buffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

const position = gl.getAttribLocation(program, 'position');
gl.enableVertexAttribArray(position);
gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);

const iResolution = gl.getUniformLocation(program, 'iResolution');
const iTime = gl.getUniformLocation(program, 'iTime');

const startTime = performance.now();

function render() {
    const elapsed = (performance.now() - startTime) / 1000;
    gl.uniform2f(iResolution, canvas.width, canvas.height);
    gl.uniform1f(iTime, elapsed);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    requestAnimationFrame(render);
}

render();
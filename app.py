import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Hide Streamlit UI elements for immersive experience
st.markdown("""
    <style>
    [data-testid="stSidebar"], section[data-testid="stSidebar"], .st-emotion-cache-16ids0d, .st-emotion-cache-6qob1r {
        display: none !important; width: 0 !important;
    }
    header, footer, #MainMenu { visibility: hidden !important; }
    .main, .block-container, [data-testid="stAppViewContainer"] {
        margin: 0 !important; padding: 0 !important; overflow: hidden !important;
        height: 100vh !important; width: 100vw !important;
    }
    iframe { border: none; width: 100vw; height: 100vh; }
    </style>
    """, unsafe_allow_html=True)

stranger_day_map = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #000; position: fixed; width: 100vw; height: 100vh; }
        canvas { display: block; position: fixed; top: 0; left: 0; }
        #grain {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: url('https://www.transparenttextures.com/patterns/stardust.png');
            opacity: 0.15; pointer-events: none; z-index: 1000;
        }
        #ui { 
            position: fixed; top: 30px; left: 30px; color: #ffcc00; 
            font-family: 'serif'; text-shadow: 2px 2px 4px #aa0000;
            z-index: 1100; pointer-events: none; opacity: 0.8;
        }
    </style>
</head>
<body>
    <div id="grain"></div>
    <div id="ui">
        <h1 id="title" style="margin:0; font-style: italic; font-size: 32px; letter-spacing: 2px;">SUMMER OF '84</h1>
        <div id="status" style="font-size: 11px; color: #ffaa66; letter-spacing: 1px;">ENCRYPTED_WORLD_v2.1 // HEADING_HOME</div>
    </div>
    <canvas id="dayCanvas"></canvas>

<script>
    const canvas = document.getElementById("dayCanvas");
    const ctx = canvas.getContext("2d");
    let cw = canvas.width = window.innerWidth;
    let ch = canvas.height = window.innerHeight;

    let _wx = 0; 
    let _cd = -1; 
    let isWarped = false;
    let isFinished = false;
    const _k = {};

    let speechText = "";
    let speechTimer = 0;
    let autoTimer = 0;
    
    // Quotes translated & refined for atmosphere
    const quotes = [
        "...The sky is red.",
        "There's no grass here...",
        "...Someone is watching me.",
        "Reality feels... inverted.",
        "...I have to run.",
        "This world is glitched...",
        "Take me back to 1984...",
        "I taste iron in the air.",
        "...It's coming.",
        "...Have I walked this path before?",
        "...Moo... (Despair)",
        "The red sky goes on forever."
    ];

    const imgDoor = new Image();
    imgDoor.crossOrigin = "anonymous";
    imgDoor.src = 'https://raw.githubusercontent.com/sevasu77/my-assets/main/spr_door_5.png';

    const imgBG = new Image();
    imgBG.crossOrigin = "anonymous";
    imgBG.src = 'https://raw.githubusercontent.com/sevasu77/my-assets/main/Red-Sky-of-Digital-Noise2%20(1).jpg';

    const particles = [];
    for(let i = 0; i < 50; i++) {
        particles.push({
            x: Math.random() * cw,
            y: Math.random() * ch,
            speed: 0.5 + Math.random() * 1,
            size: 1 + Math.random() * 2
        });
    }

    function _getPos(id) {
        const _m = [3.2, 12.8]; 
        return (id * _m[0] * 100) + (Math.sin(id) * 50);
    }

    function drawBubble(x, y, text) {
        if (!text) return;
        ctx.save();
        ctx.font = "bold 18px sans-serif";
        const metrics = ctx.measureText(text);
        const bw = metrics.width + 30;
        const bh = 36;
        const bx = x - bw / 2;
        const by = y - 110;

        ctx.fillStyle = "white";
        ctx.strokeStyle = "black";
        ctx.lineWidth = 2;
        ctx.fillRect(bx, by, bw, bh);
        ctx.strokeRect(bx, by, bw, bh);

        ctx.beginPath();
        ctx.moveTo(x - 10, by + bh);
        ctx.lineTo(x, by + bh + 15);
        ctx.lineTo(x + 10, by + bh);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.fillText(text, x, by + 24);
        ctx.restore();
    }

    function applyGlitch() {
        if (Math.random() < 0.9) return;
        ctx.save();
        if (Math.random() < 0.05) {
            ctx.globalCompositeOperation = 'difference';
            ctx.fillStyle = 'white'; ctx.fillRect(0, 0, cw, ch);
            ctx.restore(); return;
        }
        const numSlices = 5 + Math.random() * 10;
        for (let i = 0; i < numSlices; i++) {
            const sliceY = Math.random() * ch;
            const sliceH = 5 + Math.random() * 50;
            const sliceX = (Math.random() - 0.5) * 50;
            ctx.drawImage(canvas, 0, sliceY, cw, sliceH, sliceX, sliceY, cw, sliceH);
        }
        ctx.restore();
    }

    function _renderStructure(x, y, w, h, txt, col) {
        ctx.save();
        ctx.translate(x, y + h); ctx.scale(3, 0.4); ctx.rotate(0.8);
        ctx.fillStyle = "rgba(0,0,0,0.4)"; ctx.fillRect(0, -h/2, w, h);
        ctx.restore();
        ctx.fillStyle = col; ctx.fillRect(x, y, w, h);
        ctx.fillStyle = "#ffaa00"; ctx.fillRect(x + 20, y + 30, 30, 20);
        ctx.fillStyle = "#ffcc00"; ctx.font = "italic 13px serif";
        ctx.fillText(txt, x, y - 10);
    }

    function draw() {
        if (isFinished) return;
        ctx.clearRect(0, 0, cw, ch);

        if (isWarped) {
            if (imgBG.complete) ctx.drawImage(imgBG, 0, 0, cw, ch);
            particles.forEach(p => {
                p.y += p.speed; if (p.y > ch) p.y = -10;
                ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
                ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2); ctx.fill();
            });
            ctx.fillStyle = "rgba(0, 0, 0, 0.1)";
            for (let i = 0; i < ch; i += 4) ctx.fillRect(0, i, cw, 2);
            applyGlitch();

            document.getElementById("title").innerText = "THE UPSIDE DOWN";
            document.getElementById("title").style.color = "#ff0000";

            if (speechTimer > 0) {
                speechTimer--;
            } else {
                speechText = quotes[Math.floor(Math.random() * quotes.length)];
                speechTimer = 180; 
            }

            autoTimer++;
            if (autoTimer > 800) { 
                isFinished = true;
                finishSequence();
                return;
            }
        } else {
            let g = ctx.createLinearGradient(0, 0, 0, ch * 0.7);
            g.addColorStop(0, "#220033"); g.addColorStop(0.4, "#aa3300"); g.addColorStop(0.7, "#ffcc00");
            ctx.fillStyle = g; ctx.fillRect(0, 0, cw, ch);
            ctx.fillStyle = "#1a0d00"; ctx.fillRect(0, ch * 0.7, cw, ch * 0.3);

            ctx.save();
            ctx.translate(-_wx * 0.3, 0);
            [0.94, 4.68].forEach((_id, i) => {
                const _x = _getPos(_id);
                _renderStructure(_x, ch * 0.58, 120, 100, i === 0 ? "GENERAL STORE" : "🏠 MY HOME", i === 0 ? "#331100" : "#1a0800");
            });
            ctx.restore();

            ctx.save();
            ctx.translate(-_wx * 0.8, 0);
            ctx.fillStyle = "#2a1a0a";
            ctx.beginPath();
            ctx.moveTo(-5000, ch*0.7); ctx.lineTo(-5500, ch); ctx.lineTo(15000, ch); ctx.lineTo(14500, ch*0.7);
            ctx.fill();
            if (imgDoor.complete) ctx.drawImage(imgDoor, 2800, ch * 0.85 - 128, 128, 128);
            if (Math.abs((cw / 2) - (2800 - _wx * 0.8 + 64)) < 50) {
                isWarped = true;
                speechText = "WTF...!?"; 
                speechTimer = 120;
            }
            ctx.restore();
        }

        const cx = cw / 2; const cy = ch * 0.85;
        ctx.save();
        ctx.translate(cx, cy); ctx.scale(3 * _cd, 0.45); ctx.rotate(0.8);
        ctx.fillStyle = isWarped ? "rgba(0,0,0,0.6)" : "rgba(0,0,0,0.5)";
        ctx.font = "60px serif"; ctx.textAlign = "center";
        ctx.fillText("🐄", 0, 0);
        ctx.restore();

        ctx.save();
        ctx.translate(cx, cy); ctx.scale(_cd, 1);
        ctx.font = "60px serif"; ctx.textAlign = "center";
        ctx.fillStyle = isWarped ? "#888" : "white";
        ctx.fillText("🐄", 0, 0);
        ctx.restore();

        if (speechText) drawBubble(cx, cy, speechText);

        _wx += 0.45; _cd = -1;
        if(_k["arrowleft"] || _k["a"]) { _wx -= 4.5; _cd = 1; }
        if(_k["arrowright"] || _k["d"]) { _wx += 4.5; _cd = -1; }

        requestAnimationFrame(draw);
    }

    function finishSequence() {
        ctx.save();
        ctx.fillStyle = "rgba(100, 80, 40, 0.5)";
        ctx.globalCompositeOperation = "multiply";
        ctx.fillRect(0, 0, cw, ch);
        ctx.restore();

        ctx.fillStyle = "white";
        ctx.strokeStyle = "black";
        ctx.lineWidth = 4;
        ctx.font = "bold 42px serif";
        ctx.textAlign = "right";
        ctx.strokeText("To Be Continued", cw - 100, ch - 80);
        ctx.fillText("To Be Continued", cw - 100, ch - 80);
        
        ctx.strokeStyle = "white";
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.moveTo(cw - 480, ch - 95); ctx.lineTo(cw - 540, ch - 95);
        ctx.lineTo(cw - 530, ch - 110); ctx.moveTo(cw - 540, ch - 95);
        ctx.lineTo(cw - 530, ch - 80); ctx.stroke();
    }

    window.onkeydown = (e) => _k[e.key.toLowerCase()] = true;
    window.onkeyup = (e) => _k[e.key.toLowerCase()] = false;
    window.onresize = () => { cw = canvas.width = window.innerWidth; ch = canvas.height = window.innerHeight; };
    draw();
</script>
</body>
</html>
"""

st.components.v1.html(stranger_day_map, height=800)

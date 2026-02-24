import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* サイドバー、ヘッダー、メニュー、フッターを徹底的に完全削除 */
    [data-testid="stSidebar"], section[data-testid="stSidebar"], .st-emotion-cache-16ids0d, .st-emotion-cache-6qob1r {
        display: none !important;
        width: 0 !important;
    }
    header, footer, #MainMenu { visibility: hidden !important; }
    .main, .block-container, [data-testid="stAppViewContainer"] {
        margin: 0 !important; padding: 0 !important; overflow: hidden !important;
        height: 100vh !important; width: 100vw !important;
    }
    iframe { border: none; width: 100vw; height: 100vh; overflow: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

stranger_day_map = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #221100; position: fixed; width: 100vw; height: 100vh; }
        canvas { display: block; position: fixed; top: 0; left: 0; }
        #grain {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: url('https://www.transparenttextures.com/patterns/stardust.png');
            opacity: 0.15; pointer-events: none; z-index: 1000;
        }
        #ui { 
            position: fixed; top: 30px; left: 30px; color: #ffcc00; 
            font-family: 'serif'; text-shadow: 2px 2px 4px #aa0000;
            z-index: 1100; pointer-events: none;
        }
    </style>
</head>
<body>
    <div id="grain"></div>
    <div id="ui">
        <h1 style="margin:0; font-style: italic; font-size: 32px;">SUMMER OF '84</h1>
        <div style="font-size: 14px; color: #ffaa66;">Heading to My Home...</div>
    </div>
    <canvas id="dayCanvas"></canvas>

<script>
    const canvas = document.getElementById("dayCanvas");
    const ctx = canvas.getContext("2d");
    let cw = canvas.width = window.innerWidth;
    let ch = canvas.height = window.innerHeight;

    let worldX = 0; 
    let cowDir = -1;
    const keys = {};

    function draw() {
        // --- 1. 夕焼け空 ---
        let skyGrad = ctx.createLinearGradient(0, 0, 0, ch * 0.7);
        skyGrad.addColorStop(0, "#220033"); skyGrad.addColorStop(0.4, "#aa3300"); skyGrad.addColorStop(0.7, "#ffcc00");
        ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, cw, ch);

        // --- 2. 地面 ---
        ctx.fillStyle = "#1a0d00"; ctx.fillRect(0, ch * 0.7, cw, ch * 0.3);

        // --- 3. 背景（建物）：視差効果 ---
        ctx.save();
        ctx.translate(-worldX * 0.3, 0); 
        drawBuilding(300, ch*0.6, 120, 80, "GENERAL STORE", "#331100", "#ffaa00");
        drawBuilding(1500, ch*0.55, 150, 110, "🏠 MY HOME", "#1a0800", "#00ffcc");
        ctx.restore();

        // --- 4. 道：視差効果 ---
        ctx.save();
        ctx.translate(-worldX * 0.8, 0); 
        ctx.fillStyle = "#2a1a0a";
        ctx.beginPath();
        ctx.moveTo(-5000, ch*0.7); ctx.lineTo(-5500, ch);
        ctx.lineTo(15000, ch); ctx.lineTo(14500, ch*0.7);
        ctx.fill();
        ctx.restore();

        function drawBuilding(x, y, w, h, label, color, windowColor) {
            ctx.save();
            ctx.translate(x, y + h);
            ctx.scale(3, 0.5); ctx.rotate(Math.PI / 4);
            ctx.fillStyle = "rgba(0,0,0,0.5)";
            ctx.fillRect(0, -h/2, w, h);
            ctx.restore();
            ctx.fillStyle = color; ctx.fillRect(x, y, w, h);
            ctx.fillStyle = windowColor; ctx.fillRect(x + w*0.2, y + h*0.3, 30, 20);
            ctx.fillStyle = "#ffcc00"; ctx.font = "14px serif";
            ctx.fillText(label, x, y - 10);
        }

        // --- 5. プレイヤー（牛）：画面中央に固定 ---
        const cowX = cw / 2;
        const cowY = ch * 0.85;

        // 影
        ctx.save();
        ctx.translate(cowX, cowY);
        ctx.scale(3 * cowDir, 0.5); ctx.rotate(Math.PI / 4); 
        ctx.fillStyle = "rgba(0,0,0,0.5)";
        ctx.font = "60px serif"; ctx.textAlign = "center";
        ctx.fillText("🐄", 0, 0);
        ctx.restore();

        // 牛本体
        ctx.save();
        ctx.translate(cowX, cowY);
        ctx.scale(cowDir, 1);
        ctx.font = "60px serif"; ctx.textAlign = "center"; ctx.fillStyle = "white";
        ctx.fillText("🐄", 0, 0);
        ctx.restore();

        // --- 移動ロジック ---
        // ★オート歩行モード（壁紙用）：何もしなくてもゆっくり右へ進む
        worldX += 0.5; 
        cowDir = -1; 

        // キー操作による上書き（操作した時はそっちを優先）
        if(keys["arrowleft"] || keys["a"]) { worldX -= 5; cowDir = 1; }
        if(keys["arrowright"] || keys["d"]) { worldX += 5; cowDir = -1; }

        requestAnimationFrame(draw);
    }

    window.onkeydown = (e) => keys[e.key.toLowerCase()] = true;
    window.onkeyup = (e) => keys[e.key.toLowerCase()] = false;
    draw();
</script>
</body>
</html>
"""

st.components.v1.html(stranger_day_map, height=800)
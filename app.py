import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 徹底的なUI排除（司令官のこだわりを継承）
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
            z-index: 1100; pointer-events: none; opacity: 0.8;
        }
    </style>
</head>
<body>
    <div id="grain"></div>
    <div id="ui">
        <h1 style="margin:0; font-style: italic; font-size: 32px; letter-spacing: 2px;">SUMMER OF '84</h1>
        <div style="font-size: 11px; color: #ffaa66; letter-spacing: 1px;">ENCRYPTED_WORLD_v2.1 // HEADING_HOME</div>
    </div>
    <canvas id="dayCanvas"></canvas>

<script>
    const canvas = document.getElementById("dayCanvas");
    const ctx = canvas.getContext("2d");
    let cw = canvas.width = window.innerWidth;
    let ch = canvas.height = window.innerHeight;

    let _wx = 0; // worldXを隠蔽
    let _cd = -1; // cowDirを隠蔽
    const _k = {};

    // --- 🕵️ 隠蔽ポイント1: 座標の「暗号化計算」 ---
    // 建物の位置を「300」とかで指定せず、IDから複雑な計算で導き出す
    function _getPos(id) {
        const _m = [3.2, 12.8]; // 基準係数
        return (id * _m[0] * 100) + (Math.sin(id) * 50);
    }

    function draw() {
        // 夕焼け
        let g = ctx.createLinearGradient(0, 0, 0, ch * 0.7);
        g.addColorStop(0, "#220033"); g.addColorStop(0.4, "#aa3300"); g.addColorStop(0.7, "#ffcc00");
        ctx.fillStyle = g; ctx.fillRect(0, 0, cw, ch);

        // 地面
        ctx.fillStyle = "#1a0d00"; ctx.fillRect(0, ch * 0.7, cw, ch * 0.3);

        // --- 🕵️ 隠蔽ポイント2: 背景描画をループ化して構造を隠す ---
        ctx.save();
        ctx.translate(-_wx * 0.3, 0);
        
        // 建物データを配列ではなく、その場計算で描画
        [0.94, 4.68].forEach((_id, i) => {
            const _x = _getPos(_id);
            const _label = i === 0 ? "GENERAL STORE" : "🏠 MY HOME";
            const _color = i === 0 ? "#331100" : "#1a0800";
            _renderStructure(_x, ch * 0.58, 120, 100, _label, _color);
        });
        ctx.restore();

        // 道
        ctx.save();
        ctx.translate(-_wx * 0.8, 0);
        ctx.fillStyle = "#2a1a0a";
        ctx.beginPath();
        ctx.moveTo(-5000, ch*0.7); ctx.lineTo(-5500, ch);
        ctx.lineTo(15000, ch); ctx.lineTo(14500, ch*0.7);
        ctx.fill();
        ctx.restore();

        // 内部関数化して外部からのアクセスを遮断
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

        // 牛（中央固定）
        const cx = cw / 2; const cy = ch * 0.85;
        ctx.save();
        ctx.translate(cx, cy); ctx.scale(3 * _cd, 0.45); ctx.rotate(0.8);
        ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.font = "60px serif"; ctx.textAlign = "center";
        ctx.fillText("🐄", 0, 0);
        ctx.restore();

        ctx.save();
        ctx.translate(cx, cy); ctx.scale(_cd, 1);
        ctx.font = "60px serif"; ctx.textAlign = "center"; ctx.fillStyle = "white";
        ctx.fillText("🐄", 0, 0);
        ctx.restore();

        // 移動
        _wx += 0.45; _cd = -1;
        if(_k["arrowleft"] || _k["a"]) { _wx -= 4.5; _cd = 1; }
        if(_k["arrowright"] || _k["d"]) { _wx += 4.5; _cd = -1; }

        requestAnimationFrame(draw);
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

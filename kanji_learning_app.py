import streamlit as st
import streamlit.components.v1 as components
import random

# Page setup
st.set_page_config(
    page_title="漢字ニガテはんたー | 個別漢字ドリル",
    page_icon="✏️",
    layout="centered"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 16px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .student-card {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 12px;
        border-left: 6px solid #2E7D32;
        margin-bottom: 20px;
    }
    .question-box {
        background-color: #FFF9C4;
        padding: 20px;
        border-radius: 12px;
        border: 2px dashed #FBC02D;
        font-size: 24px;
        text-align: center;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .kanji-display {
        font-size: 72px;
        font-weight: bold;
        color: #1565C0;
        text-align: center;
        background: #E3F2FD;
        padding: 20px;
        border-radius: 16px;
        border: 3px solid #1976D2;
        margin-bottom: 15px;
    }
    .badge-pair {
        background-color: #FFECB3;
        color: #E65100;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA DEFINITIONS
# ---------------------------------------------------------
KANJI_DATA = {
    1: {"kanji": "両", "reading": "りょう", "type": "音読み", "phrase": "両手で持つ", "blank_phrase": "［  ］手で持つ", "hint": "「りょうて」の「りょう」"},
    2: {"kanji": "負", "reading": "ま", "type": "訓読み", "phrase": "しあいに負ける", "blank_phrase": "しあいに［  ］ける", "hint": "「まける」の「ま」"},
    3: {"kanji": "係", "reading": "かかり", "type": "訓読み", "phrase": "係の仕事", "blank_phrase": "［  ］の仕事", "hint": "「かかり」の「かかり」"},
    4: {"kanji": "員", "reading": "いん", "type": "音読み", "phrase": "全員そろう", "blank_phrase": "ぜん［  ］そろう", "hint": "「ぜんいん」の「いん」"},
    5: {"kanji": "祭", "reading": "まつり", "type": "訓読み", "phrase": "お祭りに行く", "blank_phrase": "お［  ］りに行く", "hint": "「おまつり」の「まつ」"},
    6: {"kanji": "業", "reading": "ぎょう", "type": "音読み", "phrase": "農作業", "blank_phrase": "のうさく［  ］", "hint": "「のうぎょう」の「ぎょう」"},
    7: {"kanji": "板", "reading": "ばん", "type": "音読み", "phrase": "鉄板やき", "blank_phrase": "てっ［  ］やき", "hint": "「てっぱん」の「ぱん（ばん）」"},
    8: {"kanji": "柱", "reading": "ちゅう", "type": "音読み", "phrase": "電柱", "blank_phrase": "でん［  ］", "hint": "「でんちゅう」の「ちゅう」"},
    9: {"kanji": "油", "reading": "ゆ", "type": "音読み", "phrase": "広い油田", "blank_phrase": "ひろい［  ］でん", "hint": "「ゆでん」の「ゆ」"},
    10: {"kanji": "港", "reading": "こう", "type": "音読み", "phrase": "大きな空港", "blank_phrase": "おおきなくう［  ］", "hint": "「くうこう」の「こう」"},
    11: {"kanji": "薬", "reading": "ぐすり", "type": "訓読み", "phrase": "目薬をさす", "blank_phrase": "め［  ］をさす", "hint": "「めぐすり」の「ぐすり」"},
    12: {"kanji": "笛", "reading": "ぶえ", "type": "訓読み", "phrase": "草笛をふく", "blank_phrase": "くさ［  ］をふく", "hint": "「くさぶえ」の「ぶえ」"},
    13: {"kanji": "注", "reading": "ちゅう", "type": "音読み", "phrase": "注意する", "blank_phrase": "［  ］いする", "hint": "「ちゅうい」の「ちゅう」"},
    14: {"kanji": "悪", "reading": "わる", "type": "訓読み", "phrase": "気分が悪い", "blank_phrase": "きぶんが［  ］い", "hint": "「わるい」の「わる」"},
    15: {"kanji": "者", "reading": "もの", "type": "訓読み", "phrase": "人気者", "blank_phrase": "にんき［  ］", "hint": "「にんきもの」の「もの」"},
    16: {"kanji": "勝", "reading": "しょう", "type": "音読み", "phrase": "勝負する", "blank_phrase": "［  ］ぶする", "hint": "「しょうぶ」の「しょう」"},
    17: {"kanji": "庫", "reading": "こ", "type": "音読み", "phrase": "車庫にならべる", "blank_phrase": "しゃ［  ］にならべる", "hint": "「しゃこ」の「こ」"},
    18: {"kanji": "波", "reading": "ぱ", "type": "音読み", "phrase": "電波が悪い", "blank_phrase": "でん［  ］がわるい", "hint": "「でんぱ」の「ぱ」"},
    19: {"kanji": "放", "reading": "ほう", "type": "音読み", "phrase": "ラジオ放送", "blank_phrase": "ラジオ［  ］そう", "hint": "「ほうそう」の「ほう」"},
    20: {"kanji": "勉", "reading": "べん", "type": "音読み", "phrase": "勉強する", "blank_phrase": "［  ］きょうする", "hint": "「べんきょう」の「べん」"},
    21: {"kanji": "想", "reading": "そう", "type": "音読み", "phrase": "読書感想文", "blank_phrase": "どくしょかん［  ］ぶん", "hint": "「かんそうぶん」の「そう」"},
    22: {"kanji": "写", "reading": "しゃ", "type": "音読み", "phrase": "海の写真", "blank_phrase": "うみの［  ］しん", "hint": "「しゃしん」の「しゃ」（音読みペア）", "pair": 33},
    23: {"kanji": "真", "reading": "しん", "type": "音読み", "phrase": "真実を知る", "blank_phrase": "［  ］じつをしる", "hint": "「しんじつ」の「しん」（音読みペア）", "pair": 34},
    24: {"kanji": "列", "reading": "れっ", "type": "音読み", "phrase": "列車が走る", "blank_phrase": "［  ］しゃがはしる", "hint": "「れっしゃ」の「れっ」"},
    25: {"kanji": "血", "reading": "ち", "type": "訓読み", "phrase": "足から血が出る", "blank_phrase": "あしから［  ］がでる", "hint": "「ち」の「ち」"},
    26: {"kanji": "暗", "reading": "くら", "type": "訓読み", "phrase": "暗いへや", "blank_phrase": "［  ］いへや", "hint": "「くらい」の「くら」（訓読みペア）", "pair": 35},
    27: {"kanji": "橋", "reading": "はし", "type": "訓読み", "phrase": "川に橋をかける", "blank_phrase": "かわに［  ］をかける", "hint": "「はし」の「はし」（訓読みペア）", "pair": 36},
    28: {"kanji": "暑", "reading": "あつ", "type": "訓読み", "phrase": "夏は暑い", "blank_phrase": "なつは［  ］い", "hint": "「あつい」の「あつ」（訓読みペア）", "pair": 37},
    29: {"kanji": "寒", "reading": "さむ", "type": "訓読み", "phrase": "冬は寒い", "blank_phrase": "ふゆは［  ］い", "hint": "「さむい」の「さむ」"},
    30: {"kanji": "軽", "reading": "かる", "type": "訓読み", "phrase": "軽いかばん", "blank_phrase": "［  ］いかばん", "hint": "「かるい」の「かる」"},
    31: {"kanji": "命", "reading": "いのち", "type": "訓読み", "phrase": "大切な命を知る", "blank_phrase": "たいせつな［  ］をしる", "hint": "「いのち」の「いのち」（訓読みペア）", "pair": 38},
    32: {"kanji": "第", "reading": "だい", "type": "音読み", "phrase": "第一回", "blank_phrase": "［  ］いっかい", "hint": "「だいいっかい」の「だい」"},
    33: {"kanji": "写", "reading": "うつ", "type": "訓読み", "phrase": "字を書き写す", "blank_phrase": "じをかき［  ］す", "hint": "「うつす」の「うつ」（訓読みペア）", "pair": 22},
    34: {"kanji": "真", "reading": "ま", "type": "訓読み", "phrase": "真っ白い雲", "blank_phrase": "［  ］っしろいくも", "hint": "「まっしろい」の「ま」（訓読みペア）", "pair": 23},
    35: {"kanji": "暗", "reading": "あん", "type": "音読み", "phrase": "詩を暗記する", "blank_phrase": "しを［  ］きする", "hint": "「あんき」の「あん」（音読みペア）", "pair": 26},
    36: {"kanji": "橋", "reading": "きょう", "type": "音読み", "phrase": "歩道橋", "blank_phrase": "ほどう［  ］", "hint": "「ほどうきょう」の「きょう」（音読みペア）", "pair": 27},
    37: {"kanji": "暑", "reading": "しょ", "type": "音読み", "phrase": "暑中みまい", "blank_phrase": "［  ］ちゅうみまい", "hint": "「しょちゅう」の「しょ」（音読みペア）", "pair": 28},
    38: {"kanji": "命", "reading": "めい", "type": "音読み", "phrase": "生命力", "blank_phrase": "せい［  ］りょく", "hint": "「せいめいりょく」の「めい」（音読みペア）", "pair": 31},
    39: {"kanji": "返", "reading": "かえ", "type": "訓読み", "phrase": "本を読み返す", "blank_phrase": "ほんをよみ［  ］す", "hint": "「よみかえす」の「かえ」（訓読みペア）", "pair": 47},
    40: {"kanji": "主", "reading": "しゅ", "type": "音読み", "phrase": "主語と述語", "blank_phrase": "［  ］ご強とじゅつご", "hint": "「しゅご」の「しゅ」（音読みペア）", "pair": 48},
    41: {"kanji": "州", "reading": "しゅう", "type": "音読み", "phrase": "九州の山", "blank_phrase": "きゅう［  ］のやま", "hint": "「きゅうしゅう」の「しゅう」"},
    42: {"kanji": "屋", "reading": "や", "type": "訓読み", "phrase": "犬の小屋", "blank_phrase": "いぬのこ［  ］", "hint": "「こや」の「や」"},
    43: {"kanji": "根", "reading": "ね", "type": "訓読み", "phrase": "木の根っこ", "blank_phrase": "きの［  ］っこ", "hint": "「ねっこ」の「ね」（訓読みペア）", "pair": 49},
    44: {"kanji": "荷", "reading": "に", "type": "音読み", "phrase": "荷物を持つ", "blank_phrase": "［  ］もつをもつ", "hint": "「にもつ」の「に」"},
    45: {"kanji": "守", "reading": "まも", "type": "訓読み", "phrase": "ルールを守る", "blank_phrase": "ルールを［  ］る", "hint": "「まもる」の「まも」（訓読みペア）", "pair": 50},
    46: {"kanji": "役", "reading": "やく", "type": "音読み", "phrase": "生活に役立つ", "blank_phrase": "せいかつに［  ］だつ", "hint": "「やくだつ」の「やく」"},
    47: {"kanji": "返", "reading": "へん", "type": "音読み", "phrase": "返事をする", "blank_phrase": "［  ］じをする", "hint": "「へんじ」の「へん」（音読みペア）", "pair": 39},
    48: {"kanji": "主", "reading": "おも", "type": "訓読み", "phrase": "主な出来事", "blank_phrase": "［  ］なできごと", "hint": "「おもな」の「おも」（訓読みペア）", "pair": 40},
    49: {"kanji": "根", "reading": "こん", "type": "音読み", "phrase": "大根を買う", "blank_phrase": "だい［  ］をかう", "hint": "「だいこん」の「こん」（音読みペア）", "pair": 43},
    50: {"kanji": "守", "reading": "す", "type": "音読み", "phrase": "留守番", "blank_phrase": "る［  ］ばん", "hint": "「るすばん」の「す」（音読みペア）", "pair": 45}
}

STUDENT_DATA = {
    1: {"score": 44, "incorrect": [5, 6, 7, 8, 9, 10, 20, 21, 22, 23, 24, 27, 28, 29, 30, 33, 34, 35, 36, 37, 38, 41, 43, 46, 47, 48, 49, 50]},
    2: {"score": 34, "incorrect": [2, 3, 5, 6, 9, 10, 13, 14, 15, 16, 18, 19, 20, 21, 22, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 44, 45, 46, 47, 48, 50]},
    3: {"score": None, "incorrect": list(range(1, 51))},
    4: {"score": 38, "incorrect": [7, 10, 11, 13, 14, 16, 18, 19, 21, 24, 27, 29, 30, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]},
    5: {"score": 2, "incorrect": [q for q in range(1, 51) if q != 32]},
    6: {"score": None, "incorrect": list(range(1, 51))},
    7: {"score": 46, "incorrect": [7, 8, 13, 15, 16, 18, 19, 21, 23, 28, 29, 30, 32, 33, 34, 35, 36, 37, 38, 39, 42, 45, 46, 47, 48, 49, 50]},
    8: {"score": 16, "incorrect": [3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 32, 33, 35, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 47, 48, 49, 50]},
    9: {"score": 94, "incorrect": [5, 36, 48]},
    10: {"score": None, "incorrect": list(range(1, 51))},
    11: {"score": None, "incorrect": list(range(1, 51))},
    12: {"score": 12, "incorrect": [q for q in range(1, 51) if q not in [3, 5, 17, 25, 41, 42]]},
    13: {"score": 24, "incorrect": [q for q in range(1, 51) if q not in [2, 3, 4, 9, 12, 15, 17, 25, 31, 32, 41, 45]]},
    14: {"score": 18, "incorrect": [q for q in range(1, 51) if q not in [2, 3, 23, 25, 32, 34, 40, 41, 42]]},
    15: {"score": None, "incorrect": list(range(1, 51))},
    16: {"score": 76, "incorrect": [14, 18, 19, 21, 24, 27, 30, 36, 37, 40, 46, 47]},
    17: {"score": 30, "incorrect": [q for q in range(1, 51) if q not in [1, 4, 5, 6, 11, 12, 15, 17, 22, 25, 32, 40, 41, 42, 43]]},
    18: {"score": None, "incorrect": list(range(1, 51))},
    19: {"score": 84, "incorrect": [7, 11, 15, 19, 21, 30, 37, 38]},
    20: {"score": 54, "incorrect": [11, 20, 21, 23, 24, 26, 27, 28, 29, 30, 32, 33, 35, 36, 37, 38, 39, 44, 46, 47, 48, 49, 50]},
    21: {"score": 16, "incorrect": [q for q in range(1, 51) if q not in [1, 3, 4, 5, 7, 10, 15, 25]]},
    22: {"score": 68, "incorrect": [4, 5, 6, 13, 16, 21, 24, 27, 28, 29, 30, 33, 36, 37, 46, 48]},
    23: {"score": None, "incorrect": list(range(1, 51))},
    24: {"score": 54, "incorrect": [3, 7, 14, 15, 19, 20, 21, 23, 26, 27, 30, 33, 35, 36, 37, 38, 39, 43, 44, 46, 47, 48, 50]},
    25: {"score": 84, "incorrect": [10, 14, 16, 18, 29, 31, 45, 46]},
    26: {"score": 96, "incorrect": [31, 38]},
    27: {"score": 38, "incorrect": [q for q in range(1, 51) if q not in [1, 2, 3, 4, 6, 10, 11, 13, 19, 31, 32, 36, 38, 40, 42, 43, 44, 45, 49]]},
    28: {"score": None, "incorrect": list(range(1, 51))},
    29: {"score": 16, "incorrect": [q for q in range(1, 51) if q not in [1, 2, 11, 23, 25, 32, 43, 49]]},
    30: {"score": 72, "incorrect": [22, 26, 27, 28, 29, 30, 33, 34, 35, 36, 37, 42, 44, 46]}
}

def get_student_pin(student_id):
    return f"{student_id:02d}{student_id:02d}"

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "logged_in_student" not in st.session_state:
    st.session_state.logged_in_student = None
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "mastered_questions" not in st.session_state:
    st.session_state.mastered_questions = set()
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# ---------------------------------------------------------
# CANVAS COMPONENT (HTML5 Touch Canvas)
# ---------------------------------------------------------
def render_touch_canvas(canvas_key):
    canvas_html = f"""
    <div style="text-align: center; margin: 10px 0;">
        <canvas id="canvas_{canvas_key}" width="280" height="280" style="border: 3px solid #2E7D32; border-radius: 12px; background-color: #FFFFFF; touch-action: none; cursor: crosshair; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></canvas>
        <div style="margin-top: 10px;">
            <button onclick="clearCanvas_{canvas_key}()" style="padding: 8px 16px; background-color: #FF7043; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">🗑️ ぜんぶ けす</button>
        </div>
    </div>
    <script>
        (function() {{
            const canvas = document.getElementById('canvas_{canvas_key}');
            const ctx = canvas.getContext('2d');
            let drawing = false;

            // Draw grid guide line
            function drawGrid() {{
                ctx.strokeStyle = '#E0E0E0';
                ctx.lineWidth = 1;
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                ctx.moveTo(140, 0); ctx.lineTo(140, 280);
                ctx.moveTo(0, 140); ctx.lineTo(280, 140);
                ctx.stroke();
                ctx.setLineDash([]);
            }}
            drawGrid();

            function startDraw(e) {{
                drawing = true;
                ctx.beginPath();
                const pos = getPos(e);
                ctx.moveTo(pos.x, pos.y);
            }}

            function moveDraw(e) {{
                if (!drawing) return;
                e.preventDefault();
                const pos = getPos(e);
                ctx.strokeStyle = '#212121';
                ctx.lineWidth = 10;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.lineTo(pos.x, pos.y);
                ctx.stroke();
            }}

            function endDraw() {{
                drawing = false;
            }}

            function getPos(e) {{
                const rect = canvas.getBoundingClientRect();
                const clientX = e.touches ? e.touches[0].clientX : e.clientX;
                const clientY = e.touches ? e.touches[0].clientY : e.clientY;
                return {{
                    x: clientX - rect.left,
                    y: clientY - rect.top
                }};
            }}

            window.clearCanvas_{canvas_key} = function() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                drawGrid();
            }};

            canvas.addEventListener('mousedown', startDraw);
            canvas.addEventListener('mousemove', moveDraw);
            canvas.addEventListener('mouseup', endDraw);
            canvas.addEventListener('mouseleave', endDraw);

            canvas.addEventListener('touchstart', startDraw, {{passive: false}});
            canvas.addEventListener('touchmove', moveDraw, {{passive: false}});
            canvas.addEventListener('touchend', endDraw);
        }})();
    </script>
    """
    components.html(canvas_html, height=340)

# ---------------------------------------------------------
# UI: LOGIN SCREEN
# ---------------------------------------------------------
if st.session_state.logged_in_student is None:
    st.markdown("<div class='main-title'>✏️ 漢字ニガテはんたー</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>ふくしゅうドリル（2がっき ちゅうき テスト）</div>", unsafe_allow_html=True)
    
    st.info("👋 じぶんの **しゅっせきばんごう** と **あんしょうばんごう** を いれてね！")
    
    col1, col2 = st.columns(2)
    with col1:
        student_id = st.selectbox("しゅっせきばんごう", options=list(range(1, 31)), format_func=lambda x: f"{x} ばん")
    with col2:
        pin_input = st.text_input("あんしょうばんごう (4けた)", type="password", help="例: 1番のかたは 0101")

    expected_pin = get_student_pin(student_id)

    if st.button("🚀 ドリルを はじめる！", use_container_width=True, type="primary"):
        if pin_input == expected_pin:
            st.session_state.logged_in_student = student_id
            st.session_state.current_question_index = 0
            st.session_state.show_answer = False
            st.rerun()
        else:
            st.error("❌ あんしょうばんごうが ちがいます。もう一度たしかめてね！")

    with st.expander("💡 あんしょうばんごうの ルール（せんせい・じどう用）"):
        st.write("・初期あんしょうばんごうは **「出席番号(2桁) + 出席番号(2桁)」** です。")
        st.write("  - 1番さん ➔ `0101`")
        st.write("  - 9番さん ➔ `0909`")
        st.write("  - 26番さん ➔ `2626`")

# ---------------------------------------------------------
# UI: MAIN DRILL SCREEN
# ---------------------------------------------------------
else:
    sid = st.session_state.logged_in_student
    sdata = STUDENT_DATA[sid]
    score = sdata["score"]
    incorrect_qids = sdata["incorrect"]
    
    # Header bar
    st.markdown(f"""
    <div class='student-card'>
        <div style="display:flex; justify-shadow: space-between; align-items: center;">
            <div>
                <span style="font-size:22px; font-weight:bold; color:#1B5E20;">👦👧 {sid}ばん さんの ページ</span><br>
                <span style="font-size:14px; color:#388E3C;">テストのてんすう: {score if score is not None else '未受験'}てん | ニガテ漢字: あと {len(incorrect_qids) - len(st.session_state.mastered_questions)} もん</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🔒 ログアウト（ばんごうをえらびなおす）"):
        st.session_state.logged_in_student = None
        st.rerun()

    # Progress bar
    total_weak = len(incorrect_qids)
    mastered_count = len(st.session_state.mastered_questions)
    progress_val = min(1.0, mastered_count / total_weak) if total_weak > 0 else 1.0
    st.progress(progress_val)
    st.caption(f"🎯 ニガテげきは メーター: {mastered_count} / {total_weak} もん かんりょう！")

    # Mode selector
    mode = st.radio("れんしゅう モードを えらぼう！", ["✍️ 手書きで チャレンジ！", "🔤 よみかた クイズ！"], horizontal=True)

    if not incorrect_qids:
        st.balloons()
        st.success("🎉 すごい！ぜんぶの ニガテ漢字を クリアしたよ！")
    else:
        # Get active question list (cycled)
        qid = incorrect_qids[st.session_state.current_question_index % len(incorrect_qids)]
        qdata = KANJI_DATA[qid]

        # On-Kun pair badge if applicable
        if "pair" in qdata:
            st.markdown("<span class='badge-pair'>🔄 おんくん パトロール対象（音読み・訓読みのペア漢字）</span>", unsafe_allow_html=True)

        # -------------------------------------------------
        # MODE 1: HANDWRITING CANVAS
        # -------------------------------------------------
        if mode == "✍️ 手書きで チャレンジ！":
            st.markdown(f"<div class='question-box'>【もんだい】 {qdata['blank_phrase']}</div>", unsafe_allow_html=True)
            st.caption(f"💡 ヒント: {qdata['hint']}")

            render_touch_canvas(f"q_{qid}_{st.session_state.current_question_index}")

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("👁️ こたえを みる", use_container_width=True, type="secondary"):
                    st.session_state.show_answer = True
            with col_btn2:
                if st.button("➡️ つぎの もんだい", use_container_width=True):
                    st.session_state.show_answer = False
                    st.session_state.current_question_index += 1
                    st.rerun()

            if st.session_state.show_answer:
                st.markdown(f"<div class='kanji-display'>{qdata['kanji']}</div>", unsafe_allow_html=True)
                st.markdown(f"**【せいかい】** **{qdata['kanji']}** （よみ: {qdata['reading']} / {qdata['type']}）")
                st.write(f"📝 じつぶつ: **{qdata['phrase']}**")

                col_eval1, col_eval2 = st.columns(2)
                with col_eval1:
                    if st.button("⭕️ 正解できた！", use_container_width=True, type="primary"):
                        st.session_state.mastered_questions.add(qid)
                        st.toast("🎉 すばらしい！ニガテを1つ げきは！", icon="⭕")
                        st.session_state.show_answer = False
                        st.session_state.current_question_index += 1
                        st.rerun()
                with col_eval2:
                    if st.button("❌ もういちど", use_container_width=True):
                        st.toast("💪 つぎは かけるよ！がんばろう！", icon="✍️")
                        st.session_state.show_answer = False
                        st.session_state.current_question_index += 1
                        st.rerun()

        # -------------------------------------------------
        # MODE 2: READING QUIZ
        # -------------------------------------------------
        else:
            st.markdown(f"<div class='question-box'>「{qdata['kanji']}」の ただしい よみかたは？<br><br><span style='font-size:36px; color:#D81B60;'>{qdata['phrase']}</span></div>", unsafe_allow_html=True)

            # Generate choices
            correct_reading = qdata["reading"]
            all_readings = list(set([k["reading"] for k in KANJI_DATA.values() if k["reading"] != correct_reading]))
            random.seed(qid)
            wrong_choices = random.sample(all_readings, 2)
            choices = [correct_reading] + wrong_choices
            random.seed()
            random.shuffle(choices)

            for choice in choices:
                if st.button(f"👉 {choice}", use_container_width=True):
                    if choice == correct_reading:
                        st.success(f"🎉 だいせいかい！ 「{qdata['phrase']}」 の 「{qdata['kanji']}」 は 【{qdata['type']}】の 「{choice}」 です！")
                        st.session_state.mastered_questions.add(qid)
                        st.session_state.current_question_index += 1
                    else:
                        st.error(f"❌ おしい！ ただしい よみかたは 「{correct_reading}」 でした。")
                        st.session_state.current_question_index += 1

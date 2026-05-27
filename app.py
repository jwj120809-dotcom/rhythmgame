import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 페이지 설정
st.set_page_config(page_title="FNF QWER Edition", layout="centered")

# 세션 상태(State) 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "target_key" not in st.session_state:
    st.session_state.target_key = random.choice(["Q", "W", "E", "R"])
if "message" not in st.session_state:
    st.session_state.message = "클릭하여 시작하세요!"
if "message_color" not in st.session_state:
    st.session_state.message_color = "#FF2A85"

# 점수 변동 처리 함수
def process_input(pressed_key):
    # 자바스크립트에서 보낸 키 값 처리
    if not pressed_key:
        return
        
    pressed_key = pressed_key.upper()
    
    if pressed_key == st.session_state.target_key:
        st.session_state.score += 100
        st.session_state.message = f"PERFECT! (+100) -> {pressed_key}"
        st.session_state.message_color = "#00F0FF" # 청록색
    else:
        st.session_state.score -= 50
        st.session_state.message = f"MISS! (-50) -> {pressed_key} 입력됨"
        st.session_state.message_color = "#FF2A85" # 핑크색
        
    # 다음 타겟 키 무작위 지정
    st.session_state.target_key = random.choice(["Q", "W", "E", "R"])

# --- UI 레이아웃 디자인 (사진 스타일 반영) ---
st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: #FF2A85; font-family: 'sans serif';">FNF QWER Edition (HARDCORE)</h2>
        <p style="color: #FFFFFF;">화면을 한 번 클릭한 후 <b>Q, W, E, R</b> 키를 눌러주세요!</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# 스코어 및 상태 표시창
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<h3 style='color: #00F0FF;'>SCORE: {st.session_state.score}</h3>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<h3 style='color: #FF2A85; text-align: right;'>TARGET: <span style='font-size: 40px; border: 2px solid #FF2A85; padding: 2px 15px; border-radius: 5px;'>{st.session_state.target_key}</span></h3>", unsafe_allow_html=True)

# 판정 결과 메시지 박스
st.markdown(
    f"""
    <div style="border: 2px solid #FF2A85; border-radius: 10px; padding: 40px; text-align: center; margin-top: 20px; background-color: #1F1F2E;">
        <h2 style="color: {st.session_state.message_color}; font-weight: bold;">{st.session_state.message}</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 키보드 입력 감지용 자바스크립트 컴포넌트 ---
# 사용자가 Q, W, E, R를 누르면 쿼리 파라미터를 통해 Streamlit에 값을 전달하고 페이지를 리프레시합니다.
keystroke_detector = """
<script>
    const allowedKeys = ['q', 'w', 'e', 'r', 'Q', 'W', 'E', 'R'];
    
    // 부모 창(Streamlit)의 윈도우 키 이벤트 감지
    window.parent.document.addEventListener('keydown', function(e) {
        if (allowedKeys.includes(e.key)) {
            // Streamlit 앱 URL에 누른 키를 query parameter로 전달하여 강제 새로고침(입력 인식) 촉발
            const url = new URL(window.parent.location.href);
            url.searchParams.set('key', e.key.toUpperCase());
            url.searchParams.set('t', Date.now()); // 매번 고유한 요청이 되도록 타임스탬프 추가
            window.parent.location.href = url.href;
        }
    });
</script>
"""

# HTML 컴포넌트를 보이지 않게 실행
components.html(keystroke_detector, height=0, width=0)

# URL 파라미터 읽어서 키 입력이 들어왔는지 확인 및 처리
query_params = st.query_params
if "key" in query_params:
    pressed = query_params["key"]
    # 파라미터 중복 처리를 방지하기 위해 주소창에서 'key' 제거 프로세스 시도
    # (Streamlit 구조상 즉시 지우면 무한 루프가 날 수 있으므로 세션 값과 대조하여 판단해도 좋습니다)
    
    # 단, 이전 입력과 동일한 입력 연속 처리 등을 위해 쿼리 지우기
    st.query_params.clear()
    
    # 판정 함수 실행
    process_input(pressed)
    st.rerun()

import os
import streamlit as st
import streamlit.components.v1 as components

# 1. 화면 레이아웃 설정
st.set_page_config(layout="wide", page_title="왱알왱알 운동장")

# ========================================================
# ✏️ [텍스트 수정 구역] 문구를 바꿀 땐 여기만 수정하세요!
# ========================================================
MAIN_TITLE_LINE1 = "안 알려줘서"
MAIN_TITLE_LINE2 = "내가 알아봤다"

TOGGLE_MENU_NAME = "📂 다른 주제 보기"
# ========================================================

# 2. 폴더 내 HTML 파일들을 자동으로 긁어와서 목록화하기
ARTICLES_DIR = "articles"

if not os.path.exists(ARTICLES_DIR):
    os.makedirs(ARTICLES_DIR)

html_files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith(".html")]

articles = {}
for file in html_files:
    title = file.replace(".html", "").replace("_", " ")
    articles[title] = os.path.join(ARTICLES_DIR, file)

if not articles:
    articles["아직 등록된 아티클이 없습니다."] = None

# 3. [왼쪽 영역] 사이드바 설정
with st.sidebar:
    st.markdown(
        f"""
        <style>
            .magazine-title {{
                font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 42px;
                font-weight: 800;
                line-height: 1.2;
                letter-spacing: -0.04em;
                color: #16161a;
                margin-bottom: 0px;
                padding-top: 20px;
            }}
            .magazine-title em {{ font-style: normal; color: #2a1a7e; }}
        </style>
        <div class="magazine-title">
            {MAIN_TITLE_LINE1}<br>
            <em>{MAIN_TITLE_LINE2}</em>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<div style='padding-top: 50px;'></div>", unsafe_allow_html=True)
    
    # 토글 메뉴 구성
    with st.expander(TOGGLE_MENU_NAME, expanded=True):
        selected_article_title = st.radio(
            "목록",
            list(articles.keys()),
            label_visibility="collapsed"
        )

# 4. [오른쪽 메인 영역] 선택된 아티클 HTML 임베드
html_file_path = articles[selected_article_title]

if html_file_path and os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=1500, scrolling=True)
else:
    st.info("👋 왼쪽의 '다른 주제 보기'를 열어 아티클을 선택하거나, articles 폴더에 HTML 파일을 넣어주세요!")
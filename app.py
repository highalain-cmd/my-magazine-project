import os
import streamlit as st
import streamlit.components.v1 as components

# 1. 화면 레이아웃 설정
st.set_page_config(layout="wide", page_title="왱알왱알 운동장")

# ========================================================
# ✏️ [설정 구역] 관리용 정보는 여기만 수정하세요!
# ========================================================
MAIN_TITLE_LINE1 = "안 알려줘서"
MAIN_TITLE_LINE2 = "내가 알아봤다"

TOGGLE_MENU_NAME = "📂 다른 주제 보기"

# ✅ [1] 구글 대신 들어가는 깔끔한 우마미(Umami) 트래커 코드 반영 완료!
UMAMI_SCRIPT = """
<script async src="https://cloud.umami.is/script.js" data-website-id="47145cdb-622b-4a6c-bcd5-dc5d86f0567b"></script>
"""

# [2] 디스커스 댓글창 설정 (확인하신 숏네임 반영 완료)
DISQUS_SHORTNAME = "buzz-buzz-1"  
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
    
    # 본문 아티클 출력
    components.html(html_content, height=1300, scrolling=True)
    
    # --- 💬 하단 디스커스 댓글창 구역 ---
    st.markdown("---")
    st.subheader("💬 댓글을 남겨주세요")
    
    disqus_html = f"""
    <div id="disqus_thread"></div>
    <script>
        var disqus_config = function () {{
            this.page.url = window.parent.location.href;  // 스트림릿 실제 주소 자동 인식
            this.page.identifier = "{selected_article_title}"; // 아티클 제목별로 댓글창 분리
        }};
        (function() {{ 
            var d = document, s = d.createElement('script');
            s.src = 'https://{DISQUS_SHORTNAME}.disqus.com/embed.js';
            s.setAttribute('data-timestamp', +new Date());
            (d.head || d.body).appendChild(s);
        }})();
    </script>
    <noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
    """
    # 댓글창 렌더링
    components.html(disqus_html, height=600, scrolling=True)

    # --- 📮 푸터 Contact (댓글창 아래) ---
    st.markdown(
        """
        <div style="
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
            text-align: center;
            padding: 28px 0 36px;
        ">
            <span style="font-size: 12px; color: #a0a0a5; letter-spacing: -0.01em;">Contact&nbsp;&nbsp;·&nbsp;&nbsp;</span>
            <a href="mailto:heartbring@naver.com" style="font-size: 12px; color: #8a7fc0; text-decoration: none; letter-spacing: -0.01em;">heartbring@naver.com</a>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("👋 왼쪽의 '다른 주제 보기'를 열어 아티클을 선택하거나, articles 폴더에 HTML 파일을 넣어주세요!")

# ✅ 5. 구글 애널리틱스 대신 우마미 투명 트래커 실행 (백그라운드 트래픽 집계)
components.html(UMAMI_SCRIPT, height=0, width=0)
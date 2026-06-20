import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


APP_URL = "https://parent-test.streamlit.app"

QUESTION_SCALE = {
    1: "전혀 아니다",
    2: "아니다",
    3: "보통이다",
    4: "그렇다",
    5: "매우 그렇다",
}


def load_questions():
    return [
        {"id": 1, "icon": "💗", "text": "아이가 속상해할 때 먼저 감정을 들어주는 편이다.", "type": "A"},
        {"id": 2, "icon": "📏", "text": "가정에서 지켜야 할 규칙을 명확하게 알려주는 편이다.", "type": "B"},
        {"id": 3, "icon": "🌱", "text": "아이가 스스로 선택하도록 기다려주는 편이다.", "type": "C"},
        {"id": 4, "icon": "⚖️", "text": "상황에 따라 공감과 규칙을 함께 고려한다.", "type": "D"},
        {"id": 5, "icon": "🗣️", "text": "아이와 대화하며 문제를 해결하려고 한다.", "type": "A"},
        {"id": 6, "icon": "🕒", "text": "생활 습관과 약속을 꾸준히 강조한다.", "type": "B"},
        {"id": 7, "icon": "🧩", "text": "아이가 직접 해보며 배우는 것을 중요하게 생각한다.", "type": "C"},
        {"id": 8, "icon": "🤝", "text": "아이의 감정은 받아주되 행동 기준도 함께 설명한다.", "type": "D"},
        {"id": 9, "icon": "👂", "text": "아이의 마음을 이해하려고 질문을 많이 하는 편이다.", "type": "A"},
        {"id": 10, "icon": "🚀", "text": "아이의 자율성과 책임감을 함께 키우려 한다.", "type": "C"},
    ]


def load_result_info():
    return {
        "A": {
            "name": "공감형 부모",
            "emoji": "💗",
            "summary": "아이의 마음을 먼저 살피고 정서적 연결을 중요하게 여기는 부모입니다.",
            "description": "아이의 감정을 잘 읽고 안정감을 주는 유형입니다. 아이는 부모에게 자신의 마음을 표현해도 안전하다고 느끼기 쉽습니다.",
            "strength": "아이의 감정을 잘 이해하고 정서적 안정감을 줍니다.",
            "weakness": "규칙이나 행동 기준이 약해질 수 있습니다.",
            "recommendation": "감정을 먼저 공감한 뒤, 지켜야 할 기준을 짧고 분명하게 알려주세요.",
            "talk": "“네 마음은 이해해. 하지만 이 행동은 이렇게 바꿔보자.”",
        },
        "B": {
            "name": "훈육형 부모",
            "emoji": "📏",
            "summary": "규칙, 약속, 생활 습관을 중요하게 생각하는 부모입니다.",
            "description": "아이에게 안정적인 기준과 생활 리듬을 만들어 주는 유형입니다. 예측 가능한 환경을 제공하는 데 강점이 있습니다.",
            "strength": "아이에게 안정적인 기준과 습관을 만들어 줍니다.",
            "weakness": "아이의 감정이나 속마음을 놓칠 수 있습니다.",
            "recommendation": "규칙을 말하기 전, 아이의 감정을 먼저 한 문장으로 인정해 주세요.",
            "talk": "“속상했구나. 그래도 우리 약속은 지켜야 해.”",
        },
        "C": {
            "name": "자율형 부모",
            "emoji": "🌱",
            "summary": "아이의 선택과 독립성을 존중하는 부모입니다.",
            "description": "아이 스스로 생각하고 선택하도록 기다려주는 유형입니다. 자기주도성과 책임감을 키우는 데 강점이 있습니다.",
            "strength": "아이의 자기주도성과 독립성을 키워줍니다.",
            "weakness": "기준이 부족하면 아이가 혼란스러울 수 있습니다.",
            "recommendation": "선택권을 주되 가능한 범위와 책임을 함께 알려주세요.",
            "talk": "“네가 선택해도 좋아. 대신 선택한 일은 끝까지 해보자.”",
        },
        "D": {
            "name": "균형형 부모",
            "emoji": "⚖️",
            "summary": "공감과 규칙을 함께 고려하는 유연한 부모입니다.",
            "description": "아이의 감정을 이해하면서도 필요한 기준을 제시하는 유형입니다. 상황에 따라 유연하게 대응할 수 있습니다.",
            "strength": "감정과 행동 기준을 균형 있게 다룹니다.",
            "weakness": "상황마다 기준이 달라 보일 수 있습니다.",
            "recommendation": "가정의 핵심 원칙 2~3가지를 정하고 일관되게 적용해 주세요.",
            "talk": "“네 마음도 중요하고, 우리 약속도 중요해. 함께 방법을 찾아보자.”",
        },
    }


def apply_style():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #fff8ef 0%, #fffdf9 60%, #ffffff 100%);
        }

        section.main > div {
            max-width: 760px;
            padding-top: 28px;
            padding-bottom: 80px;
        }

        .hero {
            padding: 20px 6px 10px 6px;
        }

        .hero-title {
            font-size: 2.45rem;
            font-weight: 900;
            color: #352824;
            line-height: 1.18;
            letter-spacing: -0.04em;
        }

        .hero-brand {
            text-align: center;
            margin-top: 10px;
            margin-bottom: 18px;
            font-size: 1rem;
            font-style: italic;
            font-weight: 600;
            color: #9b7d67;
            letter-spacing: 6px;
        }

        .hero-subtitle {
            font-size: 1.35rem;
            font-weight: 800;
            color: #6b4b3f;
            line-height: 1.45;
            margin-top: 18px;
        }

        .service-card, .question-card, .mini-card {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid #ffd9b3;
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(130, 78, 32, 0.10);
            margin: 18px 0;
            line-height: 1.7;
        }

        .question-label {
            font-size: 1.25rem;
            font-weight: 900;
            color: #332a2a;
            margin-bottom: 14px;
        }

        .question-text {
            font-size: 1.18rem;
            font-weight: 800;
            color: #2f2f3a;
            line-height: 1.5;
            letter-spacing: -0.03em;
        }

        .result-card {
            background: #fff3e6;
            border: 1px solid #ffd0a1;
            border-radius: 26px;
            padding: 26px;
            box-shadow: 0 12px 34px rgba(130, 78, 32, 0.12);
            margin: 18px 0;
        }

        .result-title {
            font-size: 1.75rem;
            font-weight: 900;
            color: #352824;
            line-height: 1.3;
        }

        .result-summary {
            font-size: 1.08rem;
            font-weight: 800;
            color: #6b4b3f;
            line-height: 1.6;
        }

        div.stButton > button {
            width: 100%;
            min-height: 52px;
            border-radius: 16px;
            font-size: 1.02rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ff9f43, #ff7f50);
            color: white;
            border: none;
        }

        div.stDownloadButton > button {
            width: 100%;
            min-height: 52px;
            border-radius: 16px;
            font-size: 1rem;
            font-weight: 800;
        }

        div[role="radiogroup"] label {
            font-size: 0.95rem !important;
            padding: 3px 0;
        }

        @media (max-width: 600px) {
            section.main > div {
                padding-left: 18px;
                padding-right: 18px;
                padding-top: 18px;
            }

            .hero-title {
                font-size: 1.85rem;
                line-height: 1.22;
            }

            .hero-brand {
                font-size: 0.85rem;
                letter-spacing: 4px;
                margin-top: 8px;
                margin-bottom: 14px;
            }

            .hero-subtitle {
                font-size: 1.02rem;
                line-height: 1.45;
            }

            .service-card, .question-card, .mini-card {
                padding: 18px;
                border-radius: 20px;
            }

            .question-label {
                font-size: 1.1rem;
            }

            .question-text {
                font-size: 1.02rem;
                line-height: 1.55;
            }

            .result-title {
                font-size: 1.45rem;
            }

            .result-summary {
                font-size: 0.98rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0


def reset_test():
    st.session_state.page = "home"
    st.session_state.responses = {}
    st.session_state.current_question = 0


def calculate_score(questions):
    scores = {"A": 0, "B": 0, "C": 0, "D": 0}
    for q in questions:
        scores[q["type"]] += st.session_state.responses.get(q["id"], 0)
    return scores


def analyze_type(scores):
    max_score = max(scores.values())
    top_types = [key for key, value in scores.items() if value == max_score]
    return "D" if len(top_types) > 1 else top_types[0]


def create_qr_code(url):
    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def create_pdf(result, scores):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    y = 790
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "Parenting Type Result")

    y -= 45
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, f"Result: {result['name']}")

    y -= 30
    pdf.setFont("Helvetica", 10)

    lines = [
        result["summary"],
        "",
        "Strength:",
        result["strength"],
        "",
        "Needs Improvement:",
        result["weakness"],
        "",
        "Recommendation:",
        result["recommendation"],
        "",
        "Suggested phrase:",
        result["talk"],
        "",
        f"Empathy: {scores['A']}",
        f"Discipline: {scores['B']}",
        f"Autonomy: {scores['C']}",
        f"Balance: {scores['D']}",
    ]

    for line in lines:
        pdf.drawString(50, y, line[:95])
        y -= 22

    pdf.save()
    buffer.seek(0)
    return buffer


def show_home():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">👨‍👩‍👧 육아 부모 유형 진단</div>
            <div class="hero-brand">- chulhee -</div>
            <div class="hero-subtitle">10개의 질문으로 나의 육아 성향을 알아보세요.</div>
        </div>

        <div class="service-card">
            이 검사는 부모님의 육아 성향을 <b>공감형, 훈육형, 자율형, 균형형</b>으로 나누어 안내합니다.
            <br><br>
            결과는 참고용이며, 실제 육아 상황에서는 아이의 기질과 가정 환경을 함께 고려하는 것이 좋습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("시작하기"):
        st.session_state.page = "test"
        st.session_state.current_question = 0
        st.rerun()


def show_test(questions):
    total = len(questions)
    idx = st.session_state.current_question
    q = questions[idx]

    st.progress((idx + 1) / total)
    st.markdown(f"### 진행률 {idx + 1}/{total}")

    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-label">{q['icon']} Q{q['id']}</div>
            <div class="question-text">{q['text']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current_value = st.session_state.responses.get(q["id"], 3)

    answer = st.radio(
        "나의 답변",
        options=list(QUESTION_SCALE.keys()),
        index=current_value - 1,
        format_func=lambda x: f"{x} - {QUESTION_SCALE[x]}",
    )

    st.session_state.responses[q["id"]] = answer

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← 이전", disabled=idx == 0):
            st.session_state.current_question -= 1
            st.rerun()

    with col2:
        if idx < total - 1:
            if st.button("다음 →"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("결과 보기"):
                st.session_state.page = "result"
                st.rerun()


def show_result(questions):
    scores = calculate_score(questions)
    result_type = analyze_type(scores)
    result = load_result_info()[result_type]

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-title">{result['emoji']} {result['name']}</div>
            <br>
            <div class="result-summary">{result['summary']}</div>
            <br>
            <p>{result['description']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = pd.DataFrame({
        "유형": ["공감형", "훈육형", "자율형", "균형형"],
        "점수": [scores["A"], scores["B"], scores["C"], scores["D"]],
    })

    st.subheader("📊 유형별 점수")
    st.bar_chart(df.set_index("유형"))

    st.markdown(
        f"""
        <div class="mini-card">
            <h3>✅ 강점</h3>
            <p>{result['strength']}</p>
        </div>

        <div class="mini-card">
            <h3>🔎 보완점</h3>
            <p>{result['weakness']}</p>
        </div>

        <div class="mini-card">
            <h3>🌿 추천 육아 방법</h3>
            <p>{result['recommendation']}</p>
        </div>

        <div class="mini-card">
            <h3>💬 추천 대화 문장</h3>
            <p><b>{result['talk']}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pdf = create_pdf(result, scores)

    st.download_button(
        "📄 결과 PDF 저장",
        data=pdf,
        file_name="parenting_type_result.pdf",
        mime="application/pdf",
    )

    st.subheader("📱 QR코드 공유")
    qr_bytes = create_qr_code(APP_URL)
    st.image(qr_bytes, width=170)
    st.caption(APP_URL)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("다시 검사하기"):
            reset_test()
            st.rerun()

    with col2:
        if st.button("처음으로"):
            reset_test()
            st.rerun()


def main():
    st.set_page_config(
        page_title="육아 부모 유형 진단",
        page_icon="👨‍👩‍👧",
        layout="centered",
    )

    apply_style()
    init_state()

    questions = load_questions()

    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "test":
        show_test(questions)
    elif st.session_state.page == "result":
        show_result(questions)


if __name__ == "__main__":
    main()
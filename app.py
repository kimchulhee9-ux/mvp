import streamlit as st
import pandas as pd
import numpy as np


QUESTION_SCALE = {
    1: "전혀 아니다",
    2: "아니다",
    3: "보통이다",
    4: "그렇다",
    5: "매우 그렇다",
}


def load_questions():
    return [
        {"id": 1, "text": "아이가 속상해할 때 먼저 감정을 들어주는 편이다.", "type": "A"},
        {"id": 2, "text": "가정에서 지켜야 할 규칙을 명확하게 알려주는 편이다.", "type": "B"},
        {"id": 3, "text": "아이가 스스로 선택하도록 기다려주는 편이다.", "type": "C"},
        {"id": 4, "text": "상황에 따라 공감과 규칙을 함께 고려한다.", "type": "D"},
        {"id": 5, "text": "아이와 대화하며 문제를 해결하려고 한다.", "type": "A"},
        {"id": 6, "text": "생활 습관과 약속을 꾸준히 강조한다.", "type": "B"},
        {"id": 7, "text": "아이가 직접 해보며 배우는 것을 중요하게 생각한다.", "type": "C"},
        {"id": 8, "text": "아이의 감정은 받아주되 행동 기준도 함께 설명한다.", "type": "D"},
        {"id": 9, "text": "아이의 마음을 이해하려고 질문을 많이 하는 편이다.", "type": "A"},
        {"id": 10, "text": "아이의 자율성과 책임감을 함께 키우려 한다.", "type": "C"},
    ]


def load_result_info():
    return {
        "A": {
            "name": "공감형 부모",
            "emoji": "💗",
            "description": "아이의 감정을 우선하고 대화를 중요하게 생각하는 부모 유형입니다.",
            "strength": "아이의 마음을 잘 이해하고 정서적 안정감을 줍니다.",
            "weakness": "때로는 규칙이나 행동 기준이 약해질 수 있습니다.",
            "recommendation": "먼저 감정을 공감한 뒤, 지켜야 할 행동 기준을 짧고 분명하게 알려주세요.",
        },
        "B": {
            "name": "훈육형 부모",
            "emoji": "📏",
            "description": "규칙, 약속, 생활 습관을 중요하게 생각하는 부모 유형입니다.",
            "strength": "아이에게 안정적인 기준과 생활 리듬을 만들어 줍니다.",
            "weakness": "아이의 감정이나 속마음을 놓칠 수 있습니다.",
            "recommendation": "규칙을 말하기 전 아이의 감정을 한 문장으로 먼저 인정해 주세요.",
        },
        "C": {
            "name": "자율형 부모",
            "emoji": "🌱",
            "description": "아이의 선택과 독립성을 존중하는 부모 유형입니다.",
            "strength": "아이의 자기주도성과 책임감을 키워줍니다.",
            "weakness": "기준이 부족하면 아이가 혼란스러울 수 있습니다.",
            "recommendation": "선택권을 주되 가능한 범위와 책임을 함께 알려주세요.",
        },
        "D": {
            "name": "균형형 부모",
            "emoji": "⚖️",
            "description": "공감과 규칙을 함께 고려하고 상황에 따라 유연하게 대응하는 부모 유형입니다.",
            "strength": "아이의 감정과 행동 기준을 균형 있게 다룹니다.",
            "weakness": "상황마다 기준이 달라 보일 수 있습니다.",
            "recommendation": "가정의 핵심 원칙 2~3가지를 정하고 일관되게 적용해 주세요.",
        },
    }


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


def calculate_score(questions, responses):
    scores = {"A": 0, "B": 0, "C": 0, "D": 0}

    for q in questions:
        answer = responses.get(q["id"], 0)
        scores[q["type"]] += answer

    return scores


def analyze_type(scores):
    max_score = max(scores.values())
    top_types = [k for k, v in scores.items() if v == max_score]

    if len(top_types) > 1:
        return "D"

    return top_types[0]


def show_home():
    st.markdown("# 👨‍👩‍👧 육아 부모 유형 진단")
    st.markdown("### 10개의 질문으로 나의 육아 성향을 알아보세요.")
    st.write("이 검사는 MVP 버전이며, 간단한 설문을 통해 4가지 부모 유형 중 하나를 제공합니다.")

    st.info("결과는 참고용이며, 실제 육아 상황에서는 아이의 기질과 가정 환경을 함께 고려해야 합니다.")

    if st.button("시작하기", use_container_width=True):
        st.session_state.page = "test"
        st.session_state.current_question = 0
        st.rerun()


def show_test(questions):
    total = len(questions)
    idx = st.session_state.current_question
    q = questions[idx]

    st.markdown("## 📝 설문 진행")
    st.progress((idx + 1) / total)
    st.write(f"**{idx + 1} / {total} 문항**")

    st.markdown(f"### Q{q['id']}. {q['text']}")

    current_value = st.session_state.responses.get(q["id"], 3)

    answer = st.radio(
        "나의 답변",
        options=list(QUESTION_SCALE.keys()),
        index=current_value - 1,
        format_func=lambda x: f"{x} - {QUESTION_SCALE[x]}",
        horizontal=False,
    )

    st.session_state.responses[q["id"]] = answer

    col1, col2 = st.columns(2)

    with col1:
        if st.button("이전", use_container_width=True, disabled=idx == 0):
            st.session_state.current_question -= 1
            st.rerun()

    with col2:
        if idx < total - 1:
            if st.button("다음", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("결과 보기", use_container_width=True):
                if len(st.session_state.responses) < total:
                    st.warning("모든 질문에 답해주세요.")
                else:
                    st.session_state.page = "result"
                    st.rerun()


def show_result(questions):
    result_info = load_result_info()
    scores = calculate_score(questions, st.session_state.responses)
    result_type = analyze_type(scores)
    result = result_info[result_type]

    st.markdown("## 🎉 진단 결과")
    st.markdown(f"# {result['emoji']} 당신은 **{result['name']}** 입니다")

    st.write(result["description"])

    df = pd.DataFrame({
        "유형": ["공감형", "훈육형", "자율형", "균형형"],
        "점수": [scores["A"], scores["B"], scores["C"], scores["D"]],
    })

    st.subheader("유형별 점수")
    st.bar_chart(df.set_index("유형"))

    st.subheader("강점")
    st.success(result["strength"])

    st.subheader("보완점")
    st.warning(result["weakness"])

    st.subheader("추천 육아 방법")
    st.info(result["recommendation"])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("다시 검사하기", use_container_width=True):
            reset_test()
            st.rerun()

    with col2:
        if st.button("처음 화면으로", use_container_width=True):
            reset_test()
            st.rerun()


def main():
    st.set_page_config(
        page_title="육아 부모 유형 진단 MVP",
        page_icon="👨‍👩‍👧",
        layout="centered",
    )

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
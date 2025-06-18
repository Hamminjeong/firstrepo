import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    # CSV 파일 로드 (Streamlit Cloud에서는 같은 폴더에 CSV 파일이 있어야 함)
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")

    # '구' 단위 지역만 추출
    df = df[df["행정구역"].str.contains("구 ")].copy()
    df["행정구역"] = df["행정구역"].str.replace(r"\s*\(.*\)", "", regex=True)

    # 연령 관련 컬럼 추출
    age_cols = [col for col in df.columns if "2025년05월_계_" in col and "세" in col]

    # 문자열 → 숫자 변환 (쉼표 제거 포함)
    df["2025년05월_계_100세 이상"] = df["2025년05월_계_100세 이상"].astype(str).str.replace(",", "").astype(int)
    for col in age_cols:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)

    # 세로형 데이터로 변환
    df_long = df.melt(id_vars=["행정구역"], value_vars=age_cols,
                      var_name="연령", value_name="인구수")

    # 연령 숫자 추출
    df_long["연령"] = df_long["연령"].str.extract(r'(\d{1,3})(?=세)').astype(int)

    return df_long

# 데이터 로드
df = load_data()

# 사용자 인터페이스
st.title("📊 지역별 연령 인구 구조 시각화")
selected_region = st.selectbox("지역을 선택하세요:", sorted(df["행정구역"].unique()))

filtered_df = df[df["행정구역"] == selected_region]

# Plotly 그래프
fig = px.bar(
    filtered_df,
    x="연령",
    y="인구수",
    labels={"연령": "나이", "인구수": "인구 수"},
    title=f"{selected_region}의 연령별 인구 분포",
    height=600
)
fig.update_layout(xaxis=dict(dtick=5))  # 5세 단위 눈금

st.plotly_chart(fig, use_container_width=True)

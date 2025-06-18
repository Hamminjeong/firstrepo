import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    # 로컬 파일 또는 URL로 교체 가능
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")
    df = df[df["행정구역"].str.contains("구 ")].copy()
    df["행정구역"] = df["행정구역"].str.replace(r"\s*\(.*\)", "", regex=True)

    # 연령 관련 컬럼 추출
    age_cols = [col for col in df.columns if "2025년05월_계_" in col and "세" in col]
    df["2025년05월_계_100세 이상"] = df["2025년05월_계_100세 이상"].str.replace(",", "").astype(int)
    for col in age_cols:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)

    df_long = df.melt(id_vars=["행정구역"], value_vars=age_cols,
                      var_name="연령", value_name="인구수")
    df_long["연령"] = df_long["연령"].str.extract(r"(\d+)").astype(int)
    return df_long

df = load_data()

st.title("📊 지역별 연령 인구 구조 시각화")
지역 = st.selectbox("지역을 선택하세요", sorted(df["행정구역"].unique()))
filtered = df[df["행정구역"] == 지역]

fig = px.bar(filtered, x="연령", y="인구수", title=f"{지역}의 연령별 인구 분포", labels={"연령": "나이", "인구수": "명"}, height=600)
fig.update_layout(xaxis=dict(dtick=5))
st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 제목
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

st.caption(
    "1년간 박스오피스 10위권에 든 영화 데이터를 바탕으로 "
    "영화의 분포와 여러 데이터 사이의 관계를 살펴봅니다."
)

# 데이터 불러오기
URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(URL)

    # 장르에 여러 장르가 있으면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("기타")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 숫자 데이터 숫자형으로 변환
    numeric_columns = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# 데이터 불러오기
df = load_data()

# -----------------------------------------
# 그래프 1. 장르별 영화 편수
# -----------------------------------------

st.header("그래프 1) 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]

fig = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.5,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="percent",
    hovertemplate="<b>%{label}</b><br>"
                  "영화 편수: %{value}편<br>"
                  "비율: %{percent}<extra></extra>"
)

fig.update_layout(
    height=500,
    legend_title="장르"
)

st.plotly_chart(fig, use_container_width=True)

# 그래프로 알 수 있는 것
st.markdown("---")
st.subheader("📝 이 그래프로 알 수 있는 것")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 적어 보세요.")

st.markdown("---")

# 데이터 확인
with st.expander("📋 데이터 확인하기"):
    st.dataframe(df, use_container_width=True)

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

# 데이터 주소
URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(URL)

    # 여러 장르가 있으면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("기타")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 숫자 데이터 변환
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


df = load_data()


# ==================================================
# 그래프 1. 장르별 영화 편수
# ==================================================

st.header("그래프 1) 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]

fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.5,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="percent",
    hovertemplate=
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
)

fig1.update_layout(
    height=500,
    legend_title="장르"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
st.subheader("📝 이 그래프로 알 수 있는 것")
st.info(
    "여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 적어 보세요."
)


# ==================================================
# 그래프 2. 장르 안에 들어 있는 영화
# ==================================================

st.markdown("---")
st.header("그래프 2) 장르 안에 들어 있는 영화")

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화의 총 관객수"
)

fig2.update_traces(
    hovertemplate=
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
)

fig2.update_layout(
    height=650
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("📝 이 그래프로 알 수 있는 것")
st.info(
    "여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 적어 보세요."
)


# ==================================================
# 그래프 3. 총 관객수의 히스토그램
# ==================================================

st.markdown("---")
st.header("그래프 3) 총 관객수의 분포")

# 결측값 제거
audi_data = df["total_audi"].dropna()

fig3 = px.histogram(
    audi_data,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객수 분포",
    labels={
        "total_audi": "총 관객수",
        "count": "영화 편수"
    }
)

fig3.update_layout(
    height=500,
    xaxis_title="총 관객수",
    yaxis_title="영화 편수"
)

st.plotly_chart(fig3, use_container_width=True)


# ==================================================
# 그래프 3. 자동 설명
# ==================================================

# 가장 관객이 많은 영화 찾기
valid_movies = df[
    ["movieNm", "total_audi"]
].dropna(subset=["total_audi"])

max_index = valid_movies["total_audi"].idxmax()

max_movie_name = valid_movies.loc[max_index, "movieNm"]
max_movie_audi = int(valid_movies.loc[max_index, "total_audi"])


# 히스토그램에서 가장 많은 영화가 몰린 구간 계산
min_audi = audi_data.min()
max_audi = audi_data.max()

bin_width = (max_audi - min_audi) / 20

if bin_width > 0:
    bin_numbers = ((audi_data - min_audi) / bin_width).astype(int)

    # 마지막 값이 20번 구간으로 넘어가는 것을 방지
    bin_numbers = bin_numbers.clip(upper=19)

    most_common_bin = bin_numbers.value_counts().idxmax()

    range_start = min_audi + most_common_bin * bin_width
    range_end = range_start + bin_width

else:
    range_start = min_audi
    range_end = max_audi


# 설명 문구
st.markdown("### 📌 그래프에서 알 수 있는 것")

st.write(
    f"대부분의 영화는 총 관객수 "
    f"**{range_start:,.0f}명 ~ {range_end:,.0f}명** "
    f"구간에 몰려 있습니다."
)

st.write(
    f"가장 관객이 많은 영화는 **{max_movie_name}**으로, "
    f"총 관객수는 **{max_movie_audi:,}명**입니다."
)


# ==================================================
# 데이터 확인
# ==================================================

st.markdown("---")

with st.expander("📋 데이터 확인하기"):
    st.dataframe(df, use_container_width=True)

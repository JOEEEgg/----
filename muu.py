import streamlit as st
import pandas as pd

st.title("HELLO")

# 데이터 프레임 생성 예시
data = pd.read_csv('C:/데이터분석/미니프로젝트/데이터/musinsa999.csv', encoding='cp949')

# Streamlit 애플리케이션 설정
st.title('무신사에서 내 사이즈에 맞는 상품 찾기')

# 입력 필드 생성
input_pants_length = st.number_input("총장을 입력하세요:", key="pants_length")
input_waist_section = st.number_input("허리단면을 입력하세요:", key="waist_section")
input_hip_section = st.number_input("엉덩이단면을 입력하세요:", key="hip_section")
input_thigh_section = st.number_input("허벅지단면을 입력하세요:", key="thigh_section")
input_rise_section = st.number_input("밑위를 입력하세요:", key="rise_section")
input_hem_section = st.number_input("밑단단면을 입력하세요:", key="hem_section")
input_tolerance = st.number_input("오차 범위를 입력하세요:", value=1)

# 버튼 생성
search_button = st.button("검색")

# 검색 버튼 클릭 시 데이터 조회 및 출력
if search_button:
    try:
        # 데이터 타입 변환 (문자열 컬럼을 숫자로 변환)
        numeric_columns = ['총장', '허리단면', '엉덩이단면', '허벅지단면', '밑위', '밑단단면']
        data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
        
        # 데이터 조회 및 출력
        filtered_data = data[
            (data['총장'] >= input_pants_length - input_tolerance) & (data['총장'] <= input_pants_length + input_tolerance) &
            (data['허리단면'] >= input_waist_section - input_tolerance) & (data['허리단면'] <= input_waist_section + input_tolerance) &
            (data['엉덩이단면'] >= input_hip_section - input_tolerance) & (data['엉덩이단면'] <= input_hip_section + input_tolerance) &
            (data['허벅지단면'] >= input_thigh_section - input_tolerance) & (data['허벅지단면'] <= input_thigh_section + input_tolerance) &
            (data['밑위'] >= input_rise_section - input_tolerance) & (data['밑위'] <= input_rise_section + input_tolerance) &
            (data['밑단단면'] >= input_hem_section - input_tolerance) & (data['밑단단면'] <= input_hem_section + input_tolerance)
        ]
        
        # 결과 출력
        if not filtered_data.empty:
            st.write("일치하는 데이터: ", len(filtered_data), "개")
            st.write(filtered_data)
            
        else:
            st.write("일치하는 데이터가 없습니다.")
            
    except Exception as e:
        st.write("오류가 발생했습니다:", e)

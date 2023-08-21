import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import altair as alt
import os

# 데이터 프레임 생성 예시 (데이터 파일 경로에 맞게 수정 필요)
data = pd.read_csv('C:/데이터분석/미니프로젝트/데이터/musinsa999.csv', encoding='cp949')  # 데이터 파일 경로 수정 필요
data['핏'] = data['핏'].astype(str)

# Streamlit 애플리케이션 설정
st.title('👕무신사 미니 프로젝트')

# 탭 생성
menu = ["상의", "하의"]
choice = st.sidebar.selectbox("카테고리 선택", menu)

if choice == "상의":
    st.title('상의 카테고리')
    # 상의 사이즈 입력 필드 생성
    input_tshirts_width = st.number_input("총장을 입력하세요:", key="tshirts_width")
    input_shoulder_width = st.number_input("어깨너비를 입력하세요:", key="shoulder_width")
    input_chest_section = st.number_input("가슴단면을 입력하세요:", key="chest_section")
    input_sleeve_length = st.number_input("소매길이를 입력하세요:", key="sleeve_length")
    input_tolerance = st.number_input("오차 범위를 입력하세요:", value=1)
    
    # 버튼 생성
    search_button = st.button("상품검색")
    
    if search_button:
        try:
            # 데이터 타입 변환 (문자열 컬럼을 숫자로 변환)
            numeric_columns = ['총장', '어깨너비', '가슴단면', '소매길이']
            data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
            
            # 데이터 조회 및 출력
            filtered_data = data[
                (data['총장'] >= input_tshirts_width - input_tolerance) & (data['총장'] <= input_tshirts_width + input_tolerance) &
                (data['어깨너비'] >= input_shoulder_width - input_tolerance) & (data['어깨너비'] <= input_shoulder_width + input_tolerance) &
                (data['가슴단면'] >= input_chest_section - input_tolerance) & (data['가슴단면'] <= input_chest_section + input_tolerance) &
                (data['소매길이'] >= input_sleeve_length - input_tolerance) & (data['소매길이'] <= input_sleeve_length + input_tolerance)
            ]
            
            # 상의 결과 출력 처리 코드 작성
            if not filtered_data.empty:
                st.write("일치하는 상의 데이터: ", len(filtered_data), "개")
                st.write(filtered_data)
                
                # 나의 맞는 브랜드 그래프 그리기
                if len(filtered_data) >= 2:  # 최소한 1개 이상의 샘플이 있어야 클러스터링 가능
                    brand_groups = filtered_data.groupby('브랜드').size().reset_index(name='Count')
                    max_count = brand_groups['Count'].max() + 20 # x축 범위의 최대값 설정

                    brand_chart = alt.Chart(brand_groups).mark_bar().encode(
                        x=alt.X('Count:Q', scale=alt.Scale(domain=(0, max_count))),
                        y=alt.Y('브랜드:N', sort='-x'),  # 브랜드별로 내림차순 정렬
                        color=alt.Color('브랜드:N', scale=alt.Scale(scheme='category20')),  # 다른 색상 할당
                        tooltip=['브랜드:N', 'Count:Q']
                    ).properties(
                        width=500,
                        height=300
                    )

                    st.altair_chart(brand_chart, use_container_width=True)
                else:
                    st.write("데이터가 너무 적어 클러스터링을 수행할 수 없습니다.")

    
            
                 # 내 사이즈가 선호하는 핏 그래프 그리기
                if len(filtered_data) >= 2:  # 최소한 1개 이상의 샘플이 있어야 클러스터링 가능
                    fits = filtered_data['핏'].value_counts().reset_index()
                    fits.columns = ['핏', '개수']
                    
                    # Vega-Lite로 그래프 생성 (color 인코딩 추가)
                    fit_chart = alt.Chart(fits).mark_bar().encode(
                        x='핏:N',
                        y='개수:Q',
                        color='핏:N'  # 핏 별로 다른 색상 지정
                    ).properties(
                        width=500,
                        height=300
                    ).to_dict()  # Vega-Lite 스펙으로 변환
                    
                    st.vega_lite_chart(fit_chart, use_container_width=True)
                else:
                    st.write("데이터가 너무 적어 클러스터링을 수행할 수 없습니다.")
            
        except Exception as e:
            st.write("오류가 발생했습니다:", e)

elif choice == "하의":
    st.title('하의 카테고리')
    # 하의 사이즈 입력 필드 생성
    input_pants_length = st.number_input("총장을 입력하세요:", key="pants_length")
    input_waist_section = st.number_input("허리단면을 입력하세요:", key="waist_section")
    input_hip_section = st.number_input("엉덩이단면을 입력하세요:", key="hip_section")
    input_thigh_section = st.number_input("허벅지단면을 입력하세요:", key="thigh_section")
    input_rise_section = st.number_input("밑위를 입력하세요:", key="rise_section")
    input_hem_section = st.number_input("밑단단면을 입력하세요:", key="hem_section")
    input_tolerance = st.number_input("오차 범위를 입력하세요:", value=1)
    
   # 버튼 생성
    search_button = st.button("상품검색")
    
    if search_button:
        try:
            # (데이터 타입 변환 및 데이터 조회는 이전 코드와 동일하므로 생략)
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
             # 하의 결과 출력 처리 코드 작성
            if not filtered_data.empty:
                st.write("일치하는 하의 데이터: ", len(filtered_data), "개")
                st.write(filtered_data)
               
                # 나의 맞는 브랜드 그래프 그리기
                if len(filtered_data) >= 2:  # 최소한 1개 이상의 샘플이 있어야 클러스터링 가능
                    brand_groups = filtered_data.groupby('브랜드').size().reset_index(name='Count')
                    max_count = brand_groups['Count'].max() + 15 # x축 범위의 최대값 설정
                    
                    brand_chart = alt.Chart(brand_groups).mark_bar().encode(
                        x=alt.X('Count:Q', scale=alt.Scale(domain=(0, max_count))),  # x축 범위 조정
                        y= alt.Y('브랜드:N', sort='-x'),  # 브랜드별로 내림차순 정렬
                        color=alt.Color('브랜드:N', scale=alt.Scale(scheme='category20')),  # 다른 색상 할당
                        tooltip=['브랜드:N', 'Count:Q']
                    ).properties(
                        width=500,
                        height=300
                    )

                    st.altair_chart(brand_chart, use_container_width=True)
       
            
               # 내 사이즈가 선호하는 핏 그래프 그리기
                if len(filtered_data) >= 2:  # 최소한 1개 이상의 샘플이 있어야 클러스터링 가능
                    fits = filtered_data['핏'].value_counts().reset_index()
                    fits.columns = ['핏', 'Count']  # Use 'Count' column name
                    max_count = fits['Count'].max() + 15  # x축 범위의 최대값 설정
                    
                    # Vega-Lite로 그래프 생성 (color 인코딩 추가)
                    fit_chart = alt.Chart(fits).mark_bar().encode(
                        x=alt.X('Count:Q', scale=alt.Scale(domain=(0, max_count))),  # x축 범위 설정
                        y=alt.Y('핏:N'),
                        color=alt.Color('핏:N'),  # 핏 별로 다른 색상 지정
                        tooltip=['핏:N', 'Count:Q']
                    ).properties(
                        width=500,
                        height=300
                    ).to_dict()  # Vega-Lite 스펙으로 변환
                    
                    # 그래프 위에 수치 표시
                    text = brand_chart.mark_text(
                        align='center',
                        baseline='middle',
                        dx=3  # 수치 표시 위치 조정
                    ).encode(
                        text='Count:Q'  # 표시할 수치 데이터 지정
                    )

                    st.vega_lite_chart(fit_chart, use_container_width=True)
                else:
                    st.write("데이터가 너무 적어 클러스터링을 수행할 수 없습니다.")

        except Exception as e:
            st.write("오류가 발생했습니다:", e)

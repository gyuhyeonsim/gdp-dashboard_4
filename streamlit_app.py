import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
from data_file import data, data_2, data_2_details

# Full Category Mapping
category_mapping = {
    "1-1": "Awareness - Definition",
    "1-2": "Awareness - Problem",
    "1-3": "Awareness - Opportunity",
    "1-4": "Awareness - Trend",
    "1-5": "Awareness - Size Options",
    "1-6": "Awareness - Color Options",
    "1-7": "Awareness - Specification Options",
    "1-8": "Awareness - Ingredient Options",
    "1-9": "Awareness - Shape Options",
    "1-10": "Awareness - Used Options",
    "1-11": "Awareness - Price Options",
    "1-12": "Awareness - User Options",
    "1-13": "Awareness - Alternative",
    "1-14": "Awareness - Best",
    "1-15": "Awareness - Worst",
    "1-16": "Awareness - Solution",
    "1-17": "Awareness - Place",
    "2-1": "Consideration - Brand Product Search",
    "2-2": "Consideration - Comparisons",
    "2-3": "Consideration - Product Trend",
    "2-4": "Consideration - Product Size",
    "2-5": "Consideration - Product Color",
    "2-6": "Consideration - Product Specification",
    "2-7": "Consideration - Product Ingredient",
    "2-8": "Consideration - Product Shape",
    "2-9": "Consideration - Product Used",
    "2-10": "Consideration - Product Price",
    "3-1": "Purchase - Online Purchase",
    "3-2": "Purchase - Offline Purchase",
    "3-3": "Purchase - How To Buy",
    "3-4": "Purchase - Promotion",
    "3-5": "Purchase - Conversion",
    "3-6": "Purchase - Pricing",
    "3-7": "Purchase - Review",
    "4-1": "Post-Purchase - Accessories",
    "4-2": "Post-Purchase - Dissatisfied",
    "4-3": "Post-Purchase - Tips",
    "4-4": "Post-Purchase - Customer Service",
    "4-5": "Post-Purchase - Informational Community"
}

# Main visualization
st.title("펫보험 연관 키워드 분석 리포트")

# Google Trend data analysis checkbox
use_data_2 = st.checkbox("Use Google Trend data for analysis", value=False, key='google_trend_checkbox')

# Add English description for categories
if use_data_2:
    for item in data_2:
        item["category_english"] = category_mapping.get(item["category"], "Unknown Category")
        details = data_2_details.get(item["keyword"], {})
        item["cpc"] = details.get("cpc")
        item["search_volume"] = details.get("search_volume")
        item["competition_index"] = details.get("competition_index")

    # Convert to DataFrame with additional details
    df = pd.DataFrame([{**item, **data_2_details.get(item["keyword"], {})} for item in data_2])
    
    # Plot the sum of search volume by category stage (1, 2, 3, 4)
    df["main_category"] = df["category"].str.split("-").str[0]
    search_volume_sum = df.groupby("main_category")["search_volume"].sum().reindex(['1', '2', '3', '4'], fill_value=0)
    category_labels = ['Awareness', 'Consideration', 'Purchase', 'Post-Purchase']
    search_volume_df = pd.DataFrame({'Category': category_labels, 'Search Volume': search_volume_sum.values})
    st.bar_chart(data=search_volume_df.set_index('Category'), use_container_width=True, height=400)
else:
    for item in data:
        item["category_english"] = category_mapping.get(item["category"], "Unknown Category")
    df = pd.DataFrame(data)

# Split data into tables based on the first digit of the category
df["main_category"] = df["category"].str.split("-").str[0]
category_groups = {
    "1": df[df["main_category"] == "1"],
    "2": df[df["main_category"] == "2"],
    "3": df[df["main_category"] == "3"],
    "4": df[df["main_category"] == "4"],
}

# Loop through each group and display it
for main_category, group_df in category_groups.items():
    st.subheader(f"Category {main_category} - {'Awareness' if main_category == '1' else 'Consideration' if main_category == '2' else 'Purchase' if main_category == '3' else 'Post-Purchase'}")
    st.write(f"Displaying {len(group_df)} results for Category {main_category}")
    if not group_df.empty:
        st.dataframe(group_df)
    else:
        st.write(f"No data available for Category {main_category}.")

# Additional Insights in Table Format
st.subheader("Additional Insights")

# Main Keyword Insights Table
main_keywords = [
    {"Keyword": "펫보험", "Search Volume": 1900, "CPC": 5.96},
    {"Keyword": "펫 보험", "Search Volume": 1900, "CPC": 5.96},
    {"Keyword": "반려 동물 보험", "Search Volume": 390, "CPC": 4.85},
    {"Keyword": "동물 보험", "Search Volume": 260, "CPC": 3.26},
    {"Keyword": "애완 동물 보험", "Search Volume": 70, "CPC": 3.91},
    {"Keyword": "고양이 펫 보험", "Search Volume": 50, "CPC": 7.28}
]
main_keywords_df = pd.DataFrame(main_keywords)
st.subheader("1. 메인 키워드 인사이트")
st.dataframe(main_keywords_df)
st.write("""
이들은 대부분 Awareness 단계의 키워드로, 검색량이 높고 CPC도 상대적으로 높은 편입니다. 이는 소비자들이 펫 보험의 정의와 가치를 이해하고자 하는 초기 단계에서 이러한 키워드를 자주 검색하며, 동시에 여러 기업들이 이 시장에 대한 관심을 가지고 높은 경쟁을 하고 있음을 의미합니다.
따라서 메인 키워드를 활용하여 자사 제품의 특장점을 강조하는 콘텐츠를 통해 소비자에게 초기 인식에서부터 긍정적인 이미지를 심어주는 것이 중요합니다. 특히 각 보험의 특장점, 가격 비교 등의 정보를 통해 소비자가 펫 보험에 대해 명확히 이해할 수 있도록 도와주는 것이 좋습니다.
""")

# Niche Keyword Insights Table
niche_keywords = [
    {"Keyword": "펫 보험 가격", "Search Volume": 140, "CPC": 4},
    {"Keyword": "펫 실비 보험", "Search Volume": 10, "CPC": 9.62},
    {"Keyword": "펫 보험 종류", "Search Volume": 20, "CPC": 3.62},
    {"Keyword": "펫 보험료", "Search Volume": 10, "CPC": 3.93}
]
niche_keywords_df = pd.DataFrame(niche_keywords)
st.subheader("2. 니치 키워드 인사이트")
st.dataframe(niche_keywords_df)
st.write("""
니치 키워드는 검색량이 적지만, 검색 의도가 매우 뚜렷한 롱테일 키워드로, 소비자들이 구체적인 정보(예: 가격, 실비 보험, 보험료)에 대해 궁금해하고 있음을 보여줍니다.
특히 '펫 실비 보험'(검색량: 10, CPC: 9.62)과 같은 키워드는 높은 CPC로 인해 경쟁이 치열할 수 있으나, 이를 통해 보험 비용 절감에 대한 소비자의 관심을 반영할 수 있습니다. 이와 같은 니치 키워드는 소비자가 구매 의사 결정 단계에 있는 경우가 많기 때문에, 상세한 가격 정보 및 보험 혜택에 대한 안내를 제공하는 것이 필요합니다.
""")

# Brand Keyword Utilization Suggestions Table
brand_suggestions = [
    {"Suggestion": "브랜드 인지도 제고", "Keyword": "펫보험", "Search Volume": 1900, "CPC": 5.96},
    {"Suggestion": "가격 정보 제공", "Keyword": "펫 보험 가격", "Search Volume": 140, "CPC": 4},
    {"Suggestion": "가격 정보 제공", "Keyword": "펫 실비 보험", "Search Volume": 10, "CPC": 9.62},
    {"Suggestion": "타깃 고객 세분화", "Keyword": "고양이 펫 보험", "Search Volume": 50, "CPC": 7.28}
]
brand_suggestions_df = pd.DataFrame(brand_suggestions)
st.subheader("3. 브랜드 키워드 활용 제안")
st.dataframe(brand_suggestions_df)
st.write("""
이러한 키워드 인사이트를 바탕으로 SEO 및 광고 캠페인을 진행하며, 소비자들이 자사 브랜드를 인식하고, 경쟁사 대비 우수한 상품성을 알 수 있도록 유도하는 것이 중요합니다.
""")

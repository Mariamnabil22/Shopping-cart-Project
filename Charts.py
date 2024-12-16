import streamlit as st
import pandas as pd
import plotly.express as px
import os 
import streamlit as st

st.set_page_config(layout="wide", page_title="Shopping Cart Dashboard")

csv_file_path = 'combined_data.csv'

if os.path.exists(csv_file_path):
    combined_data = pd.read_csv(csv_file_path)
else:
    st.error("The combined data file does not exist. Please check the file path.")
    st.stop()  # Stop execution if the file is not found

st.sidebar.header("User  Input Features")
show_data = st.sidebar.checkbox('Show Data', False)
size = st.sidebar.selectbox('Select size', combined_data['size'].unique())
gender = st.sidebar.selectbox('Select Gender', combined_data['gender'].unique())
age_range = st.sidebar.slider('Select Age Range', 
                               min_value=int(combined_data['age'].min()), 
                               max_value=int(combined_data['age'].max()), 
                               value=(20, 40))

filtered_data = combined_data[(combined_data['size'] == size) & 
                               (combined_data['gender'] == gender) & 
                               (combined_data['age'].between(age_range[0], age_range[1]))]

product_type_counts = filtered_data['product_type'].value_counts().reset_index()
product_type_counts.columns = ['product_type', 'count']

tabs = st.tabs(["Charts", "Statistics"])

with tabs[0]:
    col1, col2, col3 = st.columns(3)

    with col1:
        
        fig1 = px.histogram(filtered_data, x='total_price', color='gender',
                             title='Total Price Distribution by Gender', width=700)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        
        if not product_type_counts.empty:
            fig2 = px.pie(product_type_counts, names='product_type', values='count', title='Product Type Distribution')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.write("No data available for the selected filters.")

    with col3:
        
        fig3 = px.scatter(filtered_data, x='quantity_x', y='total_price', color='gender',
                           title='Total Price vs Quantity', size='quantity_x', hover_name='product_name')
        st.plotly_chart(fig3, use_container_width=True)

    
    st.header("Additional Visualizations")
   
    fig4 = px.box(filtered_data, x='product_type', y='total_price', color='gender',
                   title='Box Plot of Total Price by Product Type and Gender')
    st.plotly_chart(fig4, use_container_width=True)

    
    if 'date' in filtered_data.columns:
        sales_over_time = filtered_data.groupby('date')['total_price'].sum().reset_index()
        fig5 = px.bar(sales_over_time, x='date', y='total_price', title='Total Sales Over Time')
        st.plotly_chart(fig5, use_container_width=True)

with tabs[1]:
    st.header("Summary Statistics")
    st.write(filtered_data.describe())

    
    top_products = filtered_data.groupby('product_name')['total_price'].sum().nlargest(10).reset_index()
    st.subheader("Top 10 Products by Total Price")
    fig_top_products = px.bar(top_products, x='product_name', y='total_price', title='Top 10 Products by Total Price')
    st.plotly_chart(fig_top_products, use_container_width=True)

    if 'total_price' in filtered_data.columns and 'quantity_x' in filtered_data.columns:
        correlation_matrix = filtered_data[['total_price', 'quantity_x', 'age']].corr()
        st.subheader("Correlation Heatmap")
        fig_heatmap = px.imshow(correlation_matrix, text_auto=True, title='Correlation Heatmap')
        st.plotly_chart(fig_heatmap, use_container_width=True)

    st.subheader("Counts of Unique Values in Categorical Columns")
    categorical_columns = ['payment', 'gender', 'product_type']
    for column in categorical_columns:
        st.write(f"**{column}**")
        st.write(filtered_data[column].value_counts())
    
    st.subheader("Distribution of Total Price")
    fig_distribution = px.histogram(filtered_data, x='total_price', title='Distribution of Total Price', nbins=30)
    st.plotly_chart(fig_distribution, use_container_width=True)

    st.subheader("Box Plot of Age Distribution")
    fig_age_box = px.box(filtered_data, y='age', title='Box Plot of Age Distribution')
    st.plotly_chart(fig_age_box, use_container_width=True)

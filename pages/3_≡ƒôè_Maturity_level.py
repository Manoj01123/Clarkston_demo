import streamlit as st
import pandas as pd
import csv
import json
import plotly.graph_objects as go
import plotly


st.set_page_config(page_title="Maturity Level", 
                   layout="wide")


    
st.markdown(
    """
    <style>
    .css-18ni7ap.e8zbici2 {
        background-color: rgba(0, 0, 0, 0.8) ;
        background-repeat: no-repeat;
        background-image: url('https://clarkstonconsulting.com/wp-content/uploads/2021/11/Clarkston_Consulting_Logo_white-text-475x100-1.png');
        background-size: contain;
        background-repeat: no-repeat;
        width: 100%;
        height: 70px;
        background-position: 93%;
    }
    .e1fb0mya1.css-fblp2m.ex0cdmw0{
        background-color: rgba(256, 256, 256, 0.5) ;
    }
    .css-79elbk.e1fqkh3o10 {
        background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7) 68px, transparent 0%);
    }
    
    </style>
    """,
    unsafe_allow_html=True
    )

if 'compnay' not in st.session_state:
    st.session_state["company"] = ""

worksheet_list = ["1. Forecasting - Demand Planning", "2. New Product Development", "3. Production Planning", "4. Inventory Management", 
                  "5. Strategic Sourcing", "6. Procurement", "7. Sales & Ops Planning", "8. Distribution & Whse Mgt", 
                  "9. Transportation", "10. Master Data", "11. IT Systems", "12. Metrics", 
                  "13. LS Manufacturing", "14. LS New Product Development"]

worksheet_list_wo_num = ["Forecasting - Demand Planning", "New Product Development", "Production Planning", "Inventory Management", "Strategic Sourcing",
                  "Procurement", "Sales & Ops Planning", "Distribution & Whse Mgt", "Transportation", "Master Data",
                  "IT Systems", "Metrics", "LS Manufacturing", "LS New Product Development"]

company_list = [
    "Apple",
    "Amazon",
    "Google",
    "Netflix",
    "Meta",
    "Microsoft",
    "Tesla",
    "Intel",
    "IBM",
    "Oracle"]

with open('Clarkston_questionnaire.json', 'r') as f:
  questionnaire_data = json.load(f)

dummy_data = pd.read_csv(worksheet_list_wo_num[0]+'.csv',index_col=[0])
dummy_data.rename(columns = {'0':'0.0', '1':'1.0', '2': '2.0'}, inplace = True)
maturity_weight_list = []
for i in questionnaire_data[worksheet_list_wo_num[0]]:
    maturity_weight_list.append(questionnaire_data[worksheet_list_wo_num[0]][i])
always_list = [0]*35
never_list = [0]*35
dk_list = [0]*35
for i in dummy_data.columns:
    if '0.' in i:
        always_list += dummy_data[i]
    elif '1.' in i:
        never_list += dummy_data[i]
    elif '2.' in i:
        dk_list += dummy_data[i]
dummy_data['Always'] = always_list
dummy_data['Never'] = never_list
dummy_data['Dunno'] = dk_list
dummy_data['Weight'] = maturity_weight_list
maturity_score_list = []
for i in range(len(maturity_weight_list)):
    if always_list[i] == 0:
        if never_list[i] == 0:
            maturity_score = 0
        else:
            maturity_score = 1
            
    else:
        if always_list[i] > never_list[i]:
            maturity_score = round(((1 - (never_list[i]/(always_list[i] + never_list[i]))) * maturity_weight_list[i]), 1)
        else:
            maturity_score = 1
    maturity_score_list.append(maturity_score)
    
dummy_data['Total_Score'] = maturity_score_list
averge_score = round(dummy_data['Total_Score'].mean(),2)
total_always = dummy_data['Always'].sum()
total_never = dummy_data['Never'].sum()
total_always_percentage = round(total_always/(total_always+total_never),3)
total_never_percentage = round(total_never/(total_never+total_always),3)

level3_num = maturity_weight_list.count(3)
averge_score_level3 = round(dummy_data['Total_Score'][:level3_num].mean(),2)
total_always_level3 = dummy_data['Always'][:level3_num].sum()
total_never_level3 = dummy_data['Never'][:level3_num].sum()
total_always_level3_percentage = round(total_always_level3/(total_always_level3+total_never_level3),3)
total_never_level3_percentage = round(total_never_level3/(total_never_level3+total_always_level3),3)
    

st.sidebar.header("Filter Here:")

company_name = st.sidebar.selectbox("Select Companies", company_list)

add_sheet = st.sidebar.selectbox(
    "Select Sheets",
    worksheet_list
)

              

st.title("Supply Chain Maturity Level")
st.markdown("---")


for com in company_list:
    if company_name == com:
        st.session_state.company = com
        st.header(st.session_state.company)
        

question_list = []
ms_list = []
for sheet in questionnaire_data:
    question_list.append(questionnaire_data[sheet])
    
    sheet_name = str(list(questionnaire_data).index(sheet)+1) + ". "+ sheet
    if add_sheet == (sheet_name):
        st.subheader(sheet + " Diagnostic Results")
        
#plotly

if st.sidebar.button("Show maturity level"):
    
    col1, col2 = st.columns(2)
    
    with col1:
        data = [[averge_score_level3, total_always_level3_percentage, total_never_level3_percentage], [averge_score, total_always_percentage, total_never_percentage]]
        idx, col = ['Level 3', "All Level"], ["Average Score", "Always/Frequent","Rarely/Never"] 
        df = pd.DataFrame(data, index=idx, columns=col)
        df_style = df.style.format({'Average Score': "{:.2f}",'Always/Frequent': "{:.1%}",'Rarely/Never': "{:.1%}"})
        st.dataframe(df_style)
        
    
    col3, col4 = st.columns(2)
    
    
    with col3:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=['Level 3', 'All Level'],
            x=[total_always_level3_percentage, total_always_percentage],
            name='Always/Frequent',
            orientation='h',
            marker=dict(
                color='rgba(19, 11, 12, 0.4)',
                line=dict(color='rgba(19, 11, 12, 0.6)', width=3)
            )
        ))
        fig.add_trace(go.Bar(
            y=['Level 3', 'All Level'],
            x=[total_never_level3_percentage, total_never_percentage],
            name='Rarely/Never',
            orientation='h',
            marker=dict(
                color='rgba(255, 40, 0, 0.4)',
                line=dict(color='rgba(255, 40, 0, 0.6)', width=3)
            )
        ))
        
        fig.update_layout(
            xaxis=dict(
                showgrid=True,
                showline=True,
                zeroline=True,
             
            ),
            yaxis=dict(
                showgrid=False,
                showline=True,
            ),
            barmode='stack',
    
            showlegend=True,
        )
        
        
        fig.update_xaxes(tickformat=".1%")
        
        
        st.plotly_chart(fig, use_container_width=False, theme = "streamlit")
    
    with col4:

        fig2 = go.Figure(data=go.Scatterpolar(
          r=dummy_data['Total_Score'],
          #theta=list(question_list[0]),
          fill='toself'
        ))
        
        fig2.update_layout(
          polar=dict(
            radialaxis=dict(
              visible=True
            ),
          ),
          showlegend=False,
          
        )
        
   
        st.plotly_chart(fig2, use_container_width=False, theme = "streamlit")
    
    
    
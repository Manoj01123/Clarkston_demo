import streamlit as st
import pandas as pd
import csv
import json
import datetime
import time


st.set_page_config(page_title="Supply Chain Questionnaire", 
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



if 'time' not in st.session_state:
    st.session_state['time'] = 0
    
    
worksheet_list = ["1. Forecasting - Demand Planning", "2. New Product Development", "3. Production Planning", "4. Inventory Management", 
                  "5. Strategic Sourcing", "6. Procurement", "7. Sales & Ops Planning", "8. Distribution & Whse Mgt", 
                  "9. Transportation", "10. Master Data", "11. IT Systems", "12. Metrics", 
                  "13. LS Manufacturing", "14. LS New Product Development"]
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

positions = [
    "1. Director, Information Services/IT-1 IT-1",
    "2. Systems Analyst/IT-2 IT-2",
    "3. Director of Sales/Marketing/Sales-Marketing1 Sales-Marketing1",
    "4. Senior Product Manager/Prod Mgr 1 Prod Mgr 1",
    "5. Sales Representative/Sales Rep1 Sales Rep1",
    "6. Manager, Demand Planning/Demand Plan1 Demand Plan1	",
    "7. Promotions Analyst/Demand Plan2 Demand Plan2",
    "8. Manager, Production Planning/Prod1 Prod1",
    "9. Production Planner/Prod2 Prod2",
    "10. Director, Distribution & Logistics/Dist1 Dist1	",
    "11. Distribution & Logistics Supervisor/Dist2 Dist2",
    "12. Distribution & Logistics Analyst/Dist3 Dist3",
    "13. Director, Purchasing & Strategic Sourcing/Purchasing1 Purchasing1",
    "14. Planner/Buyer/Purchasing2 Purchasing2",
    "15. Sourcing Analyst/Sourcing1 Sourcing1",
    "16. Manager, Quality Assurance/QA Mgr1 QA Mgr1	",
    "17. QA Analyst/QA Analyst1 QA Analyst1	",
    "18. Manager, Quality Control/QC Mgr1 QC Mgr1",
    "19. Director, Customer Service/Cust Serv1 Cust Serv1",
    "20. Supervisor, Customer Service/Cust Serv2 Cust Serv2	",
    "21. Customer Service Representative/Cust Serv3 Cust Serv3"]

options = ["Don't Know/NA", "Rarely/Never", "Always/Frequent" ]

with open('Clarkston_questionnaire.json', 'r') as f:
  questionnaire_data = json.load(f)


st.title("Supply Chain Management Questionnaire")
st.markdown("---")

st.sidebar.header("Please select the type of questionnaire:")

company_name = st.sidebar.selectbox(
    "Select your company",
    company_list
 )



add_role = st.sidebar.selectbox(
    "Select the roles",
    positions
 )

add_sheet = st.sidebar.selectbox(
    "Select the Questionnaire",
    worksheet_list
)


    
current_date = datetime.date.today()
current_time = datetime.datetime.now()

#while True:
    #time.sleep(1)
    #st.write("Current time is: ", current_time)

company_name_list = []
sheet_name_list = []
role_list = []
radio_result_list =[]

st.sidebar.write("Click the Start button to begin")
if st.sidebar.button("Start"):
    st.session_state.time = time.time()
    st.sidebar.write("Started")

# Choose Sheets        
for sheet in questionnaire_data:
    sheet_name = str(list(questionnaire_data).index(sheet)+1) + ". "+ sheet
    if add_sheet == (sheet_name):
        st.subheader("Questionnaire: " + sheet_name)
        
        # Choose roles
        for p in positions:
           if add_role == p:       
                st.subheader("Role: " + p)
                
                # Create a form
                #with st.form(key=sheet):
                
                radio_result = [] 
                
                # Answer questions
                # To asign questions to two columns
                col1, col2 = st.columns(2)
                count = 0
                
                for q in questionnaire_data[sheet]:
                    if count%2==0:
                        with col1:
                            
                            add_radio = st.radio(
                                q.replace(". ","."),
                                options,
                                horizontal = True
                            )
                    else:
                        with col2:
                            
                            add_radio = st.radio(
                                q.replace(". ","."),
                                options,
                                horizontal = True
                            )
                    
                    # Gather all results
                    radio_result.append(add_radio)
                    count+=1
                    
                    
                    
                
                
                #Click the save button to local csv file
                if st.button("Save"):
                    #sheet_name_list.append(sheet)
                    #role_list.append(p)
                    #radio_result_list.append(radio_result)
                    end_time = time.time()
                    now = datetime.datetime.now()
                    submit_time = now.strftime("%H:%M:%S")
                    fill_duration = round((end_time - st.session_state.time), 3)
                    st.session_state.time = 0
                    
                    st.write("You spent " + str(fill_duration) + " mints filling this sheet")
                    with open(company_name +"_original_data.csv", mode='a') as file:
                        writer = csv.writer(file)
                        writer.writerow([sheet, p, current_date, submit_time, fill_duration, radio_result])
                    
                        #result_data = pd.DataFrame("Sheet": sheet_name_list, "Position": role_list, "Results": radio_result_list})
                        #result_data.to_csv("streamlit_dataset.csv")
                        st.success("Data saved!")
           
     
    

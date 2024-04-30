from src.services.er_visit import read_er_visit
import streamlit as st
import jsonpickle
import asyncio
from src.datasources.prisma import prisma
from langchain_core.messages import ChatMessage
async def main():
    # initiate db
    await prisma.connect()
    
    # change the id later depending on session
    er_visit = await read_er_visit(id="test")
    er_messages = er_visit.ChatMessages

    parsed_er_messages = []
    for message in er_messages:
        parsed_message = jsonpickle.decode(message.raw)
        print("role", parsed_message.type)
        print("content", parsed_message.content)
        parsed_er_messages.append({
            "role": parsed_message.type,
            "content": parsed_message.content
        })
    if "messages" not in st.session_state:
        st.session_state.messages = parsed_er_messages

    st.title('AI Triage Care')
    tabs = st.tabs(['Patient Data Entry', 'Consult With Medic'])

    with tabs[0]:

        st.header("Patient Data Entry Form")
        col1, col2 = st.columns(2)

        with col1:
            sex = st.selectbox("Sex", ["Female", "Male"])
            age = st.number_input("Age", min_value=18, max_value=90)
            arrival_mode = st.number_input("Arrival Mode", min_value=1, max_value=8, help="Type of transportation to the hospital")
            injury = st.checkbox("Injury", help="Whether the patient is injured or not")

        with col2:
            chief_complain = st.selectbox("Chief Complaint", ['pain', 'headache', 'nausea', 'trauma'], help="The patient's complaint")
            mental = st.selectbox("Mental Status", ['Alert', 'Verbose Response', 'Pain Response', 'Unresponsive'], help="The mental state of the patient")
            pain = st.checkbox("Pain", help="Whether the patient has pain")
            nrs_pain = st.slider("NRS Pain Score", 0, 10, 0, help="Nurse's assessment of pain for the patient")

        st.divider()
        col3, col4 = st.columns(2)

        with col3:
            sbp = st.number_input("Systolic Blood Pressure (SBP)", min_value=80, max_value=200)
            dbp = st.number_input("Diastolic Blood Pressure (DBP)", min_value=50, max_value=120)

        with col4:
            hr = st.number_input("Heart Rate (HR)", min_value=45, max_value=120)
            rr = st.number_input("Respiratory Rate (RR)", min_value=10, max_value=30)
            bt = st.number_input("Body Temperature (BT)", min_value=35, max_value=39)

        if st.button('Submit'):
            data = {
                "Sex": sex,
                "Age": age,
                "Arrival Mode": arrival_mode,
                "Injury": injury,
                "Chief Complaint": chief_complain,
                "Mental Status": mental,
                "Pain": pain,
                "NRS Pain Score": nrs_pain,
                "SBP": sbp,
                "DBP": dbp,
                "HR": hr,
                "RR": rr,
                "BT": bt
            }
            
            st.write("Submitted Data:")
            st.json(data)


    with tabs[1]:

        st.header("Consult With Medic")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        query_holder = st.empty()
        response_holder = st.empty()

        if prompt := st.chat_input("What's your concern?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with query_holder.chat_message("user"):
                st.write(prompt)

            with response_holder.chat_message("assistant"):
                response = "I can help you with that. Please wait a moment..."
                st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    await prisma.disconnect()
asyncio.run(main())
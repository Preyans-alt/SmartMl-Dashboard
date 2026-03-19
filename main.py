import streamlit as st
from file_upload import upload_file
from FileDatabase import MyDataMethods


dataBase = MyDataMethods()

st.title("File Transfer 📩")
st.write("Send or receive any file from anywhere!")
st.markdown("---")

st.sidebar.header('Select Option:- ')

option = st.sidebar.selectbox(
    "Select Option:",
    ["Send File ⬆️", "Receive File ⬇️"]
)


# ---------------- SEND ----------------
if option == "Send File ⬆️":
    st.header("Send File")

    # to uplode file
    file_uploded = st.file_uploader("Upload your file")

    if file_uploded:
        # to send and store file to cloudnary server---
        file_data = upload_file(file_uploded)
        st.success("File uploaded successfully!")
        # to store file url in db------
        file_code = dataBase.upload_file(file_data)

        st.write("Filename:", file_uploded.name)

        # to print file code that generate in database code file---
        st.info(f'Your File Code:- {file_code}')

# ---------------- RECEIVE ----------------
elif option == "Receive File ⬇️":
    st.header("Receive File")

    file_code = st.text_input("Enter File Code...")

    if file_code:
        if dataBase.validate_file_code(file_code):
            st.success('Download File ⬇️')
            st.info(dataBase.get_file_url(file_code))
        else:
            st.error("InValid code ❌")


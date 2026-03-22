import psycopg2
import random
import string
from dotenv import load_dotenv
# import streamlit as st
import os

load_dotenv()
class MyDataMethods:

    def dataBase(self):
        return psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            dbname=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT'),
            sslmode="require"
        )

    
    def upload_file(self,file_url):
        db = self.dataBase()
        # st.write(st.secrets)
        cursor = db.cursor()

        file_code = ''.join(random.choices(string.digits, k=10))
        
        query = 'INSERT INTO FILES (FILE_CODE,FILE_URL) VALUES (%s,%s)'
        cursor.execute(query,(file_code,file_url))

        db.commit()
        cursor.close()
        db.close()
        return file_code

    def validate_file_code(self,file_code):
        db = self.dataBase()
        cursor = db.cursor()

        query = "select FILE_CODE from FILES"

        cursor.execute(query)
        file_code_list = cursor.fetchall()

        cursor.close()
        db.close()
        
        
        if (file_code,) in file_code_list:
            return True
        else:
            return False
    
    def get_file_url(self,file_code):
        db = self.dataBase()
        cursor = db.cursor()

        query = "select FILE_URL from FILES WHERE FILE_CODE=%s"

        cursor.execute(query,(file_code,))
        file_url = cursor.fetchone()

        cursor.close()
        db.close()

        return file_url[0]
my = MyDataMethods()
# print(my.validate_file_code(5456454566))
my.upload_file('sdjflkj dfjiew kdsjfmn')
import psycopg2
import psycopg2.extras
import random
import string

class MyDataMethods:

    def dataBase(self):
        return psycopg2.connect(
            host='db.kduozkvvpoqgrysdkfnr.supabase.co',
            user='postgres',
            password='@2006Prey@n$#',
            dbname='postgres',
            port='5432'
        )
    
    def upload_file(self,file_url):
        db = self.dataBase()
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

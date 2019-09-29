__author__ = "Joshua Akangah"

import sqlite3
import time
import string
import random
import datetime

# id functions
def gen_id(typeOf):
    if typeOf == 1:
        chars = string.ascii_uppercase+string.digits
        return 'PAT-'+''.join(random.choice(chars) for _ in range(6))
    elif typeOf == 2:
        chars = string.digits+string.ascii_lowercase
        return 'RCD-'+''.join(random.choice(chars) for _ in range(6))
    elif typeOf == 3:
        chars = string.digits
        return 'BAT-'+''.join(random.choice(chars) for _ in range(6))
    elif typeOf == 4:
        chars = string.ascii_uppercase+string.ascii_lowercase
        return 'STF-'+''.join(random.choice(chars) for _ in range(3))
    elif typeOf == 5:
        chars = string.digits
        return 'APT-'+''.join(random.choice(chars) for _ in range(3))
    elif typeOf == 6:
        chars = string.digits+string.ascii_lowercase
        return 'PRS-'+''.join(random.choice(chars) for _ in range(3))
    elif typeOf == 7:
        chars = string.digits+string.ascii_lowercase
        return ''.join(random.choice(chars) for _ in range(6))
    return None

def gen_session_id():
    chars = string.ascii_uppercase+string.ascii_lowercase+string.digits
    return ''.join(random.choice(chars) for _ in range(6))

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    try:
        with open(filename, 'wb') as file:
            file.write(data)
        return True
    except:
        return False

class Database:
    def __init__(self, name='clinic.db'):
        self.name = name
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute("PRAGMA foreign_keys = ON")

            self.cursor.execute(
                """
                CREATE TABLE PATIENTS
                (ID CHAR(10) PRIMARY KEY,
                F_NAME TEXT NOT NULL,
                L_NAME TEXT NOT NULL,
                AGE INTEGER NOT NULL,
                SEX TEXT NOT NULL,
                ADDRESS TEXT NOT NULL)
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE MEDICATION
                (BATCH_NO CHAR(10) PRIMARY KEY,
                CATEGORY TEXT NOT NULL,
                NAME TEXT NOT NULL,
                EXPIRY_DATE TIMESTAMP NOT NULL,
                IN_STOCK INTEGER NOT NULL)
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE DEPARTMENT
                (ID CHAR(7) PRIMARY KEY,
                NAME TEXT NOT NULL)
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE STAFF
                (ID CHAR(7) PRIMARY KEY,
                F_NAME TEXT NOT NULL,
                L_NAME TEXT NOT NULL,
                DEPT_ID TEXT NOT NULL,
                TITLE TEXT NOT NULL,
                FOREIGN KEY(DEPT_ID) REFERENCES DEPARTMENT(ID) ON DELETE CASCADE)
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE APPOINTMENTS
                (ID CHAR(7) PRIMARY KEY,
                DATEOF TIMESTAMP NOT NULL,
                STAFF TEXT NOT NULL,
                PATIENT TEXT NOT NULL,
                TIMEOF TEXT NOT NULL,
                FOREIGN KEY(PATIENT) REFERENCES PATIENTS(ID) ON DELETE CASCADE,
                FOREIGN KEY(STAFF) REFERENCES STAFF(ID) ON DELETE CASCADE)
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE STAY
                (WARD CHAR(3) NOT NULL,
                BED INTEGER NOT NULL,
                DATE_IN TIMESTAMP NOT NULL,
                DATE_OUT TIMESTAMP NOT NULL,
                PATIENT TEXT NOT NULL,
                FOREIGN KEY(PATIENT) REFERENCES PATIENTS(ID) ON DELETE CASCADE
                )
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE PRESCRIPTIONS
                (ID CHAR(7) NOT NULL,
                BY TEXT NOT NULL,
                FOR TEXT NOT NULL,
                DATEOF TIMESTAMP NOT NULL,
                MEDICINE_NAME TEXT NOT NULL,
                FOREIGN KEY(BY) REFERENCES STAFF(ID) ON DELETE CASCADE,
                FOREIGN KEY(FOR) REFERENCES PATIENTS(ID) ON DELETE CASCADE)
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE AUTH
                (USERNAME TEXT NOT NULL,
                PASSWORD TEXT NOT NULL,
                FOREIGN KEY(USERNAME) REFERENCES STAFF(ID) ON DELETE CASCADE)
                """
            )

            # self.connection.commit()

        except sqlite3.OperationalError as e:
            print(e)

        finally:
            self.connection.commit()

            if self.connection:
                self.connection.close()

    def add_patient(self, f_name, l_name, age, sex, address, id):
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()

        try:
            EXEC = """
            INSERT INTO PATIENTS
            (ID, F_NAME, L_NAME, AGE, SEX, ADDRESS)
            VALUES
            (?, ?, ?, ?, ?, ?)

            """
            # generated_pat_id = gen_id(1)

            self.cursor.execute(f"SELECT * FROM PATIENTS WHERE ID='{id}'")

            try:
                # to catch a typeError if the id does not exist
                while len(self.cursor.fetchone()) != 0:
                    generated_id = gen_id(1)

                    self.cursor.execute(f"SELECT * FROM PATIENTS WHERE ID='{id}'")

            except TypeError:
                # meaning id does not exist
                pass

            DATA = (id, f_name, l_name, age, sex, address)

            self.cursor.execute(EXEC, DATA)

            # EXEC = """
            # INSERT INTO PATIENT_RECORDS
            # (ID, CREATED, FILE, OWNER)
            # VALUES
            # (?, ?, ?, ?)
            # """

            # generated_id = gen_id(2)

            # DATA = (generated_id, datetime.datetime.today().date(), record, generated_pat_id)

            # self.cursor.execute(f"SELECT OWNER FROM PATIENT_RECORDS WHERE OWNER='{generated_pat_id}'")

            # try:
            #     if len(self.cursor.fetchall()) != 0:
            #         return
            #     else:
            #         self.cursor.execute(EXEC, DATA)

            # except TypeError:
            #     pass

            return True

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()

            if self.connection:
                self.connection.close()

    def update_patient_record(self, pat_id, file):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            EXEC = """
            UPDATE PATIENT_RECORDS SET FILE=? WHERE OWNER=?
            """

            DATA = (file, pat_id)

            self.cursor.execute(EXEC, DATA)

            return True

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()

            if self.connection:
                self.connection.close()

    def add_medication(self, category, name, expiry, stock, bat):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            EXEC = """
            INSERT INTO MEDICATION
            (BATCH_NO, CATEGORY, NAME, EXPIRY_DATE, IN_STOCK)
            VALUES
            (?, ?, ?, ?, ?)
            """

            DATA = (bat, category, name, expiry, stock)

            self.cursor.execute(EXEC, DATA)

            return True

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()

            if self.connection:
                self.connection.close()

    def add_staff(self, f_name, l_name, dept_id, title, staff_id):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            EXEC = """
            INSERT INTO STAFF
            (ID, F_NAME, L_NAME, DEPT_ID, TITLE)
            VALUES
            (?, ?, ?, ?, ?)
            """

            DATA = (staff_id, f_name, l_name, dept_id, title)

            self.cursor.execute(EXEC, DATA)

            return True

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()

            if self.connection:
                self.connection.close()

    def add_appointment(self, patient, staff, date, time):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            EXEC = """
            INSERT INTO APPOINTMENTS
            (ID, DATEOF, PATIENT, STAFF, TIMEOF)
            VALUES
            (?, ?, ?, ?, ?)
            """

            DATA = (gen_id(5), date, patient, staff, time)

            self.cursor.execute(EXEC, DATA)

            return True

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()

            if self.connection:
                self.connection.close()


    def add_stay(self, ward, bed, date_in, date_out, patient):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            EXEC = """
            INSERT INTO STAY
            (WARD, BED, DATE_IN, DATE_OUT, PATIENT)
            VALUES
            (?, ?, ?, ?, ?)
            """

            DATA = (ward, bed, date_in, date_out, patient)

            self.cursor.execute(EXEC, DATA)

            return True

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()

            if self.connection:
                self.connection.close()

    def add_prescription(self, patient, staff, medicine_name):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            EXEC = """
            INSERT INTO PRESCRIPTIONS
            (ID, BY, FOR, DATEOF, MEDICINE_NAME)
            VALUES
            (?, ?, ?, ?, ?)
            """

            DATA = (gen_id(6), staff, patient, datetime.datetime.today().date(), medicine_name)

            self.cursor.execute(EXEC, DATA)

            return True

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()

            if self.connection:
                self.connection.close()

    def add_auth(self, username):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            pwd = gen_id(7)

            EXEC = """
                INSERT INTO AUTH (USERNAME, PASSWORD)
                VALUES (?, ?)
            """

            DATA = (username, pwd)

            self.cursor.execute(EXEC, DATA)

            return True

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()

            if self.connection:
                self.connection.close()


    def retrieve_patient(self, id, include_all=False):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            if include_all:
                self.cursor.execute("SELECT * FROM PATIENTS")

                return self.cursor.fetchall()

            self.cursor.execute(
                f"""
                SELECT * FROM PATIENTS WHERE ID='{id}'
                """
            )

            return self.cursor.fetchone()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_staff(self, stf_id):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM STAFF WHERE ID='{stf_id}'
                """
            )

            return self.cursor.fetchone()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_date_count(self, date):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT COUNT(DATEOF) FROM APPOINTMENTS WHERE DATEOF='{date}' ORDER BY DATEOF ASC
                """
            )

            return self.cursor.fetchone()[0]

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_auth_pwd(self, username):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT PASSWORD FROM AUTH WHERE USERNAME='{username}'
                """
            )

            return self.cursor.fetchone()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_pres_count(self, date):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT COUNT(DATEOF) FROM PRESCRIPTIONS WHERE DATEOF='{date}' ORDER BY DATEOF ASC
                """
            )

            return self.cursor.fetchone()[0]

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_only_staff(self):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT ID, TITLE, F_NAME, L_NAME FROM STAFF
                """
            )

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_staff_info(self, stf_id):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            selected_info = []

            #selecting all appointments
            self.cursor.execute(
                f"""
                SELECT ID, DATEOF, PATIENT, TIMEOF FROM APPOINTMENTS WHERE STAFF='{stf_id}'
                """
            )

            selected_info.append(self.cursor.fetchall())

            self.cursor.execute(
                f"""
                SELECT ID, FOR, DATEOF, MEDICINE_NAME FROM PRESCRIPTIONS WHERE BY='{stf_id}'
                """
            )

            selected_info.append(self.cursor.fetchall())

            return selected_info

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_department(self):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute("SELECT * FROM DEPARTMENT")

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_patient_info(self, id):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            selected_info = []

            #selecting all appointments
            self.cursor.execute(
                f"""
                SELECT PATIENTS.ID, APPOINTMENTS.STAFF, APPOINTMENTS.ID, APPOINTMENTS.DATEOF
                FROM PATIENTS INNER JOIN APPOINTMENTS ON PATIENTS.ID = APPOINTMENTS.PATIENT WHERE PATIENTS.ID='{id}'
                """
            )

            selected_info.append(self.cursor.fetchall())

            #selecting all hospital stays
            # Ward  Bed     Date In     Date Out
            self.cursor.execute(
                f"""
                SELECT PATIENTS.ID, STAY.WARD, STAY.BED, STAY.DATE_IN, STAY.DATE_OUT
                FROM PATIENTS INNER JOIN STAY ON PATIENTS.ID = STAY.PATIENT WHERE PATIENTS.ID='{id}'
                """
            )

            selected_info.append(self.cursor.fetchall())

            # selecting all prescriptions
            # Prescription  Batch No    Name    Prescribed by   Dated
            self.cursor.execute(
                f"""
                SELECT PATIENTS.ID, PRESCRIPTIONS.ID,  PRESCRIPTIONS.MEDICINE_NAME, PRESCRIPTIONS.BY, PRESCRIPTIONS.DATEOF
                FROM PATIENTS INNER JOIN PRESCRIPTIONS ON PATIENTS.ID=PRESCRIPTIONS.FOR WHERE PATIENTS.ID='{id}'
                """
            )

            selected_info.append(self.cursor.fetchall())

            return selected_info

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_patient_record(self, id):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM PATIENT_RECORDS WHERE ID='{id}'
                """
            )

            return self.cursor.fetchone()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_medication(self):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute("SELECT * FROM MEDICATION")

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def check_stock(self, batch):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"SELECT IN_STOCK FROM MEDICATION WHERE BATCH_NO='{batch}'")

            updated = int(self.cursor.fetchone()[0]) - 1

            self.cursor.execute(
                f"""
                UPDATE MEDICATION SET IN_STOCK='{updated}' WHERE BATCH_NO='{batch}'
                """
            )

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()
            if self.connection:
                self.connection.close()

    def update_stock(self, batch):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"SELECT IN_STOCK FROM MEDICATION WHERE BATCH_NO='{batch}'")

            updated = int(self.cursor.fetchone()[0])

            if updated > 0:
                updated -= 1
            else:
                return 'empty'

            self.cursor.execute(
                f"""
                UPDATE MEDICATION SET IN_STOCK='{updated}' WHERE BATCH_NO='{batch}'
                """
            )

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()
            if self.connection:
                self.connection.close()

    def retrieve_len_staff(self):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute("SELECT count(*) FROM STAFF")

            return self.cursor.fetchone()[0]

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_staff(self, id, by_dept=False, dept_id=None):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            if by_dept:
                self.cursor.execute(
                    f"""
                    SELECT STAFF FROM DEPARTMENT WHERE ID='{dept_id}'
                    """
                )

                selected_ids = self.cursor.fetchone()[0].split('/')
                selected_ids.pop(-1)
                staff = []

                for _ in selected_ids:
                    self.cursor.execute(
                        f"""
                        SELECT * FROM STAFF WHERE ID='{_}'
                        """
                    )

                    staff.append(self.cursor.fetchone())

                return staff

            self.cursor.execute(
                f"""
                SELECT * FROM STAFF WHERE ID='{id}'
                """
            )

            return self.cursor.fetchone()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_appointment(self, id, select_all):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            if select_all:
                self.cursor.execute("SELECT * FROM APPOINTMENTS ORDER BY DATEOF DESC")

                return self.cursor.fetchall()

            self.cursor.execute(
                f"""
                SELECT * FROM APPOINTMENTS WHERE ID='{id}'
                """
            )

            return self.cursor.fetchone()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_dept(self, dept_id):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"SELECT * FROM DEPARTMENT WHERE ID='{dept_id}'")

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_dept_staff(self, dept_id):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"SELECT * FROM STAFF WHERE DEPT_ID='{dept_id}'")

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def retrieve_stay(self):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute("SELECT * FROM STAY")

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def delete_patient(self, pat_id):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"DELETE FROM PATIENTS WHERE ID='{pat_id}'")

            return True

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.commit()

            if self.connection:
                self.connection.close()

    def search_patient(self, query):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT ID, F_NAME, L_NAME, AGE, SEX, ADDRESS, PICTURE
                FROM PATIENTS WHERE ID LIKE '%{query}%' OR F_NAME LIKE '%{query}%'
                """
            )

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def search_medication(self, query):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT *
                FROM MEDICATION WHERE BATCH_NO LIKE '%{query}%' OR NAME LIKE '%{query}%'
                """
            )

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def search_patient_record(self, query):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM PATIENT_RECORDS WHERE OWNER LIKE '%{query}%' OR ID LIKE '%{query}%'
                """
            )

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def search_medication(self, query):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM MEDICATION WHERE NAME LIKE '%{query}%' OR BATCH_NO LIKE '%{query}%' OR CATEGORY LIKE '%{query}%'
                """
            )

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def get_med_cat(self, category):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM MEDICATION WHERE CATEGORY='{category}'
                """
            )

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def search_staff(self, query):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM STAFF WHERE F_NAME LIKE '%{query}%' OR L_NAME LIKE '%{query}%' OR ID LIKE '%{query}%'
                """
            )

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def find_appointment(self, query):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM APPOINTMENTS WHERE ID LIKE '%{query}%' OR STAFF LIKE '%{query}%' OR PATIENT LIKE '%{query}%'
                """
            )

            return self.cursor.fetchall()

        except sqlite3.OperationalError as e:
            return e

        finally:
            self.connection.close()

    def validate_batch(self, batch_no):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM MEDICATION WHERE BATCH_NO='{batch_no}'
                """
            )

            try:
                a = len(self.cursor.fetchone())
                return True

            except:
                return False

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def validate_admin(self, username):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM AUTH WHERE USERNAME='{username}' AND PASSWORD='1234'
                """
            )

            try:
                a = len(self.cursor.fetchone())
                return True

            except:
                return False

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def validate_login(self, username, password):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM AUTH WHERE USERNAME='{username}' AND PASSWORD='{password}'
                """
            )

            try:
                a = len(self.cursor.fetchone())
                return True

            except:
                return False

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def select_validate_login(self, username):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT STAFF.TITLE, STAFF.F_NAME, STAFF.L_NAME, AUTH.USERNAME
                FROM STAFF INNER JOIN AUTH ON STAFF.ID=AUTH.USERNAME WHERE STAFF.ID='{username}'
                """
            )

            try:
                return self.cursor.fetchone()

            except:
                return False

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def validate_patient(self, id):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM PATIENTS WHERE ID='{id}'
                """
            )

            try:
                a = len(self.cursor.fetchone())

                return True

            except:
                return False

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def validate_staff(self, staff_id):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT * FROM STAFF WHERE ID='{staff_id}'
                """
            )

            try:
                a = len(self.cursor.fetchone())

                return True

            except:
                return False

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def count_medicines(self, cat):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT COUNT(*) FROM MEDICATION WHERE CATEGORY='{cat}'
                """
            )

            try:
                return self.cursor.fetchone()[0]

            except:
                return False

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def count_medicine_cat(self, cat):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT CATEGORY, COUNT(*) FROM MEDICATION WHERE CATEGORY='{cat}'
                """
            )

            try:
                return self.cursor.fetchall()

            except:
                return False

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

    def select_category(self):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                f"""
                SELECT CATEGORY FROM MEDICATION
                """
            )

            try:
                return self.cursor.fetchall()

            except:
                return False

        except sqlite3.OperationalError as e:
            return e

        finally:
            if self.connection:
                self.connection.close()

#
#a = Database()
#print(a.validate_login('admin', 1234))
# # for _ in range(10):
# #     print(a.add_patient("Stacy", "Aryee", 16, "F", "Sakumono estates", 'mama.png', 'lol'))
# # print(a.add_patient("Darius", "Osam", 19, "M", "Dansoman estates", 'mama.png'))
# # print(a.add_patient("Hillary", "Essuman", 24, "F", "Airport estates", 'mama.png'))
# #print(a.add_patient("Samuel", "Mensah", 12, "M", "Accra City estates", 'mama.png', 'b.png'))

# # print(a.retrieve_patient('PAT-V80UPO'))


# #print(a.add_patient_record(datetime.datetime.today().date(), 'mama.png', 'PAT-O8YCV5'))

# # for _ in a.retrieve_patient(None, True):
# #     # print(_[0
# #     print(a.add_patient_record(datetime.datetime.today().date(), convertToBinaryData('micro.pdf'), _[0]))

# #print(a.add_patient_record(datetime.datetime.today().date(), convertToBinaryData('micro.pdf'), ''))

# #print(a.delete_patient('PAT-O8YCV5'))
# #print(a.add_staff("leslie", "akangah", "lol"))
# #print(a.add_appointment('PAT-SJAC41', 'STF-raP'))

# # print(a.retrieve_patient_info('PAT-SJAC41'))

# # print(a.add_prescription('PAT-SJAC41', 'STF-raP', 'Paracetamol'))

# #print(a.validate_login('admin', '1234'))

# # PAT-O67SVK
# # a = Database()
# # # # print(a.add_medication('21','234','234',234))

# # # # a.add_stay('M3', 5, 9/1/19, 23/2/19, 'PAT-O67SVK')

# # # # a.add_prescription('PAT-O67SVK', 'STF-324', 'LONART')

# # # # a.add_appointment('PAT-O67SVK', 'safsdf')
# # # # print(a.retrieve_appointment(None, True))

# # # print(a.search_medication('malaria'))
# # print(a.update_stock('BAT-951576'))

# #print(a.add_staff('f_name', 'l_name', 'DPT-EME', 'Dr.'))

# print(a.validate_login('admin', 1234))

# a = Database()
# print(a.retrieve_date_count('2019-10-04'))
# print(a.retrieve_dept_staff('DPT-ANA'))
# # print(a.retrieve_staff('STF-YUR'))
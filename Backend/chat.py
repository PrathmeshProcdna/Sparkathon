from groq import Groq
import sqlite3
import pandas as pd

class Chat:
    def __init__(self):
        self.client = Groq(
            api_key='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'
        )

        self.client_rephrase = Groq(
            api_key='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'
        )

    def get_response(self,query):
        prompt = f"""
                schema = Given the 'hacka' table with Sales_Market_Rep_ID as the primary key and with the following column descriptions :
                    --HCP_ID:INT(nullable = FALSE) :HCP(Health Care Practitioner)/NPI IDs. This column help us to identify each HCP uniquely
                    --HCP_first_name:STRING(nullable = FALSE) :First name of the HCP
                    --HCP_Middle_Name:STRING(nullable = TRUE) :Middle name of the HCP
                    --HCP_Last_name:STRING(nullable = FALSE) :Last name of the HCP
                    --HCP_Full_Name:STRING(nullable = FALSE) :Full name of the HCP
                    --HCP_Medical_degree:STRING(nullable = FALSE) :Medical degree of HCP
                    --HCP_Gender:STRING(nullable = FALSE) :Gender of HCP
                    --HCP_Specialty:STRING(nullable = FALSE) :Specialty of HCP
                    --hcp_status:STRING(nullable = FALSE) :Activity status of HCP.  A = Active, I = Inactive, R = Retired, D = Dead
                    --HCP_Prefix:STRING(nullable = TRUE) :Title of HCP example = 'DR' means doctor
                    --HCP_Email_ID:STRING(nullable = TRUE) :Email ID of HCP
                    --HCP_Decile:INT(nullable = TRUE) :Decile of HCP 10 refers to best and 1 refers to poor
                    --HCP_ZIP:INT(nullable = TRUE) :ZIP of the HCP
                    --HCP_Locality:STRING(nullable = FALSE) :Locality of the HCP
                    --HCP_State:STRING(nullable = TRUE) :State of the HCP
                    --HCP_Primary_Account:STRING(nullable = TRUE) :Primary affiliation of the HCP
                    --HCP_Territory:STRING(nullable = TRUE) :Territory for the HCP it will be particular to each Rep
                    --HCP_Region:STRING(nullable = TRUE) :Region for the HCP it will be particular to each Rep
                    --Sales_Market_Rep_ID:INT(nullable = TRUE) :ID for the Rep
                    --Sales_Market_Rep_Name:STRING(nullable = TRUE) :Name of the market rep
                    --HCP_data_update_Year:INT(nullable = FALSE) :Year of the data update
                    Note: 1) HCP can also be read as "Health care Prectitioner", "Physician", "General Practitioner (GP)", "Primary Care Provider (PCP)", "Specialist", "Nurse Practitioner (NP)", "Physician Assistant (PA)", "Clinician", "Surgeon", "Medical Practitioner", "Healthcare Professional", "Consultant", "Therapist", "Attending Physician", "Doctor", "Medical Provider", "Specialty Care Provider", "Dentist", "Healthcare Practitioner"
                          2)Market Rep can also be identified as "Sales Representative (Sales Rep)", "Pharmaceutical Sales Representative", "Medical Sales Representative", "Territory Manager", "Field Sales Representative", "Business Development Manager (BDM)", "Account Manager", "Key Account Manager (KAM)", "Healthcare Sales Representative", "Medical Device Sales Representative", " Clinical Sales Representative", "Specialty Sales Representative", "Market Access Manager", "Hospital Sales Representative", "Field Marketing Specialist", "Regional Sales Manager", "Sales Consultant", "Account Executive", "Commercial Representative", "Product Specialist", "Territory Sales Executive"
                          3)Map   me, mine, I, my  with the name of Sales_Market_Rep_Name Grace Bennett.

                    query_prompts =  1.When generating SQL queries, always ensure that DISTINCT is applied for any selection of records or entities that need to be counted distinctly.
                                    2.Do not include any warnings, just produce the SQL query as the output. Any input validation or potential issues should be handled internally without notifying the user.
                                    3.For all string match conditions within a WHERE clause, use the LIKE operator with wildcard % at both the beginning and end of the string to allow for flexible matching.
                                    4.Provide the SQL query directly, not in a string format (i.e., no need for quotation marks or additional formatting elements), so it can be executed as is.
                Question = f{query}
                """
        
        response = self.client.chat.completions.create(
            messages=[
                {'role':'system','content':'You are working as a nlp to sql converter only so Please give a sql query according to the users question'},
                {'role':'user','content':prompt}
            ],
            model="llama-3.2-90b-text-preview"
        )
        sql_query = response.choices[0].message.content
        return sql_query 
    
    def exe_query(self,query):
        conn = sqlite3.connect('./hacka.db')
        sql_query = self.get_response(query)
        res = pd.read_sql_query(sql_query,conn)
        # -- Rephrase -- #
        response = self.client_rephrase.chat.completions.create(
            messages=[
                {'role':'system','content':'you are a rephraser agent which rephrase the sql output in the normal human text and show to user'},
                {'role':'user','content':str(res)}
            ],
            model = "llama-3.2-90b-text-preview"
        )
        ans = response.choices[0].message.content
        return ans 
    
        
    
# obj = Chat()
# query = "what is the name of rep id 47239?"
# ans = obj.exe_query(query)
# print(ans)

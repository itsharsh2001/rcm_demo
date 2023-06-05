from http.server import BaseHTTPRequestHandler, HTTPServer
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file

import json
import pandas as pd
import os
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz, process

app = Flask(__name__)
CORS(app)

current_directory = os.getcwd()
# parent_directory = os.path.dirname(os.path.dirname(current_directory))
# target_folder = 'INPUT_EXCEL_FILES'
# Construct the relative path
# relative_path = os.path.join(parent_directory, target_folder)

# Change the current working directory to the target folder
# os.chdir(relative_path)
os.chdir(current_directory)


# print(parent_directory)
# os.chdir("c:/Data/D Drive Maan Le Ise/Work/RCM/RCM Client Ki aur se aye data ko check kro/rcm_demo/INPUT_EXCEL_FILES/")



@app.route('/api/process-files', methods=['POST'])
def process_files():
    data = request.get_json()

    # with open('output.json','w') as json_file:
    #     json.dump(data, json_file)

    dataframes = {}

    for id, json_data in data.items():
        # Convert JSON data to pandas DataFrame
        # print(type(json_data))
        dataframe = pd.DataFrame(json.loads(json_data))
        dataframes[id] = dataframe
        print(id)
        # print(dataframe.columns)
        # print("bvhjvgkjlg")
        # print(dataframes[id])
    

    # column_names = [col.strip() for col in dataframes["Transactions"].columns]
    # print(column_names)
    # print(column_names[0])

    # print(dataframes[0])
    # print(dataframes['Transactions'][column_names[0]])
    # for id, json_data in data.items():
    #     if(id=='Transactions'):
    #         df = pd.read_json(json_data)

    #         # Output Excel file path
    #         output_path = 'output.xlsx'

    #         # Save DataFrame to Excel
    #         df.to_excel(output_path, index=False)

    #         # Read Excel file into DataFrame
    #         df_from_excel = pd.ExcelFile(output_path)
    #         ans=df_from_excel.parse('Sheet1')
    #         # Delete Excel file
    #         print(ans)
    #         os.remove(output_path)


    # print(ans)
    
    Transactions = dataframes['Transactions']
    Directors = dataframes['Directors']
    Client_Details = dataframes['ClientDetails']
    Vendor_Details = dataframes['VendorDetails']
    KeywordMaster = dataframes['KeywordMaster']
    SACMaster = dataframes['SACMaster']
    Testing = dataframes['Testing']

    a=[Transactions,Directors,Client_Details,Vendor_Details,KeywordMaster,SACMaster,Testing]
    

    for i in range(len(a)):
        column_names = [col.strip() for col in a[i].columns]
        a[i].columns = column_names



    column_names = [col.strip() for col in Transactions.columns]
    # Transactions.rename(columns = {Transactions.columns : column_names}, inplace = True)
    Transactions.columns = column_names
    print(Transactions.columns)
    print("alooo")
    # print(column_names)

    # Access the 'Invoice Description' column
    # invoice_description = Transactions[column_names]['Invoice Description']
    # Transactions = Transactions.parse()
    # print(invoice_description)

    # Process the dataframes as needed
    # for id, dataframe in dataframes.items():
        # Perform operations on the dataframe
        # ...

        # Example: Print the dataframe
        # print(f"DataFrame for ID {id}:")
        # print(dataframe)
        # print()

    # print(Transactions)
    # print(Directors)
    # print(Client_Details)
    # print(Vendor_Details)
    # print(KeywordMaster)
    # print(SACMaster)
    # print(Testing)


#     file1=file_paths[0]
#     file2=file_paths[1]
#     file3=file_paths[2]
#     file4=file_paths[3]
#     file5=file_paths[4]
#     file6=file_paths[5]
#     file7=file_paths[6]
    
    
#     print(file1,file2,file3,file4,file5,file6,file7)
    

    # data1 = pd.ExcelFile(relative_path)
#     data2 = pd.ExcelFile(file2)
#     data3 = pd.ExcelFile(file3)
#     data4 = pd.ExcelFile(file4)
#     data5 = pd.ExcelFile(file5)
#     data6 = pd.ExcelFile(file6)
#     data7 = pd.ExcelFile(file7)


#     #Importing sheet names in dataframes
#     Client_Details = data4.parse("Sheet1") 
#     Vendor_Details = data5.parse("Sheet1")
    # Transactions1 = data1.parse("Sheet1")
#     Directors = data6.parse("Sheet1")
    # print(Transactions==Transactions1)
#     KeywordMaster = data2.parse("Sheet1")
#     SACMaster = data3.parse("Sheet1")


    # Transactions.to_excel('updated_transactions.xlsx', index=False)

        
    #Is an Insurance agent?
    Insurance_Agents = []
    for index, row in Vendor_Details.iterrows():
        if "Yes" in str(row["Is an Insurance Agent"]):
            Insurance_Agents.append(row["Name"])
        else:
            pass
    # print(Insurance_Agents)
    #Is an Recovery agent?
    Recovery_Agents = []
    for index, row in Vendor_Details.iterrows():
        if "Yes" in str(row["Is a Recovery Agent"]):
            Recovery_Agents.append(row["Name"])
        else:
            pass

    # In[ ]:

    #Step1: Service provided by an Insurance Agent to Insurance Company
    if "Yes" in str(Client_Details["Is engaged in Insurance Business?"]):
        mask1 = Transactions["Name"].isin(Insurance_Agents)
        if mask1.any():
            Transactions.loc[mask1, "Is RCM Applicable"] = "Yes"
            Transactions.loc[mask1, "RCM Reason"] = "Service provided by insurance agent"
            Transactions.loc[mask1, "Main Conditions True Or False"] = "Yes"
            Transactions.loc[mask1, "Main Condition"] = "Service provided by insurance agent"
        else:
            pass
    

    # In[ ]:

    #Step2: Service provided by a recovery agent to a BANK/FI or NBFC
    if "Yes" in str(Client_Details["Is a Bank/NBFC/FI?"]):
        mask2 = Transactions["Name"].isin(Recovery_Agents)
        if mask2.any():
            Transactions.loc[mask2, "Is RCM Applicable"] = "Yes"
            Transactions.loc[mask2, "RCM Reason"] = "Service provided by recovery agent"
            Transactions.loc[mask2, "Main Conditions True Or False"] = "Yes"
            Transactions.loc[mask2, "Main Condition"] = "Service provided by recovery agent"
        else:
            pass

    # In[ ]:


    #Step3: Check and update for "Good mentioned u/n/4/2017"

    mask3 = Transactions['Sac Codes'].astype(str).str.startswith(('801', '14049010', '2401', '5004', '5005', '5006'))
    #mask3 = SACMaster['SAC Code'].astype(str).str.startswith(('801', '14049010', '2401', '5004', '5005', '5006'))
    #print(mask3)
    filtered_df = Transactions[mask3]

    Transactions.loc[mask3, "Is RCM Applicable"] = "Yes"
    Transactions.loc[mask3, "RCM Reason"] = "Good mentioned u/n/4/2017"
    Transactions.loc[mask3, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[mask3, "Main Condition"] = "Good mentioned u/n/4/2017"

    # In[ ]:
        

    mask_sac = SACMaster["SAC Code"]
        
    #Step4: Any service between a client & Director
    mask4 = Transactions["Name"].isin(Directors["Name"])
    Transactions.loc[mask4, "Is RCM Applicable"] = "Yes"
    Transactions.loc[mask4, "RCM Reason"] = "Service provided by Director"
    Transactions.loc[mask4, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[mask4, "Main Condition"] = "Service provided by Director"

    # In[ ]:

    #Step5: Any service between Resident Service Recipient (Client) and a Non-Resident Service Provider

    #Check for NR Vendors
    NR_Vendor = Vendor_Details["Residential Status"] == "NR"
    NR_filtered_df = Vendor_Details[NR_Vendor]

    #Check for NR Vendors present in the Transactions dataframe
    mask5 = Transactions["Name"].isin(NR_filtered_df["Name"])
    #Check for Transactions with SAC Codes's first digits as 99
    mask5a = Transactions["Sac Codes"].astype(str).str.startswith("99")
    #Check for NR Vendor Transactions whose SAC Codes starts with 99
    mask5b = mask5 & mask5a


    if "R" in str(Client_Details["Residential Status"]):
        mask5b = mask5 & mask5a
        if mask5b.any():
            Transactions.loc[mask5b, "Is RCM Applicable"] = "Yes"
            Transactions.loc[mask5b, "RCM Reason"] = "Service provided by NR"
            Transactions.loc[mask5b, "Main Conditions True Or False"] = "Yes"
            Transactions.loc[mask5b, "Main Condition"] = "Service provided by NR"
        else:
            pass

    # In[ ]:

    #Step6: GTA Services


    #Filtering for SAC Code == 996791
    GTA_Filter = Transactions["Sac Codes"] == 996791
    GTA_Filtered_df = Transactions[GTA_Filter]

    #Filtering for Govt Pan Holders
    Govt_Filter = Vendor_Details["PAN"] .str[3] == "G"
    Govt_Filtered_df = Vendor_Details[Govt_Filter]

    #Filtering for Non-Govt Pan Holders
    Not_Govt_Filter = Vendor_Details["PAN"] .str[3] != "G"
    Not_Govt_Filtered_df = Vendor_Details[Not_Govt_Filter]

    #Filtering for Keywords
    Transactions["Invoice Description"] = Transactions["Invoice Description"].fillna("")
    Transactions["Invoice Description"] = Transactions["Invoice Description"].str.lower()
    Keyword_Filter = Transactions["Invoice Description"].str.lower().str.contains("Goods Transport Agency Services", case = False)
    Keyword_Filtered_df = Transactions[Keyword_Filter]

    #Updating if Sac code = 996791 and Vendor PAN Status not equals to G
    mask6 = (Transactions["Name"].isin(Not_Govt_Filtered_df["Name"])) & (GTA_Filter)
    Transactions.loc[mask6, "Is RCM Applicable"] = "Yes"
    Transactions.loc[mask6, "RCM Reason"] = "GTA Services"
    Transactions.loc[mask6, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[mask6, "Main Condition"] = "GTA Services"

    ##Updating if Sac code = 996791 and contains keywords
    ##### NOT CLEAR WHETHER TO UPDATE IF PAN STATUS IS G AND CONTAINS KEYWORDS OR PAN STATUS NOT EQUALS G. 
    ##### BECAUSE THE SAC CODE 996791 IS FOR GTA SERVICES. SO MAYBE THIS STEP IS NOT NEEDED.

    # In[ ]:

    #Step7: Legal Representation Services by an advocate or firm

    #Filtering for Sac Codes
    Sac_Code_Filter = Transactions['Sac Codes'].astype(str).str.startswith(("998211","998212","998213","998214","998215","998216"))
    Sac_Code_filtered_df = Transactions[Sac_Code_Filter]

    #Filtering for Person or Firm Pan Holders
    P_or_F_Filter = Vendor_Details["PAN"].str[3].isin(["P","F"])
    P_or_F_Filtered_df = Vendor_Details[P_or_F_Filter]

    #Update where Sac codes match with P or F PAN Status
    mask7 = (Transactions["Name"].isin(Sac_Code_filtered_df["Name"])) & (P_or_F_Filter)
    Transactions.loc[mask7, "Is RCM Applicable"] = "Yes"
    Transactions.loc[mask7, "RCM Reason"] = "Legal Services by Advocate or a Firm"
    Transactions.loc[mask7, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[mask7, "Main Condition"] = "Legal Services by Advocate or a Firm"

    # Update for services by arbitral tribunal
    Keyword_Filter2 = Transactions["Invoice Description"].str.lower().str.contains("Services by Arbitral Tribunal", case=False)
    Keyword_Filtered2_df = Transactions[Keyword_Filter2]

    mask7a = (Transactions["Name"].isin(Keyword_Filtered2_df["Name"])) & (Sac_Code_Filter)
    Transactions.loc[mask7a, "Is RCM Applicable"] = "Yes"
    Transactions.loc[mask7a, "RCM Reason"] = "Services by Arbitral Tribunal"
    Transactions.loc[mask7a, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[mask7a, "Main Condition"] = "Services by Arbitral Tribunal"
        
    ##### WHAT ABOUT TRANSACTIONS WITH THE GIVEN SAC CODES, PAN STATUS NOT EQUAL TO "P" OR "F" AND NO KEYWORDS IN INVOICE DESCRIPTION??


    # In[ ]:

    #Step8: Sponsorship Services

    # Filter for Sac Code = 998397
    Sponsor_Filter = Transactions["Sac Codes"] == 998397
    Sponsor_Filtered_df = Transactions[Sponsor_Filter]
    Transactions.loc[Sponsor_Filter, "Is RCM Applicable"] = "Yes"
    Transactions.loc[Sponsor_Filter, "RCM Reason"] = "Sponsorship Services"
    Transactions.loc[Sponsor_Filter, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[Sponsor_Filter, "Main Condition"] = "Sponsorship Services"

    #Filter for keywords
    Keyword_Filter3 = Transactions["Invoice Description"].str.lower().str.contains("Sponsorship Services", case=False)
    Keyword_Filtered3_df = Transactions[Keyword_Filter3]
    mask8 = Transactions["Name"].isin(Keyword_Filtered3_df["Name"])
    Transactions.loc[mask8, "Is RCM Applicable"] = "Yes"
    Transactions.loc[mask8, "RCM Reason"] = "Sponsorship Services"
    Transactions.loc[mask8, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[mask8, "Main Condition"] = "Sponsorship Services"

    # In[ ]:

    #Step9: Transportation of Goods by a vessel from a place outside India

    #Filter for transactions with SAC code = 996521
    Transport_Filter = Transactions["Sac Codes"] == 996521
    Transport_Filtered_df = Transactions[Transport_Filter]


    ## 
    ## We have already filtered NR Vendors in Step5 :NR_Vendor = Vendor_Details["Residential Status"] == "NR"
    ##                                               NR_filtered_df = Vendor_Details[NR_Vendor]

    #Check for Transactions with SAC Code = 996521 and NR Vendors
    NR_Transport_Vendor = Transport_Filtered_df["Name"].isin(NR_filtered_df["Name"])
    NR_Transport_Vendor_filtered_df = Transport_Filtered_df[NR_Transport_Vendor]

    #Filter for Transactions with SAC code = 996521 and NR Vendor
    mask9 = Transactions["Name"].isin(NR_Transport_Vendor_filtered_df["Name"])
    Transactions.loc[mask9, "Is RCM Applicable"] = "Yes"
    Transactions.loc[mask9, "RCM Reason"] = "Transportation of Goods by Vessel from Outside India"
    Transactions.loc[mask9, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[mask9, "Main Condition"] = "Transportation of Goods by Vessel from Outside India"

    #Filter for keyword
    Keyword_Filter4 = Transactions["Invoice Description"].str.lower().str.contains("Transportation of Goods by Vessel from a place outside India", case=False)
    Keyword_Filtered4_df = Transactions[Keyword_Filter4]
    mask9a = Transactions["Name"].isin(Keyword_Filtered4_df["Name"])
    Transactions.loc[mask9a, "Is RCM Applicable"] = "Yes"
    Transactions.loc[mask9a, "RCM Reason"] = "Transportation of Goods by Vessel from Outside India"
    Transactions.loc[mask9a, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[mask9a, "Main Condition"] = "Transportation of Goods by Vessel from Outside India"

    #### WHAT ABOUT SAC CODE = 996521, RESIDENT VENDORS??

    # In[ ]:

    #Step10: Transactions with un-registered supplier

    Unregistered_Vendors = Vendor_Details[Vendor_Details["GSTN"].isna()]

    # Filter for transactions of un-registered GST vendors
    mask10 = Transactions["Name"].isin(Unregistered_Vendors["Name"])
    Transactions.loc[mask10, "Is RCM Applicable"] = "Yes"
    Transactions.loc[mask10, "RCM Reason"] = "Goods/Services received from un-registered service provider"
    Transactions.loc[mask10, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[mask10, "Main Condition"] = "Goods/Services received from un-registered service provider"

    # In[ ]:

    #Step11: Services provided by Govt./UT or Local Authority

    #Filter for Govt. or Local Authority Pan Holders
    G_or_L_Filter = Vendor_Details[Vendor_Details["PAN"].str[3].isin(["G","L"])]

    #Filter for transactions with SAC codes not in the list
    not_in_list = [997211,997212,996811,996812,996411]
    mask11 = ~Transactions['Sac Codes'].isin(not_in_list)
    not_in_list_df = Transactions[mask11]

    #Filter for govt/local authority PAN holders with SAC Codes not in the list
    mask11a = not_in_list_df["Name"].isin(G_or_L_Filter["Name"])
    Govt_Local_Sac_Code_df = not_in_list_df[mask11a]

    #Filter for transactions govt/local authority PAN holders with SAC Codes not in the list
    mask12a = Transactions["Name"].isin(Govt_Local_Sac_Code_df["Name"])
    Transactions.loc[mask12a, "Is RCM Applicable"] = "Yes"
    Transactions.loc[mask12a, "RCM Reason"] = "Service provided by Govt./UT or Local Authority"
    Transactions.loc[mask12a, "Main Conditions True Or False"] = "Yes"
    Transactions.loc[mask12a, "Main Condition"] = "Service provided by Govt./UT or Local Authority"

    # In[ ]:
        
    #Step12: Special SAC code based checking
        
    mask23 = Transactions['Sac Codes'].isin(SACMaster["SAC Code"])


    # Apply the mask to Transactions dataframe
    filtered_transactions = Transactions[mask23]
    # print(filtered_transactions)

    # Set default values for 'SAC Code Match' and 'Invoice Description Matched With Keywords' columns
    Transactions['SAC Code Match'] = ''
    Transactions['Invoice Description Matched With Keywords'] = ''

    # Get the matching SAC Codes from the filtered_transactions
    matching_sac_codes = filtered_transactions['Sac Codes'].unique()
    matching_rows = SACMaster['SAC Code'].isin(matching_sac_codes) & (SACMaster['Is RCM Applicable'] == 'Yes')

    matching_sac_codes_matched = SACMaster.loc[matching_rows, 'SAC Code']
    # matching_sac_codes_not_matched = matching_sac_codes[~matching_sac_codes.isin(matching_sac_codes_matched)]

    Transactions.loc[Transactions['Sac Codes'].isin(matching_sac_codes_matched), 'SAC Code Match'] = "Yes"
    Transactions.loc[Transactions['Sac Codes'].isin(matching_sac_codes_matched), 'Invoice Description Matched With Keywords'] = 'SAC Master ka SAC code matched'
    # Transactions.loc[Transactions['Sac Codes'].isin(matching_sac_codes_not_matched), 'SAC Code Match'] = False



    #Step13: Special SAC description based checking

    KeywordMaster["Keyword"] = KeywordMaster["Keyword"].apply(lambda x: str(x))
    Transactions["Invoice Description"] = Transactions["Invoice Description"].apply(lambda x: str(x))




    # Use apply and list comprehension to calculate the closest match for each row in the Transactions dataframe, considering only matches above the similarity threshold
    # Transactions['Invoice Description Matched With Keywords'] = Transactions['Invoice Description'].apply(lambda x: KeywordMaster.loc[KeywordMaster['Keyword'].apply(lambda y: str(y)[:]).apply(lambda z: fuzz.token_set_ratio(str(x), str(z))).idxmax()]['Keyword'] if KeywordMaster['Keyword'].apply(lambda y: str(y)[:-9]).apply(lambda z: fuzz.token_set_ratio(str(x), str(z))).max() >= 75 else 'N/A')


    # Create a function to check RCM Applicable value
    def check_rcm_applicable(keyword):
        rcm_applicable = KeywordMaster.loc[KeywordMaster['Keyword'] == keyword, 'Is RCM Applicable']
        if not rcm_applicable.empty and rcm_applicable.item() == 'Yes':
            return keyword
        else:
            return 'N/A'

    # Use apply and list comprehension to calculate the closest match for each row in the Transactions dataframe, considering only matches above the similarity threshold
    Transactions['Invoice Description Matched With Keywords'] = Transactions['Invoice Description'].apply(
        lambda x: check_rcm_applicable(KeywordMaster.loc[
            KeywordMaster['Keyword'].apply(lambda y: str(y)[:]).apply(
                lambda z: fuzz.token_set_ratio(str(x), str(z))
            ).idxmax()]['Keyword']
        ) if KeywordMaster['Keyword'].apply(
            lambda y: str(y)[:-9]
        ).apply(
            lambda z: fuzz.token_set_ratio(str(x), str(z))
        ).max() >= 75 else 'N/A')










    #Step14: Special GL Code based checking
    # mask32 = Transactions['GL Code'].isin(GLMaster["GL Code"])



    # filtered_df_GL = Transactions[mask32]


    # Transactions.loc[mask32, "GL Code Description if Matched"] = "GL Master ka GL code matched"
    # Transactions.loc[mask32, "GL Code Match"] = "Yes"



    # #Step15: Special GL Description based checking


    # GLMaster["GL Description"] = GLMaster["GL Description"].apply(lambda x: str(x))
    # Transactions["Invoice Description"] = Transactions["Invoice Description"].apply(lambda x: str(x))


    # # Use apply and list comprehension to calculate the closest match for each row in the Transactions dataframe, considering only matches above the similarity threshold
    # Transactions['GL Code Description if Matched'] = Transactions['Invoice Description'].apply(lambda x: GLMaster.loc[GLMaster['GL Description'].apply(lambda y: str(y)[:]).apply(lambda z: fuzz.token_set_ratio(str(x), str(z))).idxmax()]['GL Description'] if GLMaster['GL Description'].apply(lambda y: str(y)[:-9]).apply(lambda z: fuzz.token_set_ratio(str(x), str(z))).max() >= 75 else 'N/A')


    #Step 16 Priority setting
    def check_rcm_applicable(transactions):
        # Check if 'is RCM Applicable' column is blank
        is_blank = transactions['Is RCM Applicable'].isnull()

        # Iterate over rows where 'is RCM Applicable' is blank
        for i, row in transactions.iterrows():
            if is_blank[i]:
                # Filter out NaN values and find the first non-blank, non-null, non-'N/A' value (case-insensitive)
                non_blank_col = row.loc[row.index[row.index.get_loc('SAC Code Match'):]].loc[
                    ~row.loc[row.index[row.index.get_loc('SAC Code Match'):]].apply(lambda x: str(x) in ['', 'N/A', 'n/A', 'N/a','n/a', None])]

                # Exclude NaN values from the search
                non_blank_col = non_blank_col.dropna()

                # Update the 'is RCM Applicable' and 'RCM Reason' columns
                if not non_blank_col.empty:
                    transactions.at[i, 'Is RCM Applicable'] = 'Yes'
                    transactions.at[i, 'RCM Reason'] = non_blank_col.index[0]
                    print(non_blank_col.index[0])

        return transactions



    Transactions = check_rcm_applicable(Transactions)


        



    #Step17: Residual Transactions

    Transactions["Is RCM Applicable"] = Transactions["Is RCM Applicable"].fillna("No")
    Transactions["RCM Reason"] = Transactions["RCM Reason"].fillna("N/A")

    print('Hello jijijij')

    print(Transactions)
    # Transactions.to_excel('updated_transactions.xlsx', index=False)



#     # Return the response with the output file path
#     response = {'outputFilePath': f'{relative_path}\\updated_transactions.xlsx'}
#     return jsonify(response)

# def download_file():
#     file_path = request.args.get('filePath')
    
#     # Validate the file path or perform any additional checks
#     print(file_path)
#     # Serve the file as a downloadable resource
#     return send_file(file_path, as_attachment=True)
    # return jsonify({"files": len(files), "ids": len(ids), "dataframes": len(dataframes)})
    # return jsonify({"message": "Files processed successfully", "data":Transactions.to_json()})
    excel_file = 'data.xlsx'

    existing_df = pd.read_excel(excel_file)
    existing_df = Transactions
    existing_df.to_excel(excel_file, index=False)

    # Send the Excel file as a response
    return send_file(excel_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='localhost', port=8080)

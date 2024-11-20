from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from .forms import CCMS,RMR,Receipt_1,challan_status,cash_deposition
import os
from django.conf import settings
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil import parser
import warnings
warnings.filterwarnings('ignore')

# Create your views here.
def index(request):
    page_title= "Automation Page"
    return render(request,'blog/index.html',{'page_title':page_title})

def detail(request,post_id):
    return render(request,'blog/detail.html')

def old_url_redirect(request):
    return redirect(reverse('blog:new_one'))

def new_url_view(request):
    return HttpResponse("This is New URL")

def run_page(request):
    return render(request,'blog/Run_page.html')


def ccms_file(request):
    if request.method == 'POST':
        form = CCMS(request.POST, request.FILES)
        if form.is_valid():
            custom_filename = 'CCMS'  # Specify your custom filename here
            uploaded_file = request.FILES['myfile']
            ccms_uploaded_file(uploaded_file, custom_filename)
            return redirect('blog:runpage')  # Redirect to a success page after file upload
    else:
        form = CCMS()
    return render(request, 'blog/index.html', {'form': form})
    

def ccms_uploaded_file(uploaded_file, custom_filename):
    destination_folder = os.path.join(settings.MEDIA_ROOT, 'CCMS')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Extract the file extension from the original filename
    file_extension = os.path.splitext(uploaded_file.name)[1]
    
    # Append the file extension to the custom filename
    destination_path = os.path.join(destination_folder, f"{custom_filename}{file_extension}")
    
    with open(destination_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    

def ccms_script(request):
    try:
        # Read the CSV file
        #df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'CCMS', 'CCMS.csv'))
        df = pd.read_csv(r"\\10.9.57.54\RPT_VF_Collections\DAILY_RMR_VF\CCMS_VF.csv")
        
        # Filter rows
        s_df = df['MODEOFPAYMENT'] == 'Cash'
        df = df[s_df]
        
        # Sum columns
        dflist = ['EMI', 'CBC', 'AFC', 'OTHERS', 'FVC', 'SHORTFALL_RECOVERY', 'SERVICE_CHARGES', 'INSURANCE_PREMIUM', 'SECURITY_DEPOSIT', 'COLL_MARGIN_MONEY_RECD', 'BT_COMMITMENT_CHARGES', 'COLL_COMPENSATION_CHARGES', 'SALE_AMOUNT', 'SEIZURE_CHARGES', 'NPDC_CONVERSION_CHARGES', 'MI_INS_PREMIUM_REVBLE', 'SOA_CHARGES', 'CANCELLATION_CHARGES', 'HEALTH_INSURANCE_CHOLA_MS', 'PARKING_CHARGES', 'COLL_NON_PDC_CHARGES', 'PDC_SWAP_CHARGES', 'REPOSESSION_CHARGES', 'LIFE_INSURANCE_HDFC_LS', 'PROC_FEES_COLL', 'LIST_OF_DOCUMENTS', 'COPY_OF_DOCUMENTS', 'COLLECTION_CERSAI_CHARGES', 'RECOVERY_CHARGES_LEGAL', 'NOC_CHARGES']
        df['AMOUNT'] = df[dflist].sum(axis=1)
        
        # Group and aggregate
        df1 = df.iloc[:, [3, 76, 77]]
        df2 = df1.groupby(['CIF_NO', 'CHR_RECT_DATE']).sum().sort_values('CHR_RECT_DATE').reset_index()
        
        # Add a status column
        df2.loc[df2["AMOUNT"] <= 195000, "Status"] = "OK"
        df2.loc[df2["AMOUNT"] > 195000, "Status"] = "More than 1.95 lakhs"
        
        # Save to a CSV file
        output_path = os.path.join(settings.MEDIA_ROOT, 'CCMS', 'CCMS_VF_Morethan 1.95lakhs.csv')
        df2.to_csv(output_path, index=False)
        
        response = HttpResponse(open(output_path, 'rb').read(), content_type='text/csv')
        
        # Set the Content-Disposition header to force download
        response['Content-Disposition'] = 'attachment; filename="CCMS_VF_Morethan_1.95lakhs.csv"'
        
        return response 
    
    except Exception as e:
        # Handle any exceptions
        return HttpResponse(f'Error: {e}')

# RMR VIEW

def rmr_file(request):
    if request.method == 'POST':
        form_rmr = RMR(request.POST, request.FILES)
        if form_rmr.is_valid():
            custom_filename = 'RMR'  # Specify your custom filename here
            uploaded_file = request.FILES['myfile_rmr']
            rmr_uploaded_file(uploaded_file, custom_filename)
            return redirect('blog:runpage')  # Redirect to a success page after file upload
    else:
        form_rmr = RMR()
    return render(request, 'blog/index.html', {'form': form_rmr})

def rmr_uploaded_file(uploaded_file, custom_filename):
    destination_folder = os.path.join(settings.MEDIA_ROOT, 'RMR')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Extract the file extension from the original filename
    file_extension = os.path.splitext(uploaded_file.name)[1]
    
    # Append the file extension to the custom filename
    destination_path = os.path.join(destination_folder, f"{custom_filename}{file_extension}")
    
    with open(destination_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)


def rmr_script(request):
    try:
        # Read the CSV file
        #df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'RMR', 'RMR.csv'))
        df = pd.read_csv(r"\\10.9.57.54\RPT_VF_Collections\DAILY_RMR_VF\RMR_VF.csv")
        
        # Filter rows
        s_df = df['MODEOFPAYMENT'] == 'Cash'
        df = df[s_df]
        
        # Sum columns
        dflist=['EMI','CBC','AFC','OTHERS','FVC','SHORTFALL_RECOVERY','SERVICE_CHARGES','INSURANCE_PREMIUM','SECURITY_DEPOSIT','COLL_MARGIN_MONEY_RECD','BT_COMMITMENT_CHARGES','COLL_COMPENSATION_CHARGES','SALE_AMOUNT','SEIZURE_CHARGES','NPDC_CONVERSION_CHARGES','MI_INS_PREMIUM_REVBLE','SOA_CHARGES','CANCELLATION_CHARGES','HEALTH_INSURANCE_CHOLA_MS','PARKING_CHARGES','COLL_NON_PDC_CHARGES','PDC_SWAP_CHARGES','REPOSESSION_CHARGES','LIFE_INSURANCE_HDFC_LS','PROC_FEES_COLL','LIST_OF_DOCUMENTS','COPY_OF_DOCUMENTS','COLLECTION_CERSAI_CHARGES','RECOVERY_CHARGES_LEGAL','NOC_CHARGES']
        df['AMOUNT']=df[dflist].sum(axis=1)
        
        # Group and aggregate
        df1=df.iloc[:, [3,76,78]]
        df2 = df1.groupby(['CIF_NO', 'CHR_RECT_DATE']).sum().sort_values('CHR_RECT_DATE').reset_index()
        
        # Add a status column
        df2.loc[df2["AMOUNT"] <= 195000, "Status"] = "OK"
        df2.loc[df2["AMOUNT"] > 195000, "Status"] = "More than 1.95 lakhs"
        
        # Save to a CSV file
        output_path = os.path.join(settings.MEDIA_ROOT, 'RMR', 'RMR_VF_Morethan 1.95lakhs.csv')
        df2.to_csv(output_path, index=False)
        
        response = HttpResponse(open(output_path, 'rb').read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="RMR_VF_Morethan_1.95lakhs.csv"'
        
        return response
    
    except Exception as e:
        # Handle any exceptions
        return HttpResponse(f'Error: {e}')

# Daily_Receipt
def rr_file(request):
    if request.method == 'POST':
        form_rr = Receipt_1(request.POST, request.FILES)
        if form_rr.is_valid():
            for key, uploaded_file in request.FILES.items():
                custom_filename = 'Receipt_' + key 
                rr_uploaded_file(uploaded_file, custom_filename)

            return redirect('blog:runpage') 
    else:
        form_rr = Receipt_1()

    return render(request, 'blog/index.html', {'form': form_rr})

def rr_uploaded_file(uploaded_file, custom_filename):
    destination_folder = os.path.join(settings.MEDIA_ROOT, 'Receipt')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    file_extension = os.path.splitext(uploaded_file.name)[1]
    destination_path = os.path.join(destination_folder, f"{custom_filename}{file_extension}")
    
    with open(destination_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

def receipt_script(request):
    try:
        #1st File
        df=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipt_first_file.csv'),encoding='unicode_escape')

        #2nd File(Emp Id file)
        df2=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipt_second_file.csv'),encoding='unicode_escape')

        #3rd File(challan Status file)
        df4=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipt_third_file.csv'),encoding='unicode_escape')

        #4th File(Pre X file)
        df5=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipt_four_file.xlsb'),engine='pyxlsb')

        #5th File(Updated branch file)
        df3=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipt_five_file.xlsb'),engine='pyxlsb')

        #6th File(Emp Details (Role,Stage file))
        emp_dt=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipt_six_file.xlsb'),engine='pyxlsb')

        #7th File(Active list)
        active_list=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipt_seven_file.xlsx'))

        #8th File(New online rollrate file)
        dpd=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipt_eight_file.csv'),encoding='unicode_escape')

        #9th File(Used online rollrate file)
        dpd_us=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipt_nine_file.csv'),encoding='unicode_escape')

        #10th File(Expt online rollrate file)
        dpd_ex=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipt_ten_file.csv'),encoding='unicode_escape')

        #df=pd.read_csv(r'C:\Users\CB58736\Downloads\report1704972513228.csv',encoding='unicode_escape')
        df

        df1=df[df['Payment Mode'].isin(['Cash','Cheque','Draft'])]
        
        s_df=df1['LMS Sync Status']=='Awaiting'
        df_1=df1[s_df]
        
        s_df1=df_1['Status']!='Request for Cancel'
        df_2=df_1[s_df1]
        
        #df2=pd.read_csv(r'C:\Users\CB58736\Downloads\report1704972502142.csv',encoding='unicode_escape')
        df2

        lookup=pd.merge(df_2,df2[['Created By: Employee Number','Receipt No']],on='Receipt No',how='left')
        
        lookup['Value in Lakhs']=(lookup['Amount']/100000).round(2)

        lookup['Payment']=lookup['Payment Mode'].apply(lambda x:'Cash' if x=='Cash' else 'Cheque/DD' if x in ['Cheque','Draft'] else '')

        arrange=['Receipt No','Created By: Employee Number','Agreement No: Agreement Number','Created By: Full Name','ReceiptCreatedDateTime','Status','Amount','Value in Lakhs','Payment Mode','Payment','LMS Sync Status','Record Type','Receipt Batch: Hand Off Status','Source','Receipt Batch: Batch Id','Value Date','Zone','Region','Area','Branch: Account Name','Created Date','Receipt Batch: Challan: Challan Number']
        lookup_1=lookup[arrange]
        
        lookup_2=lookup_1.copy()

        lookup_2['Branch: Account Name']=lookup_2['Branch: Account Name'].str.upper()

        new_data=lookup_2.copy()

        new_data['Created Date']=pd.to_datetime(new_data['Created Date'],dayfirst=True)

        new_data['Month']=new_data['Created Date'].dt.strftime('%b %y')
        
        new_data['Today']=datetime.now().date()

        new_data['Today']=pd.to_datetime(new_data['Today'],dayfirst=True)

        new_data['Ageing']=(new_data['Today'] - new_data['Created Date']).dt.days
        
        condition=[
            (new_data['Ageing']==0),
            (new_data['Ageing']==1),
            (new_data['Ageing'].isin([2,3])),
            (new_data['Ageing'].isin([4,5,6])),
            (new_data['Ageing'].isin([7,8,9,10])),
            (new_data['Ageing'].isin([11,12,13,14,15,16,17,18,19,20])),
            (new_data['Ageing']>20)
        ]


        values=["'0","'1","'2-3","'4-6","'7-10","'11-20","'>20"]

        new_data['Group']=np.select(condition,values,default='Unknown')

        #new_data.info()

        new_data_1=new_data.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24,25,21]]
        
        #df4=pd.read_csv(r'C:\Users\CB58736\Downloads\report1704972533192.csv',encoding='unicode_escape')
        df4

        df_merged = new_data_1.merge(df4[['Physical Challan No','Bank Name','Challan Status', 'Challan: Challan Number']], left_on= 'Receipt Batch: Challan: Challan Number',right_on='Challan: Challan Number', how = 'left')

        update=df_merged.drop(columns=['Challan: Challan Number'])
        
        update['Remarks']=update['Challan Status'].apply(lambda x:'Challan Authorization Pending' if x=='Requested for Authorization' else '')

        fill_condition= (update['Remarks']=='') & (update['Status']=='Ready for Batching')

        update.loc[fill_condition,'Remarks']='Batch ID Not Created'

        upp=update.copy()

        fill_condition1=(upp['Remarks']=='') & (upp['Receipt Batch: Hand Off Status'] =='Approved')
        upp.loc[fill_condition1,'Remarks']='Handedoff to Teller'

        upp_1=upp.copy()

        fill_condition_1=(upp['Remarks']=='') & (upp['Receipt Batch: Hand Off Status'] =='Submitted')
        upp_1.loc[fill_condition_1,'Remarks']='Handedoff to Teller'

        fill_condition_11=(upp['Remarks']=='') & (upp['Challan Status'] =='Pending for Approval')
        upp_1.loc[fill_condition_11,'Remarks']='Handedoff to Teller'

        upp_2=upp_1.copy()
        
        fill_condition2=(upp_2['Remarks']=='') & (upp_2['Challan Status'] =='Challan Details Pending')
        upp_2.loc[fill_condition2,'Remarks']='Pending For Challan Image Upload'

        upp_3=upp_2.copy()

        excluded_value=['Challan Details Pending','Challan Uploaded','Requested for Authorization','Authorized']
        upp_3['Remarks'] = upp_3.apply(lambda row: 'Handed off Not Done' if row['Remarks']=='' and row['Challan Status'] not in excluded_value else row['Remarks'],axis=1)

        fill_condition3=(upp_3['Remarks']=='') & (upp_3['Challan Status'] =='Challan Uploaded')
        upp_3.loc[fill_condition3,'Remarks']='Need to Check'

        fill_conditio=(upp_3['Remarks']=='') & (upp_3['Challan Status'] =='Authorized')
        upp_3.loc[fill_conditio,'Remarks']='Need to Check'

        upp_4=upp_3.copy()

        upp_4['Pending With Whom']=upp_4.apply(lambda row: 'CFE' if row['Source']=='Online App' and row['Remarks'] in ['Batch ID Not Created','Handed off Not Done','Pending For Challan Image Upload'] else 'Teller',axis=1)

        #df5=pd.read_excel(r'C:\Users\CB58736\Downloads\Pre X.xlsb')
        df5

        nll=upp_4.merge(df5,right_on='Agreement No',left_on='Agreement No: Agreement Number',how='left')
        
        nll_upp=nll.drop(columns=['Agreement No'])
        
        #df3=pd.read_excel(r'C:\Users\CB58736\Downloads\Updated Branch List _ Jan24.xlsb',engine='pyxlsb')
        df3

        merged = nll_upp.merge(df3[['FINAL BRANCH','ZONE','STATE','REGION','AREA','BRANCH']], left_on= 'Branch: Account Name',right_on='FINAL BRANCH', how = 'left')
        
        duplicate_rows=merged[merged.duplicated(subset='Receipt No')]
        duplicate_rows

        final=merged.drop_duplicates(subset='Receipt No')
        
        #final.info()

        final_1=final.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,33,34,35,36,37,20,21,22,23,24,25,26,27,28,29,30,31]]
       
        #emp_dt=pd.read_excel(r'C:\Users\CB58736\Downloads\Emp details 05th Jan 24.xlsb',engine='pyxlsb')
        emp_dt

        d_l = final_1.merge(emp_dt[['EMPID','ROLE','COLOUR']], left_on= 'Created By: Employee Number',right_on='EMPID', how = 'left')
        
        final_2=d_l.drop(columns=['EMPID'])
        
        final_2['Created By: Employee Number']=final_2['Created By: Employee Number'].str.upper()

        #active_list=pd.read_excel(r"D:\old backup 01.11.2023\Active List.xlsx")
        active_list

        d_ll= final_2.merge(active_list[['Employee Code','Department','Product','Sub Product']], left_on= 'Created By: Employee Number',right_on='Employee Code', how = 'left')
        
        final_3=d_ll.drop(columns='Employee Code')
        
        final_3['Department']=final_3['Department'].str.upper()

        lll= final_3.merge(active_list[['Employee Code','Employment Status','Final Approved LWD']], left_on= 'Created By: Employee Number',right_on='Employee Code', how = 'left')
        
        final_4=lll.drop(columns='Employee Code')
        
        #dpd=pd.read_csv(r"C:\Users\CB58736\Desktop\Online_rollrate_VFPRIME_NEW_2024-01-11_17-25-49.csv",encoding='unicode_escape')
        dpd

        #dpd_us=pd.read_csv(r"C:\Users\CB58736\Desktop\Online_rollrate_VFPRIME_USED_2024-01-11_17-25-49.csv",encoding='unicode_escape',chunksize=100000)
        dpd_us

        #dpd_ex=pd.read_csv(r"C:\Users\CB58736\Desktop\ONLINE_ROLLRATE_EXPT_VFPRIME_2024-01-29_16-57-57.csv",encoding='unicode_escape')
        dpd_ex

        dpd_new= final_4.merge(dpd[['AGREEMENTNO','ALLOCATION_DPD','ALLOCATION_DPD_GRP']], left_on= 'Agreement No: Agreement Number',right_on='AGREEMENTNO', how = 'left')
        
        final_5=dpd_new.drop(columns='AGREEMENTNO')
        
        dpd_news= final_5.merge(dpd_us[['AGREEMENTNO','ALLOCATION_DPD','ALLOCATION_DPD_GRP']], left_on= 'Agreement No: Agreement Number',right_on='AGREEMENTNO', how = 'left')

        dpd_pr= dpd_news.merge(dpd_ex[['AGREEMENTNO','ALLOCATION_DPD','ALLOCATION_DPD_GRP']], left_on= 'Agreement No: Agreement Number',right_on='AGREEMENTNO', how = 'left')
        
        dpd_pr['ALLOCATION_DPD_x']=dpd_pr['ALLOCATION_DPD_x'].combine_first(dpd_pr['ALLOCATION_DPD_y']).combine_first(dpd_pr['ALLOCATION_DPD'])

        dpd_pr['ALLOCATION_DPD_GRP_x']=dpd_pr['ALLOCATION_DPD_GRP_x'].combine_first(dpd_pr['ALLOCATION_DPD_GRP_y']).combine_first(dpd_pr['ALLOCATION_DPD_GRP'])

        rem=dpd_pr.drop(columns=['AGREEMENTNO_y','ALLOCATION_DPD','ALLOCATION_DPD_GRP'])
        
        fg1=rem.rename({'COLOUR':'Stage','Created By: Employee Number':'EMP ID','Created By: Full Name':'EMP Name','Agreement No: Agreement Number':'AgreementNumber','ALLOCATION_DPD_x':'ALLOCATION_DPD','ALLOCATION_DPD_GRP_x':'ALLOCATION_DPD_GRP'},axis=1)
       
        fg2=fg1.drop(columns=['AGREEMENTNO_x','ALLOCATION_DPD_y','ALLOCATION_DPD_GRP_y'])
        
        dp1=fg2[(fg2['ALLOCATION_DPD'].isna()) & (fg2['Record Type']=='Closed Agreement')]
        fg2.loc[dp1.index,'ALLOCATION_DPD'] = 'Closed Agreement'

        dp2=fg2[(fg2['ALLOCATION_DPD'].isna()) & (fg2['Record Type']=='Foreclosure')]
        fg2.loc[dp2.index,'ALLOCATION_DPD'] = 'Foreclosure'

        dp3=fg2[(fg2['ALLOCATION_DPD'].isna()) & (fg2['Record Type']=='Non Agreement')]
        fg2.loc[dp3.index,'ALLOCATION_DPD'] = 'Non Agreement'

        dp4=fg2[(fg2['ALLOCATION_DPD'].isna()) & (fg2['Record Type']=='Part Foreclosure')]
        fg2.loc[dp4.index,'ALLOCATION_DPD'] = 'Part Foreclosure'

        dp5=fg2[(fg2['ALLOCATION_DPD'].isna()) & (fg2['Record Type']=='Shortfall')]
        fg2.loc[dp5.index,'ALLOCATION_DPD'] = 'Shortfall'

        dp6=fg2[(fg2['ALLOCATION_DPD'].isna()) & (fg2['Record Type']=='TA Receipt')]
        fg2.loc[dp6.index,'ALLOCATION_DPD'] = 'TA Receipt'

        fg3=fg2.copy()

        dpg1=fg3[(fg3['ALLOCATION_DPD_GRP'].isna()) & (fg3['Record Type']=='Closed Agreement')]
        fg3.loc[dpg1.index,'ALLOCATION_DPD_GRP'] = 'Closed Agreement'

        dpg2=fg3[(fg3['ALLOCATION_DPD_GRP'].isna()) & (fg3['Record Type']=='Foreclosure')]
        fg3.loc[dpg2.index,'ALLOCATION_DPD_GRP'] = 'Foreclosure'

        dpg3=fg3[(fg3['ALLOCATION_DPD_GRP'].isna()) & (fg3['Record Type']=='Non Agreement')]
        fg3.loc[dpg3.index,'ALLOCATION_DPD_GRP'] = 'Non Agreement'

        dpg4=fg3[(fg3['ALLOCATION_DPD_GRP'].isna()) & (fg3['Record Type']=='Part Foreclosure')]
        fg3.loc[dpg4.index,'ALLOCATION_DPD_GRP'] = 'Part Foreclosure'

        dpg5=fg3[(fg3['ALLOCATION_DPD_GRP'].isna()) & (fg3['Record Type']=='Shortfall')]
        fg3.loc[dpg5.index,'ALLOCATION_DPD_GRP'] = 'Shortfall'

        dpg6=fg3[(fg3['ALLOCATION_DPD_GRP'].isna()) & (fg3['Record Type']=='TA Receipt')]
        fg3.loc[dpg6.index,'ALLOCATION_DPD_GRP'] = 'TA Receipt'

        fg4=fg3.copy()

        sales=fg4[(fg4['ROLE'].isna()) & (fg4['Department']=='SALES')]
        fg4.loc[sales.index,'ROLE'] = 'SFE'

        coll=fg4[(fg4['ROLE'].isna()) & (fg4['Department']=='COLLECTION')]
        fg4.loc[coll.index,'ROLE'] = 'CFE'

        tell=fg4[(fg4['ROLE'].isna()) & (fg4['Department']=='CREDIT')]
        fg4.loc[tell.index,'ROLE'] = 'TELLER'

        #from dateutil import parser

        def parser_date_time(value):
            try:
                dt_object = parser.parse(value)
                return dt_object.date(), dt_object.strftime('%I:%M%p')
            except ValueError:
                return None, None
            
        fg4[['ReceiptCreatedDate','Time']] = fg4['ReceiptCreatedDateTime'].apply(lambda x: pd.Series(parser_date_time(x)))

        fg4['ReceiptCreatedDate']=pd.to_datetime(fg4['ReceiptCreatedDate'])
        fg4['ReceiptCreatedDate']=fg4['ReceiptCreatedDate'].dt.strftime('%m/%d/%Y')


        fg5=fg4.copy()

        #fg5.info()

        updated=fg5.iloc[:, [0,2,1,3,42,43,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41]]

        updated['ALLOCATION_DPD_GRP'] = updated['ALLOCATION_DPD_GRP'].apply(lambda x: "'" + str(x) if pd.notnull(x) else x)

        #updated['ALLOCATION_DPD_GRP']="'" +updated['ALLOCATION_DPD_GRP'].astype(str)        
        # Save to a CSV file
        output_path = os.path.join(settings.MEDIA_ROOT, 'Receipt', 'Receipts Pending List pre x.csv')
        updated.to_csv(output_path, index=False)
        
        response = HttpResponse(open(output_path, 'rb').read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Receipts Pending List pre x.csv"'
        
        return response
    
    except Exception as e:
        # Handle any exceptions
        return HttpResponse(f'Error: {e}')

# Challan Status  
def challan_file(request):
    if request.method == 'POST':
        form_ch = challan_status(request.POST, request.FILES)
        if form_ch.is_valid():
            for key, uploaded_file in request.FILES.items():
                custom_filename = 'Challan_' + key 
                challan_uploaded_file(uploaded_file, custom_filename)

            return redirect('blog:runpage') 
    else:
        form_ch = challan_status()
    
    return render(request, 'blog/index.html', {'form': form_ch})

def challan_uploaded_file(uploaded_file, custom_filename):
    destination_folder = os.path.join(settings.MEDIA_ROOT, 'Challan Status')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    file_extension = os.path.splitext(uploaded_file.name)[1]
    destination_path = os.path.join(destination_folder, f"{custom_filename}{file_extension}")
    
    with open(destination_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

def challan_script(request):
    try:
        #1st File
        df=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_first.csv'),encoding='unicode_escape')
        #2nd File(Emp Id file)
        df1=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_second.csv'),encoding='unicode_escape')
        #3rd File(challan Status file)
        df2=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_third.csv'),encoding='unicode_escape')
        #4th File(Updated branch file)
        df3=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_four.xlsb'),engine='pyxlsb',sheet_name='Base')
        #5th File(Active list file)
        active_list=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_five.xlsx'))
        #6th File(employee details file)
        emp=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_six.xlsx'))
        #7th File(Time file)
        time=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_seven.xlsx'))
        
        df

        df1

        lookup=pd.merge(df,df1[['Created By: Employee Number','Receipt No']],on='Receipt No',how='left')
        df2
        lookup_1 = lookup.merge(df2[['Challan Status','Physical Challan No','Bank Name','Challan: Challan Number']], left_on= 'Receipt Batch: Challan: Challan Number',right_on='Challan: Challan Number', how = 'left')
        f_df=lookup_1[lookup_1['Payment Mode'].isin(['Cash','Cheque','Draft'])]
        f_df['Branch: Account Name']=f_df['Branch: Account Name'].str.upper()
        df3
        df3['FINAL BRANCH']=df3['FINAL BRANCH'].str.upper()
        f_df1= f_df.merge(df3[['ZONE','STATE','REGION','AREA','BRANCH.1','FINAL BRANCH']], left_on= 'Branch: Account Name',right_on='FINAL BRANCH', how = 'left')
        f_df1['Value in Lakhs']=(f_df1['Amount']/100000).round(2)
        #emp=pd.read_excel(r'D:\share\RMR & Active list & Receipt Lwd Back up\employee details.xlsx')
        emp
        f_df2= f_df1.merge(emp[['ROLE','COLOUR','EMPID']], left_on= 'Created By: Employee Number',right_on='EMPID', how = 'left')
        f_df3=f_df2.drop(columns=['EMPID','FINAL BRANCH','Challan: Challan Number'])
        #f_df3.info()
        #active_list=pd.read_excel(r"D:\share\RMR & Active list & Receipt Lwd Back up\Active List_py.xlsx")
        active_list
        f_df4= f_df3.merge(active_list[['Department','Product','Sub Product','Business Designation','Employee Code']], left_on= 'Created By: Employee Number',right_on='Employee Code', how = 'left')
        f_df4_u=f_df4.drop(columns=['Employee Code'])
        #time=pd.read_excel(r'C:\Users\thameemmj\Desktop\gallop 4Pm.xlsx')
        time
        f_df5= f_df4_u.merge(time[['Timing','Receipt No']],on='Receipt No', how = 'left')
        #f_df5.info()
        new_df=f_df5.copy()
        new_df['Roles']=new_df['ROLE'].apply(lambda x:'CFE' if x=='CFE' else '')
        new_df_1=new_df.copy()
        fill_condition1=(new_df_1['Roles']=='') & (new_df_1['ROLE'] =='TELLER')
        new_df_1.loc[fill_condition1,'Roles']='TELLER'
        new_df1=new_df_1.copy()
        excluded_value=['CFE','TELLER']
        new_df1['Roles'] = new_df1.apply(lambda row: 'Other Than CFE' if row['ROLE'] not in excluded_value else row['Roles'],axis=1)
        new_df2=new_df1.copy()
        new_df2['Remarks']=new_df2['LMS Sync Status'].apply(lambda x:'Authorisation Done' if not x=='Awaiting' else '')
        new_df3_1=new_df2.copy()
        dp3=new_df3_1[(new_df3_1['Status']=='Batched') & (new_df3_1['LMS Sync Status']=='Awaiting') & (new_df3_1['Receipt Batch: Hand Off Status']=='Approved')]
        new_df3_1.loc[dp3.index,'Remarks'] = 'Handedoff to Teller'
        dp4=new_df3_1[(new_df3_1['Status']=='Batched') &(new_df3_1['LMS Sync Status']=='Awaiting') & (new_df3_1['Receipt Batch: Hand Off Status']=='Submitted')]
        new_df3_1.loc[dp4.index,'Remarks'] = 'Handedoff to Teller'
        dp6=new_df3_1[(new_df3_1['Status']=='Batched') & (new_df3_1['LMS Sync Status']=='Awaiting') & (new_df3_1['Challan Status']=='Pending for Approval')]
        new_df3_1.loc[dp6.index,'Remarks'] = 'Handedoff to Teller'
        fin=new_df3_1.copy()
        fill_condition_=(fin['LMS Sync Status']=='Awaiting') & (fin['Challan Status']=='Challan Details Pending')
        fin.loc[fill_condition_,'Remarks']='Pending For Challan Image Upload'

        dp2=fin[(fin['LMS Sync Status']=='Awaiting') & (fin['Challan Status']=='Requested for Authorization')]
        fin.loc[dp2.index,'Remarks'] = 'Challan Authorisation Pending'

        rej=fin[(fin['LMS Sync Status']=='Awaiting') & (fin['Challan Status']=='Rejected ')]
        fin.loc[rej.index,'Remarks'] = 'Challan Authorisation Pending'

        new_df3=fin.copy()

        fill_condition_1=(new_df3['Remarks']=='') & (new_df3['Status']=='Ready for Batching')
        new_df3.loc[fill_condition_1,'Remarks']='Batch Id Not created'

        new_df4=new_df3.copy()

        #new_df4.info()

        new_df4['CBC']= pd.Series(dtype='object')
        new_df4['AFC']= pd.Series(dtype='object')
        new_df4['FVC']= pd.Series(dtype='object')
        new_df4['CustomerID']= pd.Series(dtype='object')
        new_df4['Customer Name']= pd.Series(dtype='object')
        new_df4['SHORTFALL_RECOVERY']= pd.Series(dtype='object')
        new_df4['Others']= pd.Series(dtype='object')
        new_df4['LMS Branch']= pd.Series(dtype='object')
        new_df4['BATCHID']= pd.Series(dtype='object')

        update=new_df4.copy()

        #update.info()

        update_1=update.iloc[:, [24,25,26,27,28,0,1,4,43,42,6,29,7,9,11,5,10,39,40,41,44,45,20,2,46,47,8,21,22,23,38,30,31,37,36,35,32,33,34]]

        fg1=update_1.rename({'COLOUR':'Stage','Created By: Employee Number':'COLLECTIONAGENTID','Created By: Full Name':'COLLECTIONAGENTNAME','Agreement No: Agreement Number':'Agreement No','STATE HEAD':'STATE','BRANCH.1':'BRANCH','ReceiptCreatedDateTime':'RECEIPTENTERED_DATE','Amount':'Receipt Amount','Payment Mode':'Pay_Mode','Record Type':'Receipt Type','Source':'RECEIPT SOURCE','Bank Name':'CHALLANNO','Receipt Batch: Hand Off Status':'EMI','LMS Sync Status':'CHALLANIMAGE','Challan Status':'CHALLANAUTHORISED'},axis=1)

        fg1['Remarks']= np.where((fg1['Remarks']=='') & (fg1['Status']=='Batched'),'Handsoff Not Done',fg1['Remarks'])

        output_path = os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan Status.csv')
        fg1.to_csv(output_path, index=False)
        
        response = HttpResponse(open(output_path, 'rb').read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Challan Status.csv"'
        
        return response
    
    except Exception as e:
        # Handle any exceptions
        return HttpResponse(f'Error: {e}')

# Cash Deposition    
def cash_file(request):
    if request.method == 'POST':
        form_ca = cash_deposition(request.POST, request.FILES)
        if form_ca.is_valid():
            for key, uploaded_file in request.FILES.items():
                custom_filename = 'Cash_' + key 
                cash_uploaded_file(uploaded_file, custom_filename)

            return redirect('blog:runpage') 
    else:
        form_ca = cash_deposition()

    return render(request, 'blog/index.html', {'form': form_ca})

def cash_uploaded_file(uploaded_file, custom_filename):
    destination_folder = os.path.join(settings.MEDIA_ROOT, 'Cash deposition')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    file_extension = os.path.splitext(uploaded_file.name)[1]
    destination_path = os.path.join(destination_folder, f"{custom_filename}{file_extension}")
    
    with open(destination_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

def cash_script(request):
    try:
        #1st File
        df=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_first.csv'),encoding='unicode_escape')
        #2nd File(Emp Id file)
        df1=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_second.csv'),encoding='unicode_escape')
        #3rd File(challan Status file)
        df2=pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_third.csv'),encoding='unicode_escape')
        #4th File(Updated branch file)
        df3=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_four.xlsb'),engine='pyxlsb',sheet_name='Base')
        #5th File(Active list file)
        active_list=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_five.xlsx'))
        #6th File(employee details file)
        emp=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_six.xlsx'))
        #7th File(Time file)
        time=pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'Challan Status', 'Challan_seven.xlsx'))

        df
        df1
        lookup=pd.merge(df,df1[['Created By: Employee Number','Receipt No']],on='Receipt No',how='left')
        df2
        lookup_1 = lookup.merge(df2[['Challan Status','Physical Challan No','Bank Name','Challan: Challan Number']], left_on= 'Receipt Batch: Challan: Challan Number',right_on='Challan: Challan Number', how = 'left')
        f_df=lookup_1[lookup_1['Payment Mode'].isin(['Cash','Cheque','Draft'])]
        f_df['Branch: Account Name']=f_df['Branch: Account Name'].str.upper()
        df3
        df3['FINAL BRANCH']=df3['FINAL BRANCH'].str.upper()
        f_df1= f_df.merge(df3[['ZONE','STATE','REGION','AREA','BRANCH.1','FINAL BRANCH']], left_on= 'Branch: Account Name',right_on='FINAL BRANCH', how = 'left')
        f_df1['Value in Lakhs']=(f_df1['Amount']/100000).round(2)
        #emp=pd.read_excel(r'D:\share\RMR & Active list & Receipt Lwd Back up\employee details.xlsx')
        emp
        f_df2= f_df1.merge(emp[['ROLE','COLOUR','EMPID']], left_on= 'Created By: Employee Number',right_on='EMPID', how = 'left')
        f_df3=f_df2.drop(columns=['EMPID','FINAL BRANCH','Challan: Challan Number'])
        #f_df3.info()
        f_df3['Len']= f_df3['Physical Challan No'].apply(lambda x: len(str(x).strip()) if pd.notna(x) else x)
        #active_list=pd.read_excel(r"D:\share\RMR & Active list & Receipt Lwd Back up\Active List_py.xlsx")
        active_list
        f_df4= f_df3.merge(active_list[['Department','Product','Sub Product','Business Designation','Employee Code']], left_on= 'Created By: Employee Number',right_on='Employee Code', how = 'left')
        f_df4_u=f_df4.drop(columns=['Employee Code'])
        #time=pd.read_excel(r'C:\Users\thameemmj\Desktop\gallop 4Pm.xlsx')
        time
        f_df5= f_df4_u.merge(time[['Timing','Receipt No']],on='Receipt No', how = 'left')
        #f_df5.info()
        new_df=f_df5.copy()
        s_df=new_df['Payment Mode']=='Cash'
        df_1=new_df[s_df]
        df_1
        s_df1=df_1['Source']=='Online App'
        df_2=df_1[s_df1]
        df_2
        df_2['Remarks']=df_2.apply(lambda row:'Airtel Deposition' if row['Bank Name']=='HDFC-IMPS-CA00040310011598CASH COLL' and row['Len']== 17 else ('Fino Pay' if row['Len'] == 11 else ('Ebix Deposition' if row['Len']== 15 else ('Spice Money Deposition' if row['Len']== 20 else None))),axis=1)
        df_2
        df_3=df_2.copy()
        df_3['Remarks'] = df_3.apply(lambda row: 'Bank Deposition' if not pd.isna(row['Bank Name']) and row['Bank Name']!='HDFC-IMPS-CA00040310011598CASH COLL' and row['Bank Name']!= 0 else None if row['Remarks'] is None else row['Remarks'], axis=1)
        df_4=df_3.copy()
        dp1=df_4[(df_4['Physical Challan No'].isna()) & (df_4['Bank Name'].isna())]
        df_4.loc[dp1.index,'Remarks'] = 'Not Deposited'
        df_4
        #df_4.info()
        update=df_4.iloc[:, [24,25,26,27,28,0,1,4,6,29,7,9,11,20,2,22,23,30,31,38,37,32,36,33,34,35]]
        fg1=update.rename({'COLOUR':'Stage','Created By: Employee Number':'COLLECTIONAGENTID','Created By: Full Name':'COLLECTIONAGENTNAME','Agreement No: Agreement Number':'Agreement No','STATE HEAD':'STATE','BRANCH.1':'BRANCH','ReceiptCreatedDateTime':'RECEIPTENTERED_DATE','Amount':'Receipt Amount','Payment Mode':'Pay_Mode','Record Type':'Receipt Type','Source':'RECEIPT SOURCE','Bank Name':'CHALLANNO'},axis=1)
        fg1
        output_path = os.path.join(settings.MEDIA_ROOT, 'Cash deposition', 'Cash deposition.csv')
        fg1.to_csv(output_path, index=False)
        
        response = HttpResponse(open(output_path, 'rb').read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Cash deposition.csv"'
        
        return response
    
    except Exception as e:
        # Handle any exceptions
        return HttpResponse(f'Error: {e}')

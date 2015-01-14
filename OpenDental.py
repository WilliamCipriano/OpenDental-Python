#Imports
import os
import MySQLdb
import MySQLdb.cursors
from datetime import date
import re
import traceback
import sys
import string

#Globals
cur = ""
today = date.today()
path = os.path.dirname(__file__).replace('\\library.zip','')
config = path + '\OpenDentalDatabaseConfig.ini'
errorreporting = path + '\DatabaseErrors.ini'
databaseinfo = []

#Database connection uses the file located at config to load credentials. 
def DatabaseConnection():   
    global cur
    global errorreporting
    global config  
    try:
        config = open(config, 'r')
    except Exception as ex:
        errorlog = open(errorreporting, 'a')
        errorlog.write('\n Config File Loading Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
        errorlog.close()
        return False
    
    try:
        config = config.read().split('=')
        Host = config[1].split('\n')[0]
        Host = Host[1:]
        Username = config[2].split('\n')[0]
        Username = Username[1:]
        Password = config[3].split('\n')[0]
        Password = Password[1:]
        DatabaseName = config[4][1:]
        databaseinfo = [Host, Username, Password, DatabaseName]
    except Exception as ex:
        errorlog = open(errorreporting, 'a')
        errorlog.write('\n Config File Syntax Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
        errorlog.close()
        return False
    
    try:       
        Database = MySQLdb.connect(host=Host,
                                   user=Username,
                                   passwd=Password,
                                   db=DatabaseName,
                                   cursorclass=MySQLdb.cursors.DictCursor)
        cur = Database.cursor()      
    except Exception as ex:
        errorlog = open(errorreporting, 'a')
        errorlog.write('\n MySql Connection Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
        errorlog.close()
        return False
        
    return True

def DefineDatabase(Host,Username,Password,DatabaseName):
    global cur
    global errorreporting
    global config

    try:
        Database = MySQLdb.connect(host=Host,
                                   user=Username,
                                   passwd=Password,
                                   db=DatabaseName,
                                   cursorclass=MySQLdb.cursors.DictCursor)
        cur = Database.cursor()
    except Exception as ex:
        errorlog = open(errorreporting, 'a')
        errorlog.write('\n MySql Connection Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
        errorlog.close()
        return False

    return True
   

def GetPatientDetails(PatNum):
    global today
    global errorreporting   
    try:
        global cur
        PatData = {}
        cur.execute("SELECT * FROM patient WHERE PatNum=" + str(PatNum))
        row = cur.fetchone()
#Last Name
        if (row['LName'] != ''):
            PatData['LastName'] = row['LName']
        else:
            PatData['LastName'] = False
#First Name        
        if (row['FName'] != ''):
            PatData['FirstName'] = row['FName']
        else:
            PatData['FirstName'] = False
#Middle Inital        
        if (row['MiddleI'] != ''):
            PatData['MiddleInitial'] = row['MiddleI']
        else:
            PatData['MiddleInital'] = False
#Nick Name        
        if (row['Preferred'] != ''):
            PatData['PreferredName'] = row['Preferred']
        else:
            PatData['PreferredName'] = False
#Status
        if (row['PatStatus'] == 0):
            PatData['Status'] = 'Patient'
        elif (row['PatStatus'] == 1):
            PatData['Status'] = 'Non-Patient'
        elif (row['PatStatus'] == 2):
            PatData['Status'] = 'Inactive'
        elif (row['PatStatus'] == 3):
            PatData['Status'] = 'Archived'
        elif (row['PatStatus'] == 4):
            PatData['Status'] = 'Deleted'
        elif (row['PatStatus'] == 5):
            PatData['Status'] = 'Deceased'
        elif (row['PatStatus'] == 6):
            PatData['Status'] = 'Prospective'
        elif (row['PatStatus'] == ''):
            PatData['Status'] = False
        else:
            PatData['Status'] = row['PatStatus']
#Gender
        if (row['Gender'] == 0):
            PatData['Gender'] = 'Male'
        elif (row['Gender'] == 1):
            PatData['Gender'] = 'Female'
        elif (row['Gender'] == 2):
            PatData['Gender'] = 'Unknown'
        else:
            PatData['Gender'] = False
#Marital Status
        if (row['Position'] == 0):
            PatData['MaritalStatus'] = 'Single'
        elif (row['Position'] == 1):
            PatData['MaritalStatus'] = 'Married'
        elif (row['Position'] == 2):
            PatData['MaritalStatus'] = 'Child'
        elif (row['Position'] == 3):
            PatData['MaritalStatus'] = 'Widowed'
        elif (row['Position'] == 4):
            PatData['MaritalStatus'] = 'Divorced'
        else:
            PatDate['MaritalStatus'] = False
#Birthday and Age            
        if (row['Birthdate'] != ''):
            PatData['Birthday'] = row['Birthdate']
            PatData['Age'] = today.year - PatData['Birthday'].year - ((today.month, today.day) < (PatData['Birthday'].month, PatData['Birthday'].day))
        else:
            PatData['Birthday'] = False
            PatData['Age'] = False
#Social Security Number
        if (row['SSN'] != ''):    
            PatData['SocialSecurityNumber'] = row['SSN']
        else:
            PatData['SocialSecurityNumber'] = False
#Address Line One
        if (row['Address'] != ''):
            PatData['Address'] = row['Address']
        else:
            PatData['Address'] = False
#Address Line Two
        if (row['Address2'] != ''):
            PatData['Address2'] = row['Address2']
        else:
            PatData['Address2'] = False
#City
        if (row['City'] != ''):
            PatData['City'] = row['City']
        else:
            PatData['City'] = False
#State
        if (row['State'] != ''):
            PatData['State'] = row['State']
        else:
            PatData['State'] = False
#Postal Code
        if (row['Zip'] != ''):
            PatData['PostalCode'] = row['Zip']
        else:
            PatData['PostalCode'] = False
#Home Phone
        if (row['HmPhone'] != ''):
            PatData['HomePhone'] = re.findall(r'\w+', row['HmPhone'])
        else:
            PatData['HomePhone'] = False
#Work Phone
        if (row['WkPhone'] != ''):
            PatData['WorkPhone'] = re.findall(r'\w+', row['WkPhone'])
        else:
            PatData['WorkPhone'] = False
#Cell Phone
        if (row['WirelessPhone'] != ''):
            PatData['CellPhone'] = re.findall(r'\w+', row['WirelessPhone'])
        else:
            PatData['CellPhone'] = False
#Guarantor
        if (row['Guarantor'] != ''):
            PatData['Guarantor'] = row['Guarantor']
        else:
            PatData['Guarantor'] = False
#Credit Type
        if (row['CreditType'] != ''):
            PatData['Credit'] = row['CreditType']
        else:
            PatData['Credit'] = False
#Email
        if (row['Email'] != ''):
            PatData['Email'] = row['Email']
        else:
            PatData['Email'] = False
#Salutation
        if (row['Salutation'] != ''):
            PatData['Salutation'] = row['Salutation']
        else:
            PatData['Salutation'] = False
#Individual Balance
        if (row['EstBalance'] != ''):
            PatData['IndividualBalance'] = round(row['EstBalance'],2)
        else:
            PatData['IndividualBalance'] = False
#Primary Provider
        if (row['PriProv'] != ''):
            try:
                cur.execute("SELECT * FROM provider WHERE ProvNum='" + str(row['PriProv']) + "'")
                prov = cur.fetchone()
                providerlookup = True
                if (prov['MI'] != ''):
                    PatData['PrimaryProvider'] = prov['FName'] + " " + prov['MI'] + ". " + prov['LName']
                else:
                    PatData['PrimaryProvider'] = prov['FName'] + " " + prov['LName']
            except Exception as ex:
                errorlog = open(errorreporting, 'a')
                errorlog.write('\n Patient Provider Lookup Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
                errorlog.close()
                providerlookup = False
        else:
            PatData['PrimaryProvider'] = False
#Provider Specialty
        if (providerlookup):
            if (prov['Specialty'] != ''):
                if (prov['Specialty'] == 0):
                    PatData['PrimaryProviderSpecialty'] = 'General Dentist'
                elif (prov['Specialty'] == 1):
                    PatData['PrimaryProviderSpecialty'] = 'Hygienist'
                elif (prov['Specialty'] == 2):
                    PatData['PrimaryProviderSpecialty'] = 'Endodontist'
                elif (prov['Specialty'] == 3):
                    PatData['PrimaryProviderSpecialty'] = 'Pediatrician'
                elif (prov['Specialty'] == 4):
                    PatData['PrimaryProviderSpecialty'] = 'Periodontal'
                elif (prov['Specialty'] == 5):
                    PatData['PrimaryProviderSpecialty'] = 'Prosthodontic'
                elif (prov['Specialty'] == 6):
                    PatData['PrimaryProviderSpecialty'] = 'Orthodontic'
                elif (prov['Specialty'] == 7):
                    PatData['PrimaryProviderSpecialty'] = 'Denturist'
                elif (prov['Specialty'] == 8):
                    PatData['PrimaryProviderSpecialty'] = 'Oral Surgeon'
                elif (prov['Specialty'] == 9):
                    PatData['PrimaryProviderSpecialty'] = 'Assistant'
                elif (prov['Specialty'] == 10):
                    PatData['PrimaryProviderSpecialty'] = 'Lab Technician'
                elif (prov['Specialty'] == 11):
                    PatData['PrimaryProviderSpecialty'] = 'Pathologist'
                elif (prov['Specialty'] == 12):
                    PatData['PrimaryProviderSpecialty'] = 'Public Health Specialist'
                elif (prov['Specialty'] == 12):
                    PatData['PrimaryProviderSpecialty'] = 'Radiologist'
                else:
                    PatData['PrimaryProviderSpecialty'] = 'Dentist'
        else:
            PatData['PrimaryProviderSpecialty'] = False
#Primary Provider Suffix
        if (providerlookup):
            if (prov['Suffix'] != ''):
                PatData['PrimaryProviderSuffix'] = prov['Suffix']
            else:
                PatData['PrimaryProviderSuffix'] = False
        else:
            PatData['PrimaryProviderSuffix'] = False
#Secondary Provider
        if (row['SecProv'] != ''):
            try:
                cur.execute("SELECT * FROM provider WHERE ProvNum='" + str(row['PriProv']) + "'")
                prov = cur.fetchone()
                providerlookup = True
                if (prov['MI'] != ''):
                    PatData['SecondaryProvider'] = prov['FName'] + " " + prov['MI'] + ". " + prov['LName']
                else:
                    PatData['SecondaryProvider'] = prov['FName'] + " " + prov['LName']
            except Exception as ex:
                errorlog = open(errorreporting, 'a')
                errorlog.write('\n Patient Provider Lookup Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
                errorlog.close()
                providerlookup = False
        else:
            PatData['SecondaryProvider'] = False
#Provider Specialty
        if (providerlookup):
            if (prov['Specialty'] != ''):
                if (prov['Specialty'] == 0):
                    PatData['SecondaryProviderSpecialty'] = 'General Dentist'
                elif (prov['Specialty'] == 1):
                    PatData['SecondaryProviderSpecialty'] = 'Hygienist'
                elif (prov['Specialty'] == 2):
                    PatData['SecondaryProviderSpecialty'] = 'Endodontist'
                elif (prov['Specialty'] == 3):
                    PatData['SecondaryProviderSpecialty'] = 'Pediatrician'
                elif (prov['Specialty'] == 4):
                    PatData['SecondaryProviderSpecialty'] = 'Periodontal'
                elif (prov['Specialty'] == 5):
                    PatData['SecondaryProviderSpecialty'] = 'Prosthodontic'
                elif (prov['Specialty'] == 6):
                    PatData['SecondaryProviderSpecialty'] = 'Orthodontic'
                elif (prov['Specialty'] == 7):
                    PatData['SecondaryProviderSpecialty'] = 'Denturist'
                elif (prov['Specialty'] == 8):
                    PatData['SecondaryProviderSpecialty'] = 'Oral Surgeon'
                elif (prov['Specialty'] == 9):
                    PatData['SecondaryProviderSpecialty'] = 'Assistant'
                elif (prov['Specialty'] == 10):
                    PatData['SecondaryProviderSpecialty'] = 'Lab Technician'
                elif (prov['Specialty'] == 11):
                    PatData['SecondaryProviderSpecialty'] = 'Pathologist'
                elif (prov['Specialty'] == 12):
                    PatData['SecondaryProviderSpecialty'] = 'Public Health Specialist'
                elif (prov['Specialty'] == 12):
                    PatData['SecondaryProviderSpecialty'] = 'Radiologist'
                else:
                    PatData['SecondaryProviderSpecialty'] = 'Dentist'
        else:
            PatData['SecondaryProviderSpecialty'] = False
#Secondary Provider Suffix
        if (providerlookup):
            if (prov['Suffix'] != ''):
                PatData['SecondaryProviderSuffix'] = prov['Suffix']
            else:
                PatData['SecondaryProviderSuffix'] = False
        else:
            PatData['SecondaryProviderSuffix'] = False
#Fee Schedule
        if (row['FeeSched'] != '' and row['FeeSched'] != 0):
            try:
                cur.execute("SELECT Description FROM feesched WHERE FeeSchedNum =" + str(row['FeeSched']) + "")
                fee = cur.fetchone()
                PatData['FeeSchedule'] = fee['Description']
            except Exception as ex:
                errorlog = open(errorreporting, 'a')
                errorlog.write('\n Patient Fee Schedule Lookup Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
                errorlog.close()
                PatData['FeeSchedule'] = False
        else:
            PatData['FeeSchedule'] = False
#Billing Type
        if (row['BillingType'] != ''):
            try:
                cur.execute("SELECT ItemName FROM definition WHERE DefNum ='" + str(row['BillingType']) + "'")
                bill = cur.fetchone()
                PatData['BillingType'] = bill['ItemName']
            except Exception as ex:
                errorlog = open('C:\Users\Dentex\Desktop\GetCopay\Errors.log', 'a')
                errorlog.write('\n Patient Billing Type Lookup Error: ' + str(ex))
                errorlog.close()
                PatData['FeeSchedule'] = False
#Image Folder, Category, and Image
        if (row['ImageFolder'] != ''):
            PatData['ImageFolder'] = row['ImageFolder']
            try:
                cur.execute("SELECT DefNum FROM definition WHERE ItemName = 'Patient Pictures' AND IsHidden=0")
                define = cur.fetchone()
                PatData['PatientPicturesCategory'] = define['DefNum']
                cur.execute("SELECT * FROM document WHERE PatNum = '" + str(PatNum) + "' AND DocCategory = " + str(PatData['PatientPicturesCategory']))
                define = cur.fetchone()
                if (define):
                    PatData['Image'] = define['FileName']
                else:
                    PatData['Image'] = False
            except Exception as ex:
                errorlog = open(errorreporting, 'a')
                errorlog.write('\n Patient Image Lookup Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
                errorlog.close()
                PatData['FeeSchedule'] = False
        else:
            PatData['ImageFolder'] = False
#Contact Note
        if (row['AddrNote'] != ''):
            PatData['ContactNote'] = row['AddrNote']
        else:
            PatData['ContactNote'] = False
#Financial Note
        if (row['FamFinUrgNote'] != ''):
            PatData['FinancialNote'] = row['FamFinUrgNote']
        else:
            PatData['FinancialNote'] = False
#Medical Notes
        if (row['MedUrgNote'] != ''):
            PatData['MedicalNote'] = row['MedUrgNote']
        else:
            PatData['MedicalNote'] = False
#Appointment Note
        if (row['ApptModNote'] != ''):
            PatData['AppointmentNote'] = row['ApptModNote']
        else:
            PatData['AppointmentNote'] = False
#Student Status
        if (row['StudentStatus'] == ''):
            PatData['StudentStatus'] = 'Nonstudent'
        else:
            if (row['StudentStatus'] == 'N'):
                PatData['StudentStatus'] = 'Nonstudent'
            elif (row['StudentStatus'] == 'P'):
                PatData['StudentStatus'] = 'Part Time'
            elif (row['StudentStatus'] == 'F'):
                PatData['StudentStatus'] = 'Full Time'
            else:
                PatData['StudentStatus'] = row['StudentStatus']
#School Name
        if (row['SchoolName'] != ''):
            PatData['School'] = row['SchoolName']
        else:
            PatData['School'] = False
#Chart Number
        if (row['ChartNumber'] != ''):
            PatData['Chart'] = row['ChartNumber']
        else:
            PatData['Chart'] = False
#Medicaid ID
        if (row['MedicaidID'] != ''):
            PatData['MedicaidID'] = row['MedicaidID']
        else:
            PatData['MedicaidID'] = False
#Thirty Day Balance
        if (row['Bal_0_30'] != ''):
            PatData['30DayBalance'] = round(row['Bal_0_30'],2)
        else:
            PatData['30DayBalance'] = False
#Sixty Day Balance
        if (row['Bal_31_60'] != ''):
            PatData['60DayBalance'] = round(row['Bal_31_60'],2)
        else:
            PatData['60DayBalance'] = False
#Ninty Day Balance
        if (row['Bal_61_90'] != ''):
            PatData['90DayBalance'] = round(row['Bal_61_90'],2)
        else:
            PatData['90DayBalance'] = False
#Over Ninty Day Balance
        if (row['BalOver90'] != ''):
            PatData['90DayPlusBalance'] = round(row['BalOver90'],2)
        else:
            PatData['90DayPlusBalance'] = False
#Insurance Estimate
        if (row['InsEst'] != ''):
            PatData['InsuranceEstimate'] = round(row['InsEst'],2)
        else:
            PatData['InsuranceEstimate'] = False
#Total Balance
        if (row['BalTotal'] != ''):
            PatData['Balance'] = round(row['BalTotal'],2)
        else:
            PatData['Balance'] = False
#Employer Data
        if (row['EmployerNum'] != '' and row['EmployerNum'] != 0):
            try:
                cur.execute("SELECT * FROM employer WHERE EmployerNum = " + str(row['EmployerNum']))
                employer = cur.fetchone()
                PatData['Employer'] = employer['EmpName']
                PatData['EmployerAddress'] = employer['Address']
                PatData['EmployerAddress2'] = employer['Address2']
                PatData['EmployerCity'] = employer['City']
                PatData['EmployerState'] = employer['State']
                PatData['EmployerZip'] = employer['Zip']
                PatData['EmployerPhone'] = re.findall(r'\w+',employer['Phone'])
                PatData['EmployerNumber'] = row['EmployerNum']
            except Exception as ex:
                errorlog = open(errorreporting, 'a')
                errorlog.write('\n Employer Lookup Error: ' + str(ex))
                errorlog.close()
                PatData['Employer'] = False
                PatData['EmployerAddress'] = False
                PatData['EmployerAddress2'] = False
                PatData['EmployerCity'] = False
                PatData['EmployerState'] = False
                PatData['EmployerPostalCode'] = False
                PatData['EmployerPhone'] = False
                PatData['EmployerNumber'] = False
        else:
            PatData['Employer'] = False
            PatData['EmployerAddress'] = False
            PatData['EmployerAddress2'] = False
            PatData['EmployerCity'] = False
            PatData['EmployerState'] = False
            PatData['EmployerZip'] = False
            PatData['EmployerPhone'] = False
#Race
            if (row['Race'] != False):
                if (row['Race'] == 0):
                    PatData['Race'] = 'Unknown'
                elif (row['Race'] == 1):
                    PatData['Race'] = 'Multiracial'
                elif (row['Race'] == 2):
                    PatData['Race'] = 'Hispanic/Latino'
                elif (row['Race'] == 3):
                    PatData['Race'] = 'African American'
                elif (row['Race'] == 4):
                    PatData['Race'] = 'Caucasian'
                elif (row['Race'] == 5):
                    PatData['Race'] = 'Hawaiian or Pacific Islander'
                elif (row['Race'] == 6):
                    PatData['Race'] = 'Native American'
                elif (row['Race'] == 7):
                    PatData['Race'] = 'Asian'
                elif (row['Race'] == 8):
                    PatData['Race'] = 'Other'
                elif (row['Race'] == 9):
                    PatData['Race'] = 'Aboriginal'
                elif (row['Race'] == 10):
                    PatData['Race'] = 'Black Hispanic'
                else:
                    PatData['Race'] = row['Race']
            else:
                PatData['Race'] = False
#County
        if (row['County'] != ''):
            PatData['County'] = row['County']
        else:
            PatData['County'] = False
#Grade Level
        if (row['GradeLevel'] != '' and row['GradeLevel'] != 0):
            if (row['GradeLevel'] == 13):
                PatData['Grade'] = 'Prenatal'
            elif (row['GradeLevel'] == 14):
                PatData['Grade'] = 'Prekindergarten'
            elif (row['GradeLevel'] == 15):
                PatData['Grade'] = 'Kindergarten'
            elif (row['GradeLevel'] == 16):
                PatData['Grade'] = 'Other'
            else:
                PatData['Grade'] = row['GradeLevel']
#Date of first vist
        if (row['DateFirstVisit'] != ''):
            PatData['FirstVisit'] = row['DateFirstVisit']
        else:
            PatData['FirstVisit'] = False
#Has Insurance                  
        if (row['HasIns'] == "I"):
            PatData['HasInsurance'] = True
        else:
            PatData['HasInsurance'] = False
#Premedicated
        if (row['Premed'] == 1):
            PatData['Premedicated'] = True
        else:
            PatData['Premedicated'] = False
#Prefered Confirm Method
        if (row['PreferConfirmMethod'] != ''):
            if (row['PreferConfirmMethod'] == 0):
                PatData['ConfirmMethod'] = 'None Specified'
            elif (row['PreferConfirmMethod'] == 1):
                PatData['ConfirmMethod'] = 'Do Not Call'
            elif (row['PreferConfirmMethod'] == 2):
                PatData['ConfirmMethod'] = 'Home Phone'
            elif (row['PreferConfirmMethod'] == 3):
                PatData['ConfirmMethod'] = 'Work Phone'
            elif (row['PreferConfirmMethod'] == 4):
                PatData['ConfirmMethod'] = 'Cell Phone'
            elif (row['PreferConfirmMethod'] == 5):
                PatData['ConfirmMethod'] = 'Email'
            elif (row['PreferConfirmMethod'] == 6):
                PatData['ConfirmMethod'] = 'Check Notes'
            elif (row['PreferConfirmMethod'] == 7):
                PatData['ConfirmMethod'] = 'Postal Mail'
            elif (row['PreferConfirmMethod'] == 8):
                PatData['ConfirmMethod'] = 'Text Message'
#Prefered Contact Method
        if (row['PreferContactMethod'] != ''):
            if (row['PreferContactMethod'] == 0):
                PatData['ContactMethod'] = 'None Specified'
            elif (row['PreferContactMethod'] == 1):
                PatData['ContactMethod'] = 'Do Not Call'
            elif (row['PreferContactMethod'] == 2):
                PatData['ContactMethod'] = 'Home Phone'
            elif (row['PreferContactMethod'] == 3):
                PatData['ContactMethod'] = 'Work Phone'
            elif (row['PreferContactMethod'] == 4):
                PatData['ContactMethod'] = 'Cell Phone'
            elif (row['PreferContactMethod'] == 5):
                PatData['ContactMethod'] = 'Email'
            elif (row['PreferContactMethod'] == 6):
                PatData['ContactMethod'] = 'Check Notes'
            elif (row['PreferContactMethod'] == 7):
                PatData['ContactMethod'] = 'Postal Mail'
            elif (row['PreferContactMethod'] == 8):
                PatData['ContactMethod'] = 'Text Message'
#Prefered Recall Method
        if (row['PreferRecallMethod'] != ''):
            if (row['PreferRecallMethod'] == 0):
                PatData['RecallMethod'] = 'None Specified'
            elif (row['PreferRecalltMethod'] == 1):
                PatData['RecallMethod'] = 'Do Not Call'
            elif (row['PreferRecallMethod'] == 2):
                PatData['RecallMethod'] = 'Home Phone'
            elif (row['PreferRecallMethod'] == 3):
                PatData['RecallMethod'] = 'Work Phone'
            elif (row['PreferRecallMethod'] == 4):
                PatData['RecallMethod'] = 'Cell Phone'
            elif (row['PreferRecallMethod'] == 5):
                PatData['RecallMethod'] = 'Email'
            elif (row['PreferRecallMethod'] == 6):
                PatData['RecallMethod'] = 'Check Notes'
            elif (row['PreferRecallMethod'] == 7):
                PatData['RecallMethod'] = 'Postal Mail'
            elif (row['PreferRecallMethod'] == 8):
                PatData['RecallMethod'] = 'Text Message'
#Schedule Before Time
        if (row['SchedBeforeTime'] != ''):
            PatData['ScheduleBefore'] = row['SchedBeforeTime']
        else:
            PatData['ScheduleBefore'] = False
#Schedule After Time
        if (row['SchedAfterTime'] != ''):
            PatData['ScheduleAfter'] = row['SchedAfterTime']
        else:
            PatData['ScheduleAfter'] = False
#Schedule Day of the Week
        if (row['SchedDayOfWeek'] != ''):
            PatData['ScheduleDay'] = row['SchedDayOfWeek']
        else:
            PatData['ScheduleDay'] = False
#Language
        if (row['Language'] == 'en'):
            PatData['Language'] = 'English'
        elif (row['Language'] == 'fr'):
            PatData['Language'] = 'French'
        elif (row['Language'] == 'es'):
            PatData['Language'] = 'Spanish'
        elif (row['Language'] == ''):
            PatData['Language'] = False
        else:
            PatData['PrimaryLanguage'] = row['Language']
#Admit Date
        if (row['AdmitDate'] != ''):
            PatData['AdmissionDate'] = row['AdmitDate']
        else:
            PatData['AdmissionDate'] = False
#Title
        if (row['Title'] != ''):
            PatData['Title'] = row['Title']
        else:
            PatData['Title'] = False
#Pay Plan Due
        if (row['PayPlanDue'] != ''):
            PatData['PayPlanDueDate'] = row['PayPlanDue']
        else:
            PatData['PayPlanDueDate'] = False
#Site Number, Description, and Note
        if (row['SiteNum'] != '' and row['SiteNum'] != 0):
            try:
                cur.execute("SELECT * FROM site WHERE SiteNum = " + str(row['SiteNum']))
                site = cur.fetchone()
                PatData['Site'] = row['SiteNum']
                if (site['Description'] != ''):
                    PatData['SiteDescription'] = site['Description']
                else:
                    PatData['SiteDescription'] = False
                if (site['Note'] != ''):
                    PatData['SiteNote'] = site['Note']
                else:
                    PatData['SiteNote'] = False
            except Exception as ex:
                errorlog = open(errorreporting, 'a')
                errorlog.write('\n Site Sql Query Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
                errorlog.close()
#Last Edit
        if (row['DateTStamp'] != ''):
            PatData['LastEdit'] = row['DateTStamp']
        else:
            PatData['LastEdit'] = False
#Medical Decision Maker
        if (row['ResponsParty'] != '' and row['ResponsParty'] != 0):
            try:
                cur.execute("SELECT Address, Address2, City, State, Zip, FName, LName, MiddleI, WorkPhone, HomePhone, WirelessPhone, Email FROM patient WHERE PatNum = " + str(row['ResponsParty']))
                decider = cur.fetchone()
                if (decider['MiddleI'] != ''):
                    PatData['DeciderName'] = decider['FName'] + " " + decider['MiddleI'] + " " + decider['LName']
                else:
                    PatData['DeciderName'] = decider['FName'] + " " + decider['LName']
                PatData['Decider'] = row['ResponsParty']
                PatData['DeciderAddress'] = decider['Address']
                PatData['DeciderAddress2'] = decider['Address2']
                PatData['DeciderCity'] = decider['City']
                PatData['DeciderState'] = decider['State']
                PatData['DeciderPostalCode'] = decider['Zip']
                PatData['DeciderHomePhone'] = re.findall(r'\w+',decider['HmPhone'])
                PatData['DeciderWorkPhone'] = re.findall(r'\w+',decider['WkPhone'])
                PatData['DeciderCellPhone'] = re.findall(r'\w+',decider['WirelessPhone'])
                PatData['DeciderEmail'] = decider['Email']            
            except Exception as ex:
                errorlog = open(errorreporting, 'a')
                errorlog.write('\n Decider Sql Query Error: ' + str(ex))
                errorlog.close()
        else:
            PatData['DeciderName'] = False
            PatData['Decider'] = False
            PatData['DeciderAddress'] = False
            PatData['DeciderAddress2'] = False
            PatData['DeciderCity'] = False
            PatData['DeciderState'] = False
            PatData['DeciderPostalCode'] = False
            PatData['DeciderHomePhone'] = False
            PatData['DeciderWorkPhone'] = False
            PatData['DeciderCellPhone'] = False
            PatData['DeciderEmail'] = False
#Canadian Eligibility Code
        if (row['CanadianEligibilityCode'] != '' and row['CanadianEligibilityCode'] != 0):
            if (row['CanadianEligibilityCode'] == 1):
                PatData['CEcode'] = 'Full Time Student'
            elif (row['CanadianEligibiltyCode'] == 2):
                PatData['CEcode'] = 'Disabled'
            elif (row['CanadianEligibiltyCode'] == 3):
                PatData['CEcode'] = 'Disabled Student'
            elif (row['CandianEligibiltyCode'] == 4):
                PatData['CEcode'] = 'Not Applicable'
            else:
                PatData['CEcode'] = False
        else:
            PatData['CEcode'] = False
#Asked to arrive early
        if (row['AskToArriveEarly'] != ''):
            PatData['ArriveEarly'] = row['AskToArriveEarly']
        else:
            PatData['ArriveEarly'] = False
#Online Password
        if (row['OnlinePassword'] != ''):
            PatData['Password'] = row['OnlinePassword']
        else:
            PatData['Password'] = False
#Prefer Contact Confidential
        if (row['PreferContactConfidential'] != ''):
            if (row['PreferContactConfidential'] == 0):
                PatData['ContactConfidential'] = 'None Specified'
            elif (row['PreferContactConfidential'] == 1):
                PatData['ContactConfidential'] = 'Do Not Call'
            elif (row['PreferContactConfidential'] == 2):
                PatData['ContactConfidential'] = 'Home Phone'
            elif (row['PreferContactConfidential'] == 3):
                PatData['ContactConfidential'] = 'Work Phone'
            elif (row['PreferContactConfidential'] == 4):
                PatData['ContactConfidential'] = 'Cell Phone'
            elif (row['PreferContactConfidential'] == 5):
                PatData['ContactConfidential'] = 'Email'
            elif (row['PreferContactConfidential'] == 6):
                PatData['ContactConfidential'] = 'Check Notes'
            elif (row['PreferContactConfidential'] == 7):
                PatData['ContactConfidential'] = 'Postal Mail'
            elif (row['PreferContactConfidential'] == 8):
                PatData['ContactConfidential'] = 'Text Message'
        else:
            PatData['ContactConfidential'] = False
#Super Family
        if (row['SuperFamily'] != '' and row['SuperFamily'] != 0 and row['SuperFamily'] != PatNum ):
            try:
                cur.execute("SELECT Address, Address2, City, State, Zip, FName, LName, MiddleI, WorkPhone, HomePhone, WirelessPhone, Email FROM patient WHERE PatNum = " + str(row['SuperFamily']))
                guarantor = cur.fetchone()
                if (guarantor ['MiddleI'] != ''):
                    PatData['GuarantorName'] = guarantor['FName'] + " " + guarantor['MiddleI'] + " " + guarantor['LName']
                else:
                    PatData['GuarantorName'] = guarantor['FName'] + " " + guarantor['LName']
                PatData['Guarantor'] = row['SuperFamily']
                PatData['GuarantorAddress'] = guarantor['Address']
                PatData['GuarantorAddress2'] = guarantor['Address2']
                PatData['GuarantorCity'] = guarantor['City']
                PatData['GuarantorState'] = guarantor['State']
                PatData['GuarantorPostalCode'] = guarantor['Zip']
                PatData['GuarantorHomePhone'] = re.findall(r'\w+',guarantor['HmPhone'])
                PatData['GuarantorWorkPhone'] = re.findall(r'\w+',guarantor['WkPhone'])
                PatData['GuarantorCellPhone'] = re.findall(r'\w+',guarantor['WirelessPhone'])
                PatData['GuarantorEmail'] = guarantor['Email']            
            except Exception as ex:
                errorlog = open(errorreporting, 'a')
                errorlog.write('\n Guarantor Sql Query Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
                errorlog.close()
        elif (row['SuperFamily'] == PatNum):
            PatData['Guarantor'] = PatNum
            PatData['GuarantorAddress'] = PatData['Address']
            PatData['GuarantorAddress2'] = PatData['Address2']
            PatData['GuarantorCity'] = PatData['City']
            PatData['GuarantorState'] = PatData['State']
            PatData['GuarantorPostalCode'] = PatData['PostalCode']
            PatData['GuarantorHomePhone'] = PatData['HomePhone']
            PatData['GuarantorWorkPhone'] = PatData['WorkPhone']
            PatData['GuarantorCellPhone'] = PatData['CellPhone']
            PatData['GuarantorEmail'] = PatData['Email']
#Text Message
            if (row['TxtMsgOk'] != ''):
                if (row['TxtMsgOk'] == 0):
                    PatData['TextMessage'] = 'Unknown'
                elif (row['TxtMsgOk'] == 1):
                    PatData['TextMessage'] = True
                elif (row['TxtMsgOk'] == 2):
                    PatData['TextMessage'] = False
            else:
                PatData['TextMessage'] = 'Unknown'
#Procedures
        PatData['ProcedureDate'] = []
        PatData['ProcedureAppointmentNumber'] = []
        PatData['ProcedureFee'] = []
        PatData['ProcedureSurface'] = []
        PatData['ProcedureToothNumber'] = []
        PatData['ProcedureProviderNumber'] = []
        PatData['ProcedureDiagnosis'] = []
        PatData['ProcedureDateCompleted'] = []
        PatData['ProcedureStatment'] = []
        PatData['ProcedureLocked'] = []
        PatData['ProcedureChanged'] = []
        PatData['ProcedureToothRange'] = []
        PatData['ProcedureStatus'] = []
        PatData['ProcedureTreatmentPlannedDate'] = []
        PatData['ProcedureNumber'] = []
        PatData['ProcedureMedicalCode'] = []
        PatData['ProcedureDescription'] = []
        PatData['ProcedureAbbreviatedDescription'] = []
        PatData['ProcedureCategoryNumber'] = []
        PatData['ProcedureLaymenTerm'] = []
        
     
        try:
            cur.execute("SELECT * FROM procedurelog WHERE PatNum = " + PatNum)
            CompletedProcs = cur.fetchall()
            for CompletedProcs in CompletedProcs:
                if (CompletedProcs['ProcDate'] != ''):
                    PatData['ProcedureDate'].append(CompletedProcs['ProcDate'])
                else:
                    PatData['ProcedureDate'].append(False)
                    
                if (CompletedProcs['AptNum'] != ''):
                    PatData['ProcedureAppointmentNumber'].append(CompletedProcs['AptNum'])
                else:
                    PatData['ProcedureAppointmentNumber'].append(False)

                if (CompletedProcs['ProcFee'] != ''):
                    PatData['ProcedureFee'].append(CompletedProcs['ProcFee'])
                else:
                    PatData['ProcedureFee'].append(False)

                if (CompletedProcs['Surf'] != ''):
                    PatData['ProcedureSurface'].append(CompletedProcs['Surf'])
                else:
                    PatData['ProcedureSurface'].append(False)

                if (CompletedProcs['ToothNum'] != ''):
                    PatData['ProcedureToothNumber'].append(CompletedProcs['ToothNum'])
                else:
                    PatData['ProcedureToothNumber'].append(False)

                if (CompletedProcs['ProvNum'] != ''):
                    PatData['ProcedureProviderNumber'].append(CompletedProcs['ProvNum'])
                else:
                    PatData['ProcedureProviderNumber'].append(False)

                if (CompletedProcs['Dx'] != ''):
                    PatData['ProcedureDiagnosis'].append(CompletedProcs['Dx'])
                else:
                    PatData['ProcedureDiagnosis'].append(False)

                if (CompletedProcs['ProcDate'] != ''):
                    PatData['ProcedureDateCompleted'].append(CompletedProcs['ProcDate'])
                else:
                    PatData['ProcedureDateCompleted'].append(False)

                if (CompletedProcs['StatementNum'] != ''):
                    PatData['ProcedureStatment'].append(CompletedProcs['StatementNum'])
                else:
                    PatData['ProcedureStatment'].append(False)

                if (CompletedProcs['IsLocked'] == 0):
                    PatData['ProcedureLocked'].append(False)
                elif (CompletedProcs['IsLocked'] == 1):
                    PatData['ProcedureLocked'].append(True)

                if (CompletedProcs['DateTStamp'] != ''):
                    PatData['ProcedureChanged'].append(CompletedProcs['DateTStamp'])
                else:
                    PatData['ProcedureChanged'].append(False)

                if (CompletedProcs['ToothRange'] != ''):
                    PatData['ProcedureToothRange'].append(CompletedProcs['ToothRange'])
                else:
                    PatData['ProcedureToothRange'].append(False)

                if (CompletedProcs['DateTP'] != ''):
                    PatData['ProcedureTreatmentPlannedDate'].append(CompletedProcs['DateTP'])
                else:
                    PatData['ProcedureTreatmentPlannedDate'].append(False)
                    
                if (CompletedProcs['ProcStatus'] == 1):
                    PatData['ProcedureStatus'].append('Treatment Plan')
                elif (CompletedProcs['ProcStatus'] == 2):
                    PatData['ProcedureStatus'].append('Complete')
                elif (CompletedProcs['ProcStatus'] == 3):
                    PatData['ProcedureStatus'].append('Existing Current Provider')
                elif (CompletedProcs['ProcStatus'] == 4):
                    PatData['ProcedureStatus'].append('Existing Other Provider')
                elif (CompletedProcs['ProcStatus'] == 5):
                    PatData['ProcedureStatus'].append('Referred Out')
                elif (CompletedProcs['ProcStatus'] == 6):
                    PatData['ProcedureStatus'].append('Deleted')
                elif (CompletedProcs['ProcStatus'] == 7):
                    PatData['ProcedureStatus'].append('Condition')
                else:
                    PatData['ProcedureStatus'] = False

                if (CompletedProcs['ProcNum'] != ''):
                    PatData['ProcedureNumber'].append(CompletedProcs['ProcNum'])
                else:
                    PatData['ProcedureNumber'].append(False)

                if (CompletedProcs['CodeNum'] != ''):
                    PatData['ProcedureCodeNumber'] = CompletedProcs['MedicalCode']
                else:
                    PatData['ProcedureCodeNumber'] = False

                if (PatData['ProcedureCodeNumber'] != False):
                     cur.execute("SELECT ProcCode, Descript, AbbrDesc, LaymanTerm, ProcCat FROM procedurecode WHERE CodeNum = " + str(CompletedProcs['CodeNum']))
                     Code = cur.fetchone()
                     if (Code['ProcCode'] != ''):
                         PatData['ProcedureMedicalCode'].append(Code['ProcCode'])
                     else:
                         PatData['ProcedureMedicalCode'].append(False)
                         
                     if (Code['Descript'] != ''):
                         PatData['ProcedureDescription'].append(Code['Descript'])
                     else:
                         PatData['ProcedureDescription'].append(False)
                         
                     if (Code['AbbrDesc'] != ''):
                         PatData['ProcedureAbbreviatedDescription'].append(Code['AbbrDesc'])
                     else:
                         PatData['ProcedureAbbreviatedDescription'].append(False)
                         
                     if (Code['LaymanTerm'] != ''):
                         PatData['ProcedureLaymenTerm'].append(Code['LaymanTerm'])
                     else:
                         PatData['ProcedureLaymenTerm'].append(False)
                         
                     if (Code['ProcCat'] != ''):
                         PatData['ProcedureCategoryNumber'].append(Code['ProcCat'])
                     else:
                         PatData['ProcedureCategoryNumber'].append(False)
                         

                    
                 
        except Exception as ex:
            errorlog = open(errorreporting, 'a')
            errorlog.write('\n Procedure Sql Query Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
            errorlog.close()
                
#Appointments and Insurance
        PatData['AppointmentDate'] = []
        PatData['AppointmentStatus'] = []
        PatData['AppointmentNumber'] = []
        
        PatData['AppointmentInsurance1num'] = []
        PatData['AppointmentInsurance1'] = []
        PatData['AppointmentInsurance1type'] = []
        PatData['AppointmentInsurance1carriernumber'] = []
        PatData['AppointmentCopayFeeSchedule1'] = []
        PatData['AppointmentFeeSchedule1'] = []
        
        PatData['AppointmentInsurance2num'] = []
        PatData['AppointmentInsurance2'] = []
        PatData['AppointmentInsurance2type'] = []
        PatData['AppointmentInsurance2carriernumber'] = []
        PatData['AppointmentCopayFeeSchedule2'] = []
        PatData['AppointmentFeeSchedule2'] = []
               
        try:
            cur.execute("SELECT * FROM appointment WHERE PatNum = " + PatNum)
            Appointments = cur.fetchall()
            for Appointment in Appointments:
                if (Appointment['AptDateTime'] != ''):
                    PatData['AppointmentDate'].append(Appointment['AptDateTime'])
                else:
                    Appointment['AptDateTime'].append(False)
                    
                if (Appointment['AptStatus'] == 1):
                    PatData['AppointmentStatus'].append('Scheduled')
                elif (Appointment['AptStatus'] == 2):
                    PatData['AppointmentStatus'].append('Complete')
                elif (Appointment['AptStatus'] == 3):
                    PatData['AppointmentStatus'].append('Not Scheduled')
                elif (Appointment['AptStatus'] == 4):
                    PatData['AppointmentStatus'].append('As Soon As Possible')
                elif (Appointment['AptStatus'] == 5):
                    PatData['AppointmentStatus'].append('Broken')
                elif (Appointment['AptStatus'] == 6):
                    PatData['AppointmentStatus'].append('Planned')
                elif (Appointment['AptStatus'] == 7):
                    PatData['AppointmentStatus'].append('See Note')
                elif (Appointment['AptStatus'] == 8):
                    PatData['AppointmentStatus'].append('Completed/See Note')
                else:
                    PatData['AppointmentStatus'].append(False)

                if (Appointment['AptNum'] != ''):
                    PatData['AppointmentNumber'].append(Appointment['AptNum'])
                else:
                    PatData['AppointmentNumber'].append(False)                  

                if (Appointment['InsPlan1'] != '' and Appointment['InsPlan1'] != 0):
                    try:
                        cur.execute("SELECT * FROM insplan WHERE PlanNum = " + str(Appointment['InsPlan1']))
                        Insurance1 = cur.fetchone()
                        
                        if (Appointment['InsPlan1'] != ''):
                            PatData['AppointmentInsurance1num'].append(Appointment['InsPlan1'])
                        else:
                            PatData['AppointmentInsurance1num'].append(False)
                            

                        if (Insurance1['PlanType'] == ''):
                            PatData['AppointmentInsurance1type'].append('Precentage')
                        elif (Insurance1['PlanType'] == 'p'):
                            PatData['AppointmentInsurance1type'].append('PPO Percentage')
                        elif (Insurance1['PlanType'] == 'f'):
                            PatData['AppointmentInsurance1type'].append('Flat')
                        elif (Insurance1['PlanType'] == 'c'):
                            PatData['AppointmentInsurance1type'].append('Capitation')
                        else:
                            PatData['AppointmentInsurance1type'].append(False)
                            
                        if (Insurance1['CopayFeeSched'] != ''):
                            PatData['AppointmentCopayFeeSchedule1'].append(Insurance1['CopayFeeSched'])
                        else:
                            PatData['AppointmentCopayFeeSchedule1'].append(Insurance1[False])

                        if (Insurance1['FeeSched'] != ''):
                            PatData['AppointmentFeeSchedule1'].append(Insurance1['FeeSched'])
                        else:
                            PatData['AppointmentFeeSchedule1'].append(False)
                                    
                        
                    except Exception as ex:
                        errorlog = open(errorreporting, 'a')
                        errorlog.write('\n Insurance 1 Sql Query Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
                        errorlog.close()

                if (Appointment['InsPlan2'] != '' and Appointment['InsPlan2'] != 0):
                    try:
                        cur.execute("SELECT * FROM insplan WHERE PlanNum = " + str(Appointment['InsPlan2']))
                        Insurance1 = cur.fetchone()
                        PatData['AppointmentInsurance2num'].append(Appointment['InsPlan2'])
                        if (Insurance1['PlanType'] == ''):
                            PatData['AppointmentInsurance2type'].append('Precentage')
                        elif (Insurance1['PlanType'] == 'p'):
                            PatData['AppointmentInsurance2type'].append('PPO Percentage')
                        elif (Insurance1['PlanType'] == 'f'):
                            PatData['AppointmentInsurance2type'].append('Flat')
                        elif (Insurance1['PlanType'] == 'c'):
                            PatData['AppointmentInsurance2type'].append('Capitation')
                        else:
                            PatData['AppointmentInsurance2type'].append(False)
                            
                        if (Insurance2['CopayFeeSched'] != ''):
                            PatData['AppointmentCopayFeeSchedule2'].append(Insurance1['CopayFeeSched'])
                        else:
                            PatData['AppointmentCopayFeeSchedule2'].append(Insurance1[False])
                            
                        if (Insurance1['FeeSched'] != ''):
                            PatData['AppointmentFeeSchedule2'].append(Insurance2['FeeSched'])
                        else:
                            PatData['AppointmentFeeSchedule2'].append(False)
                    except Exception as ex:
                        errorlog = open(errorreporting, 'a')
                        errorlog.write('\n Insurance 2 Sql Query Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
                        errorlog.close()                                                                    

        except Exception as ex:
            errorlog = open(errorreporting, 'a')
            errorlog.write('\n Appointment Sql Query Error: ' + str(ex))
            errorlog.close()
#Claims
        try:
            PatData['ClaimNumber'] = []
            PatData['ClaimProcedureNumber'] = []
            PatData['ClaimInsurancePercentage'] = []
            PatData['ClaimInsurancePercentageOveride'] = []
            PatData['ClaimCopayAmount'] = []
            PatData['ClaimCopayAmountOverride'] = []
            PatData['ClaimDeductible'] = []
            cur.execute("SELECT * FROM claimproc WHERE PatNum = " + str(PatNum))
            Claims = cur.fetchall()
            if Claims:
                for Claim in Claims:
                    if (Claim['ClaimNum'] != ''):
                        PatData['ClaimNumber'].append(Claim['ClaimNum'])
                    else:
                        PatData['ClaimNumber'].append(False)
                        
                    if (Claim['ProcNum'] != ''):
                        PatData['ClaimProcedureNumber'].append(Claim['ProcNum'])
                    else:
                        PatData['ClaimProcedureNumber'].append(False)

                    if (Claim['Percentage'] != ''):
                        PatData['ClaimInsurancePercentage'].append(Claim['Percentage'])
                    else:
                        PatData['ClaimInsurancePercentage'].append(False)

                    if (Claim['PercentOverride'] != ''):
                        PatData['ClaimInsurancePercentageOveride'].append(Claim['PercentOverride'])
                    else:
                        PatData['ClaimInsurancePercentageOveride'].append(False)

                    if (Claim['CopayAmt'] != ''):
                        PatData['ClaimCopayAmount'].append(Claim['CopayAmt'])
                    else:
                        PatData['ClaimCopayAmount'].append(False)
                        
                    if (Claim['CopayOverride'] != ''):
                        PatData['ClaimCopayAmountOverride'].append(Claim['CopayOverride'])
                    else:
                        PatData['ClaimCopayAmountOverride'].append(False)

                    if (Claim['DedApplied'] != ''):
                        PatData['ClaimDeductible'].append(Claim['DedApplied'])
                    else:
                        PatData['ClaimDeductible'].append(False)
        except Exception as ex:
            errorlog = open(errorreporting, 'a')
            errorlog.write('\n Claim Sql Query Error: ' + str(ex))
            errorlog.close()                                       
        
    except Exception as ex:
        errorlog = open(errorreporting, 'a')
        errorlog.write('\n Patient Sql Query Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
        errorlog.close()
        return False
    
    return PatData

#Category Lookup Functions
def CategoryNumberLookup(code):
    return CategoryNumberDefinition(CategoryNumberSearch(code))


def CategoryNumberSearch(code):
    global errorreporting
    try:
        all=string.maketrans('','')
        nodigs=all.translate(all, string.digits)
        global cur
        matches = []
        distance = []
        cur.execute("SELECT * FROM covspan")
        coveragespan = cur.fetchall()
        for span in coveragespan:

            From = int(span['FromCode'][1:])

            To = int(span['ToCode'][1:])

            Code = int(code[1:])

            if (span['CovCatNum'] != 1):
                if (From <= Code):
                    if (To >= Code):
                        matches.append(span['CovCatNum'])
                        distance.append(abs(From - To))


        shortest = distance.index(min(distance))
        match = matches[shortest]


        return match
    except Exception as ex:
        errorlog = open(errorreporting, 'a')
        errorlog.write('\n Category Number Search Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
        errorlog.close()
        return False

def CategoryNumberDefinition(CovCatNumber):
    Result = {}
    try:        
        cur.execute("SELECT * FROM covcat WHERE CovCatNum =" + str(CovCatNumber))
        coveragecat = cur.fetchone()
        if (coveragecat['Description'] != ''):
            Result['Description'] = coveragecat['Description']
        else:
            Result['Description'] = False
            
        if (coveragecat['DefaultPercent'] != ''):
            Result['DefaultPercentage'] = coveragecat['DefaultPercent']
        else:
            Result['DefaultPercentage'] = False

        if (coveragecat['CovOrder'] != ''):
            Result['Order'] = coveragecat['CovOrder']
        else:
            Result['Order'] = False

        if (coveragecat['EbenefitCat'] != ''):
            Result['BenefitCategoryNumber'] = coveragecat['EbenefitCat']
        else:
            Result['BenefitCategoryNumber'] = False

        if (coveragecat['EbenefitCat'] != ''):
            if (coveragecat['EbenefitCat'] == 0):
                Result['BenefitCategory'] = 'None'
            elif (coveragecat['EbenefitCat'] == 1):
                Result['BenefitCategory'] = 'General'
            elif (coveragecat['EbenefitCat'] == 2):
                Result['BenefitCategory'] = 'Diagnostic'
            elif (coveragecat['EbenefitCat'] == 3):
                Result['BenefitCategory'] = 'Periodontics'
            elif (coveragecat['EbenefitCat'] == 4):
                Result['BenefitCategory'] = 'Restorative'
            elif (coveragecat['EbenefitCat'] == 5):
                Result['BenefitCategory'] = 'Endodontics'
            elif (coveragecat['EbenefitCat'] == 6):
                Result['BenefitCategory'] = 'Maxillofacial Prosthetics'
            elif (coveragecat['EbenefitCat'] == 7):
                Result['BenefitCategory'] = 'Crowns'
            elif (coveragecat['EbenefitCat'] == 8):
                Result['BenefitCategory'] = 'Accident'
            elif (coveragecat['EbenefitCat'] == 9):
                Result['BenefitCategory'] = 'Orthodontics'
            elif (coveragecat['EbenefitCat'] == 10):
                Result['BenefitCategory'] = 'Prosthodontics'
            elif (coveragecat['EbenefitCat'] == 11):
                Result['BenefitCategory'] = 'Oral Surgery'
            elif (coveragecat['EbenefitCat'] == 12):
                Result['BenefitCategory'] = 'Routine Preventive'
            elif (coveragecat['EbenefitCat'] == 13):
                Result['BenefitCategory'] = 'Diagnostic X-Ray'
            elif (coveragecat['EbenefitCat'] == 14):
                Result['BenefitCategory'] = 'Adjunctive'

            return Result
        
    except Exception as ex:
        errorlog = open(errorreporting, 'a')
        errorlog.write('\n Category Definition Error 2: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
        errorlog.close()
        return False


def BenefitPercentageLookup(Type,Insurance):
    Percentages = []
    try:
        cur.execute("SELECT * FROM benefit WHERE PlanNum =" + str(Insurance) + " AND CovCatNum=" + str(Type) + " AND BenefitType=1")
        Benefit = cur.fetchone()
        if (Benefit):
            return Benefit['Percent']
        else:
            return 0
    except Exception as ex:
        errorlog = open(errorreporting, 'a')
        errorlog.write('\n Benefit Percentage Lookup Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
        errorlog.close()
        return False

def PrimaryPlanLookup(PatNum):
    if (PatNum != ""):
        try:        
            cur.execute("SELECT * FROM patplan WHERE PatNum =" + str(PatNum))
            Plan = cur.fetchone()
            if (Plan):
                cur.execute("SELECT * FROM inssub WHERE InsSubNum =" + str(Plan['InsSubNum']))
                Plan = cur.fetchone()
                return Plan['PlanNum']
            else:
                return 0
        except Exception as ex:
            errorlog = open(errorreporting, 'a')
            errorlog.write('\n Patient Insurance Plan Lookup Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
            errorlog.close()
            return False
    else:
        return False

def CreateUser(number = 9223372036854775807, name = "", group = 1, employee = 0, clinic = 0, provider = 0, hidden = 0, popups = 0, password = 1, restricted = 0, tasklist=0):
    user = [number, name, group, employee, clinic, provider, hidden, popups, password, restricted]
    print len(user)
    try:
        cur.execute("INSERT INTO userod "
                    "(UserNum, UserName, UserGroupNum, EmployeeNum, ClinicNum, ProvNum, IsHidden, DefaultHidePopups, PasswordIsStrong, ClinicIsRestricted, TaskListInBox)"
                    " VALUES ('%i','%s','%i','%i','%i','%i','%i','%i','%i','%i','%i')" % (number, name, group, employee, clinic, provider, hidden, popups, password, restricted, tasklist))
        return True
    except Exception as ex:
            errorlog = open(errorreporting, 'a')
            errorlog.write('\n User Creation Error: ' + str(ex) + ' on line ' + format(sys.exc_info()[-1].tb_lineno))
            errorlog.close()
            return False

def deleteattachedclaims(procedure = 0):
    if (procedure != 0):
        cur.execute("SELECT ProcNum, ClaimNum FROM claimproc WHERE ProcNum =" + str(procedure))
        claimnumber = cur.fetchone()
        cur.execute("DELETE from claimproc WHERE ClaimNum =" + str(claimnumber['ClaimNum']))
        cur.execute("DELETE from claim WHERE ClaimNum =" + str(claimnumber['ClaimNum']))
        return True


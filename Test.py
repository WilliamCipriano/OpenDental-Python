import OpenDental
import pickle

def manual():

    def yorn(data):
        if data == 'Y' or data == 'y':
            return True
        elif data == 'N' or data == 'n':
            return False
        else:
            print 'Invalid Input!'
            return False

    print "Attempt to load previously saved configuration?"
    check = raw_input('Y/N?')
    if yorn(check):
        if OpenDental.DatabaseConnection():
            return True


    def write(host, username, password, database, path):
        try:
            f = open(path, 'w')
            f.write('Host = ' + host + '\nUsername = ' + username + '\nPassword = ' + password + '\nDatabase = ' + database)
            f.close()
            return True
        except Exception as ex:
            return False

    print "Please enter OpenDental database details."
    host = raw_input('Host?:')
    username = raw_input('Username?')
    password = raw_input('Password?')
    database = raw_input('Database?')
    print "Save this configuration?"
    save = raw_input('Y/N?')
    if yorn(save):
        import os
        path = os.path.dirname(__file__).replace('\\library.zip', "")
        path += '\OpenDentalDatabaseConfig.ini'
        if os.path.isfile(path):
            print "configuration already exists! Overwrite?"
            overwrite = raw_input('Y/N?')
            if yorn(overwrite):
                if write(host ,username ,password ,database, path):
                    print "Parameters updated successfully."
                else:
                    print "Save failed."
        else:
            if write(host ,username ,password ,database, path):
                print "Data saved."
            else:
                print "Save failed"

    else:
        print "Data not saved."


    print 'Attempting to connect to database'
    if OpenDental.DefineDatabase(host, username, password, database):
        print "connection successful"
        return True
    else:
        print "connection failed!"
        return False



manual()
x = 0
while True:
    print "select patient by patient number:"
    patientnum = raw_input('patient number:')
    patient = OpenDental.GetPatientDetails(patientnum)
    f = open('patientnumber' + patientnum + '-' + str(x) + '-DUMP.txt', 'w')
    pickle.dump(patient, f)
    x += 1
    print patient

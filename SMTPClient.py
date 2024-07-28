import tkinter as tk
from tkinter import filedialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class EmailClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Client")
        self.geometry("500x500")

        # Create the GUI elements
        self.sender_label = tk.Label(self, text="Sender:")
        self.sender_entry = tk.Entry(self)
        self.recipient_label = tk.Label(self, text="Recipient:")
        self.recipient_entry = tk.Entry(self)
        self.subject_label = tk.Label(self, text="Subject:")
        self.subject_entry = tk.Entry(self)
        self.body_label = tk.Label(self, text="Body:")
        self.body_text = tk.Text(self, height=10, width=50)
        self.attachment_label = tk.Label(self, text="Attachment:")
        self.attachment_entry = tk.Entry(self)
        self.attachment_button = tk.Button(self, text="Browse", command=self.select_attachment)
        self.send_button = tk.Button(self, text="Send", command=self.send_email)

        # Grid layout
        self.sender_label.grid(row=0, column=0, padx=10, pady=10)
        self.sender_entry.grid(row=0, column=1, padx=10, pady=10)
        self.recipient_label.grid(row=1, column=0, padx=10, pady=10)
        self.recipient_entry.grid(row=1, column=1, padx=10, pady=10)
        self.subject_label.grid(row=2, column=0, padx=10, pady=10)
        self.subject_entry.grid(row=2, column=1, padx=10, pady=10)
        self.body_label.grid(row=3, column=0, padx=10, pady=10)
        self.body_text.grid(row=3, column=1, padx=10, pady=10)
        self.attachment_label.grid(row=4, column=0, padx=10, pady=10)
        self.attachment_entry.grid(row=4, column=1, padx=10, pady=10)
        self.attachment_button.grid(row=4, column=2, padx=10, pady=10)
        self.send_button.grid(row=5, column=1, padx=10, pady=10)

    def select_attachment(self):
        file_path = filedialog.askopenfilename()
        self.attachment_entry.delete(0, tk.END)
        self.attachment_entry.insert(0, file_path)

    def send_email(self):
        sender = self.sender_entry.get()
        recipient = self.recipient_entry.get()
        subject = self.subject_entry.get()
        body = self.body_text.get("1.0", tk.END)
        attachment = self.attachment_entry.get()

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment:
            with open(attachment, 'rb') as f:
                part = MIMEApplication(
                    f.read(),
                    Name=attachment.split('/')[-1]
                )
                part['Content-Disposition'] = f'attachment; filename="{attachment.split("/")[-1]}"'
                msg.attach(part)

        try:
            with smtplib.SMTP('localhost') as smtp:
                smtp.send_message(msg)
            print('Email sent successfully!')
        except smtplib.SMTPException as e:
            print(f'Error sending email: {e}')

if __name__ == "__main__":
    app = EmailClient()
    app.mainloop()

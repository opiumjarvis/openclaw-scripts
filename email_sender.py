#!/usr/bin/env python3
"""
OpenClaw Email Sender
Sends personalized cold emails with tracking
"""

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, smtp_host, smtp_port, email, password):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.sent = []
        
    def send(self, to_email, subject, body, html=False):
        """Send single email"""
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
            
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
                
            self.sent.append({'to': to_email, 'subject': subject})
            print(f"✓ Sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to {to_email}: {e}")
            return False
            
    def send_batch(self, leads, template, delay=30):
        """Send batch with delay"""
        for lead in leads:
            # Personalize template
            body = template.format(
                first_name=lead.get('first_name', ''),
                last_name=lead.get('last_name', ''),
                company=lead.get('company', ''),
                **lead
            )
            
            self.send(lead['email'], lead.get('subject', 'Quick question'), body)
            time.sleep(delay)  # Rate limiting
            
    def get_stats(self):
        """Get sending stats"""
        return {
            'total_sent': len(self.sent),
            'success_rate': len(self.sent) / max(1, len(self.sent))
        }

# Example usage
if __name__ == "__main__":
    sender = EmailSender(
        smtp_host="smtp.gmail.com",
        smtp_port=587,
        email="your-email@gmail.com",
        password="your-app-password"
    )
    
    # Example template
    template = """Hey {first_name},

Quick question about {company}...

Best,
Your Name"""
    
    # Would load leads and send
    # sender.send_batch(leads, template)

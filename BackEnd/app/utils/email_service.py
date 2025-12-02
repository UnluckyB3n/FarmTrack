import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import os


class EmailService:
    """
    Email service for sending notifications.
    In production, configure SMTP_* environment variables.
    In development, emails are printed to console.
    """
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'localhost')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('SMTP_FROM_EMAIL', 'noreply@farmtrack.example.com')
        self.dev_mode = os.getenv('EMAIL_DEV_MODE', 'true').lower() == 'true'
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_content: Optional[str] = None
    ) -> bool:
        """
        Send an email to a recipient.
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            html_content: HTML version of email body
            plain_content: Plain text version (optional, defaults to HTML stripped)
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if self.dev_mode:
            # In development mode, print to console instead of sending
            print("\n" + "="*60)
            print("📧 EMAIL (Dev Mode - Not Sent)")
            print("="*60)
            print(f"From: {self.from_email}")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print("-"*60)
            print(html_content)
            print("="*60 + "\n")
            return True
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Attach plain text and HTML versions
            if plain_content:
                part1 = MIMEText(plain_content, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_password_reset_email(self, to_email: str, reset_token: str, username: str) -> bool:
        """
        Send a password reset email with token.
        
        Args:
            to_email: User's email address
            reset_token: Secure reset token
            username: User's username
        
        Returns:
            bool: True if sent successfully
        """
        reset_url = f"http://localhost:3000/forgot-password?token={reset_token}"
        
        subject = "Password Reset Request - FarmTrack"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #1e3a8a;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 30px;
                    border-radius: 5px;
                }}
                .button {{
                    display: inline-block;
                    background-color: #1e3a8a;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .token {{
                    background-color: #e0e7ff;
                    padding: 15px;
                    border-radius: 5px;
                    font-family: monospace;
                    font-size: 14px;
                    word-break: break-all;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔒 Password Reset Request</h1>
                </div>
                <div class="content">
                    <p>Hello <strong>{username}</strong>,</p>
                    
                    <p>We received a request to reset your password for your FarmTrack account.</p>
                    
                    <p>Click the button below to reset your password:</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_url}" class="button">Reset Password</a>
                    </div>
                    
                    <p>Or copy and paste this token into the password reset form:</p>
                    
                    <div class="token">
                        {reset_token}
                    </div>
                    
                    <p><strong>⏰ This link will expire in 1 hour.</strong></p>
                    
                    <p>If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>
                </div>
                <div class="footer">
                    <p>FarmTrack - Livestock Traceability System</p>
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_content = f"""
        Password Reset Request - FarmTrack
        
        Hello {username},
        
        We received a request to reset your password for your FarmTrack account.
        
        Use this token to reset your password: {reset_token}
        
        Or visit: {reset_url}
        
        This link will expire in 1 hour.
        
        If you didn't request a password reset, you can safely ignore this email.
        
        ---
        FarmTrack - Livestock Traceability System
        """
        
        return self.send_email(to_email, subject, html_content, plain_content)
    
    def send_anomaly_alert_email(
        self,
        to_email: str,
        username: str,
        animal_id: int,
        animal_name: str,
        event_type: str,
        anomaly_reason: str
    ) -> bool:
        """
        Send an anomaly detection alert email to regulators.
        
        Args:
            to_email: Regulator's email address
            username: Regulator's username
            animal_id: ID of the animal with anomaly
            animal_name: Name of the animal
            event_type: Type of event that triggered anomaly
            anomaly_reason: Description of the anomaly
        
        Returns:
            bool: True if sent successfully
        """
        dashboard_url = "http://localhost:3000/regulator/dashboard"
        trace_url = f"http://localhost:3000/regulator/trace?animal={animal_id}"
        
        subject = f"⚠️ Anomaly Detected - Animal #{animal_id}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #dc2626;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .content {{
                    background-color: #fef2f2;
                    padding: 30px;
                    border-left: 4px solid #dc2626;
                }}
                .info-box {{
                    background-color: white;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .button {{
                    display: inline-block;
                    background-color: #1e3a8a;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 5px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Anomaly Detected</h1>
                </div>
                <div class="content">
                    <p>Hello <strong>{username}</strong>,</p>
                    
                    <p>An anomaly has been detected in the FarmTrack system that requires your attention.</p>
                    
                    <div class="info-box">
                        <p><strong>Animal:</strong> {animal_name} (ID: #{animal_id})</p>
                        <p><strong>Event Type:</strong> {event_type}</p>
                        <p><strong>Anomaly Reason:</strong> {anomaly_reason}</p>
                    </div>
                    
                    <p>Please review this anomaly and take appropriate action.</p>
                    
                    <div style="text-align: center;">
                        <a href="{trace_url}" class="button">Trace Animal</a>
                        <a href="{dashboard_url}" class="button">View Dashboard</a>
                    </div>
                </div>
                <div class="footer">
                    <p>FarmTrack - Livestock Traceability System</p>
                    <p>This is an automated compliance alert.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_content = f"""
        Anomaly Detected - FarmTrack
        
        Hello {username},
        
        An anomaly has been detected in the FarmTrack system.
        
        Animal: {animal_name} (ID: #{animal_id})
        Event Type: {event_type}
        Anomaly Reason: {anomaly_reason}
        
        Please review this anomaly:
        Trace Animal: {trace_url}
        Dashboard: {dashboard_url}
        
        ---
        FarmTrack - Livestock Traceability System
        """
        
        return self.send_email(to_email, subject, html_content, plain_content)


# Singleton instance
email_service = EmailService()

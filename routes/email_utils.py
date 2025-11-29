"""
Email Utility Functions
Handles sending email notifications
"""
from flask_mail import Message
from flask import current_app
from extensions import mail


def send_scholarship_approval_email(student_email, student_name, scholarship_type, amount, semester):
    """Send email notification when scholarship is approved"""
    
    # Check if email sending is enabled
    if not current_app.config.get('SEND_EMAILS', True):
        print(f"[Email Disabled] Would have sent scholarship approval email to {student_email}")
        return True
    
    subject = "🎉 Scholarship Approved - SSMP BUP"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .highlight {{ background: #fff; padding: 20px; border-left: 4px solid #4caf50; margin: 20px 0; }}
            .amount {{ font-size: 28px; font-weight: bold; color: #2c5f2d; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Congratulations!</h1>
                <p>Your scholarship has been approved</p>
            </div>
            <div class="content">
                <p>Dear <strong>{student_name}</strong>,</p>
                
                <p>We are pleased to inform you that your scholarship application has been <strong>approved</strong>!</p>
                
                <div class="highlight">
                    <p><strong>Scholarship Details:</strong></p>
                    <ul>
                        <li><strong>Type:</strong> {scholarship_type}</li>
                        <li><strong>Amount:</strong> <span class="amount">৳{amount:,.2f}</span></li>
                        <li><strong>Semester:</strong> {semester}</li>
                    </ul>
                </div>
                
                <p>The scholarship amount will be credited to your student account shortly.</p>
                
                <p>Keep up the excellent academic performance!</p>
                
                <p>Best regards,<br>
                <strong>Bangladesh University of Professionals</strong><br>
                Scholarship Management System</p>
                
                <div class="footer">
                    <p>This is an automated email from SSMP. Please do not reply to this email.</p>
                    <p>&copy; 2025 Bangladesh University of Professionals. All rights reserved.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = Message(subject=subject,
                     recipients=[student_email],
                     html=html_body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_stipend_approval_email(student_email, student_name, stipend_type, amount, semester):
    """Send email notification when stipend application is approved"""
    
    # Check if email sending is enabled
    if not current_app.config.get('SEND_EMAILS', True):
        print(f"[Email Disabled] Would have sent stipend approval email to {student_email}")
        return True
    
    subject = "✅ Stipend Application Approved - SSMP BUP"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .highlight {{ background: #fff; padding: 20px; border-left: 4px solid #2196f3; margin: 20px 0; }}
            .amount {{ font-size: 28px; font-weight: bold; color: #1976d2; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Application Approved!</h1>
                <p>Your stipend application has been approved</p>
            </div>
            <div class="content">
                <p>Dear <strong>{student_name}</strong>,</p>
                
                <p>Great news! Your stipend application has been <strong>approved</strong> by the department.</p>
                
                <div class="highlight">
                    <p><strong>Stipend Details:</strong></p>
                    <ul>
                        <li><strong>Type:</strong> {stipend_type}</li>
                        <li><strong>Amount:</strong> <span class="amount">৳{amount:,.2f}</span></li>
                        <li><strong>Semester:</strong> {semester}</li>
                    </ul>
                </div>
                
                <p>The stipend amount will be disbursed according to university schedule.</p>
                
                <p>Congratulations and keep up the good work!</p>
                
                <p>Best regards,<br>
                <strong>Bangladesh University of Professionals</strong><br>
                Scholarship Management System</p>
                
                <div class="footer">
                    <p>This is an automated email from SSMP. Please do not reply to this email.</p>
                    <p>&copy; 2025 Bangladesh University of Professionals. All rights reserved.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = Message(subject=subject,
                     recipients=[student_email],
                     html=html_body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_stipend_rejection_email(student_email, student_name, stipend_type, semester):
    """Send email notification when stipend application is rejected"""
    
    # Check if email sending is enabled
    if not current_app.config.get('SEND_EMAILS', True):
        print(f"[Email Disabled] Would have sent stipend rejection email to {student_email}")
        return True
    
    subject = "Stipend Application Status - SSMP BUP"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .highlight {{ background: #fff; padding: 20px; border-left: 4px solid #f44336; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Application Update</h1>
                <p>Regarding your stipend application</p>
            </div>
            <div class="content">
                <p>Dear <strong>{student_name}</strong>,</p>
                
                <p>We regret to inform you that your stipend application has not been approved at this time.</p>
                
                <div class="highlight">
                    <p><strong>Application Details:</strong></p>
                    <ul>
                        <li><strong>Type:</strong> {stipend_type}</li>
                        <li><strong>Semester:</strong> {semester}</li>
                        <li><strong>Status:</strong> <strong style="color: #d32f2f;">Rejected</strong></li>
                    </ul>
                </div>
                
                <p>This decision may be based on various factors including budget constraints, eligibility criteria, or application completeness.</p>
                
                <p>We encourage you to maintain your academic performance and consider applying in future semesters.</p>
                
                <p>If you have any questions, please contact your department office.</p>
                
                <p>Best regards,<br>
                <strong>Bangladesh University of Professionals</strong><br>
                Scholarship Management System</p>
                
                <div class="footer">
                    <p>This is an automated email from SSMP. Please do not reply to this email.</p>
                    <p>&copy; 2025 Bangladesh University of Professionals. All rights reserved.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = Message(subject=subject,
                     recipients=[student_email],
                     html=html_body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

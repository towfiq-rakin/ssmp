"""
Test Email Configuration
Run this script to verify email setup works correctly
"""
from app import create_app
from routes.email_utils import send_scholarship_approval_email, send_stipend_approval_email, send_stipend_rejection_email

# Create app context
app = create_app()

with app.app_context():
    print("Testing email configuration...")
    print("=" * 50)
    
    # Test scholarship approval email
    print("\n1. Testing Scholarship Approval Email...")
    result = send_scholarship_approval_email(
        student_email="towfiqomarrakin@gmail.com",  # Replace with your email
        student_name="Test Student",
        scholarship_type="Chancellor Scholarship",
        amount=15000,
        semester="Semester 3"
    )
    print(f"Result: {'Success ✓' if result else 'Failed ✗'}")
    
    # Test stipend approval email
    print("\n2. Testing Stipend Approval Email...")
    result = send_stipend_approval_email(
        student_email="23524202131@student.bup.edu.bd",  # Replace with your email
        student_name="Test Student",
        stipend_type="General Stipend",
        amount=6000,
        semester="Semester 3"
    )
    print(f"Result: {'Success ✓' if result else 'Failed ✗'}")
    
    # Test stipend rejection email
    print("\n3. Testing Stipend Rejection Email...")
    result = send_stipend_rejection_email(
        student_email="23524202131@student.bup.edu.bd",  # Replace with your email
        student_name="Test Student",
        stipend_type="General Stipend",
        semester="Semester 3"
    )
    print(f"Result: {'Success ✓' if result else 'Failed ✗'}")
    
    print("\n" + "=" * 50)
    print("Email testing complete!")
    print("\nIf you see errors, check your:")
    print("1. Gmail App Password configuration")
    print("2. MAIL_USERNAME and MAIL_PASSWORD in config.py")
    print("3. Internet connection")

# Gmail SMTP Email Setup Guide

## Step 1: Enable 2-Factor Authentication on Gmail

1. Go to your Google Account: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Under "How you sign in to Google", enable "2-Step Verification"
4. Follow the prompts to set up 2FA

## Step 2: Generate App Password

1. After enabling 2FA, go to: https://myaccount.google.com/apppasswords
2. Under "Select app", choose "Mail"
3. Under "Select device", choose "Other (Custom name)"
4. Enter "SSMP Flask App" as the name
5. Click "Generate"
6. **IMPORTANT:** Copy the 16-character password (remove spaces)
   - Example: `abcd efgh ijkl mnop` → `abcdefghijklmnop`

## Step 3: Update config.py

Open `config.py` and update these lines:

```python
# Email Configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'  # Replace with your Gmail
MAIL_PASSWORD = 'abcdefghijklmnop'      # Replace with your App Password
MAIL_DEFAULT_SENDER = ('SSMP BUP', 'your-email@gmail.com')
```

## Step 4: Test Email Configuration

1. Update `test_email.py` and replace `test@example.com` with your email
2. Run the test:
   ```bash
   python test_email.py
   ```
3. Check your inbox for 3 test emails

## Alternative: Using Environment Variables (Recommended for Production)

Instead of hardcoding credentials, use a `.env` file:

1. Create a file named `.env` in your project root:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=abcdefghijklmnop
   ```

2. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

3. Update `config.py` to load from .env:
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()  # Add this line at the top

   class Config:
       # ... existing config ...
       MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
       MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
   ```

4. Add `.env` to `.gitignore` to keep credentials secure

## Troubleshooting

### Error: "Username and Password not accepted"
- Double-check your Gmail address
- Verify App Password is correct (no spaces)
- Ensure 2FA is enabled

### Error: "SMTPAuthenticationError"
- Regenerate App Password
- Make sure you're using App Password, not regular Gmail password

### Error: "Connection refused"
- Check internet connection
- Verify MAIL_SERVER and MAIL_PORT are correct

### Emails not arriving
- Check spam/junk folder
- Verify recipient email address is correct
- Check Gmail sent folder to confirm emails were sent

## Security Notes

- **Never commit** actual credentials to GitHub
- Use `.env` file for sensitive data
- Add `.env` to `.gitignore`
- For production, use environment variables on your server
- Consider using email service providers (SendGrid, Mailgun) for production

## How It Works

When admin approves/rejects scholarships or stipends:

1. **Scholarship Approved** → Student receives green-themed success email
2. **Stipend Approved** → Student receives blue-themed success email
3. **Stipend Rejected** → Student receives red-themed notification email

All emails include:
- Student name
- Scholarship/Stipend type
- Amount (for approvals)
- Semester information
- Professional HTML formatting with BUP branding

## Email Templates

The emails use beautiful HTML templates with:
- Gradient headers
- Color-coded styling (green for success, blue for approval, red for rejection)
- Professional BUP branding
- Mobile-responsive design
- Clear call-to-action information

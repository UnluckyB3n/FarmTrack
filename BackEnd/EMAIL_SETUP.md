# Email Configuration

FarmTrack includes an email notification system for password resets and anomaly alerts.

## Development Mode

By default, emails are NOT sent but printed to the console for development purposes.

Set `EMAIL_DEV_MODE=true` in your environment (default) to enable console output.

## Production Configuration

To enable actual email sending in production, configure these environment variables:

```bash
# Email Configuration
EMAIL_DEV_MODE=false
SMTP_HOST=smtp.gmail.com          # Your SMTP server
SMTP_PORT=587                     # SMTP port (587 for TLS, 465 for SSL)
SMTP_USER=your-email@gmail.com    # SMTP username
SMTP_PASSWORD=your-app-password   # SMTP password or app password
SMTP_FROM_EMAIL=noreply@farmtrack.com  # From address
```

### Gmail Example

For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an App Password at https://myaccount.google.com/apppasswords
3. Use the app password in `SMTP_PASSWORD`

```bash
EMAIL_DEV_MODE=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM_EMAIL=noreply@farmtrack.com
```

### Other SMTP Providers

**SendGrid:**
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

**Mailgun:**
```bash
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@your-domain.mailgun.org
SMTP_PASSWORD=your-mailgun-password
```

**AWS SES:**
```bash
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USER=your-ses-smtp-username
SMTP_PASSWORD=your-ses-smtp-password
```

## Email Templates

The system includes two email templates:

### 1. Password Reset Email
Sent when a user requests a password reset via `/auth/forgot-password`.

Features:
- Secure reset token
- 1-hour expiration
- Direct reset link
- Styled HTML template

### 2. Anomaly Alert Email
Sent to all regulators when an anomaly is detected in the system.

Features:
- Animal information
- Anomaly details
- Direct links to trace page and dashboard
- Red alert styling

## Testing Emails

In development mode (default), emails are printed to the console:

```
============================================================
📧 EMAIL (Dev Mode - Not Sent)
============================================================
From: noreply@farmtrack.example.com
To: user@example.com
Subject: Password Reset Request - FarmTrack
------------------------------------------------------------
[HTML content displayed here]
============================================================
```

## Email Service API

The email service is available at `app.utils.email_service`:

```python
from app.utils.email_service import email_service

# Send password reset
email_service.send_password_reset_email(
    to_email="user@example.com",
    reset_token="secure_token",
    username="john_doe"
)

# Send anomaly alert
email_service.send_anomaly_alert_email(
    to_email="regulator@example.com",
    username="regulator1",
    animal_id=123,
    animal_name="Bessie",
    event_type="vaccination",
    anomaly_reason="Duplicate vaccination record"
)

# Send custom email
email_service.send_email(
    to_email="user@example.com",
    subject="Custom Subject",
    html_content="<h1>Hello</h1>",
    plain_content="Hello"
)
```

## Troubleshooting

### Emails not sending in production

1. Check `EMAIL_DEV_MODE` is set to `false`
2. Verify SMTP credentials are correct
3. Check SMTP server allows connections from your IP
4. Review firewall rules for SMTP port access
5. Check application logs for error messages

### Gmail authentication errors

- Ensure 2FA is enabled
- Generate a new App Password
- Use the App Password, not your regular password
- Check "Less secure app access" is not required (App Passwords bypass this)

### Connection timeouts

- Verify SMTP_HOST and SMTP_PORT are correct
- Check if your hosting provider blocks SMTP ports
- Try alternative ports (587 for TLS, 465 for SSL)
- Consider using a dedicated email service like SendGrid or Mailgun

## Security Best Practices

1. **Never commit credentials** - Use environment variables only
2. **Use App Passwords** - Don't use your main email password
3. **Enable TLS** - Always use port 587 with STARTTLS
4. **Limit sender permissions** - Use a dedicated sending account
5. **Monitor email logs** - Watch for bounces and delivery issues
6. **Rate limiting** - Consider implementing rate limits for email sending
7. **Validate recipients** - Ensure email addresses are valid before sending

## Docker Configuration

Add email configuration to your `docker-compose.yml`:

```yaml
services:
  api:
    environment:
      - EMAIL_DEV_MODE=false
      - SMTP_HOST=smtp.gmail.com
      - SMTP_PORT=587
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASSWORD=${SMTP_PASSWORD}
      - SMTP_FROM_EMAIL=noreply@farmtrack.com
```

And create a `.env` file (not committed to git):

```bash
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for Flutter web

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp_email(recipient_email, recipient_name, otp):
    """Send OTP email using Gmail SMTP"""
    
    # Email configuration
    sender_email = "shiffterss@gmail.com"
    sender_password = "xcfheqnaujhwfpej"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "SHIFFTERS - Email Verification Code"
        message["From"] = f"SHIFFTERS <{sender_email}>"
        message["To"] = recipient_email
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f8f9fa;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .otp-box {{
                    background: #fff;
                    border: 2px solid #667eea;
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                    margin: 20px 0;
                }}
                .otp-code {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #667eea;
                    letter-spacing: 5px;
                    margin: 10px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #666;
                    font-size: 14px;
                }}
                .warning {{
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚛 SHIFFTERS</h1>
                <p>Let's Relocate</p>
            </div>
            
            <div class="content">
                <h2>Hello {recipient_name}!</h2>
                <p>Welcome to <strong>SHIFFTERS</strong>! We're excited to have you join our community.</p>
                
                <p>To complete your account registration, please verify your email address using the code below:</p>
                
                <div class="otp-box">
                    <p>Your Verification Code:</p>
                    <div class="otp-code">{otp}</div>
                </div>
                
                <div class="warning">
                    <strong>⚠️ Important:</strong>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li>This code will expire in <strong>10 minutes</strong></li>
                        <li>Don't share this code with anyone</li>
                        <li>If you didn't request this code, please ignore this email</li>
                    </ul>
                </div>
                
                <p>Enter this code in the SHIFFTERS app to verify your email and activate your account.</p>
                
                <p>If you have any questions or need assistance, feel free to contact our support team.</p>
                
                <div class="footer">
                    <p>Best regards,<br><strong>The SHIFFTERS Team</strong></p>
                    <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                    <p>This is an automated message. Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_content = f"""
        SHIFFTERS - Email Verification
        
        Hello {recipient_name}!
        
        Welcome to SHIFFTERS! We're excited to have you join our community.
        
        Your email verification code is: {otp}
        
        Please enter this code in the app to verify your email address.
        
        IMPORTANT:
        - This code will expire in 10 minutes
        - Don't share this code with anyone
        - If you didn't request this code, please ignore this email
        
        Best regards,
        The SHIFFTERS Team
        """
        
        # Attach parts
        text_part = MIMEText(text_content, "plain")
        html_part = MIMEText(html_content, "html")
        
        message.attach(text_part)
        message.attach(html_part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return True, "Email sent successfully"
        
    except Exception as e:
        return False, str(e)

@app.route('/send-otp', methods=['POST'])
def send_otp():
    """API endpoint to send OTP"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Email and name are required'
            }), 400
        
        recipient_email = data['email']
        recipient_name = data['name']
        
        # Generate OTP
        otp = generate_otp()
        
        # Send email
        success, message = send_otp_email(recipient_email, recipient_name, otp)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'otp': otp
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'OTP server is running'})

def run_server():
    """Run the Flask server"""
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == '__main__':
    print("Starting SHIFFTERS OTP Server...")
    print("Server will be available at: http://127.0.0.1:5000")
    print("Health check: http://127.0.0.1:5000/health")
    print("Send OTP endpoint: http://127.0.0.1:5000/send-otp")
    run_server()

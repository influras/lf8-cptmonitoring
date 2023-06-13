import unittest
from unittest.mock import patch

import EmailService


class TestEmailService(unittest.TestCase):
    @patch('EmailService.smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        recipient_email = 'test@example.com'
        message = 'Test message'
        hostname = 'test-host'

        smtp_instance = mock_smtp.return_value.__enter__.return_value
        smtp_instance.send_message.return_value = {}

        result = EmailService.send_email(recipient_email, message, hostname)

        self.assertTrue(result)

    @patch('EmailService.smtplib.SMTP')
    def test_send_email_failure(self, mock_smtp):
        recipient_email = 'test@example.com'
        message = 'Test message'
        hostname = 'test-host'

        smtp_instance = mock_smtp.return_value.__enter__.return_value
        smtp_instance.send_message.side_effect = Exception('SMTP error')

        result = EmailService.send_email(recipient_email, message, hostname)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

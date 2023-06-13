import unittest
from tkinter import *

import HardwareInfo


class TestHardwareInfo(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.root.withdraw()  # Verstecke das Hauptfenster für die GUI-Tests
        self.drives_text = Text(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_send_email_wrapper_valid_email(self):
        email_entry = "test@example.com"
        result = HardwareInfo.send_email_wrapper(email_entry)
        self.assertTrue(result)

    def test_send_email_wrapper_invalid_email(self):
        email_entry = "invalid_email"
        result = HardwareInfo.send_email_wrapper(email_entry)
        self.assertFalse(result)

    def test_send_email_wrapper_email_failure(self):
        # Mock die send_email-Funktion, um einen Fehler zu simulieren
        def mock_send_email(email, file_contents, hostname):
            return False

        HardwareInfo.emServ.send_email = mock_send_email

        email_entry = "test@example.com"
        result = HardwareInfo.send_email_wrapper(email_entry)
        self.assertFalse(result)

    def test_emailSendWindow_valid_email(self):
        # Mock die Methode zum Anzeigen der Bestätigungsmeldung
        def mock_email_sent_confirmation():
            self.email_sent_confirmation = True

        HardwareInfo.emailSentConfirmation.pack_forget = mock_email_sent_confirmation

        HardwareInfo.emailSendWindow()
        email_entry = self.root.children["!toplevel"].children["!entry"]
        email_entry.insert(0, "test@example.com")
        send_button = self.root.children["!toplevel"].children["!button"]
        send_button.invoke()

        self.assertTrue(self.email_sent_confirmation)

    def test_emailSendWindow_invalid_email(self):
        HardwareInfo.emailSendWindow()
        email_entry = self.root.children["!toplevel"].children["!entry"]
        email_entry.insert(0, "invalid_email")
        send_button = self.root.children["!toplevel"].children["!button"]
        send_button.invoke()

        error_label = self.root.children["!toplevel"].children["!label"]
        self.assertEqual(error_label.cget("text"), "Falsches E-Mail Format! - Richtig: xx@xx.xx")

    def test_update_info(self):
        HardwareInfo.update_info()

        # Überprüfe, ob die CPU-Auslastung aktualisiert wurde
        cpu_label = HardwareInfo.cpu_label
        cpu_message = cpu_label.cget("text")
        self.assertRegex(cpu_message, r"CPU-Auslastung: \d+%")

        # Überprüfe, ob die RAM-Auslastung aktualisiert wurde
        ram_label = HardwareInfo.ram_label
        ram_message = ram_label.cget("text")
        self.assertRegex(ram_message, r"RAM-Auslastung: \d+%, Verwendet: \d+\.\d+ GB, Insgesamt: \d+\.\d+ GB")

        # Überprüfe, ob die Festplattenauslastung aktualisiert wurde
        drives_text = self.drives_text
        drives_text_content = drives_text.get("1.0", "end-1c")
        self.assertNotEqual(drives_text_content, "")

        # Überprüfe, ob die Netzwerkauslastung aktualisiert wurde
        net_label = HardwareInfo.net_label
        net_message = net_label.cget("text")
        self.assertRegex(net_message, r"Netzwerkauslastung: Gesendet: \d+ Bytes, Empfangen: \d+ Bytes")

        # Überprüfe, ob die laufenden Prozesse aktualisiert wurden
        processes_text = HardwareInfo.processes_text
        processes_text_content = processes_text.get("1.0", "end-1c")
        self.assertNotEqual(processes_text_content, "")


if __name__ == "__main__":
    unittest.main()
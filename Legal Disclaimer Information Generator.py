#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextBrowser

class LegalInfoGenerator(QWidget):
    def __init__(self):
        super().__init__()

        # Create buttons
        self.terms_of_service_button = QPushButton("Terms of Service")
        self.privacy_policy_button = QPushButton("Privacy Policy")
        self.disclaimer_button = QPushButton("Disclaimer")

        # Create text display
        self.text_display = QTextBrowser()

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.terms_of_service_button)
        layout.addWidget(self.privacy_policy_button)
        layout.addWidget(self.disclaimer_button)
        layout.addWidget(self.text_display)
        self.setLayout(layout)

        # Connect buttons to functions
        self.terms_of_service_button.clicked.connect(self.display_terms_of_service)
        self.privacy_policy_button.clicked.connect(self.display_privacy_policy)
        self.disclaimer_button.clicked.connect(self.display_disclaimer)

    def display_terms_of_service(self):
        self.text_display.setPlainText("""
        Terms of Service
        1. Introduction
        This document outlines the terms of service for using the website. By accessing and using the website, you agree to be bound by these terms. If you do not agree with these terms, you should not use the website.
        2. Content
        The website and its content are provided for informational purposes only. The website makes no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the website or the information, products, services, or related graphics contained on the website for any purpose. Any reliance you place on such information is strictly at your own risk.
        3. Limitation of Liability
        In no event will the website be liable for any loss or damage including without limitation, indirect or consequential loss or damage, or any loss or damage whatsoever arising from loss of data or profits arising out of, or in connection with, the use of this website.
        4. Changes to Terms of Service
        The website reserves the right to modify these terms of service at any time. Your continued use of the website following any changes to these terms constitutes your acceptance of the new terms.
        """)

    def display_privacy_policy(self):
        self.text_display.setPlainText("""
        Privacy Policy
        1. Introduction
        This privacy policy sets out how the website collects, uses, and protects any information that you provide when using the website. The website is committed to ensuring that your privacy is protected.
        2. Information Collection and Use
        The website may collect personal information from you, such as your name and email address, when you use the website. This information     is used to contact you about the services on the website in which you have expressed interest. The website may also use your information to respond to any inquiries you may have.
        3. Information Protection
        The website is committed to ensuring the security of your personal information. To prevent unauthorized access or disclosure, the website has implemented suitable physical, electronic, and managerial procedures to safeguard and secure the information collected online.
        4. Use of Cookies
        The website may use "cookies" to improve your experience. A cookie is a small file that is placed on your computer's hard drive. Cookies enable the website to recognize your browser and remember certain information. You may choose to set your web browser to refuse cookies, or to alert you when cookies are being sent. If you do so, please note that some parts of the website may not function properly.
        5. Third-Party Links
        The website may include links to third-party websites. These third-party sites have separate and independent privacy policies. The website therefore has no responsibility or liability for the content and activities of these linked sites. Nonetheless, the website seeks to protect the integrity of its site and welcomes any feedback about these sites.
        6. Changes to Privacy Policy
        The website may change this privacy policy from time to time. Your continued use of the website following any changes to this policy constitutes your acceptance of the new policy.
        """)

    def display_disclaimer(self):
        self.text_display.setPlainText("""
        Disclaimer
        1. Introduction
        The information contained on the website is for general information purposes only. The website makes no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the website or the information, products, services, or related graphics contained on the website for any purpose.
        2. Limitation of Liability
        The website will not be liable for any loss or damage including without limitation, indirect or consequential loss or damage, or any loss or damage whatsoever arising from loss of data or profits arising out of, or in connection with, the use of this website.
        3. External Links
        The website may contain links to external websites. The website is not responsible for the content of these external websites.
        4. Changes to Disclaimer
        The website may change this disclaimer from time to time. Your continued use of the website following any changes to this disclaimer constitutes your acceptance of the new disclaimer.
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    legal_info_generator = LegalInfoGenerator()
    legal_info_generator.show()
    sys.exit(app.exec_())



# In[ ]:





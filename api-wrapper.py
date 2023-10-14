from gmail_api_wrapper.crud.read import GmailAPIReadWrapper

gmail_api = GmailAPIReadWrapper()

gmail_api.check_new_mail(sender='do-not-reply@centraldispatch.com')
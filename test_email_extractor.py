from tools.email_extractor import extract_email

html_sample = '<a href="mailto:test@example.com">Contact</a>'
result = extract_email(html_sample)
print('Email found:', result)

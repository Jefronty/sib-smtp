# sib-smtp
SendInBlue SMTP mailer

* import into other Python scripts
* call directly with JSONic argument
* valid SendInBlue SMTP credentials required (_saved to sib.py_)
* optionally set default sender and recipient email addresses, making _t_ and _f_ values optional

# Example
```
import mailer
email = {}

# subject
email['s'] = 'Test email'

# message body
email['m'] = 'This email is only a test'

# recipient email address
eamil['t'] = 'me@example.net'

# sender
email['f'] = 'My custom mailer <info@example.net>'

mailer.sendMessage( email )
```
## or from terminal
`python mailer.py '{"s": "Test email", "m": "This email is only a test", "t": "me@example.net", "f": "My custom mailer <info@example.net>"}'`

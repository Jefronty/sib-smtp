import smtplib, json, os, sys

#credentials
import sib

# optional default values
default = {
	'sender': '', # ex: suto-mailer <noreply@mydomain.net>
	'recipient': '' # email address to receive message when no recipient is specified
}

# param is a dict with required keys: 's' (subject) and 'm' (message)
# optional keys: 'f' (from), 't' (To), 'h' (headers)
# h can be a formatted header string, list or tuple of header strings, or dict of k:v header pairs
def sendMessage(param):
	if 's' in param:
		subject = param['s']
	else:
		return {'status': False, 'description': 'missing subject [s]'}
	if 'm' in param:
		message = param['m']
	else:
		return {'status': False, 'description': 'missing body [m]'}
	if 'h' in param:
		headers = param['h']
		_type = type( headers )
	else:
		headers = False

	# create and send email
	mailserver = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
	mailserver.login(sib.user, sib.pw)

	# defaults
	sender = default['sender']
	recipient = default['recipient']
	if 'f' in param:
		sender = param['f']
	if 't' in param:
		recipient = param['t']
	if recipient == '':
		return {'status': False, 'description': 'no recipient named, set parameter [t]'}

	email = 'From: %s\nTo: %s' % (sender, recipient)
	email += '\nSubject: '+ param['s']
	if headers:
		# add custom headers
		if _type in (tuple, list):
			for h in headers:
				email += '\n%s' % h
		elif _type is dict:
			for k in headers:
				email += '\n%s: %s' % (k, headers[k])
		if _type is str:
			email += '\n%s' % headers
	email += "\n\n" + param['m']
	mailserver.sendmail(sender, recipient, email)
	return {'status': True, 'description': 'sent message'}

# file colled directly with JSONic string as argument
if __name__ == '__main__':
	try:
		arg = sys.argv[1]
	except:
		print( "No parameter provided!\nquitting" )
		sys.exit()
	try:
		param = json.loads( arg )
	except:
		print( "Valid JSON not found\nquitting" )
		sys.exit()

	sendMessage( param )

import smtplib, json, os, sys

#credentials
import sib

default = {
	'sender': 'My SMTP mailer <noreply@mydomain.net>',
	'recipient': '' # email address to receive message when no recipient is specified
}

def sendMessage(param):
	try:
		subject = param['s']
	except:
		return {'status': False, 'description': 'missing subject [s]'}
	try:
		message = param['m']
	except:
		return {'status': False, 'description': 'missing body [m]'}

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

import smtplib, json, os, sys

#credentials
import sib

__version__ = (1,0,2)

# optional default values
default = {
	'sender': '', # ex: suto-mailer <noreply@mydomain.net>
	'recipient': '' # email address to receive message when no recipient is specified
}

# param is a dict with required keys: 's' (subject) and 'm' (message)
# optional keys: 'f' (from), 't' (To), 'h' (headers)
# h can be a formatted header string, list or tuple of header strings, or dict of k:v header pairs
def sendMessage(param, show=False, extra={}):
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

	# add custom headers
	if extra:
		try:
			email += addHeader(extra)
		except:
			pass
	elif 'h' in param:
		try:
			email += addHeader(param['h'])
		except:
			pass
	email += "\n\n" + param['m']
	if show:
		print(email)
	try:
		mailserver.sendmail(sender, recipient, email)
	except:
		return {'status': False, 'description': 'Sendinblue API failed'}
	return {'status': True, 'description': 'sent message'}

def addHeader(val):
	_type = type(val)
	ret = []
	if _type is str:
		return '\n%s' % val
	elif _type in (tuple, list):
		for v in val:
			ret += addHeader(v)
	elif _type is dict:
		for k in val:
			ret += '\n%s: %s' % (k, val[k])
	return ''.join(ret)

# file colled directly
if __name__ == '__main__':
	import argparse
	desc = "Standalone script for sending simple email messages, message and subject values are required"
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('jsonic', nargs='?', help='parameters as JSON string [legacy support]')
	parser.add_argument('-s', '--subject', help='email subject string')
	parser.add_argument('-m', '--message', help='email body content')
	parser.add_argument('-f', '--from', help='sender email address to use, can include a name [Sender <sender@example.com]')
	parser.add_argument('-t', '--to', help='recipient email address')
	parser.add_argument('-d', '--header', nargs='+', help='custom header string')
	parser.add_argument('-v', '--verbose', action='store_true', help='display email content')
	parser.add_argument('-V', '--version', action='version', version='SendInBlue SMTP mailer v%s' % '.'.join(map(str, list(__version__))))
	arg = {}
	args = parser.parse_args()

	if args.jsonic:
		try:
			arg = json.loads(args.jsonic.strip("' "))
		except:
			print( args.jsonic )
			pass
	# individually given variables override jsonic values
	for key in ('message', 'subject', 'from', 'to'):
		val = getattr(args, key)
		if val:
			arg[key[0]] = val
	if not arg:
		print( "No parameter provided!\nquitting" )
		sys.exit()

	sendMessage(arg, extra=args.header, show=args.verbose)

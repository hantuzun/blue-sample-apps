#!/usr/bin/env python
#*******************************************************************************
#*   Ledger Blue
#*   (c) 2016 Ledger
#*
#*  Licensed under the Apache License, Version 2.0 (the "License");
#*  you may not use this file except in compliance with the License.
#*  You may obtain a copy of the License at
#*
#*      http://www.apache.org/licenses/LICENSE-2.0
#*
#*  Unless required by applicable law or agreed to in writing, software
#*  distributed under the License is distributed on an "AS IS" BASIS,
#*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#*  See the License for the specific language governing permissions and
#*  limitations under the License.
#********************************************************************************
from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
from secp256k1 import PublicKey

textToSign = "hello"

dongle = getDongle(True)
publicKey = dongle.exchange(bytes("8004000000".decode('hex')))
print "publicKey " + str(publicKey).encode('hex')
try:
	p1 = 0x80
	amount = "10.32"
	apdu = bytes("8010".decode('hex')) + chr(p1) + chr(0x00) + chr(len(amount)) + bytes(amount)
        amount_disp = dongle.exchange(apdu)
	offset = 0
	while offset <> len(textToSign):
		if (len(textToSign) - offset) > 255:
			chunk = textToSign[offset : offset + 255] 
		else:
			chunk = textToSign[offset:]
		if (offset + len(chunk)) == len(textToSign):
			p1 = 0x80
		else:
			p1 = 0x00
		apdu = bytes("8002".decode('hex')) + chr(p1) + chr(0x00) + chr(len(chunk)) + bytes(chunk)
		signature = dongle.exchange(apdu)
		offset += len(chunk)  
	print "signature " + str(signature).encode('hex')
	publicKey = PublicKey(bytes(publicKey), raw=True)
	signatureStuct = publicKey.ecdsa_deserialize(bytes(signature))
	print "verified " + str(publicKey.ecdsa_verify(bytes(textToSign), signatureStuct))
	sig = bytes(signature)
	try:
		sig_raw = publicKey.ecdsa_deserialize(sig)
		good = publicKey.ecdsa_verify(textToSign, sig_raw)
	except:
		good = False
	print good
except CommException as comm:
	if comm.sw == 0x6985:
		print "Aborted by user"
	else:
		print "Invalid status " + comm.sw 

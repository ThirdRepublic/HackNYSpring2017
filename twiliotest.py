from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACd462406da1770f0815a80eb4a74ffc40"
# Your Auth Token from twilio.com/console
auth_token  = "22dc45c5e28d04abe7fb277b75d3affc"

client = Client(account_sid, auth_token)

call = client.calls.create(to="+13473366702",
                           from_="+13476573267",
                           url="http://54.212.203.160/source/voice.xml")


message = client.messages.create(
    to="", 
    from_="+13476573267",
    body="Hello from Python!")


print(call.sid)
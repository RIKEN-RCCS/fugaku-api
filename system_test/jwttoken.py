import jwt
import sys
import time

sub = sys.argv[1]
secret = sys.argv[2]
iat = str(int(time.time()))
jwtToken = jwt.encode({"sub":sub, "iat":iat}, secret, algorithm="HS256")
print(f"{jwtToken}")

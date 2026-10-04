class security_log:
    def __init__(self,IP):
        self.IP=IP
    def parse_log_entry(self,log_line: str) -> dict:
        self.log_line=log_line

        for i in self.log_line:
            if self.IP not in i:
                raise InvalidLogFormatError("Log line does not contain IP address!")

user=security_log("8:0:10:9")

try:
    user.parse_log_entry({"Name":"Raju","IP":"8;0:10:9")


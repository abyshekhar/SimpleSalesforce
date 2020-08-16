import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType

loginInfo = json.load(open('login.json'))
username = loginInfo["username"]
password = loginInfo["password"]
security_token = loginInfo["securitytoken"]
domain = 'login'

# sf = Salesforce(username=username,password=password,security_token=security_token,domain=domain)
# the method below returns the session id and the instance as a tuple
session_id, instance = SalesforceLogin(username=username,
                                       password=password,
                                       security_token=security_token,
                                       domain=domain)

sf = Salesforce(instance=instance, session_id=session_id)
# print(dir(sf))
# print salesforce version
# print(sf.sf_version)

for item in dir(sf):
    if not item.startswith('-'):
        if (isinstance(getattr(sf, item), str)):
            print('Property Name:{0};Value"{1}'.format(item, getattr(sf,
                                                                     item)))

metadata_org = sf.describe()
# print(metadata_org.keys())
print(metadata_org['encoding'])
print(metadata_org['maxBatchSize'])
print(metadata_org['sobjects'])
df_sobjects = pd.DataFrame(metadata_org['sobjects'])
df_sobjects.to_csv('org metadata info.csv', index=False)

# method 1
account = sf.account
print(type(account))
account_metadata = account.describe()
print(type(account_metadata))
df_account_metadata = pd.DataFrame(account_metadata.get('fields'))
df_account_metadata.to_csv('account_metadata.csv', index=False)

# method2
contact = SFType('Contact', session_id, instance)
contact_metadata = contact.describe()
df_contact_metadata = pd.DataFrame(contact_metadata.get('fields'))
df_contact_metadata.to_csv('contact_metadata.csv', index=False)

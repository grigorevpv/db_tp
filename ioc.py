from injector import Injector

from api.repositories.connect import PostgresDataContext

psgDc = PostgresDataContext()

ioc = Injector([psgDc])
print(ioc)

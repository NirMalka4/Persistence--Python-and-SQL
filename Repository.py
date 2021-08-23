import sqlite3
from DAO import _Vaccines, _Suppliers, _Clinics, _Logistics
from DTO import Vaccine


class _Repository:
    vaccineIDCounter = totalInventory = totalDemand = totalReceived = totalSent = 0

    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()
        pass

    def creatTables(self):
        with self._conn:
            cursor = self._conn.cursor()
            cursor.executescript('CREATE TABLE vaccines(id INTEGER PRIMARY KEY, date DATETIME NOT NULL,'
                                 'supplier INTEGER REFERENCES suppliers(id),quantity INTEGER NOT NULL);'
                                 'CREATE TABLE suppliers(id INTEGER PRIMARY KEY,name TEXT NOT NULL,'
                                 'logistic INTEGER REFERENCES logistics(id));'
                                 'CREATE TABLE clinics(id INTEGER PRIMARY KEY,location TEXT NOT NULL,demand INTEGER NOT NULL,'
                                 'logistic INTEGER REFERENCES logistics(id));'
                                 'CREATE TABLE logistics(id INTEGER PRIMARY KEY,name TEXT NOT NULL,'
                                 'count_sent INTEGER NOT NULL,count_received INTEGER NOT NULL);'
                                 'CREATE TRIGGER VerifyLegalDemand AFTER UPDATE ON clinics '
                                 'FOR EACH ROW BEGIN UPDATE clinics SET demand=0 where demand<0; END;'
                                 'CREATE TRIGGER VerifyLegalQuantity AFTER UPDATE ON vaccines '
                                 'FOR EACH ROW BEGIN DELETE FROM vaccines WHERE quantity<=0; END;'
                                 )
            self._conn.commit()
        pass

    def receiveShipment(self, name, amount, date):
        supplierData = self.suppliers.getSupplierDetails(name)
        self.vaccines.insert(Vaccine(self.vaccineIDCounter,date, supplierData[0], amount))
        self.vaccineIDCounter += 1
        self.logistics.setCountReceived(amount, supplierData[1])
        self._conn.commit()
        self.updateReceiving(amount)
        return self.createOutput()

    def sendShipment(self, location, amount):
        warehouse = self.clinics.updateClinicDemand(location, amount)
        self.logistics.setCountSent(amount, warehouse)
        self.vaccines.updateInventory(amount)
        self.updateDelivery(amount)
        return self.createOutput()

    def updateDelivery(self, amount):
        self.totalSent += amount
        self.totalDemand -= amount
        self.totalInventory -= amount
        pass

    def updateReceiving(self, amount):
        self.totalInventory += amount
        self.totalReceived += amount
        pass

    def createOutput(self):
        return "{},{},{},{}".format(str(self.totalInventory), str(self.totalDemand), str(self.totalReceived), str(
            self.totalSent))

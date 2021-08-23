# Define methods for handling specific DB table
import DTO
from DTO import Vaccine


class _Vaccines:

    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute('INSERT INTO vaccines VALUES (?,?,?,?)',
                           (vaccine.id,vaccine.date, vaccine.supplier, vaccine.quantity))
        self._conn.commit()
        pass

    # Update vaccines inventory,maintain that older vaccines shipped prior to new ones
    def updateInventory(self, amount):

        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute('SELECT id,quantity,date FROM vaccines ORDER BY date ASC')
            inventory = cursor.fetchall()
            for row in inventory:
                currVaccineID = row[0]
                currVaccineQuantity = row[1]
                # deduct the supplied vaccines amount from current vaccine's quantity
                # if the supplied vaccines is exceeding current entry, it will be removed by predefined trigger
                # proceed to another iteration
                if amount <= 0:
                    break
                cursor.execute('UPDATE vaccines SET quantity=quantity-? WHERE id=?', (amount, currVaccineID))
                amount = amount - currVaccineQuantity

        pass


class _Suppliers:

    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute('INSERT INTO suppliers VALUES (?,?,?)', (supplier.id, supplier.name, supplier.logistic))
        pass

    def getSupplierDetails(self, name):
        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute('SELECT id,logistic FROM suppliers WHERE name=?', (name,))
            return cursor.fetchone()


class _Clinics:

    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute('INSERT INTO clinics VALUES (?,?,?,?)',
                           (clinic.id, clinic.location, clinic.demand, clinic.logistic))
        pass

    def updateClinicDemand(self, location, amount):
        warehouse = None
        with self._conn:
            cursor = self._conn.cursor()
            # Retrieve Clinic located in "location" with highest demand
            cursor.execute('SELECT id,demand,logistic FROM clinics WHERE location=? ORDER BY demand DESC', (location,))
            clinic = cursor.fetchone()
            # Deduct amount from current Clinic demand
            cursor.execute('UPDATE clinics SET demand=demand-? WHERE id=?', (amount, clinic[0]))
            warehouse = clinic[2]
        return warehouse


class _Logistics:

    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute('INSERT INTO logistics VALUES (?,?,?,?)', (logistic.id, logistic.name
                                                                      , logistic.count_sent, logistic.count_received))
        pass

    # Update relevant logistic service attribute "count_received"
    def setCountReceived(self, amount, warehouse):
        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute('UPDATE logistics SET count_received=count_received+? WHERE  id=? ',
                           (amount, warehouse))
        pass

    # Update relevant logistic service attribute "count_sent"
    def setCountSent(self, amount, warehouse):
        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute('UPDATE logistics SET count_sent=count_sent+? WHERE id=? ', (amount, warehouse))
        pass

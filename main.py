import Repository
import sys
from DTO import Vaccine, Supplier, Clinic, Logistic


def init_db(path):
    config = open(path, 'r')
    """
    Loading all line as there data to DB
    """
    amount = config.readline().strip('\n').split(',')
    repo.vaccineIDCounter = int(amount[0]) + 1
    for num in range(int(amount[0])):
        line = config.readline().strip('\n').split(',')
        repo.vaccines.insert(Vaccine(line[0], line[1], line[2], line[3]))
        repo.totalInventory += int(line[3])

    for num in range(int(amount[1])):
        line = config.readline().strip('\n').split(',')
        repo.suppliers.insert(Supplier(line[0], line[1], line[2]))

    for num in range(int(amount[2])):
        line = config.readline().strip('\n').split(',')
        repo.clinics.insert(Clinic(line[0], line[1], line[2], line[3]))
        repo.totalDemand += int(line[2])

    for num in range(int(amount[3])):
        line = config.readline().strip('\n').split(',')
        repo.logistics.insert(Logistic(line[0], line[1], line[2], line[3]))

    config.close()


def operate(path):
    """
    handle all orders
    """
    order = open(path, 'r')
    for line in order.readlines():
        line = line.strip('\n').split(',')
        if len(line) == 2:
            sendShip(line)
        else:
            reciveShip(line)
    order.close()


def reciveShip(line):
    """
    handle all receives and adding line to log file
    """
    log.write(repo.receiveShipment(line[0], int(line[1]), line[2]) + '\n')


def sendShip(line):
    """
    handle all sends and adding line to log file
    """
    log.write(repo.sendShipment(line[0], int(line[1])) + '\n')


def main():
    global repo, log
    repo = Repository._Repository()
    repo.creatTables()
    init_db(sys.argv[1])
    log = open(sys.argv[3], 'w')
    operate(sys.argv[2])
    repo.close()


if __name__ == '__main__':
    main()

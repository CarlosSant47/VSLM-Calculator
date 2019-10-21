# Autor Original en Java burhanloey
# Autor del Port en Python CarlosSant47

import math


class NeedNet:
    name = ""
    need = 0
    def __init__(self, n, ne):
        self.need = ne
        self.name = n




class Subnet:
    name = ""
    neededSize = 0
    allocatedSize = 0
    address = ""
    decMask = ""
    range = ""
    broadcast = ""
    mask = ""


class Integer:
    # Esta clase y su metodo tuve que extraerlos de la clase Integer de Java y Adaptarlos ya que no existian en Python
    SIZE = 32

    def highestOneBit(self):
        var0 = int(self)
        var0 |= var0 >> 1
        var0 |= var0 >> 2
        var0 |= var0 >> 4
        var0 |= var0 >> 8
        var0 |= var0 >> 16
        return var0 - (var0 >> 1)


def burbuja(subnets):
    A = subnets
    for i in range(1, len(A)):
        for j in range(0, len(A) - i):
            if A[j + 1].need > A[j].need:
                aux = A[j]
                A[j] = A[j + 1]
                A[j + 1] = aux
    return A


def convertIpToQuartet(ipAddress):
    octet1 = int((ipAddress >> 24) & 255)
    octet2 = int((ipAddress >> 16) & 255)
    octet3 = int((ipAddress >> 8) & 255)
    octet4 = int(ipAddress & 255)

    return str(octet1) + "." + str(octet2) + "." + str(octet3) + "." + str(octet4)


def findUsableHosts(mask):
    return int(math.pow(2, Integer.SIZE - mask) - 2)


def toDecMask(mask):
    if mask == 0:
        return "0.0.0.0"
    allOne = -1
    shifted = allOne << (Integer.SIZE - mask)
    return convertIpToQuartet(shifted)


def convertQuartetToBinaryString(majorNet):
    ip = majorNet.split(".")
    octet1 = ip[0]
    print(octet1)
    octet2 = int(ip[1])
    octet3 = int(ip[2])
    octet4 = ip[3]
    temp = octet4.split("/")
    octet4 = int(temp[0])
    result = int(octet1)
    result = int((result << 8) + octet2)
    result = int((result << 8) + octet3)
    result = int((result << 8) + octet4)
    return result


def calcMask(needSize):
    highestBit = Integer.highestOneBit(needSize)
    position = (int(math.log(highestBit) / math.log(2)))
    return Integer.SIZE - (position + 1)


def findFirstIp(majorNet):
    ip = majorNet.split("/")
    mask = int(ip[1])
    print(mask)
    offset = Integer.SIZE - mask
    majorAddress = convertQuartetToBinaryString(majorNet)
    first = (majorAddress >> offset) << offset
    return first


def calcVLSM(network, subnets):
    listsorted = burbuja(subnets)
    output = []
    currentIp = findFirstIp(network)
    for i in range(len(listsorted)):
        subnet = Subnet()

        subnet.name = listsorted[i].name
        subnet.address = convertIpToQuartet(currentIp)
        neededSize = int(listsorted[i].need)
        subnet.neededSize = neededSize
        mask = calcMask(neededSize)
        subnet.decMask = toDecMask(mask);
        subnet.mask = "/" + str(mask)
        allocatedSize = findUsableHosts(mask)
        subnet.allocatedSize = allocatedSize
        subnet.broadcast = convertIpToQuartet(currentIp + allocatedSize + 1)
        firstUsableHost = convertIpToQuartet(currentIp + 1)
        lastUsableHost = convertIpToQuartet(currentIp + allocatedSize)
        subnet.range = firstUsableHost + " - " + lastUsableHost
        output.append(subnet)
        currentIp += allocatedSize + 2

    return output


def main():
    network = "57.80.1.0/20"
    print("Bienvenido al VSLM Subnet Calculartor")
    print("Intrdouce la red con su submascara Ejemplo: 10.0.0.0/24")
    #network = network
    print("Introduce las redes que necesite")
    subnets = []
    subnets.append(NeedNet("Estudiantes", 1250))
    subnets.append(NeedNet("Contaduria", 70))
    subnets.append(NeedNet("Maestros", 10))
    subnets.append(NeedNet("Seguridad", 20))
    subnets.append(NeedNet("Telefonos", 40))

    result = calcVLSM(network, subnets)
    for i in range(len(result)):
        print(result[i].name + "\t" +
              str(result[i].neededSize) + "\t" +
              str(result[i].allocatedSize) + "\t" +
              result[i].address + "\t" +
              result[i].mask + "\t" +
              result[i].decMask + "\t" +
              result[i].range + "\t" +
              result[i].broadcast + "\t")



if __name__ == ('__main__'):
    main()

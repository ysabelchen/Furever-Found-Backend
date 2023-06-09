# Using the SagaPython language (created by the blockchain company PraSaga)
# Creating a generic asset class
# This will be a foundation class, but this is a rough example of it
# By default, class objects are owned by a global account object
# Class objects may be created, and owned by other accounts

def __hdr():
    hdr = {'acct': 'aaa',
           'seq': 1000,        # next sequence number
           'maxGU': 10,
           'feePerGU': 1,
           'extraPerGU': 2
           }
    return hdr


def __CMIClasses():

    # no signature required for creating global classes
    @SagaClass(CMIConst.SPClassObject)
    class ClsShelter:

        SagaFieldTable = []       # no user visible fields

        @SagaMethod()
        def __init__(self, name: str, address: str, description: str, initcount: int):
            self.assetcount = initcount  # internal instance variable
            self.name = name
            self.address = address
            self.description = description
            self.callcounter = 0
            self.pets = []

        @SagaMethod()
        def Increment(self, inc: int):
            self.assetcount += inc
            return self.assetcount

        @SagaMethod()
        def Decrement(self, dec: int):
            if self.assetcount - dec > 0:
                self.assetcount -= dec
                return self.assetcount
            else:
                raise RuntimeError("negative asset counts are illegal")

        @SagaMethod()
        def GetCount(self):
            return self.assetcount

        @SagaMethod()
        def GetAddress(self):
            return self.address

        @SagaMethod()
        def GetName(self):
            return self.name

        @SagaMethod()
        def GetDescription(self):
            return self.description

        # TODO: once adding an asset to an account is clear, we will be able to link the pet to a shelter by ID
        # until then, we're simply storing a list of petIDs.
        @SagaMethod()
        def AddPet(self, petId: str):
            self.pets.append(petId)

        @SagaMethod()
        def GetPets(self):
            return self.pets

        # internal method - example counts number of calls
        def callcount(self):
            self.callcounter += 1


def __body():

    # The name ClsShelter is only available to the transaction script
    # The objectID must be retrieved if the intent is to use the class
    # log it for user to recover it, could also store it in another object
    Log("Class ClsShelter LOID: ", ClsShelter.oid)

    # An instance of the new class can be instantiated
    classvar = ClsObjVar(ClsShelter)

    # initialized with 1 count of asset
    # Shelters and Owners should be instantiated as accounts, but no clear examples exist of how to instantiate / declare one.
    objloid = classvar.new(CMIConst.SPSystemAccount,
                           "San Mateo Shelter", "123 Main Street, San Mateo, CA",
                           "This is a description of a nice shelter in San Mateo",
                           1)
    objloid = objloid[0]
    #objloid1 = objloid[1]
    Log("ClsShelter Object Instance: ", objloid.oid)

    #Log("ClsShelter Object Instance: ", objloid1.oid)

    objvar = ClsObjVar(objloid)

    try:
        # illegal increment the local callcounter variable. callcount is internal only
        objvar.callcount()
    except:
        pass

    #count = objvar.Increment(10)
    #Log("Increment Count: ", count)

    objvar.AddPet("Whiskers1")
    objvar.AddPet("Sparky")
    objvar.AddPet("Fluffy")

    # make the objvar persistent by inserting it in the account list
    # acctvar.Insert(objvar)    # also sets owner field of objvar

    Log("the pets at shelter ", objvar.GetName(), "are : ", objvar.GetPets())

    return True


def __tail():
    return {'hash': 12345,
            'sig': (rvalue, svalue)    # tuple of r and s value for signature
            }
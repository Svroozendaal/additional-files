import csv
from rdflib import Graph, Literal, Namespace, RDF, URIRef, RDFS
from rdflib.namespace import XSD


# Load the existing RDF triples from your ontology
graph = Graph()

# Define the namespace for your ontology
CGO = Namespace("https://www.tno.nl/agrifood/ontology/common-greenhouse-ontology#")
OM = Namespace("https://www.ontology-of-units-of-measure.org/resource/om-2/")
SSN = Namespace("https://www.w3.org/ns/ssn/")

ROBOT = Namespace(CGO + "Robot")
GREENHOUSE = Namespace(CGO + "Greenhouse")
GREENHOUSESENSOR = Namespace(CGO + "GreenhouseSensor")
LOCATION = Namespace(CGO + "Location")
NOTIFICATION = Namespace(CGO + "Notification")
HONESTMESSAGE = Namespace(CGO + "HonestMessage")
CRMESSAGE = Namespace(CGO + "CoRangerMessage")

graph.bind("cgo", CGO)
graph.bind("om", OM)
graph.bind("ssn", SSN)

graph.bind("robot", ROBOT)
graph.bind("greenhouse", GREENHOUSE)
graph.bind("location", LOCATION)
graph.bind("Notification", NOTIFICATION)
graph.bind("HonestMsg", HONESTMESSAGE)
graph.bind("CoRangerMsg", CRMESSAGE)



# Read and process the CSV file
with open('test_sheet.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
            
        # Greenhouse
        greenhouseURI = GREENHOUSE[row["greenhouse_id"]]  # Identifier of the greenhouse
        graph.add((greenhouseURI, RDF.type, CGO.greenhouse)) #the greenhouse is of type CGO.greenhouse
            # Attributes of the 
        graph.add((greenhouseURI, CGO.hasID, Literal(row["greenhouse_id"], datatype=XSD.string)))
        graph.add((greenhouseURI, CGO.hasMapImage, Literal(row["greenhouse_map_image"])))
        
        # Robot
        robotURI = ROBOT[row["_id"]]  # Identifier of the robot
        graph.add((robotURI, RDF.type, CGO[row["type"] + "robot"]))  # robot is a subclass of robotrobot
        graph.add((greenhouseURI, CGO.robot, robotURI))
        # has as notification
            # Attributes of the Robot
        graph.add((robotURI, CGO.hasID, Literal(row["_id"], datatype=XSD.string)))
        graph.add((robotURI, CGO.hasNameString, Literal(row["call_sign"])))
        graph.add((robotURI, CGO.hasBatteryPercentage, Literal(row["battery"], datatype=XSD.integer)))

        graph.add((robotURI, SSN.hasProperty, OM.TotalDistanceTravelled))
        graph.add((robotURI, OM.TotalDistanceTravelled, Literal(row["driven_kms"])))
        graph.add((robotURI,  CGO.hasColorCode, Literal(row["type_color"])))

        graph.add((robotURI, CGO.hasServiceData, Literal(row["service_date"])))
        graph.add((robotURI, CGO.hasSerialNumber, Literal(row["bot_serial_number"], datatype=XSD.string)))
        graph.add((robotURI, CGO.lastUpdateTime, Literal(row["last_update_time"],  datatype=XSD.string)))
        graph.add((robotURI, CGO.lastUpdateTime, Literal(row["last_update_time"],  datatype=XSD.string)))
        # location of the Robot: robotLocation
        robotLocationURI = LOCATION[row["_id"]]
        graph.add((robotLocationURI, RDF.type, CGO.location)) # robotTypeURI is of type new_ontology.location
            # Connections of the robotLocation
        graph.add((robotURI, CGO.location, robotLocationURI))  # The robot -  has a location - robotLocation
            # Attributes of the robotLocation
        graph.add((robotLocationURI, CGO.hasLongitude, Literal(row["bot_pixel_x"])))
        graph.add((robotLocationURI, CGO.hasLatitude, Literal(row["bot_pixel_y"])))
        graph.add((robotLocationURI, CGO.hasAltitude, Literal(row["bot_pixel_z"])))


        # Status of the Robot: robotStatus
        robotStatusURI = URIRef(CGO[row["status"]])
        graph.add((robotStatusURI, RDF.type, CGO.robotStatus)) # robotStatusURI is of type new_ontology.robotStatus
            # Connections of the robotStatus
        graph.add((robotURI, CGO.robotStatus, robotStatusURI))  # The robot -  has a phase - robotStatus
        #
            # Attributes of the robotStatus
        graph.add((robotStatusURI, CGO.hasColorCode, Literal(row["status_color"])))      
        
        
        # Notification
        notificationURI = URIRef(NOTIFICATION[row["_id"]])  # Identifier of the notification
        graph.add((notificationURI, RDF.type, CGO.Notification)) #the notificatino is of type new_ontology notifictaion
            # Connections of the notification
        graph.add((notificationURI, CGO.isSentBy, robotURI))  # The robot -  has a notification - notification
        
        
        graph.add((notificationURI, CGO.contains, CGO.Message))
        
        MessageURI = URIRef(HONESTMESSAGE[row["_id"]])
        graph.add((MessageURI, RDF.type, CGO.HonestMessage))
        graph.add((MessageURI, CGO.hasConfidence, Literal(row["Confidence"]))) 
        graph.add((MessageURI, CGO.hasClassOutput, Literal(row["class_output"]))) 
        graph.add((MessageURI, CGO.hasBoundaryCoordinates, Literal(row["BoundryboxCoordinates"]))) 
               
            # Attributes of the notification
        graph.add((notificationURI, CGO.containsCustomSENSmsg, Literal(row["notification"])))
        graph.add((notificationURI, CGO.containsCustomSENSmsg, Literal(row["notification_message"])))
        
        sensorURI = URIRef(GREENHOUSESENSOR[row["notification_source"]])
        graph.add((sensorURI, RDF.type, CGO.GreenhouseSensor))
        graph.add((notificationURI, CGO.hasSource, sensorURI))
      


# Read and process the coranger csv data
with open('coranger data.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        
        
        MessageURI = URIRef(CRMESSAGE)
        graph.add((MessageURI, RDF.type, CGO.CRMessage))
        graph.add((MessageURI, CGO.hasDate, Literal(row["Date"]))) 
        graph.add((MessageURI, CGO.hasPosition, Literal(row["Position"]))) 
        graph.add((MessageURI, CGO.inPath, Literal(row["Pathnr"])))
        graph.add((MessageURI, CGO.wasReceivedAt, Literal(row["Time_Start"])))
        graph.add((MessageURI, CGO.wasSendOutAt, Literal(row["Time_End"])))    
        graph.add((MessageURI, CGO.hasDate, Literal(row["Date"])))    


# Save the updated RDF graph to an .ttl file
graph.serialize(destination="updated_ontology.ttl", format='ttl')

    


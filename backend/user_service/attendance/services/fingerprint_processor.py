from models import HardwareNode
from entities.models import University, School, Department, Set
from users.models import User

def process_fingerprint_scan(device_name, data):
    #data = fingerprint_id, timestamp
    device_name = data.get("device_name")
    event_type = data.get("event_type") #"fingerprint_scan" | "fingerprint_enrolled"
    fingerprint_id = data.get("fingerprint")
    timestamp = data.get("timestamp")

    if event_type == "fingerprint_scan":
        """
        Mark Attendance:
            [device_name: UNI_SCH_DPT_DVID]

            [{
                "event_type": "fingerprint_scan" | "fingerprint_enrolled",
                "fingerprint_id": 42,
                "timestamp": "2026-08-14T20:30:00Z"
            }]

            -get dept+start_year from device_name - this identifies the set, from there we get timetable/timetableentries/timetableentriesschedule
            -get user using fingerprint_stamp: device_name + fingerprint_id
            -create attendance object for user or mark present if created, for that user, for that timetableentryschedule->timetableentry->cource
            
            -I needed a way to tie the machine to a set
            -using level: the student will have to register every session and the device will have to receive new firmware update
            -using reg_no..2021, would have been a good idea but I remembered direct entry students
            -using set was the only unique way: currently set was year_lower/year_upper, so I changed it to start_year/end_year(inspired by linkedIn), but that was kind of too much.. so I though of using one year, (year_admitted or year_graduating).. we only truly know the former while the latter is liable to change(depending ASUU strike, or student having additional year),
            so for consistency, and the DE students simply belong to Sets (which might not necessarilly tally the first four numbers of their reg number)
        """
        try:
            hardware_node = HardwareNode.objects.get(name=device_name)
            #few more stuff
        except HardwareNode.DoesNotExist:
            print("The specified device does not exist")
            return
        try:
            uni, sch, dept, start_yr, sn = device_name.split("_")
            university = University.objects.get(code=uni)
            school = Department.objects.get(code=sch, university=university)
            department = Department.objects.get(code=dept, school=school)
            set = Set.objects.get(department=department, start_yr=start_yr)
        except:
            print("Could not retrieve, university, school, department or set, Check device name/thingname")

        """db pseudocode:
            #Obtain current timetable schedule for the retrieved set
            #first get current date, from the utc timestamp sent
            #map date to day
            #get timetable_entries for that day
            #get timetable_schedule in range of the time from timestamp
            #---error handling---
            #get user using fingerprint_stamp: (enrolled)device_name + fingerprint_id
            #create attendance object for user
            #
        """
        print(date)
        



    #database logic
    


def process_device_status(device_name, data):
    #handles device status
    pass
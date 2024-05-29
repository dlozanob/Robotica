#!/usr/bin/env python

'''
-- JOINT LIMITS ---
| J1: 0 - 819     |
| J2: 215 - 830   |
| J3: 215 - 810   |
| J4: 215 - 817   |
| J5: 224 - 1021  |
-------------------

-- JOINT LIMITS ---
Grados
| J1: 60 - 245     |
| J2: 90 - -90   |
| J3: 90 - -90   |
| J4: 90 - -90 |
| J5: 0 - 0 |

Equivalencia
| J1: 200 - 835 |
| J2: 200 - 850  |
| J3: 200 - 840   |
| J4: 200 - 835  |
| J5: 0 - 0 |

OFFSET = 500

Factor por grado
| J1: 0.45 |
| J2: 3.6  |
| J3: 3.5   |
| J4: 3.53  |
| J5: 0 - 0 |


P1: 



-------------------


'''
import rospy
import time
from dynamixel_workbench_msgs.srv import DynamixelCommand

def jointCommand(command, id_num, addr_name, value, time):
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:
        dynamixel_command = rospy.ServiceProxy(
            '/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        result = dynamixel_command(command,id_num,addr_name,value)
        #rate.sleep()
        rospy.sleep(time)
        return result.comm_result
    except rospy.ServiceException as exc:
        print(str(exc))

def setTorqueLimits(tl):
    for i in range(len(tl)):
        jointCommand('', i + 1, 'Torque_Limit', tl[i], 0)

def setPose(q, takt):
    for i in range(len(q)):
        jointCommand('', i + 1, 'Goal_Position', q[i], takt)


def readData():
    try:
        with open('/home/daniel/catkin_ws/src/px_robot/scripts/jointData.txt', 'r') as f:
            content = f.read()
        #raise Exception
        #raise FileReadException("File not available rn")
    except Exception:
        print("File not available rn")
   
    content = content[1:-1].split('\n')
    content = [int(float(x)) for x in content]
    return content

def correctValues(data):
    a = list(data)
    factors = [3.53, 3.6, 3.5, 3.53, 3.5]
    for i in range(len(a)):
        a[i] = int((-1*a[i]+90)*factors[0]+200)
        #a[i] = int(500-a[i])
    return a

if __name__ == '__main__':
    global rate
    rospy.init_node('client_node', anonymous=False)
    takt = 1
    #rate = rospy.Rate(0.3)
    try:
        torqueLimits = [600, 500, 400, 400, 300]
        prevJointData = [0, 0, 0, 0, 0]

        setTorqueLimits(torqueLimits)
        while True:
            
            jointData = readData()
            jointData = correctValues(jointData)
            print("\nReceived:\t{0}\n".format(jointData))

            # Update pose
            if (not(jointData == prevJointData)):
                setPose(jointData, takt)
                prevJointData = list(jointData)
            time.sleep(0.5)

    except rospy.ROSInterruptException:
        pass

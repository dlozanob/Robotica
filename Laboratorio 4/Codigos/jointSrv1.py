#!/usr/bin/env python

'''
-- JOINT LIMITS ---
| J1: 0 - 819     |
| J2: 215 - 830   |
| J3: 215 - 810   |
| J4: 215 - 817   |
| J5: 224 - 1021  |
-------------------
'''
import rospy
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


if __name__ == '__main__':
    global rate
    rospy.init_node('client_node', anonymous=False)
    takt = 1
    #rate = rospy.Rate(0.3)
    try:
        #torqueLimits = [600, 500, 400, 400, 400]
        torqueLimits = [600, 500, 400, 400, 300]
        p1 = [0, 398, 850, 426, 1021]
        p2 = [206, 684, 746, 742, 400]
        
        c0 = [827, 545, 509, 514, 700]
        c1 = [507, 317, 334, 287, 410]
        c2 = [848, 480, 315, 392, 410]
        c3 = [827, 415, 315, 212, 600]

        setTorqueLimits(torqueLimits)
        setPose(p1, takt)
        setPose(p2, takt)
        setPose(p1, takt)

        setPose(c0, takt)
        # jointCommand('', 1, 'Goal_Position', c1[0], takt)
        # jointCommand('', 2, 'Goal_Position', 320, takt)
        # jointCommand('', 2, 'Goal_Position', c1[1], takt)
        # jointCommand('', 3, 'Goal_Position', c1[2], takt)
        # jointCommand('', 4, 'Goal_Position', c1[3], takt)
        # jointCommand('', 5, 'Goal_Position', c1[4], takt)

        # jointCommand('', 2, 'Goal_Position', c2[1], takt)
        # jointCommand('', 1, 'Goal_Position', c2[0], takt)
        # jointCommand('', 3, 'Goal_Position', c2[2], takt)
        # jointCommand('', 4, 'Goal_Position', c2[3], takt)
        # jointCommand('', 5, 'Goal_Position', c2[4], takt)

        # jointCommand('', 1, 'Goal_Position', c3[0], takt)
        # jointCommand('', 2, 'Goal_Position', c3[1], takt)
        # jointCommand('', 4, 'Goal_Position', c3[3], takt)
        # jointCommand('', 3, 'Goal_Position', c3[2], takt) 
        # jointCommand('', 5, 'Goal_Position', c3[4], takt)
        # setPose(c0, takt)



    except rospy.ROSInterruptException:
        pass

'''
ORIGINAL:
J1: 150
J2: 152.93
J3: 62.4
J4: 150
'''

'''
HOME:
J1: 0
J2: 116.89
J3: 249.9
J4: 124.8
'''

'''
HOME: (ORIGINAL = 0)
J1: -150 +
J2: -36 -
J3: 186.6 -
J4: -25.2 -
'''

'''
POSE 2: (ORIGINAL = 0)
J1: -90.23 +
J2:  49.51 -
J3: 157.03 -
J4: 67.38 -
'''




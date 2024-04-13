import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportRelative
import termios, sys, os
import numpy as np

from std_srvs.srv import Empty as EmptyServiceCall

TERMIOS = termios

def sgn(num):
    s = 0
    if(num < 0): s = -1
    elif(num > 0): s = 1
    return s 

def limFilter(vf, curSgn):
    ls = 50
    li = 1
    if((curSgn == li and vf > ls) or (curSgn == -li and vf < -ls)):
        vf = ls
        vf *= curSgn
    elif((curSgn == li and vf < li) or (curSgn == -li and vf > -li)):
        vf = li
        vf *= curSgn
    return vf

def getKey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    c = str(c)[2]
    return c

def updateState(x, y, th, status):
    vel_msg.linear.x = x
    vel_msg.linear.y = y
    vel_msg.angular.z = th
    vel_pub.publish(vel_msg)

    if(status == 1):
        tp_abs(initPose[0], initPose[1], 0)
    elif(status == -1):
        tp_rel(0, np.pi)

def main():
    global vel_pub, vel_msg, tp_abs, tp_rel, initPose
    
    rospy.init_node('jog_node')
    clear_background = rospy.ServiceProxy('clear', EmptyServiceCall)
    vel_pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    tp_abs = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
    tp_rel = rospy.ServiceProxy('turtle1/teleport_relative', TeleportRelative)

    vf = 1
    ac = 2
    initPose = [5.544444561004639, 5.544444561004639]

    while True:
        
        x, y, th = 0, 0, 0
        status = 0
        curSgn = sgn(vf)
	
        key = getKey()
        if(key in ('w', 'W')):
            y = vf
        elif(key in ('a', 'A')):
            x = -vf
        elif(key in ('s', 'S')):
            y = -vf
        elif(key in ('d', 'D')):
            x = vf
        elif(key in ('q', 'Q')):
            th = -50*(vf*np.pi)/180
        elif(key in ('e', 'E')):
            th = 50*vf*np.pi/180
        elif(key in ('m', 'M')):
            vf += ac*curSgn
        elif(key in ('n', 'N')):
            vf -= ac*curSgn
        elif(key in ('r', 'R')):
            status = 1
            vf = np.abs(vf)
            curSgn = sgn(vf)
        elif(key == ' '):
            status = -1
            vf *= -1
            curSgn = sgn(vf)
        elif(key in ('z', 'Z')):
            print('Process terminated.')
            break

        vf = limFilter(vf, curSgn)
        updateState(x, y, th, status)
    return 0

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print('Exception ocurred')


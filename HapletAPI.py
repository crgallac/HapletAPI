"""
A library to interface Haplet through serial connection
"""
import serial

class Haplet():
    """
    Models an Arduino connection
    """

    def __init__(self, serial_port='COM7', baud_rate=57600,
            read_timeout=2): #2 ms 
        """
        Initializes the serial connection to the Haplet board
        """
        self.conn = serial.Serial(serial_port, baud_rate)
        self.conn.timeout = read_timeout # Timeout for readline()

    def write_force(self, mode, fx, fy):
        """
        Performs a pinMode() operation on pin_number
        Internally sends b'M{mode}{pin_number} where mode could be:
        - I for INPUT
        - O for OUTPUT
        - P for INPUT_PULLUP MO13
        """

        command = (''.join(('W',mode,':',str(fx), str(fy)))).encode()
        #print 'set_pin_mode =',command,(''.join(('W',mode,':',str(fx), str(fy))))
        self.conn.write(command)

    def read_task_state(self, mode):
        """
        Performs a digital read on pin_number and returns the value (1 or 0)
        Internally sends b'RD{pin_number}' over the serial connection
        """
        
        command = (''.join(('R', mode))).encode()
        self.conn.write(command)
        line_received = self.conn.readline().decode().strip()
        header, x, y, xdot, ydot  = line_received.split(':') # e.g. P:1.0:2.0:3.0:4.0
        if header == ('P'):
            # If header matches
            return (float(x), float(y), float(xdot), float(ydot))


   def read_joint_state(self, mode):
        """
        Performs a digital read on pin_number and returns the value (1 or 0)
        Internally sends b'RD{pin_number}' over the serial connection
        """
        
        command = (''.join(('R', mode))).encode()
        self.conn.write(command)
        line_received = self.conn.readline().decode().strip()
        header, q1, q2, q1dot, q2dot  = line_received.split(':') # e.g. P:1.0:2.0:3.0:4.0
        if header == ('J'):
            # If header matches
            return (float(q1), float(q2), float(q1dot), float(q2dot))

    def close(self):
        """
        To ensure we are properly closing our connection to the
        Arduino device. 
        """
        self.conn.close()
        print ('Connection to Arduino closed')

import queue
from pylsl import StreamInlet, resolve_stream
from easytello import tello
my_drone = tello.Tello()
"""Example program to show how to read a multi-channel time series from LSL."""


queue_len = 50

q = queue.Queue(maxsize = queue_len)
# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('name', 'OpenViBE Stream1')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])
takeOffOrNot = 0
while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    sample, timestamp = inlet.pull_sample()
    if(sample[0]>0):
        tmp = 1
    else:
        tmp = 0
        
    if q.qsize()<queue_len:
        q.put(tmp)
    else:
        _ = q.get()
        q.put(tmp)

    
    ratio = (sum(list(q.queue))/len(list(q.queue)))


    if ratio>0.9 and len(list(q.queue)) == queue_len:
        print("take off",ratio)
        my_drone.takeoff()
        
    elif ratio<0.7:
        print("land it",ratio)
        my_drone.land()
        
        
#     print(list(q.queue), ratio)
#     print(timestamp, sample[0], tmp)
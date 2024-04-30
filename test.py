#create a loop that loops thorugh the list over and over

frames = ["frame1", "frame2", "frame3", "frame4"]

x = 0
print(frames[x])
x+=1
print(frames[x])
x+=1
print(frames[x])
x+=1
print(frames[x])
x+=1
# x is now 4
# print(frmaes[x])
firstFrame = x%len(frames)
print(frames[firstFrame])

clock = pg.time.clock()
then = 0 
last_update = 0
current_frame = 0
while True:
    #print("forever....")
    now = pg.time.get_ticks()
    if now - then > 200:
        print(frames[firstFrame])
        print("time for a new frame")
        print(now)
        then = now
    clock.tick(FPS)





#x = 0
#while True:
    #   print(frames[x])
    #  x = (x + 1) % len(frames)
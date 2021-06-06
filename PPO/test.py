import gym 

env = gym.make('gym_robot_arm:robot-arm-v0')

for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print("[",t,"]","observation:",observation,"reward:",reward,"action:",action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()

# import numpy as np
# import time
# import matplotlib.pyplot as plt

# x = np.linspace(0, 10, 100)
# y = np.cos(x)

# plt.ion()

# figure, ax = plt.subplots(figsize=(8,6))
# line1, = ax.plot(x, y)

# plt.title("Dynamic Plot of sinx",fontsize=25)

# plt.xlabel("X",fontsize=18)
# plt.ylabel("sinX",fontsize=18)

# for p in range(100):
#     updated_y = np.cos(x-0.05*p)
    
#     line1.set_xdata(x)
#     line1.set_ydata(updated_y)
    
#     figure.canvas.draw()
    
#     figure.canvas.flush_events()
#     time.sleep(0.1)
import os
import gym
import numpy as np
from ppo_torch import Agent
from utils import plot_learning_curve

if __name__ == '__main__':
    render_on = False
    env = gym.make('gym_robot_arm:robot-arm-v0')
    #env = gym.make('CartPole-v0')
    n_episode = 100
    n_learn_step = 50
    n_iter = 100
    batch_size = 64
    n_epochs = 10
    #alpha = 0.09
    alpha = 0.0003
    agent = Agent(n_actions=env.action_space.n, batch_size=batch_size, 
                    alpha=alpha, n_epochs=n_epochs, 
                    input_dims=env.observation_space.shape)
    
    figure_file = os.getcwd() + '/plots/robot_arm.png'
    #figure_file = os.getcwd() + '/plots/cartpole.png'

    best_score = env.reward_range[0]
    score_history = []

    learn_iters = 0
    avg_score = 0
    n_steps = 0

    for episode in range(n_episode):
        observation = env.reset()
        done = False
        score = 0
        for iter in range(n_iter):
            if render_on:
                env.render()
            action, prob, val = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            n_steps += 1
            score += reward
            agent.remember(observation, action, prob, val, reward, done)
            if n_steps % n_learn_step == 0:
                agent.learn()
                learn_iters += 1
            observation = observation_
            #print('[',episode+1,'/',n_episode,']','[',iter+1,'/',n_iter,']', 'action', action, 'reward %.1f' % reward)
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            agent.save_models()

        print('episode', episode, 'score %.1f' % score, 'avg score %.1f' % avg_score,
                'time_steps', n_steps, 'learning_steps', learn_iters)
        
    x = [i+1 for i in range(len(score_history))]
    plot_learning_curve(x, score_history, figure_file)
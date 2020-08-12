#!/usr/bin/env python
import gym
import gym_gvgai
import sys, os, pickle
import signal
from random import randint

def team(name, team_score, team_win):
    d = {}
    d['name'] = name
    d['score'] = team_score
    d['win'] = team_win
    d['games'] = []
    return d


def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError
 
        def time_limit(*args, **kwargs):
            action_num = len(kwargs['actions'])
            try:
                signal.signal(signal.SIGALRM, handle) 
                signal.setitimer(signal.ITIMER_REAL, num)
                r = func(*args, **kwargs)
                signal.setitimer(signal.ITIMER_REAL, 0)
            except RuntimeError as e:
                r = callback(action_num)
            return r
 
        return time_limit
 
    return wrap

def after_timeout(action_num):  # random action if agent's response time is greater than 40ms
    action_id = randint(0,action_num-1)
    return action_id

@set_timeout(0.06, after_timeout)  # limit to 40ms for each second
def agent_action(state_obs, actions):
    action_id = agent.act(state_obs, actions)
    return action_id

usr = sys.argv[1]
new_team = team(user, [], [])


testing_times = 20
# Predefined names referring to framework
games = ['golddigger', 'treasurekeeper', 'waterpuzzle']
test_levels = ['lvl2', 'lvl3', 'lvl4']

try: 
    import Agent as Agent
    for game_name in games:
        for level in test_levels:
            env = gym_gvgai.make('gvgai-' + game_name + '-'+level+'-v0')
            agent = Agent.Agent()
            # print('Starting ' + env.env.game + " with Level " + str(env.env.lvl))
            total_score = []  # record every testing score
            win_num = 0
            # reset environment
            actions = env.env.GVGAI.actions()
            state_obs = None
            INFO = game_name + level + "\n"
            print(game_name, level)
            for i in range(testing_times):  # testing 20 times
                current_score = 0  # record current testing round score
                state_obs = env.reset()
                for t in range(2000):
                    action_id = agent_action(state_obs, actions=actions)
                    state_obs, incre_score, done, debug = env.step(action_id)
                    current_score += incre_score
                    if done:
                        print("Game over at game tick " + str(t+1) + " with player " + debug['winner'] + ", score is " + str(current_score))
                        break

                if (debug['winner'] == "PLAYER_WINS"):
                    win_num += 1
                total_score.append(current_score)
            avr_score = sum(total_score) / testing_times
            
            
            new_team["win"].append(win_num)
            new_team["score"].append(avr_score)
            new_team["games"].append(game_name + "-" + level)

    success = True
except Exception as err:
    success = False
    print("Error"+str(err))



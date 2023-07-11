from snake_agent import snakeAgent
from snake_environment import SnakeEnv
from tqdm import tqdm
import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecEnvWrapper 
from snake_helper import training_evaluation
import pickle
import argparse

def run_A2C(size, is_training = True):
    n_episodes = 50_000
    model = 'A2C'
    
    #env = VecEnvWrapper(env)
    if is_training:
        env = SnakeEnv(render_mode=None, size = size, model=model)
        #env = make_vec_env(env, n_envs=1)
        model = A2C("MultiInputPolicy", env, verbose=1)
        model.learn(total_timesteps=n_episodes)
        model.save("a2c_snake")

    else:
        env = SnakeEnv(render_mode='human', size = size, model=model)
        env = gym.wrappers.RecordEpisodeStatistics(env, deque_size=n_episodes)
        model = A2C.load("a2c_snake")
        obs = env.reset()      
        for _ in range(n_episodes):
            obs, info = env.reset()
            done = False
            # play one episode
            while not done:
                action, _states = model.predict(obs, deterministic=True)
                obs, rewards, terminated, truncated, info = env.step(action)
                # update if the environment is done and the current obs
                done = terminated or truncated
            print("Score: {}".format(env.score))

def run_q_learning(size, is_training = True):
    n_episodes = 1_000
    model = 'q_learn'

    if is_training:
        # hyperparameters
        learning_rate = 0.01
        start_epsilon = 1.0
        epsilon_decay = start_epsilon / (n_episodes / 2)  # reduce the exploration over time
        final_epsilon = 0.001
        
        render_mode = None
        env = SnakeEnv(render_mode=render_mode, size = size, model=model)
        env = gym.wrappers.RecordEpisodeStatistics(env, deque_size=n_episodes)
        agent = snakeAgent(
            learning_rate=learning_rate,
            initial_epsilon=start_epsilon,
            epsilon_decay=epsilon_decay,
            final_epsilon=final_epsilon,
            env=env
        )
        for episode in tqdm(range(n_episodes)):
            obs, info = env.reset()
            done = False
            # play one episode
            while not done:
                action = agent.get_action(obs, env, is_training)
                next_obs, reward, terminated, truncated, info = env.step(action)
                # update the agent
                agent.update(obs, action, reward, terminated, next_obs)
                # update if the environment is done and the current obs
                done = terminated or truncated
                obs = next_obs
            agent.decay_epsilon()

        training_evaluation(env, agent)
        pickle.dump(agent, open('agent.pkl', 'wb'))
    else:
        agent = pickle.load(open('agent.pkl', 'rb'))
        render_mode = 'human'
        env = SnakeEnv(render_mode=render_mode, size = size, model=model)
        env = gym.wrappers.RecordEpisodeStatistics(env, deque_size=n_episodes)
        print(len(agent.q_values))
        for _ in range(n_episodes):
            obs, info = env.reset()
            done = False
            while not done:
                action = agent.get_action(obs, env, is_training)
                obs, reward, terminated, truncated, info = env.step(action)
                #print(info)
                # update if the environment is done and the current obs
                done = terminated or truncated
            print("Score: {}".format(env.score))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument('--train', default=False, action='store_true')
    parser.add_argument('--test' , dest='train', action='store_false')
    parser.add_argument("-m", default = None, required = True, choices=["qlearn", "a2c"], help = "Specify model to be played")
    parser.add_argument("-s", default = None, required = True, help = "Play areas are squares, specify length. Agent must be trained in a given play area to be tested later")

    args = parser.parse_args()
    t = args.train
    m = args.m
    s = int(args.s)

    if m == 'qlearn':
        run_q_learning(s, is_training = t)
    else:
        run_A2C(s, is_training = t)

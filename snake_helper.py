from snake_agent       import snakeAgent
from snake_environment import SnakeEnv
from tqdm              import tqdm
from stable_baselines3 import PPO
from stable_baselines3 import A2C
from datetime          import datetime
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env  import VecEnvWrapper 
from stable_baselines3.common.vec_env  import SubprocVecEnv
import gymnasium         as gym
import numpy             as np
import matplotlib.pyplot as plt
import pickle

def run_PPO(size, is_training = True):
    n_episodes = 200_000
    model = 'PPO'
    
    if is_training:
        env = SnakeEnv(render_mode = None, size = size, model = model)
        #vec_env = make_vec_env("CartPole-v1", n_envs=4)
        model = PPO("MultiInputPolicy", env, verbose=1)
        model.learn(total_timesteps=n_episodes)
        model.save("ppo_snake")
    else:
        env = SnakeEnv(render_mode = 'human', size = size, model = model)
        env = gym.wrappers.RecordEpisodeStatistics(env, deque_size=n_episodes)
        model = PPO.load("ppo_snake")
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

def run_A2C(size, is_training = True):
    n_episodes = 200_000
    model = 'A2C'
    
    if is_training:
        env = SnakeEnv(render_mode = None, size = size, model = model)
        model = A2C("MultiInputPolicy", env, verbose=1)
        model.learn(total_timesteps=n_episodes)
        model.save("a2c_snake")

    else:
        env = SnakeEnv(render_mode='human', size = size, model=model)
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

def run_q_learning(size, is_pickle = False, is_training = True):
    n_episodes = 500
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
        if is_pickle:
            agent = pickle.load(open('q_learn.pkl', 'rb'))
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

def training_evaluation(env, agent):
    rolling_length = 500
    fig, axs = plt.subplots(ncols=3, figsize=(12, 5))
    axs[0].set_title("Episode rewards")
    # compute and assign a rolling average of the data to provide a smoother graph
    reward_moving_average = (
        np.convolve(
            np.array(env.return_queue).flatten(), np.ones(rolling_length), mode="valid"
        )
        / rolling_length
    )
    axs[0].plot(range(len(reward_moving_average)), reward_moving_average)
    axs[1].set_title("Episode lengths")
    length_moving_average = (
        np.convolve(
            np.array(env.length_queue).flatten(), np.ones(rolling_length), mode="same"
        )
        / rolling_length
    )
    axs[1].plot(range(len(length_moving_average)), length_moving_average)
    axs[2].set_title("Training Error")
    training_error_moving_average = (
        np.convolve(np.array(agent.training_error), np.ones(rolling_length), mode="same")
        / rolling_length
    )
    axs[2].plot(range(len(training_error_moving_average)), training_error_moving_average)
    plt.tight_layout()

    file_name = get_file_name()
    plt.savefig('./runs/' + file_name)

def get_file_name():
    
    # get current date and time
    current_datetime = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        
    # create a file object along with extension
    file_name = current_datetime + ".png"
    
    return file_name
from snake_agent import snakeAgent
from snake_environment import SnakeEnv
from tqdm import tqdm
import gymnasium as gym
from stable_baselines3.sac.policies import MlpPolicy
from stable_baselines3 import SAC
from snake_helper import training_evaluation
import pickle


def run_SAC(size):
    env = SnakeEnv(render_mode=None, size = size)
    #rl_agent = SAC.load("SAC", env, learning_rate=0.00007)
    rl_agent = SAC("MlpPolicy", env, verbose=1, learning_rate=0.000001, learning_starts=1000)
    rl_agent.learning_rate = 0.003 # Not needed
    rl_agent.learn(total_timesteps=100000)
    rl_agent.save("SAC_Learned")

def run_q_learning(size, is_training = True):

    n_episodes = 200_000

    
    if is_training:

        # hyperparameters
        learning_rate = 0.01
        start_epsilon = 1.0
        epsilon_decay = start_epsilon / (n_episodes / 2)  # reduce the exploration over time
        final_epsilon = 0.1
        
        render_mode = None

        env = SnakeEnv(render_mode=render_mode, size = size)
        env = gym.wrappers.RecordEpisodeStatistics(env, deque_size=n_episodes)


        agent = snakeAgent(
            learning_rate=learning_rate,
            initial_epsilon=start_epsilon,
            epsilon_decay=epsilon_decay,
            final_epsilon=final_epsilon,
            env=env
        )

        counter = 0

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

                '''if counter > 0.1 * n_episodes:
                    env._render_frame()'''

            agent.decay_epsilon()
            counter  = counter + 1

        training_evaluation(env, agent)

        pickle.dump(agent, open('agent.pkl', 'wb'))
    
    else:

        agent = pickle.load(open('agent.pkl', 'rb'))

        render_mode = 'human'

        env = SnakeEnv(render_mode=render_mode, size = size)
        env = gym.wrappers.RecordEpisodeStatistics(env, deque_size=n_episodes)

        #print(agent.q_values)
    
        for episode in range(n_episodes):
            obs, info = env.reset()
            done = False

            # play one episode
            while not done:
                action = agent.get_action(obs, env, is_training)
                next_obs, reward, terminated, truncated, info = env.step(action)

                # update if the environment is done and the current obs
                done = terminated or truncated
                obs = next_obs

            print("Score: {}".format(env.score))
    

if __name__ == "__main__":
    
    run_q_learning(10, is_training = False)

    #run_SAC()

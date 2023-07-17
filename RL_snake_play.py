from snake_helper import run_PPO, run_A2C, run_q_learning
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'Guide how to use RL_snake_play.py')
    parser.add_argument('--train', default = False, action='store_true')
    parser.add_argument('--test' , dest = 'train', action='store_false')
    parser.add_argument("-m", default = None, required = True, choices=["qlearn", "a2c", "ppo"], help = "Specify model to be played. Example: python RL_snake_play.py -s 20 -m qlearn --train")
    parser.add_argument("-s", default = None, required = True, help = "Play areas are squares, specify length. Agent must be trained in a given play area to be tested later")
    parser.add_argument("-q", default = False, required = False, type = bool, help = "Use pre-trained Q-learning model, -q True")

    args = parser.parse_args()
    t = args.train
    m = args.m
    s = int(args.s)
    q = args.q

    if m == 'qlearn' or q:
        run_q_learning(s, q, is_training = t)
    elif m == 'a2c':
        run_A2C(s, is_training = t)
    elif m == 'ppo':
        run_PPO(s, is_training = t)

#coding: utf-8
from __future__ import division
import argparse

from PIL import Image
import numpy as np
#import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Convolution2D, Permute
from keras.optimizers import Adam
import keras.backend as K

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor, Env
from rl.callbacks import FileLogger, ModelIntervalCheckpoint

import ctypes

INPUT_SHAPE = (84, 84)
WINDOW_LENGTH = 4

#=====================iniciar a memoria compartilhada com o controle==============
import sys

""" Initiate the path to blackboard (Shared Memory)"""
sys.path.append('../../Blackboard/src/')
"""Import the library Shared memory """
from SharedMemory import SharedMemory 
""" Treatment exception: Try to import configparser from python. Write and Read from config.ini file"""
try:
    """There are differences in versions of the config parser
    For versions > 3.0 """
    from ConfigParser import ConfigParser
except ImportError:
    """For versions < 3.0 """
    from ConfigParser import ConfigParser 

""" Instantiate bkb as a shared memory """
bkb = SharedMemory()
""" Config is a new configparser """
config1 = ConfigParser()
""" Path for the file config.ini:"""
config1.read('../../Control/Data/config.ini')
""" Mem_key is for all processes to know where the blackboard is. It is robot number times 100"""
mem_key = int(config1.get('Communication', 'no_player_robofei'))*100 
"""Memory constructor in mem_key"""
Mem = bkb.shd_constructor(mem_key)
#===================================================================================


class AtariProcessor(Processor):
    def process_observation(self, observation):
        assert observation.ndim == 3  # (height, width, channel)
        image_pointer = testlib.leitura_int()
        im_width = image_pointer[0]
        im_height = image_pointer[1]
        im_size_array = im_width*im_height*3+2
        imgM = np.array(image_pointer[2:im_size_array]).reshape( im_height, im_width, 3)
        img = Image.fromarray(imgM.astype('uint8'))
#        img.show()
        img = img.resize(INPUT_SHAPE).convert('L')  # resize and convert to grayscale
#        img.show()
        processed_observation = np.array(img)
        assert processed_observation.shape == INPUT_SHAPE
        return processed_observation.astype('uint8')  # saves storage in experience memory

    def process_state_batch(self, batch):
        # We could perform this processing step in `process_observation`. In this case, however,
        # we would need to store a `float32` array instead, which is 4x more memory intensive than
        # an `uint8` array. This matters if we store 1M observations.
        processed_batch = batch.astype('float32') / 255.
        return processed_batch

    def process_reward(self, reward):
        return np.clip(reward, -1., 1.)


testlib = ctypes.CDLL('/home/fei/RoboFEI-HT_DRL/AI/DRL/examples/blackboard/blackboard.so') #chama a lybrary que contem as funções em c++
testlib.using_shared_memory()   #usando a função do c++
testlib.leitura_int.restype = ctypes.POINTER(ctypes.c_int) #define o tipo de retorno da função, neste caso a função retorna ponteiro int

parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=['train', 'test'], default='train')
parser.add_argument('--env-name', type=str, default='goalKeeper')
parser.add_argument('--weights', type=str, default=None)
args = parser.parse_args()

# Get the environment and extract the number of actions.
#env = gym.make("BreakoutDeterministic-v4")
env = Env(testlib, Mem, bkb)
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space


# Next, we build our model. We use the same model that was described by Mnih et al. (2015).
input_shape = (WINDOW_LENGTH,) + INPUT_SHAPE
model = Sequential()
if K.image_dim_ordering() == 'tf':
    # (width, height, channels)
    model.add(Permute((2, 3, 1), input_shape=input_shape))
elif K.image_dim_ordering() == 'th':
    # (channels, width, height)
    model.add(Permute((1, 2, 3), input_shape=input_shape))
else:
    raise RuntimeError('Unknown image_dim_ordering.')
model.add(Convolution2D(32, 8, 8, subsample=(4, 4)))
model.add(Activation('relu'))
model.add(Convolution2D(64, 4, 4, subsample=(2, 2)))
model.add(Activation('relu'))
model.add(Convolution2D(64, 3, 3, subsample=(1, 1)))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())


bkb.write_int(Mem,'LIBERA_ACT', 0)
bkb.write_int(Mem,'ACAO_EXECUTADA', 0)
bkb.write_int(Mem,'RESET_ENV', 0)
bkb.write_int(Mem,'RESP_RESET', 0)
bkb.write_int(Mem,'RECOMPENSA', 0)
bkb.write_int(Mem,'FINALIZADO', 0)
bkb.write_int(Mem,'INICIO_SIMU', 1)


# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=1000000, window_length=WINDOW_LENGTH)
processor = AtariProcessor()

# Select a policy. We use eps-greedy action selection, which means that a random action is selected
# with probability eps. We anneal eps from 1.0 to 0.1 over the course of 1M steps. This is done so that
# the agent initially explores the environment (high eps) and then gradually sticks to what it knows
# (low eps). We also set a dedicated eps value that is used during testing. Note that we set it to 0.05
# so that the agent still performs some random actions. This ensures that the agent cannot get stuck.
policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.001, nb_steps=1500000)

# The trade-off between exploration and exploitation is difficult and an on-going research topic.
# If you want, you can experiment with the parameters or use a different policy. Another popular one
# is Boltzmann-style exploration:
# policy = BoltzmannQPolicy(tau=1.)
# Feel free to give it a try!

dqn = DQNAgent(model=model, nb_actions=nb_actions, policy=policy, memory=memory, enable_dueling_network=True,
               processor=processor, nb_steps_warmup=50000, gamma=.99, target_model_update=10000,
               train_interval=4, delta_clip=1.)
dqn.compile(Adam(lr=.00025), metrics=['mae'])


weights_filename = 'duel_dqn_{}_weights.h5f'.format(args.env_name)
if args.weights:
    weights_filename = args.weights
dqn.load_weights(weights_filename)
dqn.test(env, nb_episodes=10, visualize=True)

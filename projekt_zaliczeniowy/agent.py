
import game
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense

class DeepQAgent:
    def __init__(self, num_actions, state_size, learning_rate=0.001, discount_factor=0.99, initial_exploration_rate=1.0, exploration_decay_rate=0.99, min_exploration_rate=0.01):
        self.num_actions = num_actions
        self.state_size = state_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = initial_exploration_rate
        self.exploration_decay_rate = exploration_decay_rate
        self.min_exploration_rate = min_exploration_rate
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.num_actions, activation='linear'))
        model.compile(loss='mse', optimizer='adam')
        return model

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return random.randrange(self.num_actions)
        q_values = self.model.predict(state,verbose=0)
        return np.argmax(q_values[0])

    def update_q_values(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = (reward + self.discount_factor * np.amax(self.model.predict(next_state,verbose=0)[0]))
        target_f = self.model.predict(state,verbose=0)
        target_f[0][action] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)

    def decay_exploration_rate(self):
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay_rate)
env = game.SnakeGameEnv()
env.reset()


num_states = 7
num_actions = 4

agent = DeepQAgent(num_actions,num_states)

num_episodes = 100000
for episode in range(num_episodes):
    state = np.array(list(env.reset().values())).ravel().reshape(1, -1)
    #print(state)
    done = False
    total_reward = 0

    while not done:

        action = agent.choose_action(state)
        #print(state)
        
        next_state, reward, done, info = env.step(action)
        next_state = np.array(list(next_state.values())).ravel().reshape(1, -1)
        
        agent.update_q_values(state, action, reward, next_state,done)
        state=next_state

        #env.render()
        if done:
            break
        
        total_reward += reward
        
    print(f"Episode {episode + 1}: Total Reward = {total_reward}")
    agent.decay_exploration_rate()

agent.model.save('trained_model.h5')

if __name__ == "__main__":
from sample_players import DataPlayer
import random
from isolation import DebugState
import numpy as np

def debug_print_state(state):
    dbstate = DebugState.from_state(state)
    print(dbstate)

class OpenningBook(object):
    def __init__(self, book={}):
        self.book = book # book[node] = [win, loss]
        self.player_id = 1

    def update(self, state, win, loss):
        node = self._get_node(state)
        if node not in self.book:
            self.book[node] = [0, 0]
        self.book[node][0] += win
        self.book[node][1] += loss

    @staticmethod
    def _get_node(state):
        return (state.board, *state.locs)

    def build_tree(self, state, depth=4):
        if depth <= 0 or state.terminal_test():
            win, loss = 0, 0
            for _ in range(1):
                if self.simulate(state) > 0:    win += 1
                else:                           loss += 1
            return loss, win

        total_win, total_loss = 0, 0
        for action in state.actions():
            result_state = state.result(action)
            win, loss = self.build_tree(state.result(action), depth - 1)
            self.update(result_state, win, loss)
            total_win += win; total_loss += loss

        return total_loss, total_win

    def simulate(self, state):
        player_id = self.player_id
        while not state.terminal_test():
            state = state.result(random.choice(state.actions()))
        return -1 if state.utility(player_id) < 0 else 1

    def best_action(self, state):
        '''
        find best action from this state and return its action
        '''
        actions = state.actions()
        results = [state.result(action) for action in actions]
        nodes = [self._get_node(result) for result in results]
        stats = [self.book[node] for node in nodes]
        ratios = [win / (win + loss) for win,loss in stats]
        max_ratio = max(ratios)
        max_indices = [idx for idx,ratio in enumerate(ratios) if ratio == max_ratio]
        return actions[random.choice(max_indices)]

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)

        if state.ply_count < 4:
            self.queue.put(OpenningBook(self.data).best_action(state))
        else:
            self.queue.put(self.minimax(state, depth=3))

    def minimax(self, state, depth):

        def min_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1))
            return value

        def max_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1))
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)


'''
Code for openning book
This code should be executed before running the game
Thie code will create and save data.pickle file
'''
if __name__ == '__main__':
    from isolation import Isolation
    import pickle

    book = OpenningBook()
    state = Isolation()
    win, loss = book.build_tree(state, 4)
    with open('data.pickle', 'wb') as f:
        pickle.dump(book.book, f)

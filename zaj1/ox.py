

class OX:
    ALL_SPACES = list('123456789')
    X, O, BLANK = 'X', 'O', ' '
    def __init__(self):
        self.playerX = Player(OX.X)
        self.playerO = Player(OX.O)
        self.board = Board()
    def play(self):
        print('Witaj w grze kółko i krzyżyk!')
        currentPlayer, nextPlayer = self.playerX, self.playerO
        while True:
            print(self.board)  # Wyświetl planszę na ekranie.
            move = None
            while not self.board.isValidSpace(move):
                print(f'Jaki jest ruch gracza {currentPlayer}? (1-9)')
                move = input()
            self.board.updateBoard(move, currentPlayer)  # Wykonanie ruchu.
            # Sprawdzenie, czy gra jest zakończona:
            if self.board.isWinner(currentPlayer):  # Sprawdzenie, kto wygrał.
                print(self.board)
                print(f"{currentPlayer} wygrał grę!")
                break
            elif self.board.isBoardFull():  # Sprawdzenie remisu.
                print(self.board)
                print('Gra zakończyła się remisem!')
                break
            currentPlayer, nextPlayer = nextPlayer, currentPlayer  # Zmiana gracza.
        print('Dziękuję za grę!')


class Player:
    def __init__(self,symbol):
        if symbol != OX.X and symbol != OX.O:
            raise ValueError("Invalid input")
        self.symbol=symbol
    def __str__(self):
        return str(self.symbol)


class Board:
    def __init__(self):
        self.board = {}
        for space in OX.ALL_SPACES:
            self.board[space] = OX.BLANK 
    def __str__(self):
         return f'''
            {self.board['1']}|{self.board['2']}|{self.board['3']} 1 2 3 
            -+-+- 
            {self.board['4']}|{self.board['5']}|{self.board['6']} 4 5 6 
            -+-+- 
            {self.board['7']}|{self.board['8']}|{self.board['9']} 7 8 9'''
    def updateBoard(self, space, player):
            self.board[space] = player.symbol
    def isValidSpace(self,space):
        if space is None:
            return False
        return space in OX.ALL_SPACES or self.board[space] == OX.BLANK
        
    def isBoardFull(self):    
        for space in OX.ALL_SPACES:
            if self.board[space] == OX.BLANK:
                return False # Jeśli nawet jedno pole jest puste, zwracaj False.
        return True # Nie ma wolnych pól, zatem zwróć True
    def isWinner(self, player):
        b, p = self.board, player.symbol # Krótsze nazwy jako "składniowy cukier".
    # Sprawdzenie, czy trzy takie same znaki występują w wierszach, kolumnach i po przekątnych.
        return ((b['1'] == b['2'] == b['3'] == p) or # poziomo na górze
            (b['4'] == b['5'] == b['6'] == p) or # poziomo w środku
            (b['7'] == b['8'] == b['9'] == p) or # poziomo u dołu
            (b['1'] == b['4'] == b['7'] == p) or # pionowo z lewej
            (b['2'] == b['5'] == b['8'] == p) or # pionowo w środku
            (b['3'] == b['6'] == b['9'] == p) or # pionowo z prawej
            (b['3'] == b['5'] == b['7'] == p) or # przekątna 1
            (b['1'] == b['5'] == b['9'] == p)) # przekątna 2



def main():
    oxGame = OX()
    oxGame.play()

if __name__ == '__main__':
    main() # Wywołaj main(), jeśli ten moduł został uruchomiony, a nie zaimportowany.
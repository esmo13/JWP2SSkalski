ALL_SPACES = list('123456789')  # Klucze słownika planszy KIK.
X, O, BLANK = 'X', 'O', ' '  # Stałe reprezentujące wartości tekstowe.



class Player:
    def __init__(self,symbol):
        if symbol != X and symbol != O:
            raise ValueError("Invalid input")
        self.symbol=symbol
    def __str__(self):
        return str(self.symbol)


class Board:
    def __init__(self):
        self.board = {}
        for space in ALL_SPACES:
            self.board[space] = BLANK 
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
        return space in ALL_SPACES or self.board[space] == BLANK
        
    def isBoardFull(self):    
        for space in ALL_SPACES:
            if self.board[space] == BLANK:
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
    """Rozgrywka w kółko i krzyżyk."""
    print('Witaj w grze kółko i krzyżyk!')
    #gameBoard = getBlankBoard()  # Utwórz słownik planszy KIK.
    gameBoard = Board()
    #currentPlayer, nextPlayer = X, O  # X wykonuje ruch jako pierwszy, O jako następny.
    currentPlayer, nextPlayer = Player(X), Player(O)
    while True:
        print(gameBoard)  # Wyświetl planszę na ekranie.

        # Zadawaj graczowi pytanie, aż wprowadzi prawidłową liczbę od 1 do 9:
        move = None
        while not gameBoard.isValidSpace(move):
            print(f'Jaki jest ruch gracza {currentPlayer}? (1-9)')
            move = input()
        gameBoard.updateBoard(move, currentPlayer)  # Wykonanie ruchu.
        # Sprawdzenie, czy gra jest zakończona:
        if gameBoard.isWinner(currentPlayer):  # Sprawdzenie, kto wygrał.
            print(gameBoard)
            print(f"{currentPlayer} wygrał grę!")
            break
        elif gameBoard.isBoardFull():  # Sprawdzenie remisu.
            print(gameBoard)
            print('Gra zakończyła się remisem!')
            break
        currentPlayer, nextPlayer = nextPlayer, currentPlayer  # Zmiana gracza.
    print('Dziękuję za grę!')


# def getBlankBoard():
#     """Tworzy nową, pustą planszę gry w kółko i krzyżyk."""
#     board = {}  # Plansza jest reprezentowana przez słownik Pythona.
#     for space in ALL_SPACES:
#         board[space] = BLANK  # Wszystkie pola na początku są puste.
#     return board


# def getBoardStr(board):
#     """Zwraca tekstową reprezent if space is None:
#         return False
#     return space in ALL_SPACES or board[space] == BLANKację planszy."""
#     return f'''
#             {board['1']}|{board['2']}|{board['3']} 1 2 3 
#             -+-+- 
#             {board['4']}|{board['5']}|{board['6']} 4 5 6 
#             -+-+- 
#             {board['7']}|{board['8']}|{board['9']} 7 8 9'''
# def isValidSpace(board, space):
#     """Zwraca True, jeśli pole na planszy ma prawidłowy numer i pole jest puste."""
   
# def isWinner(board, player):
#     """Zwraca True, jeśli gracz jest zwycięzcą tej planszy KIK."""
#     b, p = board, player # Krótsze nazwy jako "składniowy cukier".
#     # Sprawdzenie, czy trzy takie same znaki występują w wierszach, kolumnach i po przekątnych.
#     return ((b['1'] == b['2'] == b['3'] == p) or # poziomo na górze
#             (b['4'] == b['5'] == b['6'] == p) or # poziomo w środku
#             (b['7'] == b['8'] == b['9'] == p) or # poziomo u dołu
#             (b['1'] == b['4'] == b['7'] == p) or # pionowo z lewej
#             (b['2'] == b['5'] == b['8'] == p) or # pionowo w środku
#             (b['3'] == b['6'] == b['9'] == p) or # pionowo z prawej
#             (b['3'] == b['5'] == b['7'] == p) or # przekątna 1
#             (b['1'] == b['5'] == b['9'] == p)) # przekątna 2
# def isBoardFull(board):
#     """Zwraca True, jeśli wszystkie pola na planszy są zajęte."""
#     for space in ALL_SPACES:
#         if board[space] == BLANK:
#             return False # Jeśli nawet jedno pole jest puste, zwracaj False.
#     return True # Nie ma wolnych pól, zatem zwróć True.
# def updateBoard(board, space, mark):
#     """Ustawia pole na planszy na podany znak."""
#     board[space] = mark

if __name__ == '__main__':
    main() # Wywołaj main(), jeśli ten moduł został uruchomiony, a nie zaimportowany.
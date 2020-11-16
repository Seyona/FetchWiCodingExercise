from pydantic import BaseModel
from transaction import Transaction
from typing import List


class User(BaseModel):
    id: int
    name: str
    # List of all positive transactions
    transactions: List['Transaction']
    # List of all transactions
    allTransactions: List['Transaction']

    """
    Deducts the points from the payers (going in order of when the transaction happened)
    Returns a dictionary <payer_name, points_deducted>
    """
    def deduct_points_from_payers(self, points):
        pointsByPayer = []
        # Create a list of tuples to make a mapping of payer to points

        deduct_dict = {}
        currentPoints = points

        for i in range(len(self.transactions)):
            key = self.transactions[i].payer_name

            # Check if the transaction has more points than we are trying to deduct
            # If it does just set the current transaction value to the difference
            if currentPoints - self.transactions[i].points.points <= 0:
                self.transactions[i].points = self.transactions[i].points.points - currentPoints
                deduct_dict[key] = deduct_dict.get(key, 0) - currentPoints

            else:
                # Track how many points we are deducting since it istrying to deduct more points than the current transaction has
                pointsDeducted = currentPoints - (currentPoints - self.transactions[i].points.points)
                deduct_dict[key] = deduct_dict.get(key, 0) - pointsDeducted
                currentPoints -= pointsDeducted

        return deduct_dict

    "Gets the total number of points in the transactions list"
    def get_points_total(self):
        return 0 if not self.transactions else sum([x.points.points for x in self.transactions])

    """
       Adds transaction for the user
       if the points_value is positive, the transaction and allTransaction list will have an entry appended
       if the points_value is negative,
            - If the number of points is greater than the total points the payer_name has it will return an error message
                ** This is not the best solution, but it is not clear from the prompt what should be done in this case.
            - It will go down the list of positive points and subtract what it can from it
            - If the subtraction reduces the value to zero we'll move on to the next element
            - Before sorting it will remove all indices that have a value of 0
    """
    def add_transaction(self, payer_name, points, date_str):
        transaction = Transaction(payer_name, points, date_str)
        if points > 0:
            self.transactions.append(transaction)
            self.allTransactions.append(transaction)
        else:
            self.allTransactions.append(transaction)
            tempPoints = abs(points)
            totalPoints = self.get_points_total()
            if tempPoints > totalPoints:  # Based on the examples we shouldn't hit this, but this is good to check so it doesn't fly into an infinite loop
                return "Attempting to deduct more points than the user has"
            while tempPoints > 0:
                for i in range(0, len(self.transactions)):
                    value = self.transactions[i].points.points - tempPoints
                    if tempPoints < 0:
                        tempPoints = abs(tempPoints)
                        self.transactions[i].points.points = 0
                    else:
                        self.transactions[i].points.points = value

            # Remove all nonzero / negative values from the points list
            self.transactions = [transaction for transaction in self.transactions if transaction.points.points > 0]

        self.transactions.sort(key=lambda transactions: transactions.points.date)
        self.allTransactions.sort(key=lambda transactions: transactions.points.date)
        return ""


    """
    Sums all all transactions and organizes them by payer
    """
    def sum_transactions_by_payer(self):
        transaction_dict = {}

        for transaction in self.transactions:
            key = transaction.payer_name
            transaction_dict[key] = transaction_dict.get(key, 0) + transaction.points.points

        return transaction_dict



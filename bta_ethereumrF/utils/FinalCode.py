# import base64
# from io import BytesIO

import requests
import pandas as pd
from web3 import Web3
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class EthereumTransactionHistory:
    def __init__(self, etherscan_api_key):
        self.etherscan_api_key = etherscan_api_key
        self.w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/7593d863808b4bbb8a83949b4d8bb8ce'))

    def get_transaction_history(self, public_address):
        etherscan_endpoint = f"https://api.etherscan.io/api?module=account&action=txlist&address={public_address}&startblock=0&endblock=99999999&sort=asc&apikey={self.etherscan_api_key}"
        response = requests.get(etherscan_endpoint)

        if response.status_code == 200:
            return response.json()['result'] 
        else:
            print(f"Enter a correct public address: {response.status_code}")
            return None

    def fetch_transactions_df(self, public_address):
        transactions = self.get_transaction_history(public_address)
        if transactions:
            transactions_df = pd.DataFrame(transactions)
            return transactions_df[['from', 'to']]
        else:
            return None

class MyEthereumTransactions(EthereumTransactionHistory):
    def __init__(self, etherscan_api_key):
        super().__init__(etherscan_api_key)
        self.fetched_addresses = set()

    def dfs_transaction_history(self, public_address, dataset_file, depth=0, max_depth=10, graph=None, matched_addresses=None):
        if graph is None:
            graph = nx.DiGraph()
        if matched_addresses is None:
            matched_addresses = set()

        if depth > max_depth:
            return graph

        dataset_df = pd.read_csv(dataset_file)
        dataset_addresses = set(dataset_df['address'].str.lower())

        if public_address.lower() in dataset_addresses:
            graph.add_node(public_address)
            graph.nodes[public_address]['match'] = True
            matched_addresses.add(public_address.lower())
            return graph

        transactions_df = self.fetch_transactions_df(public_address)
        if transactions_df is None:
            print(f"Enter a correct public address , this address {public_address} might wrong.")
            return graph
        if len(transactions_df) > 50:
            print(f"Excluding address {public_address} with more than 50 transactions.")
            return graph

        self.fetched_addresses.add(public_address.lower())
        graph.add_node(public_address)

        for _, transaction in transactions_df.iterrows():
            graph.add_edge(transaction['from'], transaction['to'])

        if depth < max_depth:
            child_addresses = set(transactions_df['to'].str.lower()) | set(transactions_df['from'].str.lower()) - self.fetched_addresses
            for child_address in child_addresses:
                if child_address not in self.fetched_addresses:
                    graph = self.dfs_transaction_history(child_address, dataset_file, depth + 1, max_depth, graph, matched_addresses)

        for node in graph.nodes:
            if node.lower() in matched_addresses:
                graph.nodes[node]['match'] = True
            neighbors = set(graph.successors(node)) | set(graph.predecessors(node))
            if neighbors & matched_addresses:
                graph.nodes[node]['connected_to_matched'] = True

        return graph

def visualize_graph(graph, dataset_file, user_address):
    plt.figure(figsize=(12, 8))
    
    pos = nx.spring_layout(graph)
    pos[user_address] = np.array([0.5, 0.8])  
    
    for node, coordinates in pos.items():
        if node != user_address:
            if np.linalg.norm(coordinates - pos[user_address]) < 0.1:
                pos[node] = pos[node] * 1.2 
    
    node_color = []
    node_size = []
    for node in graph.nodes:
        if node == user_address:
            node_size.append(1500)  
        else:
            node_size.append(700)  
        
        if graph.nodes[node].get('match'):
            node_color.append('red')
        elif graph.nodes[node].get('connected_to_matched'):
            node_color.append('orange')
        else:
            node_color.append('lightblue')

    nx.draw_networkx(graph, pos, with_labels=True, node_size=node_size, node_color=node_color, font_size=8)
    plt.title('Ethereum Transaction History Graph')
    plt.axis('off')
    plt.show()


def main():
    etherscan_api_key = 'REPLACE WITH YOUR API '
    dataset_file = r'REPLACE WITH YOUR PATH /TestAddresses.csv'
    my_transactions = MyEthereumTransactions(etherscan_api_key)

    public_address = input("Enter your Ethereum public address: ").lower()
    transaction_graph = my_transactions.dfs_transaction_history(public_address, dataset_file, max_depth=3)
    visualize_graph(transaction_graph, dataset_file, public_address)

if __name__ == '__main__':
    main()

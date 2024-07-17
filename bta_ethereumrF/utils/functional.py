from django.utils.safestring import mark_safe

from .FinalCode import MyEthereumTransactions, visualize_graph


def transaction_history_graph(public_address: str):
    etherscan_api_key = "REPLACE WITH YOUR API"
    dataset_file = r"TestAddresses.csv"
    my_transactions = MyEthereumTransactions(etherscan_api_key)
    error_message = None

    transaction_graph = my_transactions.dfs_transaction_history(
        public_address, dataset_file, max_depth=3
    )
    if str(transaction_graph) == "DiGraph with 0 nodes and 0 edges":
        error_message = (
            f"Enter a correct public address, this address  {public_address} might be wrong"
        )

    visualized_graph = visualize_graph(transaction_graph, dataset_file, public_address)
    return mark_safe(visualized_graph), error_message

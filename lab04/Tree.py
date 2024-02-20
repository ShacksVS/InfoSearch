import re


class TreeNode:
    def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self, words):
        self.root = None
        for word in words:
            self.insert_word(word)

    def insert_word(self, new_item):
        if self.root is None:
            self.root = TreeNode(new_item)
            return

        runner = self.root
        while True:
            if new_item == runner.item:
                return  # Avoid duplicates
            if new_item < runner.item:
                if runner.left is None:
                    runner.left = TreeNode(new_item)
                    return
                runner = runner.left
            else:
                if runner.right is None:
                    runner.right = TreeNode(new_item)
                    return
                runner = runner.right

    def search(self, query):
        query = query.lower().replace('*', '.*')
        regex = re.compile(f'^{query}$')
        results = []
        self.search_subtree(self.root, regex, results)
        return results

    def search_subtree(self, node, regex, results):
        if node is None:
            return
        if regex.match(node.item):
            results.append(node.item)
        self.search_subtree(node.left, regex, results)
        self.search_subtree(node.right, regex, results)

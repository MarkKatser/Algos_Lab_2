import random
import matplotlib.pyplot as plt
from bst import BST

def calculate_height(node):
    if node is None:
        return 0
    return 1 + max(calculate_height(node.left), calculate_height(node.right))

def get_bst_height(tree):
    return calculate_height(tree.root)

def generate_unique_random_keys(n):
    keys = set()
    while len(keys) < n:
        keys.add(random.randint(0, n * 100))
    keys_list = list(keys)
    random.shuffle(keys_list)
    return keys_list

def experiment_bst_height(max_keys, step):
    sizes = []
    heights = []
    
    for n in range(step, max_keys + 1, step):
        keys = generate_unique_random_keys(n)
        
        tree = BST()
        for key in keys:
            tree.insert(key)
        
        height = get_bst_height(tree)
        sizes.append(n)
        heights.append(height)
    
    return sizes, heights

def plot_results(sizes, heights):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, heights, 'b-o', linewidth=2, markersize=4)
    
    plt.xlabel('Количество ключей (n)', fontsize=12)
    plt.ylabel('Высота дерева (h)', fontsize=12)
    plt.title('Зависимость высоты BST от количества ключей', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def main():
    MAX_KEYS = 10000
    STEP = 100
    
    sizes, heights = experiment_bst_height(
        max_keys=MAX_KEYS,
        step=STEP
    )
    
    plot_results(sizes, heights)

if __name__ == "__main__":
    main()
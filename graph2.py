import random
import matplotlib.pyplot as plt
import numpy as np
from avl import AVLTree
from rbt import RedBlackTree

def calculate_height(node):
    if node is None:
        return 0
    return 1 + max(calculate_height(node.left), calculate_height(node.right))

def calculate_rbt_height(node, nil_node):
    if node is None or node == nil_node:
        return 0
    return 1 + max(calculate_rbt_height(node.left, nil_node), 
                   calculate_rbt_height(node.right, nil_node))

def get_avl_height(tree):
    return calculate_height(tree.root)

def get_rbt_height(tree):
    if tree.root is None:
        return 0
    return calculate_rbt_height(tree.root, tree.NIL)

def generate_unique_random_keys(n):
    keys = set()
    while len(keys) < n:
        keys.add(random.randint(0, n * 100))
    keys_list = list(keys)
    random.shuffle(keys_list)
    return keys_list

def experiment_avl_height(max_keys, step):
    sizes = []
    heights = []
    
    for n in range(step, max_keys + 1, step):
        keys = generate_unique_random_keys(n)
        tree = AVLTree()
        for key in keys:
            tree.insert(key)
        height = get_avl_height(tree)
        sizes.append(n)
        heights.append(height)
    
    return sizes, heights

def experiment_rbt_height(max_keys, step):
    sizes = []
    heights = []
    
    for n in range(step, max_keys + 1, step):
        keys = generate_unique_random_keys(n)
        tree = RedBlackTree()
        for key in keys:
            tree.insert(key)
        height = get_rbt_height(tree)
        sizes.append(n)
        heights.append(height)
    
    return sizes, heights

def plot_results(sizes, avl_heights, rbt_heights):
    sizes_array = np.array(sizes)
    
    avl_upper = np.log2(sizes_array + 1)
    avl_lower = 1.44 * np.log2(sizes_array + 2) - 0.328
    
    rbt_upper = 2 * np.log2(sizes_array + 1)
    rbt_lower = np.log2(sizes_array + 1)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    ax1.plot(sizes, avl_heights, 'b-o', label='Высота (эксперимент)', linewidth=2, markersize=4)
    ax1.plot(sizes, avl_upper, 'g--', label='Верхняя оценка АВЛ', linewidth=2, alpha=0.7)
    ax1.plot(sizes, avl_lower, 'r--', label='Нижняя оценка АВЛ', linewidth=2, alpha=0.7)
    ax1.set_xlabel('Количество ключей (n)', fontsize=12)
    ax1.set_ylabel('Высота дерева (h)', fontsize=12)
    ax1.set_title('Зависимость высоты АВЛ дерева от количества ключей', fontsize=13, fontweight='bold')
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(sizes, rbt_heights, 'b-o', label='Высота (эксперимент)', linewidth=2, markersize=4)
    ax2.plot(sizes, rbt_upper, 'g--', label='Верхняя оценка КЧ', linewidth=2, alpha=0.7)
    ax2.plot(sizes, rbt_lower, 'r--', label='Нижняя оценка КЧ', linewidth=2, alpha=0.7)
    ax2.set_xlabel('Количество ключей (n)', fontsize=12)
    ax2.set_ylabel('Высота дерева (h)', fontsize=12)
    ax2.set_title('Зависимость высоты КЧ дерева от количества ключей', fontsize=13, fontweight='bold')
    ax2.legend(loc='best', fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def main():
    MAX_KEYS = 10000
    STEP = 100
    
    avl_sizes, avl_heights = experiment_avl_height(
        max_keys=MAX_KEYS,
        step=STEP
    )
    
    rbt_sizes, rbt_heights = experiment_rbt_height(
        max_keys=MAX_KEYS,
        step=STEP
    )
    
    plot_results(avl_sizes, avl_heights, rbt_heights)

if __name__ == "__main__":
    main()
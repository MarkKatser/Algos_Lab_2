from collections import deque

class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.right) - self.get_height(node.left)

    def right_rotate(self, y):
        # y - узел, вокруг которого выполняется поворот
        x = y.left  # x - левый потомок y
        T2 = x.right  # T2 - правое поддерево x
        
        # Выполняем поворот
        x.right = y  # y становится правым потомком x
        y.left = T2  # T2 становится левым потомком y

        self.update_height(y)
        self.update_height(x)
        
        # возвращаем новый корень поддерева
        return x  # x теперь корень поддерева

    def left_rotate(self, x):
        # x теперь повоорот вокруг него
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        self.update_height(x)
        self.update_height(y)
        
        return y

    def insert(self, value, node=None):
        if node is None:
            if self.root is None:
                self.root = AVLNode(value)
                return True
            self.root = self.insert(value, self.root)
            return True
        if value == node.value:
            return node
        
        if value < node.value:
            if node.left is None:
                node.left = AVLNode(value)
            else:
                node.left = self.insert(value, node.left)
        else:
            if node.right is None:
                node.right = AVLNode(value)
            else:
                node.right = self.insert(value, node.right)
        
        self.update_height(node)
        
        balance = self.get_balance(node)  # Получаем баланс-фактор
        
        # Левое поддерево перевешивает
        if balance < -1 and self.get_balance(node.left) <= 0:
            return self.right_rotate(node)
        
        # Правое поддерево перевешивает
        if balance > 1 and self.get_balance(node.right) >= 0:
            return self.left_rotate(node)
        
        # Левое-правое поддерево перевешивает
        if balance < -1 and self.get_balance(node.left) > 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        # Правое-левое поддерево перевешивает
        if balance > 1 and self.get_balance(node.right) < 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node

    def insert_list(self, values):
        results = []
        for value in values:
            result = self.insert(value)
            results.append(result)
        return results

    def search(self, value, node=None):
        if node is None:
            node = self.root
        
        if node is None:
            return False
        
        if value == node.value:
            return True
        
        if value < node.value:
            return self.search(value, node.left)
        else:
            return self.search(value, node.right)

    def find_min_node(self, node):
        if node.left is None:
            return node
        
        return self.find_min_node(node.left)

    def delete(self, value, node=None):
        if node is None:
            if self.root is None:
                return False
            old_root_exists = self.root is not None
            self.root = self.delete(value, self.root)
            return old_root_exists
        
        if node is None:
            return None
        
        if value < node.value:
            node.left = self.delete(value, node.left)
        elif value > node.value:
            node.right = self.delete(value, node.right)
        else:            
            # нет левого потомка
            if node.left is None:
                return node.right
            
            # нет правого потомка
            elif node.right is None:
                return node.left
            
            # есть оба потомка
            else:
                successor = self.find_min_node(node.right)
                node.value = successor.value
                node.right = self.delete(successor.value, node.right)
        
        if node is None:
            return None
        
        self.update_height(node)
        
        balance = self.get_balance(node)
        
        # Левое поддерево перевешивает
        if balance < -1 and self.get_balance(node.left) <= 0:
            return self.right_rotate(node)
        
        # Правое поддерево перевешивает
        if balance > 1 and self.get_balance(node.right) >= 0:
            return self.left_rotate(node)
        
        # Левое-правое поддерево перевешивает
        if balance < -1 and self.get_balance(node.left) > 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        # Правое-левое поддерево перевешивает
        if balance > 1 and self.get_balance(node.right) < 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node

    def find_min(self, node=None):
        if node is None:
            if self.root is None:
                return None
            return self.find_min(self.root)
        
        if node.left is None:
            return node.value
        
        return self.find_min(node.left)

    def find_max(self, node=None):
        if node is None:
            if self.root is None:
                return None
            return self.find_max(self.root)
        if node.right is None:
            return node.value
        
        return self.find_max(node.right)

    def priamoi_obhod(self, node=None, result=None):
        if result is None:
            result = []
            if node is None:
                node = self.root
        
        if node is None:
            return result
        
        result.append(node.value)
        self.priamoi_obhod(node.left, result)
        self.priamoi_obhod(node.right, result)
        return result

    def centr_obhod(self, node=None, result=None):
        if result is None:
            result = []
            if node is None:
                node = self.root
        
        if node is None:
            return result
        
        self.centr_obhod(node.left, result)
        result.append(node.value)
        self.centr_obhod(node.right, result)
        return result

    def obratni_obhod(self, node=None, result=None):
        if result is None:
            result = []
            if node is None:
                node = self.root
        
        if node is None:
            return result
        
        self.obratni_obhod(node.left, result)
        self.obratni_obhod(node.right, result)
        result.append(node.value)
        return result

    def shiroki_obhod(self):
        if self.root is None:
            return []
        
        result = []
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            result.append(node.value)
            
            if node.left is not None:
                queue.append(node.left)
            
            if node.right is not None:
                queue.append(node.right)
        
        return result

    def display(self):
        if self.root is None:
            print("Дерево пустое")
            return
        
        self._display(self.root, "", True)

    def _display(self, node, prefix, is_last):
        if node is None:
            return
        
        balance = self.get_balance(node)
        print(prefix + ("└── " if is_last else "├── ") + str(node.value) + f" (h={node.height}, b={balance})")
        
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        children = []
        if node.right is not None:
            children.append(node.right)
        if node.left is not None:
            children.append(node.left)
        
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            self._display(child, new_prefix, is_last_child)



def main():
    tree = AVLTree()
    
    print("=" * 60)
    print("\nДоступные команды:")
    print("  1 - Вставить значение")
    print("  11 - Вставить список значений")
    print("  2 - Найти значение")
    print("  3 - Удалить значение")
    print("  4 - Найти минимум")
    print("  5 - Найти максимум")
    print("  6 - Прямой обход")
    print("  7 - Центрированный обход")
    print("  8 - Обратный обход")
    print("  9 - Обход в ширину")
    print("  10 - Показать дерево")
    print("  0 - Выход")
    print("=" * 60)
    
    while True:
        try:
            choice = input("\nВыберите команду (0-11): ").strip()
            
            if choice == "0":
                break
            
            elif choice == "1":
                value = int(input("Введите значение для вставки: "))
                if tree.insert(value):
                    print(f"Значение {value} успешно вставлено (дерево автоматически сбалансировано)")
                else:
                    print(f"Значение {value} уже существует в дереве")
            
            elif choice == "11":
                values_str = input("Введите значения через пробел или запятую: ").strip()
                if ',' in values_str:
                    values_list = [int(x.strip()) for x in values_str.split(',')]
                else:
                    values_list = [int(x.strip()) for x in values_str.split()]
                results = tree.insert_list(values_list)
                inserted = sum(1 for r in results if r)
                skipped = len(results) - inserted
                print(f"Вставлено значений: {inserted}, пропущено (уже существуют): {skipped}")
                print(f"Дерево автоматически сбалансировано")
            
            elif choice == "2":
                value = int(input("Введите значение для поиска: "))
                if tree.search(value):
                    print(f"Значение {value} найдено в дереве")
                else:
                    print(f"Значение {value} не найдено в дереве")
            
            elif choice == "3":
                value = int(input("Введите значение для удаления: "))
                if tree.delete(value):
                    print(f"Значение {value} успешно удалено (дерево автоматически сбалансировано)")
                else:
                    print(f"Значение {value} не найдено в дереве")

            elif choice == "4":
                min_value = tree.find_min()
                if min_value is not None:
                    print(f"Минимальное значение: {min_value}")
                else:
                    print("Дерево пустое, минимум не найден")
            
            elif choice == "5":
                max_value = tree.find_max()
                if max_value is not None:
                    print(f"Максимальное значение: {max_value}")
                else:
                    print("Дерево пустое, максимум не найден")
            
            elif choice == "6":
                result = tree.priamoi_obhod()
                print(f"Прямой обход: {result}")
            
            elif choice == "7":
                result = tree.centr_obhod()
                print(f"Центрированный обход: {result}")
            
            elif choice == "8":
                result = tree.obratni_obhod()
                print(f"Обратный обход: {result}")
            
            elif choice == "9":
                result = tree.shiroki_obhod()
                print(f"Обход в ширину: {result}")
            
            elif choice == "10":
                tree.display()
            
            else:
                print("Неверная команда! Пожалуйста, выберите число от 0 до 11.")
        
        except ValueError:
            print("Ошибка! Пожалуйста, введите корректное число.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
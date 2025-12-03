from collections import deque

class RBNode:
    def __init__(self, value, color='RED'):
        self.value = value
        self.left = None
        self.right = None
        self.color = color
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.root = None
        self.NIL = RBNode(None, 'BLACK') #типа черный листик

    def is_red(self, node):
        if node is None or node == self.NIL:
            return False
        return node.color == 'RED'

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        
        x.parent = y.parent
        
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        
        x.right = y
        y.parent = x


    def fix_insert(self, node):

        while node.parent is not None and self.is_red(node.parent): #пока папка красный
            if node.parent.parent is not None and node.parent == node.parent.parent.left: #если батя - левый от деда
                uncle = node.parent.parent.right  # то дядя правый
                
                if uncle is not None and uncle != self.NIL and self.is_red(uncle): 
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    # дядя черный
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node) # ты теперь левый, поздравляю
                    
                    # очев, что ты теперь левый
                    node.parent.color = 'BLACK'
                    if node.parent.parent is not None:
                        node.parent.parent.color = 'RED'
                        self.right_rotate(node.parent.parent)
                    break
            else:
                if node.parent.parent is not None:
                    uncle = node.parent.parent.left
                    
                    # дядя красный
                    if uncle is not None and uncle != self.NIL and self.is_red(uncle):
                        node.parent.color = 'BLACK'
                        uncle.color = 'BLACK'
                        node.parent.parent.color = 'RED'
                        node = node.parent.parent
                    else:
                        # дядя черный
                        if node == node.parent.left:
                            node = node.parent
                            self.right_rotate(node)
                            # ты теперь правый, поздравляю
                        
                        # очев, что ты теперь правый
                        node.parent.color = 'BLACK'
                        if node.parent.parent is not None:
                            node.parent.parent.color = 'RED'
                            self.left_rotate(node.parent.parent)
                        break
                else:
                    # деда нет покидаем чат
                    break
        
        # корень всегда черный
        if self.root is not None:
            self.root.color = 'BLACK'

    def insert(self, value, node=None, parent=None):
        if node is None:
            if self.root is None:
                new_node = RBNode(value, 'BLACK')
                new_node.left = self.NIL
                new_node.right = self.NIL
                self.root = new_node
                return True
            result = self.insert(value, self.root, None)
            return result
        
        if value == node.value:
            return False
        
        if value < node.value:
            if node.left == self.NIL:
                new_node = RBNode(value, 'RED')
                new_node.left = self.NIL
                new_node.right = self.NIL
                new_node.parent = node
                node.left = new_node
                self.fix_insert(new_node) #жоска фиксим
                return True
            else:
                return self.insert(value, node.left, node)
        else:
            if node.right == self.NIL:
                new_node = RBNode(value, 'RED')
                new_node.left = self.NIL
                new_node.right = self.NIL
                new_node.parent = node
                node.right = new_node
                self.fix_insert(new_node) # опять жоска фиксим
                return True
            else:
                return self.insert(value, node.right, node)

    def insert_list(self, values):
        results = []
        for value in values:
            result = self.insert(value)
            results.append(result)
        return results

    def find_node(self, value, node=None):
        if node is None:
            node = self.root
        
        while node != self.NIL and node is not None:
            if value == node.value:
                return node
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        
        return None

    def search(self, value):
        return self.find_node(value) is not None

    def find_min_node(self, node):
        while node.left != self.NIL and node.left is not None:
            node = node.left
        return node

    def fix_delete(self, x):
        while x != self.root and x is not None and x.parent is not None and not self.is_red(x):
            if x.parent is not None and x == x.parent.left:
                w = x.parent.right  # братик икса
                
                # брат красный
                if w is not None and w != self.NIL and self.is_red(w):
                    w.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.left_rotate(x.parent)
                    w = x.parent.right
                
                # брат и племяшки черные
                if w is not None and w != self.NIL and not self.is_red(w.left) and not self.is_red(w.right):
                    w.color = 'RED'
                    x = x.parent
                elif w is not None and w != self.NIL:
                    # брат черный, левый племяшка красный, правый черный (интересно, как так получилось?)
                    if not self.is_red(w.right):
                        if w.left is not None and w.left != self.NIL:
                            w.left.color = 'BLACK'
                        w.color = 'RED'
                        self.right_rotate(w)
                        w = x.parent.right
                    
                    # брат черный, правый племяшка красный
                    if w is not None and w != self.NIL:
                        w.color = x.parent.color
                        x.parent.color = 'BLACK'
                        if w.right is not None and w.right != self.NIL:
                            w.right.color = 'BLACK'
                        self.left_rotate(x.parent)
                        x = self.root
            elif x.parent is not None:
                w = x.parent.left
                
                # брат красный
                if w is not None and w != self.NIL and self.is_red(w):
                    w.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.right_rotate(x.parent)
                    w = x.parent.left
                
                # брат и племяшки черные
                if w is not None and w != self.NIL and not self.is_red(w.right) and not self.is_red(w.left):
                    w.color = 'RED'
                    x = x.parent
                elif w is not None and w != self.NIL:
                    # брат черный, правый племяшка красный, левый черный (да что у них там происходит?)
                    if not self.is_red(w.left):
                        if w.right is not None and w.right != self.NIL:
                            w.right.color = 'BLACK'
                        w.color = 'RED'
                        self.left_rotate(w)
                        w = x.parent.left
                    
                    # брат черный, левый племяшка красный (асу)
                    if w is not None and w != self.NIL:
                        w.color = x.parent.color
                        x.parent.color = 'BLACK'
                        if w.left is not None and w.left != self.NIL:
                            w.left.color = 'BLACK'
                        self.right_rotate(x.parent)
                        x = self.root
        
        # x всегда черный
        if x is not None:
            x.color = 'BLACK'

    def delete(self, value):
        if self.root is None:
            return False
        
        z = self.find_node(value)
        if z is None:
            return False
        
        y = z
        y_original_color = y.color
        x = self.NIL
        
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self.find_min_node(z.right)
            y_original_color = y.color
            x = y.right
            
            if y.parent == z:
                if x != self.NIL:
                    x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                if y.right != self.NIL:
                    y.right.parent = y
            
            self._transplant(z, y)
            y.left = z.left
            if y.left != self.NIL:
                y.left.parent = y
            y.color = z.color
        
        if y_original_color == 'BLACK':
            self.fix_delete(x)
        
        return True


    def _transplant(self, u, v): #заменяем u на v
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        
        if v != self.NIL and v is not None:
            v.parent = u.parent

    def find_min(self, node=None):
        if node is None:
            if self.root is None:
                return None
            return self.find_min(self.root)

        if node.left == self.NIL or node.left is None:
            return node.value
        
        return self.find_min(node.left)

    def find_max(self, node=None):
        if node is None:
            if self.root is None:
                return None
            return self.find_max(self.root)
        
        if node.right == self.NIL or node.right is None:
            return node.value
        
        return self.find_max(node.right)

    def priamoi_obhod(self, node=None, result=None):
        if result is None:
            result = []
            if node is None:
                node = self.root
        
        if node is None or node == self.NIL:
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
        
        if node is None or node == self.NIL:
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
        
        if node is None or node == self.NIL:
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
            if node != self.NIL and node is not None:
                result.append(node.value)
                
                if node.left != self.NIL and node.left is not None:
                    queue.append(node.left)
                
                if node.right != self.NIL and node.right is not None:
                    queue.append(node.right)
        
        return result

    def display(self, node=None, prefix="", is_last=True):
        if node is None:
            if self.root is None:
                print("Дерево пустое")
                return
            node = self.root
            prefix = ""
            is_last = True
        
        if node is None or node == self.NIL:
            return
        
        color_symbol = 'R' if node.color == 'RED' else 'B'
        print(prefix + ("└── " if is_last else "├── ") + str(node.value) + f" ({color_symbol})")
        
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        children = []
        if node.right != self.NIL and node.right is not None:
            children.append(node.right)
        if node.left != self.NIL and node.left is not None:
            children.append(node.left)
        
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            self.display(child, new_prefix, is_last_child)


def main():
    tree = RedBlackTree()  
    print("=" * 60)
    print("\nДоступные команды:")
    print("  1 - Вставить значение")
    print("  11 - Вставить список значений")
    print("  2 - Найти значение")
    print("  3 - Удалить значение")
    print("  4 - Найти минимум")
    print("  5 - Найти максимум")
    print("  6 - Прямой обход (preorder)")
    print("  7 - Центрированный обход (inorder)")
    print("  8 - Обратный обход (postorder)")
    print("  9 - Обход в ширину (level-order)")
    print("  10 - Показать дерево (с цветами узлов)")
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
from collections import deque #очередь для обхода в ширину

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value, node=None):
        if node is None:
            if self.root is None:
                self.root = Node(value)
                return True
            return self.insert(value, self.root) 
        
        if value == node.value:
            return False #значение уже есть
        
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
                return True
            else:
                return self.insert(value, node.left)
        else:
            if node.right is None:
                node.right = Node(value)
                return True
            else:
                return self.insert(value, node.right) 

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
            return node
        elif value > node.value:
            node.right = self.delete(value, node.right)
            return node
        else:
            if node.left is None:
                return node.right
            
            elif node.right is None:
                return node.left
            
            else:
                successor = self.find_min_node(node.right)
                node.value = successor.value #этот узел = преемнику
                node.right = self.delete(successor.value, node.right)
                return node 

    def find_min(self, node=None):
        if node is None:
            if self.root is None:
                return None
            return self.find_min(self.root)
        
        if node.left is None:
            return node.value
        
        return self.find_min(node.left)
    
    def find_min_node(self, node):
        if node.left is None:
            return node
        return self.find_min_node(node.left)

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
            node = queue.popleft() #извлекаем узел из начала очереди
            result.append(node.value) #добавляем значение узла в результат
            if node.left is not None: #если у узла есть левый потомок, добавляем его в очередь
                queue.append(node.left)
            if node.right is not None: #если у узла есть правый потомок, добавляем его в очередь
                queue.append(node.right)
        return result

    def display(self, node=None, prefix="", is_last=True):
        if node is None:
            if self.root is None:
                print("Дерево пустое")
                return
            node = self.root
            prefix = ""  # для корня префикс пустой
            is_last = True  # корень всегда единственный на уровне
        
        if node is None:
            return #если узел пустой, прекращаем рекурсию
        
        # └── для последнего ребёнка, ├── для остальных
        print(prefix + ("└── " if is_last else "├── ") + str(node.value))
        
        # если текущий узел последний - добавляем 4 пробела,  если не последний - добавляем "│   "
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        children = []
        if node.right is not None:
            children.append(node.right)
        if node.left is not None:
            children.append(node.left)
        
        #выводим всех потомков
        for i, child in enumerate(children):
            #определяем, является ли текущий потомок последним в списке
            is_last_child = (i == len(children) - 1)
            # рекурсивный вызов с накопленным префиксом и флагом
            self.display(child, new_prefix, is_last_child)

def main():
    tree = BST()  #пустое бст
    
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
                    print(f"Значение {value} успешно вставлено")  
                else:
                    print(f"Значение {value} уже существует в дереве")  
            elif choice == "11":
                values_str = input("Введите значения через пробел или запятую: ").strip()
                if ',' in values_str:
                    values_list = [int(x.strip()) for x in values_str.split(',')] #пробуем разделить
                else:
                    values_list = [int(x.strip()) for x in values_str.split()] #тоже 
                results = tree.insert_list(values_list)
                inserted = sum(1 for r in results if r) #считаем успешные успехи
                skipped = len(results) - inserted #и бузуспешные безуспехи
                print(f"Вставлено значений: {inserted}, пропущено (уже существуют): {skipped}")
            
            elif choice == "2":
                value = int(input("Введите значение для поиска: "))
                if tree.search(value):  
                    print(f"Значение {value} найдено в дереве")  
                else:
                    print(f"Значение {value} не найдено в дереве")  
            elif choice == "3":
                value = int(input("Введите значение для удаления: "))  
                if tree.delete(value):  
                    print(f"Значение {value} успешно удалено")  
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
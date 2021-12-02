# Create a class COMPOSITION with the names of goods, their quantity
# and price. Define methods for working with these data fields and
# overload operations to replenish product information, retrieve product
# information, generate a report on the availability of goods in stock
# according to the request.

import mysql.connector


class Good:
    """Contains info about name, quantity and price of product

    to be used in Composition class to be added to the database"""
    def __init__(self, name, quantity, price, good_id=None):
        self.__id = good_id
        self.__name = name
        self.__quantity = quantity
        self.__price = price

    def __repr__(self):
        """String representation of the good"""
        return f'{self.__dict__.items()}'

    @property
    def name(self):
        return self.__name

    @property
    def quantity(self):
        return self.__quantity

    @property
    def price(self):
        return self.__price

    @property
    def id(self):
        return self.__id

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Name must be str')
        self.__name = value

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int):
            raise TypeError('Quantity must be int')
        self.__quantity = value

    @price.setter
    def price(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError('Price must be float or int')
        self.__price = value

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError('id must be int')
        self.__id = value


class Composition:
    """Is created to operate with goods and database"""
    def __init__(self, table_name):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database='composition'
        )
        self.__table_name = 'Composition_' + table_name
        mycursor = self.mydb.cursor(buffered=True)
        mycursor.execute('CREATE DATABASE IF NOT EXISTS composition')
        mycursor.execute('CREATE TABLE IF NOT EXISTS `{self.table_name}` ('
                              'id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, '
                              'name VARCHAR(30), '
                              'quantity INT, '
                              'price FLOAT)')
        mycursor.close()

    def __iadd__(self, good: Good):
        """Add a good to the composition

        to be used as CompositionObj += GooodObj"""
        if not isinstance(good, Good):
            raise ValueError('Good must be Good class type')

        mycursor = self.mydb.cursor(buffered=True)

        if good.name in self:
            raise ValueError('Element with this id or name already exists')

        func = 'INSERT INTO `%s` (name, quantity, price) VALUES (%s, %s, %s)'
        mycursor.execute(func, (self.table_name, good.name, good.quantity, good.price))

        self.mydb.commit()
        mycursor.close()

    def __delitem__(self, key):
        """Delete a good from the composition

        to be used as del CompositionObj[key], where key is name or id or Good"""
        if not isinstance(key, (int, str, Good)):
            raise ValueError('Key must be int(to search by `id`) or str(to search by `name`) or Good class')

        if key not in self:
            raise ValueError(f'Element with parameter [{key}] doesn\'t exist')

        mycursor = self.mydb.cursor(buffered=True)
        func = ''
        if isinstance(key, Good):
            key = key.name
        if isinstance(key, str):
            func = 'DELETE FROM `%s` WHERE name=`%s`'
        else:
            if key < 0:
                raise ValueError('id can\'t be less than 0')
            func = 'DELETE FROM `%s` WHERE id=`%s`'
        mycursor.execute(func, (self.table_name, key,))

        self.mydb.commit()
        mycursor.close()

    def __contains__(self, key):
        """Find a good in the composition

        to be used as: key in CompositionObj, where key is name or id or Good"""
        if not isinstance(key, (str, int, Good)):
            raise ValueError('Key must be str or int or Good class')

        mycursor = self.mydb.cursor(buffered=True)

        if isinstance(key, Good):
            key = key.name
        if isinstance(key, str):
            mycursor.execute('SELECT `name` FROM `%s`', (self.table_name,))
        else:
            if key < 0:
                raise ValueError('id can\'t be less than 0')
            mycursor.execute('SELECT `id` FROM %s', (self.table_name,))

        row = ()
        while row is not None:
            row = mycursor.fetchone()
            if row is not None and key in row:
                return True
        mycursor.close()

    def __getitem__(self, key):
        """Get a good from the composition

        to be used as: CompositionObj[key], where key is either name or id"""
        if not isinstance(key, (str, int)):
            raise ValueError('Key must be str or int')

        if key not in self:
            raise ValueError(f'Element with parameter [{key}] doesn\'t exist')

        mycursor = self.mydb.cursor(buffered=True)

        func = ''
        if isinstance(key, int):
            if key < 0:
                raise ValueError('id can\'t be less than 0')
            func = 'SELECT * FROM %s WHERE id=%s'
        else:
            func = 'SELECT * FROM %s WHERE name=%s'

        mycursor.execute(func, (self.table_name, key,))

        row = mycursor.fetchone()
        mycursor.close()
        return Good(row[1], row[2], row[3], row[0])

    def __setitem__(self, key, good):
        """Set a good in the composition (kind of updating of an existing good)

        to be used as: CompositionObj[key] = GoodObj"""
        if not isinstance(key, (str, int)):
            raise ValueError('Key must be str or int')
        if not isinstance(good, Good):
            raise ValueError('Good must be Good class type')

        if key not in self:
            raise ValueError(f'Element with parameter [{key}] doesn\'t exist')

        if good.name in self:
            raise ValueError(f'New value of good({good.name}) already exists')
        if good.id in self:
            raise ValueError(f'New value of good({good.id}) already exists')

        mycursor = self.mydb.cursor(buffered=True)

        func = f'SELECT * FROM %s WHERE id=%s'
        mycursor.execute(self.table_name, func, (key,))

        if isinstance(key, int):
            func = 'UPDATE %s SET name = %s, quantity = %s, price = %s WHERE id = %s'
        else:
            func = 'UPDATE %s SET name = %s, quantity = %s, price = %s WHERE name = %s'

        mycursor.execute(func, (self.table_name, good.name, good.quantity, good.price, key))
        self.mydb.commit()
        mycursor.close()

    def __isub__(self, other):
        """Subtract other table value

        when used with itself, starts self-destruction,
        to be used as: CompositionObj1 -= CompositionObj2"""
        if not isinstance(other, Composition):
            raise TypeError('Operand must be Composition class type')

        mycursor = self.mydb.cursor(buffered=True)
        func = ''
        if other == self:
            func = 'DROP TABLE `%s`'
            mycursor.execute(func, (self.table_name,))
        else:
            func = 'SELECT * FROM `%s` LEFT JOIN `%s` USING (name) WHERE %s.name IS NULL'
            mycursor.execute(func, (self.table_name, other.table_name, other.table_name,))

        mycursor.execute(func)
        mycursor.close()

    @property
    def table_name(self):
        return self.__table_name

    @table_name.setter
    def table_name(self, value):
        self.__table_name = value


if __name__ == '__main__':
    a = Composition('first')
    b = Composition('second')
    g = Good('mouse', 1, 999)
    b -= b
    print(g in a)
    a += g
    del a[g]
    del a[1]
    print(2 in a)
    print(1 in a)
    print(a['phone'])
    print(a[2])
    a[2] = g



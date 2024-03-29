# SQL
---
## SQL(Structured Query Language)
> 왜 SQL을 쓸까?  
> 방대한 양의 데이터를 구체적으로 특정하지 않고도 제어할 수 있는 고 레벨의 언어이기 때문이다.  
## Data Definition
### CREATE TABLE : Make table
  ```SQL
  CREATE TABLE Moive(
    title VARCHAR(10),
    year INT
  );
  
  DROP TABLE Movie; // 테이블 삭제.
  ```
### Element Declaration
  - INT(INTEGER)
  - REAL(FLOAT)
  - CHAR(n) : fixed length 'n'
  - VARCHAR(n) : string up to 'n'
### Dates and Times
  - DATE '2002-09-30' : Type of DATE
  - TIME '15:30:02.5' : Type of TIME
### Define Keys
  ```SQL
  CREATE TABLE Beers(
    name CHAR(20) UNIQUE, // Same as PRIMARY KEY
    manf CHAR(20)
  );
  CREATE TABLE Sells( // Multiattribute KEY
    bar CHAR(20),
    beer VARCHAR(20),
    price REAL,
    PRIMARY KEY(bar, beer)
  );
  ```
  - 여기서, PRIMARY KEY와 UNIQUE의 차이는
  - PRIMARY KEY는 NULL Attribute가 어떤 Tuple 내에도 존재해서는 안된다.
  - UNIQUE는 NULL Attribute 또한 존재할 수 있다.
### Other Declaration for Attributes
  ```SQL
  CREATE TABLE Drinkers(
    name CHAR(30) PRIMARY KEY,
    addr CHAR(50) DEFAULT '123 Sesame St.',
    phone CHAR(16) NOT NULL
  );
  ```
### Inserting a Tuple
  ```SQL
  INSERT INTO Drinkers(name, addr, phone) // 굳이 원형을 적지 않아도 되지만, 적어주는 것이 어떤 Attribute를 추가했는지 안헀는지 알기 쉽다.
  VALUES ('Jin-Seop Sim', 'Pusan 234', '010-1234-5678');
  ```
  - 만약 필요한 Attribute를 다 입력하지 않으면 어떻게 될까? 그럼 NULL 값으로 채워지게 되므로, Anomaly가 발생할 수가 있다!
  - 따라서 반드시 NOT NULL 선언을 해주어야 NULL 값이 들어가지 않는다.
### Adding Attributes
  ```SQL
  ALTER TABLE Bars ADD // 이는 새 Column을 만드는 Clause이다.
    phone char(16) DEFAULT 'unlisted';
    
  UPDATE Customers
  SET City = 'Busan' // 이렇게 UPDATE SET Clause를 이용하면, Column이 아닌 한국에 사는 사람들의 도시만(Row) 바꾸게 된다.
  WHERE Country = 'Korea';
  ```
  
### Deleting Attributes
  ```SQL
  ALTER TABLE Bars
    DROP license; // 이는 Column을 통째로 지우는 Clause이다.
  
  DELETE FROM Customers // 이렇게 DELETE FROM을 이용하면, 한국에 사는 사람들의 Records를 모두 지운다.
  WHERE Country = 'Korea'; // WHERE문을 안쓰게 되면 해당 Table의 모든 Records를 다 삭제한다.
  ```
- Views in SQL
  ```SQL
  CREATE VIEW CanDrink AS
    SELETC drinker, beer
    FROM Frequents, Sells
    WHERE Frequents.bar = Sells.bar;
  ```
  - SQL에는 View라는 __Virtual Table__ 이 존재한다.
  - 이는 DB에 물리적으로 구현되어 있지 않은 가상의 테이블이며, 전체 데이터에 대해 일부만 열람 가능하도록 할 수 있게 만든 테이블이다.
  - 뷰의 수정 결과는 뷰를 정의한 기본 테이블에도 똑같이 적용된다.
  - 장점
    - 사용자에 따라 특정 정보만 접근이 가능하도록 하므로, DB 보안에 용이하다.
    - 복잡한 명령문이 간단해진다.
  - 단점
    - 뷰의 정의를 바꿀 수 없다.
    - 삽입, 갱신, 삭제 연산에 대해 제한이 있다.
## Data Manipulation
### Select-From-Where
- Select : Projection과 동일한 기능을 한다
- From : Select와 동일한 기능을 한다.
- Where : 어떤 Relation에서 가져올 것인가?
``` SQL
SELECT name // Beers Table의 OB에서 Manf한 Beer의 Name을 Projection 해라.
FROM Beers
WHERE manf = 'OB'; // Condition을 걸어서 Relation을 지정할 수 있다.
```
- ```SELECT``` 명령문에서 ```*``` 를 붙이게 되면 __모든 Attribute__ 라는 의미가 된다.
- Renaming Attributes
```SQL
SELECT name AS Beer, manf AS Company // name을 Beer이란 이름으로 Projection하고 manf를 Company란 이름으로 Projection한다.
FROM Beers
WHERE manf = 'OB';
SELECT name, 'EXPENSIVE' AS PriceRate // PriceRate라는 Column을 새로 만들어 EXPENSIVE라는 문구로 채운다.
FROM Beers
WHERE price > 40;
```
- Expressions in SELECT
```SQL
SELECT price * 2 AS new_price // 가격에 X2를 한 결과로 Projection을 한다.
FROM Sells;
```
### Function in SELECT
```SQL
SELECT MIN(Price) // MAX(Price), AVG(Price), SUM(Price), COUNT(Price) 등 함수가 사용이 가능하다.
FROM Beers 
```
### Patterns in DB
- % : 모든 문자열을 탐색하는 패턴 (ex) bl% ==> bl, black, blue, blur..)
- _ : 모든 CHAR을 탐색하는 패턴 (ex) h_t ==> hat, hit, hot..)
- [] : [] 안에 있는 CHAR이 들어간 단어가 있는 지 찾을 수 있다. (ex) h[oa]t ==> hat, hot)
- ^ : ^뒤에 오는 CHAR이 들어간 단어가 아닌 단어들을 찾는다. (ex) h[^oa]t ==> hit, hut...)
- - : [] 안에 찾을 CHAR의 범위를 지정한다. (ex) h[a-c]t ==> hat, hbt, hct)
- Example
```SQL
SELECT name
FROM Drinkers
WHERE phone LIKE '%555-_ _ _ _'; // 핸드폰 번호가 ???555-???? 인 사람들을 찾는 것.
```
### NULL Values
> SQL Relation 내의 Tuple들은 하나 이상의 NULL 값을 가질 수 있다.
- Comparing NULL with values : __With Three Valued Logic(TRUE, FALSE, UNKNOWN)__
  - 어떤 값이든지 NULL과 비교를 하면 __진리 값(Truth value)__ 은 __UNKNOWN__ 이 된다.
  - 어떤 값이든지 NULL과 연산을 하면 __값(Value)__ 은 __UNKNWON__ 이 되어 버린다.
  - 하지만 Query는 WHERE 구문에 대한 값이 TRUE일 때만 Tuple을 생성한다.
- NULL Value의 존재를 확인할 때는, ```WHERE PostalCode IS NULL``` 이렇게 ```IS NULL``` Clause를 사용한다.
### Three Valued Logic
- TRUE = 1, FALSE = 0, UNKNWON = 1/2.
- AND = MIN, OR = MAX, NOT(x) = 1-x.
- Example
  - TRUE AND (FALSE OR NOT(UNKNOWN)) = MIN(1, MAX(0, (1-1/2))) = 1/2 = __UNKNOWN__
  - 어떤 값이든지 NULL과 연산하면 __UNKNOWN__ 이 된다고 했다.
- 왜 2 Valued Logic의 법칙과 3 Valued Logic의 법칙은 다른가?
  - p OR NOT p = TRUE(2 Valued)
  - p가 UNKNOWN 이라고 가정하면, 위의 식의 결과는 당연히 1/2(UNKNOWN)이 된다.
  - 따라서 둘은 아예 다른 법칙을 가진다!
## Multi-Relation Queries
> 제목 그대로 하나 이상의 Relation을 참조하는 Query이다.  
> FROM 구문 내에 1개 이상의 Relation을 집어 넣는다.  
```SQL
SELECT beer
FROM Likes, Frequents // 두 개의 Relation을 참조.
WHERE bar = 'Joe''s Bar' AND Frequents.drinker = Likes.drinker; // 서로 다른 Relation 이지만 같은 이름의 Attribute가 존재, Dot으로 구분.
```
- 이를 표로 가시화 시키면 아래와 같다.
![image](https://user-images.githubusercontent.com/71700079/142446009-4434de06-fefc-4261-b8a8-0a8a107b1b28.png)  
```SQL
SELECT b1.name, b2.name
FROM Beers b1, Beers b2 // 이렇게 하나의 테이블을 두 가지 이름으로 만들어서
WHERE b1.manf = b2.manf AND b1.name < b2.name; // 같은 제조사를 가진 두 맥주를 알파벳 순서의 Tuple로 반환한다. (Bud, Miller)
```
### Set operator
- Union : 두 Clause의 결과를 합친다.
- Intersection : 두 Clause 결과의 공통된 부분만 뽑아낸다.
```SQL
(SELECT name, address
FROM MoiveStar
WHERE gender = 'F')
INTERSECT // 이렇게 교집합을 찾으면, netWorth가 1000만을 넘는 여성 배우의 이름과 주소를 뽑아낸다.
(SELECT name, address
FROM MovieExec
WHERE netWorth > 10000000)
```
- Difference : 두 Clause의 교집합을 뺀 나머지를 뽑아낸다.
## Subqueries
> Subquery는 Query문의 SFW Statemnet내에 Query를 한번 더 집어 넣는 것이다.  
- Example
```SQL
SELECT Bar
FROM Sells
WHERE beer = 'Miller' AND price = (SELECT price // 이렇게 SFW 쿼리문 내의 조건을 SFW 쿼리문으로 거는 것!
                                   FROM Sells // Joe's Bar에서 파는 Miller의 가격이 된다.
                                   WHERE bar = 'Joe''s Bar' AND beer = 'Miller');
```
### IN operator
> Subquery의 결과가 Value가 아닌 하나 이상의 Tuple이 될 때 사용한다.
```SQL
SELECT *
FROM Beers
WHERE name IN (SELECT beer // 이 Subquery는 Fred가 좋아하는 맥주들의 집합이 되므로
               FROM Likes // IN Operator을 사용해 주어야 한다.
               WHERE drinker = 'Fred');
```
### Exists operator
> 논리 연산자로 Subquery의 결과가 Empty하지 않을 경우, True를 반환해주는 연산자이다.  
> 반대로 NOT EXISTS는 결과가 Empty하여야 True를 반환한다.  
> IN, NOT IN Operator와 잘 구분해서 사용할 것!  
```SQL
SELECT b1.name
FROM Beers b1, b2
WHERE NOT EXISTS(SELECT * // b1과 b2의 제조사가 같고 이름이 다른 경우가 존재하지 않을 때만 b1.name을 출력하겠다는 말이다.
                 FROM Beers // EXIST는 그 반대라고 생각하면 된다.
                 WHERE b1.manf = b2.manf AND b1.name <> b2.name);
```
### Any operator
> 논리 연산자로 EXIST와 같은 원리로 동작을 한다.  
> ANY 이후의 Subquery가 반환하는 Tuple과 어떤 Attribute를 비교하여 Attribute가 Subquery가 반환한 Tuple들의 원소에 대해 하나라도 >, <, = 를 만족할 경우 True를 반환한다.  
> 연산의 결과가 TRUE일 때만 내가 SELECT한 것을 출력한다.  
```SQL
SELECT old.title
FROM Movie old
WHERE old.year < ANY(SELECT year // 이 Subquery가 반환하는 Movie의 year들 중에 Old.year보다
                     FROM Movie  // 큰 (최신) 연도가 하나라도 있을 경우 old.title을 반환한다.
                     title = old.title);
```
### All operator
> ANY와 같은 종류의 논리 연산자이다.  
> ALL 이후의 Subquery와 어떤 Attribute를 비교하여 Attribute가 Subquery가 반환한 Tuple들의 원소에 대해 모두 >, <, = 를 만족할 경우 True를 반환한다.  
> 연산의 결과가 TRUE일 때만 내가 SELECT한 것을 출력한다.  
```SQL
SELECT Employee_id, Department, id, Salary
FROM Employees
WHERE Salary > ALL (SELECT Salary
                    FROM Employees
                    WHERE Department_id = 20);
```
- 위의 예제는 부서ID가 20인 부서의 사람들이 받는 모든 사람의 연봉보다 더 많은 연봉을 받는 사람들의 정보를 Select한다.
## Join Operator
- CROSS JOIN : Cartesian Product
- JOIN : Theta Join
- NATURAL JOIN : Natural Join, 앞서 배웠듯이 Theta join 중에서 연산자가 '=' 인 것이 Natural Join이다.
- NATURAL JOIN : Natural Join, 앞서 배웠듯이 Theta join 중에서 연산자가 '=' 인 것이 Natural Join이다. 근데? 중복되는 Column을 지우는.
## Aggregation Operator
- SUM() : 합을 구한다.
- AVG() : 평균을 구한다.
- COUNT() : 수를 센다.
- MIN(), MAX() : 최소, 최대를 구한다.
- 이 함수들은, NULL Value들은 무시하고 결과를 출력한다. 만약 non-NULL Value가 없다면, 결과도 NULL이다.
- Example
```SQL
SELECT AVG(DISTINCT price)
FROM Sells
WHERE beer = 'Bud'; // 버드와이저의 가격의 평균을 구한다. 대신 중복없이.
SELECT bar, MIN(price) // 이렇게는 쓸 수 없다.
FROM Sells // 왜냐하면 Aggregation이 사용되었으면, 반드시 다른 column도 aggregate거나 group화 되어야 하기 때문이다.
WHERE beer = 'Bud'; // bar은 그냥 column이라서, 이는 SQL에서 쓸 수 없다.
```
## Grouping Operator
```SQL
SELECT drinker, AVG(price)
FROM Frequents, Sells
WHERE beer = 'Bud' AND Frequents.bar = Sells.bar
GROUP BY drinker // drinker column을 기준으로 Group화 시킨다.
// 이렇게 그룹화하면 Drinker이 자주가는 bar들의 Budwiser 가격의 평균이 Drinker의 옆으로 달리게 된다.
```
### Grouping - Having
> Having 연산자는 Group by 이후의 WHERE이라고 생각하면 된다.  
```SQL
SELECT beer, AVG(price)
FROM Sells
GROUP BY beer
HAVING COUNT(bar) >= 3 // 이렇게 조건을 걸면 3개 이상의 bar에서 팔리는 beer만 Group화 된다.
SELECT COUNT(CustomerID), Country // Country와 Customer의 수를 SELECT 하는데,
FROM Customers
GROUP BY Country // Country에 대해 그룹화 한다. 즉 한 나라에 몇 명의 고객이 있는가?
HAVING COUNT(CustomerID) > 5 // 그룹화를 했을 때, 고객이 6명 이상인 나라만 출력
ORDER BY COUNT(CustomerID) DESC; // 내림차순 정렬
```
## Database modification with Subquery
- Insertion
```SQL
INSERT INTO PotBuddies // PotBuddies라는 Table에 
(SELECT d2.drinker // Sally와 같은 Bar에 다니는 Sally가 아닌 Drinker들을 한번에 저장하는 Subquery이다.
 FROM Frequetns d1, Frequents d2
 WHERE d1.drinker = 'Sally' AND 
       d2.drinker <> 'Sally' AND // d2를 출력하는데, d2는 샐리가 아닌 사람들.
       d1.bar = d2.bar // 하지만 그 사람들은 샐리와 다니는 bar가 같다.
 );
 ```
 - Deletion
 ```SQL
DELETE FROM Likes // 모든 Column 삭제.
DELETE FROM Beers b
WHERE EXISTS(SELECT name // Beers의 b와 같은 제조사지만, 이름이 다른 Beer들이 있다면 True를 반환.
             FROM Beers  // 즉, 한 제조사 당 Beer을 하나만 남기겠다는 말이다.
             WHERE manf = b.manf AND name <> b.name); 
DELETE FROM Beers b
WHERE EXISTS(SELECT a.name FROM Beers a // 이렇게 내부에 a를 새로 선언해서 Delete를 해버리면, 모든 Tuple을 다 지워버린다.
             WHERE a.manf = b.manf AND a.name <> b.name); // 왜? Deletion 방식이 Mark all tuples 방식이기 때문.
```
- Deletion은 Subquery에 해당하는 모든 Tuple에 Mark를 해놓고, Marked tuples를 모두 지워버린다.
- 위의 예시는 b를 제외한 나머지에 모두 Mark를 하지만, 그 아래의 예시는 모든 Tuples에 다 Mark를 해버리므로 안되는 것!
- 앞서 살펴보았던 NO EXISTS의 예시와 유사하다!
## Foreign Key
> Foreign Key(외래키)란 다른 Table의 Key 값을 의미한다.  
> 우리는 다른 Table의 Key 값을 주로 참조한다.  
```SQL
CREATE TABLE Studio(
  name CHAR(20) PRIMARY KEY,
  address VARCHAR(100),
  presC# INT REFERNCE MovieExec(cert#) // 이 부분이 Foreign Key 참조 부분이다.
);
// 혹은 pres C# INT, 
//      FOREIGN KEY (presC#) REFERENCE MovieExec(cert#) 로 선언해도 된다.
```
### Referential Constraint
> 앞서 우리가 배웠던 것들 중에 Referential Integrity, 참조 무결성이 있었다.  
> 그것은 우리가 참조하려는 외래 키가 실제로 존재하는 값이어야 한다는 것이다.  
> 그렇지 않을 경우에는 Violation이 발생하는 것이다.  
### Deferable vs Non Deferable
```SQL
CREATE TABLE Studio(
  name CHAR(20) PRIMARY KEY,
  address VARCHAR(100),
  presC# INT UNIQUE,
  REFERNCE MovieExec(cert#) DEFERABLE INITIALLY DEFERED
);
```
- Deferable : Violation이 발생하면, 일단 미뤄두고 테이블에 Key나 Attributes들을 모두 삽입한 뒤에 다시 참조한다.
- Non-Deferable : Violation이 발생하면, 무조건 그 Query는 Refuse된다.

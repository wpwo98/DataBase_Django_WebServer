# SQL Grammer
---
## Policy with Foriegn Key
### SET NULL
### CASCADE
> 외래키를 Reference 할 때에 발생할 수 있는 위반들을 제한하기 위해 우리는 여러가지 제약 조건을 걸 필요가 있다.  
> 아래와 같은 정책들을 통해서 __Dangling Pointer(허상 포인터)__ 의 발생을 방지할 수 있다.  
### SET NULL & CASCADE
```SQL
CREATE TABEL Sells(
  bar CHAR(20),
  beer CHAR(20),
  price REAL,
  FOREIGN KEY(beer) REFERENCES Beers(name)
  ON DELETE SET NULL // 여기도 CASCADE를 사용할 수 있다.
  ON UPDATE CASCADE);
```
- SET NULL : Beers에서 해당하는 FK(외래키)가 지워졌다면, Sells Table에서는 NULL로 처리한다.
  - 이 제약조건은 DELETE에서만 사용이 가능하다.
- CASCADE : Beers나 Sells에서 해당하는 FK가 지워지면, 양쪽 Table에서 모두 지워진다.
  - Update도 마찬가지로 FK가 업데이트 되면, 양쪽 Table 모두 자동으로 Update된다.
  - 이 제약 조건은 Update, Delete 모두 사용 가능하다.

## Checks
> Table을 만들 때 추가할 Attribute들에 대한 제약 조건을 걸 수 있다.  
### Attribute-Based Chcecks
> Value가 Insert될 때나, Update될 때 체크한다.  
> 이 조건에 대한 검사는 Attribute가 Insert 될 때, Update 될 때마다 검사한다.  
```SQL
CREATE TABLE(
)
CREATE TABLE Sells(
  bar CHAR(20),
  beer CHAR(20) CHECK (beer IN SELECT name FROM Beers)), // Beer Table에 있는 Beer만 받는다.
  price REAL CHECK(price <= 5.00)
);
```
### Tuple-Based Checks
> 위와 같이 Attribute들에 각각 제약 조건을 걸 수도 있지만,  
> 아래와 같이 Tuple로 묶어서 한번에 OR 또는 AND로 
```SQL
CREATE TABLE(
  bar CHAR(20),
  beer CHAR(20),
  price REAL,
  CHECK (bar = 'Joe''s Bar' OR price <= 5.00)
)
```
### Assertions(Table-Based Checks)
> CHECK는 해당 Relation 내에서 검사를 진행하는 것이지만, Assertion을 만들어서 일반화된 제약조건을 만들 수 있다.  
> 보통 NOT EXISTS 구문과 함께 많이 쓰인다.  
> 어떤 Relation이든지 Modification을 했다면, 무조건 검사하도록 한다.  
```SQL
CREATE ASSERTION NoRipoffBars CHECK
  NOT EXISTS(
    SELECT bar FROM Sells
    SELECT bar FROM Sells // Sells Table는 평균 가격이 5달러 이하로 내려갈 수 없다.
    GROUP BY bar
    HAVING 5.00 < AVG(price)
  )
    HAVING 5.00 < AVG(price) // 해당 Relation이 Subquery문을 True로 만들게 되는 Query가 들어왔을 경우
  )                          // Not exists 문은 False를 반환하게 된다. 따라서 이 Query는 Rejection 된다.
CREATE ASSERTION FewBar CHECK(
  (SELECT COUNT(*) FROM Bars) <= (SELECT COUNT(*) FROM Drinkers)
  // Drinkers보다 Bars가 많이 존재할 수 없다.
);
```
- Drop Assertion
```SQL
DROP ASSERTION name; // 이렇게 제거가 가능하다.
```
### Triggers
> CHECK, Assertion 보다 ECA(Event-Condition-Action)에 대해 더 강력한 표현이다.  
```SQL
CREATE TRIGGER BeerTrigger
  AFTER INSERT ON Sells
  REFERENCING NEW ROW AS NewTuple
  AFTER INSERT ON Sells // 여기가 Event 부이다.
  REFERENCING NEW ROW AS NewTuple. // Event가 발생을 할 때에만 Trigger이 작동한다.
  FOR EACH ROW
  WHEN(NewTuple.Beer NOT IN
       SELECT name FROM Beers)
  INSERT INTO Beers(name)
  WHEN(NewTuple.Beer NOT IN // 여기가 Condition 부이다.
       SELECT name FROM Beers) // 이 Condition을 충족해야만 아래의 Action 부가 실행이 된다.
  INSERT INTO Beers(name) // 여기가 Action 부이다.
         VALUES(NewTuple.beer);
```

## Transaction
> DB에서 __Transaction이란__ 일종의 Scheduling이다.  
> 어떤 사용자 두 명이 Query를 동시에 넣었을 때, 이를 동시처리 해버리면 분명 충돌이 생길 것이다.  
> 이 때, Transaction이 DB를 충돌 없이 일관성과 지속성을 유지하도록 도와준다.  
> 따라서 Transaction을 잘 설계하는 것이 중요하다.  
![image](https://user-images.githubusercontent.com/71700079/144832718-88acb090-23e9-403d-a6db-75eff0831966.png)  

### Transaction Operation
```SQL
START TRANSACTION;
  SELECT @A:=seatNo
  FROM Flights
  WHERE fltNo=123 AND FltDATE=DATE '2008-12-25' AND seatStatus='available';
  
  UPDATE Flights
  SET seatStatus='occupied'
  WHERE FltNo=123 AND FltDate=Date '2008-12-25' AND seatNo=@A
COMMIT;
```
- Commit 연산 : 일련의 Transaction 과정이 성공적으로 끝 마쳐야 Commit 연산이 실행되고, DB에 반영이 된다.
- Rollback 연산 : 일련의 Transaction 과정이 실패했을 경우, 연산을 실행하기 이전 지점으로 복원을 시킨다.
- 두 연산 모두 Consistency를 유지하는 쪽으로 동작을 하는 것이다.  
![image](https://user-images.githubusercontent.com/71700079/144834325-22793d21-429f-444f-a027-c459d3bace5d.png)  

### ACID
- Atomicity(원자성) : Transaction이 모두 DB에 등록이 되던가, 아니면 싹 다 등록이 되지 않아야 한다.(일부 등록 이런건 X)
- Consistency(일관성) : 작업 처리의 결과가 항상 일관성 있어야 한다.
- Isolation(독립성) : 각 Transaction은 서로의 연산 과정에 끼어들 수 없으며 모두 독립적으로 진행된다.
- Durability(지속성) : Transaction이 반영되었을 때, 그 결과는 영구 지속 되어야 한다.

### Serializability
> Serializability(직렬성)는 Concurrency(동시성)와 대조되는 용어이다.  
> 각 Transaction들이 일정한 순서를 가지고 직렬적으로 실행을 되는 것을 말한다.  
> Transaction은 왜 직렬성을 가지고 실행되어야만 할까?  
- 만약 Transaction이 Concurrent하게 진행된다면 어떤 문제가 발생할까?
  - Lost Update Problem  
  ![image](https://user-images.githubusercontent.com/71700079/144845298-bb2eb384-bceb-4cef-927e-518d195a8f68.png)  

  - Uncommitted Dependancy Problem  
  ![image](https://user-images.githubusercontent.com/71700079/144845325-7e955995-29e7-461c-a119-56dcf7f43bc0.png)  

  - Inconsistent Analysis Problem  
  ![image](https://user-images.githubusercontent.com/71700079/144845351-50f8d0a2-0836-4bde-b253-0bda0f9f7222.png)  

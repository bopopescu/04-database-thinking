- [1.3. MySQL](#13-mysql)
  - [1.3.1. Storage Engine](#131-storage-engine)
    - [1.3.1.1. Các khái niệm](#1311-các-khái-niệm)
      - [1.3.1.1.1. Table Lock vs Row Lock](#13111-table-lock-vs-row-lock)
      - [1.3.1.1.2. Full Text Search](#13112-full-text-search)
    - [1.3.1.2. MyISAM](#1312-myisam)
    - [1.3.1.3. InnoDB](#1313-innodb)
    - [1.3.1.4. Memory](#1314-memory)
    - [1.3.1.5. CSV](#1315-csv)
    - [1.3.1.6. Archive](#1316-archive)
    - [1.3.1.7. Blackhole](#1317-blackhole)
    - [1.3.1.8. NDB (còn được gọi là NDBCLUSTER)](#1318-ndb-còn-được-gọi-là-ndbcluster)
    - [1.3.1.9. Merge](#1319-merge)
    - [1.3.1.10. Federated](#13110-federated)
    - [1.3.1.11. So sánh cụ thể MyISAM vs InnoDB](#13111-so-sánh-cụ-thể-myisam-vs-innodb)
    - [1.3.1.12. So sánh chung](#13112-so-sánh-chung)
  - [1.3.2. Installation](#132-installation)
  - [1.3.3. Data Types](#133-data-types)
    - [1.3.3.1. Các kiểu dữ liệu cơ bản](#1331-các-kiểu-dữ-liệu-cơ-bản)
    - [1.3.3.2. Kiểu dữ liệu đặc biệt utf8mb4](#1332-kiểu-dữ-liệu-đặc-biệt-utf8mb4)
  - [1.3.4. Transaction](#134-transaction)
    - [1.3.4.1. Transaction](#1341-transaction)
      - [1.3.4.1.1. Transaction là gì?](#13411-transaction-là-gì)
      - [1.3.4.1.2. Kiểu của transaction](#13412-kiểu-của-transaction)
      - [1.3.4.1.3. Các thuộc tính của Transaction](#13413-các-thuộc-tính-của-transaction)
      - [1.3.4.1.4. Rủi ro khi thực thi transaction](#13414-rủi-ro-khi-thực-thi-transaction)
      - [1.3.4.1.5. Xử lý transaction](#13415-xử-lý-transaction)
        - [1.3.4.1.5.1. Lệnh COMMIT](#134151-lệnh-commit)
        - [1.3.4.1.5.2. Lệnh ROLLBACK](#134152-lệnh-rollback)
        - [1.3.4.1.5.3. Lệnh SAVEPOINT](#134153-lệnh-savepoint)
        - [1.3.4.1.5.4. Lệnh SET TRANSACTION](#134154-lệnh-set-transaction)
    - [1.3.4.2. Distributed transaction](#1342-distributed-transaction)
      - [1.3.4.2.1. Two Phase Commit](#13421-two-phase-commit)
      - [1.3.4.2.2. Các giải pháp đảm bảo Eventually Consistency](#13422-các-giải-pháp-đảm-bảo-eventually-consistency)
        - [1.3.4.2.2.1. Phương pháp lưu log kết quả giao dịch theo transaction id](#134221-phương-pháp-lưu-log-kết-quả-giao-dịch-theo-transaction-id)
        - [1.3.4.2.2.2. Sử dụng cặp queue Request và Response.](#134222-sử-dụng-cặp-queue-request-và-response)
  - [1.3.5. Isolation](#135-isolation)
    - [1.3.5.1. Read Uncommitted](#1351-read-uncommitted)
    - [1.3.5.2. Read Committed](#1352-read-committed)
    - [1.3.5.3. Repeatable read](#1353-repeatable-read)
    - [1.3.5.4. Serializable](#1354-serializable)
    - [1.3.5.5. SnapShot](#1355-snapshot)
    - [1.3.5.6. Tóm tắt Isolation Level](#1356-tóm-tắt-isolation-level)
  - [1.3.6. Connector](#136-connector)
    - [1.3.6.1. JDBC Driver for MySQL (Connector/J)](#1361-jdbc-driver-for-mysql-connectorj)
    - [1.3.6.2. Python Driver for MySQL (Connector/Python)](#1362-python-driver-for-mysql-connectorpython)

-------------------------------

## 1.3. MySQL

[Basic MySQL Tutorial](http://www.mysqltutorial.org/basic-mysql-tutorial.aspx)

[MySQL Tutorial](https://www.tutorialspoint.com/mysql/index.htm)

### 1.3.1. Storage Engine

Storage Engine thực chất là cách MySQL lưu trữ dữ liệu trên đĩa cứng. MySQL lưu mỗi database như là một thư mục con nằm dưới thư mục data. Khi một table được tạo ra, MySQL sẽ lưu định nghĩa bảng ở file đuôi .frm và tên trùng với tên của bảng được tạo. Việc quản lý định nghĩa bảng là nhiệm vụ của MySQL server, dù rằng mỗi storage engine sẽ lưu trữ và đánh chỉ mục (index) dữ liệu khác nhau.

**InnoDB** là kiểu mặc định và cơ bản nhất của storage engine và Oracle đề xuất sử dụng nó cho các bảng ngoại trừ một vài trường hợp đặc biệt (lệnh **CREATE TABLE** sẽ tạo ra **InnoDB** tables theo mặc định).

MySQL Server sử dụng kiến trúc pluggable storage engine để cho phép storage engines được load hoặc không load lên từ MySQL server.

Để xác định loại storage engine nào được server hỗ trợ, dùng lệnh **SHOW ENGINES**. Giá trị trong những cột được hỗ trợ sẽ chỉ ra khi nào engine được sử dụng, có gía trị YES hoặc NO hoặc DEFAULT sẽ chỉ ra rằng đã có sẵn, không có sẵn, hoặc có sẵn và hiện tại đang thiết lập mặc định cho storage engine.

```sql
mysql> SHOW ENGINES\G
*************************** 1. row ***************************
      Engine: InnoDB
     Support: DEFAULT
     Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
          XA: YES
  Savepoints: YES
*************************** 2. row ***************************
      Engine: MRG_MYISAM
     Support: YES
     Comment: Collection of identical MyISAM tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 3. row ***************************
      Engine: MEMORY
     Support: YES
     Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 4. row ***************************
      Engine: BLACKHOLE
     Support: YES
     Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 5. row ***************************
      Engine: MyISAM
     Support: YES
     Comment: MyISAM storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 6. row ***************************
      Engine: CSV
     Support: YES
     Comment: CSV storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 7. row ***************************
      Engine: ARCHIVE
     Support: YES
     Comment: Archive storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 8. row ***************************
      Engine: PERFORMANCE_SCHEMA
     Support: YES
     Comment: Performance Schema
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 9. row ***************************
      Engine: FEDERATED
     Support: NO
     Comment: Federated MySQL storage engine
Transactions: NULL
          XA: NULL
  Savepoints: NULL
9 rows in set (0.00 sec)

mysql>
```

#### 1.3.1.1. Các khái niệm

##### 1.3.1.1.1. Table Lock vs Row Lock

Trong MySQL có 2 khái niệm locking khác nhau nhằm phục vụ mục đích transactional read/write: Table Lock & Row Lock.

- Table lock là lock được tạo ra để ngăn các transaction khác can thiệp vào 1 "table" được lock để tránh việc thay đổi dữ liệu trong quá trình 1 câu query đang được thực thi ở 1 table đó.

- Row lock là lock được tạo ra để ngăn các transaction khác can thiệp vào "row" được lock để tránh việc thay đổi dữ liệu trong quá trình 1 câu query đang diễn ra.

Khi sử dụng MySQL, Table locks sẽ có ưu thế hơn trong một số tình huống:

- Hầu hết query đến table đều là lệnh đọc

- Query đến table có cả đọc và ghi, trong đó lệnh ghi như Update / Delete chỉ ứng dụng với 1 row nào đó có thể lọc theo key cụ thể. Ví dụ:

```
UPDATE tbl_name SET column=value WHERE unique_key_col=key_value;
DELETE FROM tbl_name WHERE unique_key_col=key_value;
```

- Lệnh SELECT được dùng với INSERT, và ít lệnh UPDATE / DELETE được sử dụng.

- Nhiều lệnh scan, GROUP BY trên cả table mà ko kèm theo thao tác write.

Với những tình huống trên, (và database của bạn vẫn đang dùng MyISAM) nên cân nhắc sử dụng Table locks thay vì row locks để ít tốn tài nguyên hơn.

##### 1.3.1.1.2. Full Text Search

Full text search (gọi tắt là FTS) là cách tự nhiên nhất để tìm kiếm thông tin, hệt như Google, ta chỉ cần gõ từ khóa và nhấn enter thế là có kết quả trả về.

Về mặt cơ bản, điều làm nên sự khác biệt giữa Full text search và các kĩ thuật search thông thường khác chính là “Inverted Index”.

**Minh họa**:

![](https://viblo.asia/uploads/322ca697-dea7-4eac-a98e-90f8fcf50068.png)

**Ưu điểm**:

- Kết quả search trả về nhiều.

- Khi đánh index thì tốc độ search Nhanh

- Tối ưu hơn việc sử dụng LIKE khi thao tác với các trường text lớn.

**Nhược điểm**:

- Độ chính xác thấp 

- Độ nhiễu cao

- Từ đồng nghĩa (synonyms)

- Từ cấu tạo bằng chữ đầu của cụm từ (acronym)

- Vấn đề với tìm kiếm tiếng Việt có dấu và không dấu

#### 1.3.1.2. MyISAM

Table-level locking giới hạn hiệu suất read/write dữ liệu, vì vậy nó thường được sử dụng cho các công việc read-only hoặc read-mostly trong các cấu hình Web và lưu trữ dữ liệu.

Chuyển đổi 1 table sang MyISAM: `ALTER TABLE table_name ENGINE = MyISAM;`

**Ưu điểm**: 

- Engine hỗ trợ **Full Text Search** lập chỉ mục toàn văn, cung cấp thuật toán tìm kiếm khá giống Google. 

- Kiến trúc đơn giản nên có tốc độ truy suất (đọc và tìm kiếm) nhanh nhất trong các loại Storage Engine.

**Nhược điểm**: 

- MyISAM hoạt động theo cơ chế **Table Level Locking**, nên khi có hành động thực hiện (thêm/sửa/xóa) 1 bản ghi nào đó trong table thì table đó sẽ bị khóa lại, chờ tới khi hành động này được thực hiện xong thì hành động kia mới tiếp tục được thực hiện.

- Kiến trúc đơn giản, không ràng buộc nên loại Storage Engine này rất dễ bị crash, hỏng chỉ mục với những table có số lượng bản ghi lớn. 

#### 1.3.1.3. InnoDB

Là Storage Engine mặc định trong MySQL 5.7. InnoDB là một Storage Engine transaction-safe (tuân thủ ACID) cho MySQL có các commit, rollback và khả năng khôi phục lỗi để bảo vệ dữ liệu người dùng. Row-level locking của InnoDB và kiểu nonlocking read của Oracle-style làm tăng sự đồng thời và hiệu suất của nhiều người dùng. InnoDB lưu trữ dữ liệu người dùng trong các clustered indexes để giảm I/O cho các truy vấn thông thường dựa trên các primary key. Để duy trì tính toàn vẹn của dữ liệu, InnoDB cũng hỗ trợ các ràng buộc toàn vẹn Foreign Key.

Chuyển đổi một table sang InnoDB: `ALTER TABLE table_name ENGINE = InnoDB;`

**Ưu điểm**:

- Engine này kiểm tra tính toàn vẹn và ràng buộc dữ liệu rất cao, khó xảy ra tình trạng hỏng chỉ mục và crash table.

- Hoạt động theo cơ chế **Row Level Locking**, vì vậy trong lúc thực hiện các hành động (thêm/sửa/xóa) trên 1 bản ghi, thì các hoạt động ở bản ghi khác trên table vẫn diễn ra bình thường.

- Hỗ trợ Transaction giúp đảm bảo an toàn khi thực hiện một khối lệnh SQL đảm bảo nhất quán dữ liệu.

**Nhược điểm**:

- Hoạt động cần nhiều RAM hơn, nhưng nếu so sánh với MyISAM trong trường hợp tần suất Insert/Update/Delete lớn thì có khi sẽ lớn hơn vì cơ chế Table Level Locking sẽ gây ra hàng đợi lớn, gây chậm quá trình xử lý.

#### 1.3.1.4. Memory

Lưu trữ tất cả dữ liệu trong RAM, để truy cập nhanh trong các môi trường đòi hỏi tra cứu nhanh các dữ liệu không quan trọng. Engine này trước đây gọi là HEAP Engine. Storage Engine này đang sử dụng ít dần, do InnoDB với vùng bộ đệm cung cấp một cách mục đích chung và bền để giữ hầu hết hoặc tất cả dữ liệu trong memory, và NDBCLUSTER cung cấp tra cứu giá trị quan trọng nhanh cho các bộ dữ liệu phân tán lớn.

#### 1.3.1.5. CSV

Các bảng của nó thực sự là các tập tin văn bản với các giá trị được phân cách bởi dấu phẩy. Các bảng CSV cho phép bạn nhập hoặc đổ dữ liệu ở định dạng CSV, để trao đổi dữ liệu với các tập lệnh và ứng dụng đọc và ghi cùng một định dạng. Vì bảng CSV không được lập chỉ mục, bạn thường giữ dữ liệu trong các bảng InnoDB trong quá trình hoạt động bình thường và chỉ sử dụng các bảng CSV trong giai đoạn nhập hoặc xuất.

#### 1.3.1.6. Archive

Các bảng nhỏ gọn, không biểu hiện này được dùng để lưu trữ và truy xuất số lượng lớn các thông tin kiểm tra lịch sử, lưu trữ, hoặc kiểm tra an toàn.

#### 1.3.1.7. Blackhole

Công cụ lưu trữ Blackhole chấp nhận nhưng không lưu dữ liệu, tương tự như `/dev/null` trên Unix. Các truy vấn luôn trả về một tập rỗng. Các bảng này có thể được sử dụng trong các cấu hình nhân bản, nơi các lệnh DML được gửi đến các slave server, nhưng các master server không giữ bản sao dữ liệu của chính nó.

#### 1.3.1.8. NDB (còn được gọi là NDBCLUSTER)

Công cụ cơ sở dữ liệu được nhóm lại này đặc biệt phù hợp với các ứng dụng đòi hỏi thời gian hoạt động và tính khả dụng cao nhất có thể.

#### 1.3.1.9. Merge

Cho phép một DBA MySQL hoặc nhà phát triển hợp lý nhóm một loạt các bảng MyISAM giống hệt nhau và tham chiếu chúng như một đối tượng. Tốt cho các môi trường VLDB như lưu trữ dữ liệu.

#### 1.3.1.10. Federated

Cung cấp khả năng liên kết máy chủ MySQL riêng biệt để tạo ra một cơ sở dữ liệu hợp lý từ nhiều máy chủ vật lý. Rất tốt cho môi trường phân phối hoặc môi trường dữ liệu mart.

#### 1.3.1.11. So sánh cụ thể MyISAM vs InnoDB

| MyISAM                                                                                                                                         | InnoDB                                                                |
|------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Hỗ trợ Table - Level Locking                                                                                                                   | Hỗ trợ Row - Level Locking                                            |
| Được thiết kế cho nhu cầu về tốc độ (speed)                                                                                                    | Được thiết kế để đạt hiệu suất tối đa khi xử lý lượng dữ liệu lớn     |
| Không hỗ trợ Foreign keys vì thế nên chúng ta gọi MySQL với MyISAM là DBMS                                                                     | Hỗ trợ Foreign keys vì thế nên chúng ta gọi MySQL với InnoDB là RDBMS |
| Lưu trữ tables, data, indexes của nó trong không gian đĩa bằng cách sử dụng 3 file riêng biệt (table_name.FRM, table_name.MYD, table_name.MYI) | Lưu trữ tables, indexes của nó trong 1 không gian bảng                |
| Không hỗ trợ Transaction                                                                                                                       | Có hỗ trợ Transaction                                                 |
| Hỗ trợ Full Text Search                                                                                                                        | Từ version 5.5 trở về sau, InnoDB có hỗ trợ Full Text Search          |


- Với 1 ứng dụng dạng Blog, News, ... thì nên dùng MyISAM để cho hiệu suất tốt.

- Với ứng dụng dạng Forum, Socials network thì nên sử dụng InnoDB để tốc độ Insert/Update dữ liệu cao nhất.

#### 1.3.1.12. So sánh chung

Các loại storage engine được cung cấp bởi MySQL được thiết kế để sử dụng tùy theo các trường hợp, bảng sau cung cấp một các nhìn tổng quan về một vài storage engine của MySQL.

Feature	| MyISAM | Memory | InnoDB | Archive | NDB
---|---|---|---|---|---
B-tree indexes |Yes|Yes|Yes|No|No
Backup/point-in-time recovery (note 1)|Yes|Yes|Yes|Yes|Yes
Cluster database support|No|No|No|No|Yes
Clustered indexes|No|No|Yes|No|No
Compressed data|Yes (note 2)|No|Yes|Yes|No
Data caches|No|N/A|Yes|No|Yes
Encrypted data (note 3)|Yes|Yes|Yes|Yes|Yes
Foreign key support|No|No|Yes|No|Yes (note 4)
Full-text search indexes|Yes|No|Yes (note 5)|No|No
Geospatial data type support|Yes|No|Yes|Yes|Yes
Geospatial indexing support|Yes|No|Yes (note 6)|No|No
Hash indexes|No|Yes|No (note 7)|No|Yes
Index caches|Yes|N/A|Yes|No|Yes
Locking granularity|Table|Table|Row|Row|Row
MVCC|No|No|Yes|No|No
Replication support (note 1)|Yes|Limited (note 8)|Yes|Yes|Yes
Storage limits|256TB|RAM|64TB|None|384EB
T-tree indexes|No|No|No|No|Yes
Transactions|No|No|Yes|No|Yes
Update statistics for data dictionary|Yes|Yes|Yes|Yes|Yes

Các lưu ý :

1. Được hiện thực trong server chứ không riêng storage engine.
2. Kết hợp MyISAM tables và chỉ hỗ trợ khi sử dụng định dạng kết hợp dòng. Bảng được sử dụng để định dạng kết hợp dòng với MyISAM chỉ được đọc.
3. Hiện thực trong server thông qua các hàm mã hóa. Data-at-rest được mã hóa được hỗ trợ từ phiên bản MySQL 5.7 trở về sau.
4. Hỗ trợ cho khóa ngoại được sẵn sàng ở MySQL Cluster NDB và phiên bản 7.3 về sau.
5. InnoDB được hỗ trợ cho FULLTEXT indexes sẵn sàng ở phiên bản MySQL 5.6 về sau.
6. InnoDB hỗ trợ cho indexing geospatial được sẵn sàng ở phiên bản MySQL 5.7 về sau.

7. InnoDB utilizes hash indexes internally for its Adaptive Hash Index feature.

### 1.3.2. Installation

![](https://www.ntu.edu.sg/home/ehchua/programming/sql/images/MySQL_DBMS.png)

MySQL hoạt động như một client-server system qua TCP/IP network.

Server chạy trên machine với IP adress trên TCP port number được chọn (default TCP port number là 3306).

[Install MySQL Server on Ubuntu](https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu/)

- Install MySQL Server:

```
sudo apt-get update
sudo apt-get install mysql-server #Install MySQL
sudo ufw allow mysql #Allow remote access
systemctl start mysql #Start the MySQL service
systemctl enable mysql #Launch at reboot
```

- Start the mysql shell: `sudo /usr/bin/mysql -u root -p`

Set the root password: 
`UPDATE mysql.user SET authentication_string = PASSWORD('password') WHERE User = 'root';`

`FLUSH PRIVILEGES;`

- View users: `SELECT User, Host, authentication_string FROM mysql.user;`

- Create a database: `CREATE DATABASE demodb;`

- Add a database user: 

`INSERT INTO mysql.user (User,Host,authentication_string,ssl_cipher,x509_issuer,x509_subject) VALUES('demouser','localhost',PASSWORD('demopassword'),'','','');`

`FLUSH PRIVILEGES;`

- Grant database user permissions:

```
GRANT ALL PRIVILEGES ON demodb.* to demouser@localhost; #Full permissions for demodb
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'demouser'@'localhost';
2 rows in set (0.00 sec)
```

### 1.3.3. Data Types

#### 1.3.3.1. Các kiểu dữ liệu cơ bản

[Data Types](https://o7planning.org/vi/10321/du-lieu-va-cau-truc-trong-mysql#a206046)

MySQL sử dụng nhiều kiểu dữ liệu, được chia thành 3 loại: kiểu Number, kiểu Datetime, và kiểu String.

* Kiểu dữ liệu Number

  Kiểu dữ liệu| Mô tả
  --|--
  TINYINT(size)|Lưu trữ một số nguyên có giá trị từ -128 đến -127 hoặc 0 đến 255
  SMALLINT(size)| Lưu trữ một số nguyên có giá trị từ -32768 đến 32767 hoặc 0 đến 65535
  MEDIUMINT(size)|Lưu trữ một số nguyên có giá trị từ -8388608 đến 8388607 hoặc 0 đến 16777215
  INT(size)|Lưu trữ một số nguyên có giá trị từ -2147483648 đến 2147483647 hoặc 0 đến 4294967295
  BIGINT(size)|Lưu trữ một số nguyên có giá trị từ -9223372036854775808 đến 9223372036854775807 hoặc 0 đến 18446744073709551615.
  FLOAT(size,d)|Lưu trữ một số thập phân loại nhỏ (Ví dụ: 567.25). Tham số “size” dùng để xác định kích thước tối đa của phần nguyên. Tham số “d” dùng để xác định kích thước tối đa của phần thập phân.    Tuy nhiên điều này là không bắt buộc, vì mặc định là (10,2).
  DOUBLE(size,d)|Lưu trữ một số thập phân loại lớn. Tham số “size” dùng để xác định kích thước tối đa của phần nguyên. Tham số “d” dùng để xác định kích thước tối đa của phần thập phân. Mặc định là (16,4).
  DECIMAL(size,d)|Lưu trữ như một chuỗi, cho phép một dấu thập phân cố định. Tham số “size” dùng để xác định kích thước tối đa của phần nguyên. Tham số “d” dùng để xác định kích thước tối đa của phần thập phân.

* Kiểu dữ liệu String

  Kiểu dữ liệu| Mô tả
  --|--
  CHAR(size)|Dữ liệu kiểu chuỗi có độ dài cố định: Độ dài từ 1 đến 255 kí tự, có thể được chỉ định trước hoặc không
  VARCHAR(size)| Dữ liệu kiểu chuỗi có độ dài thay đổi. Độ dài từ 1 đến 255 kí tự 
  TINYTEXT| Dùng để lưu trữ một chuỗi ký tự có chiều dài tối đa là 255 ký tự
  TEXT| Dùng để lưu trữ một chuỗi ký tự có chiều dài tối đa là 65,535 ký tự
  BLOB| Dùng để lưu trữ dữ liệu nhị phân tối đa là 65,535 byte
  MEDIUMTEXT|Dùng để lưu trữ một chuỗi ký tự có chiều dài tối đa là 16,777,215 ký tự
  MEDIUMBLOB|Dùng để lưu trữ dữ liệu nhị phân tối đa là 16,777,215 byte
  LONGTEXT|Dùng để lưu trữ một chuỗi ký tự có chiều dài tối đa là 4,294,967,295 ký tự
  LONGBLOB|Dùng để lưu trữ dữ liệu nhị phân tối đa là 4,294,967,295 byte
  ENUM|Khi định nghĩa một trường kiểu này, tức là, ta đã chỉ ra một danh sách các đối tượng mà trường phải nhận (có thể là Null). Ví dụ, nếu ta muốn một trường nào đó chỉ nhận một trong các giá trị "A" hoặc "B" hoặc "C" thì ta phải định nghĩa kiểu ENUM cho nó như sau: ENUM ('A', 'B', 'C'). Và chỉ có các giá trị này (hoặc NULL) có thể xuất hiện trong trường đó.

* Kiểu dữ liệu DateTime

  Kiểu dữ liệu| Mô tả
  --|--
  DATE|Một date trong định dạng YYYY-MM-DD, giữa 1000-01-01 và 9999-12-31
  DATETIME|Một tổ hợp Date và Time trong định dạng YYYY-MM-DD HH:MM:SS, giữa 1000-01-01 00:00:00 và 9999-12-31 23:59:59
  TIMESTAMP|Một Timestamp từ giữa nửa đêm ngày 1/1/1970 và 2037 (dạng YYYYMMDDHHMMSS)
  TIME|Lưu time trong định dạng HH:MM:SS
  YEAR(M)|Lưu 1 năm trong định dạng 2 chữ số hoặc 4 chữ số. Nếu độ dài được xác định là 2 (ví dụ: YEAR(2)), YEAR có thể từ 1970 tới 2069 (70 tới 69). Nếu độ dài được xác định là 4, YEAR có thể từ 1901 tới 2155. Độ dài mặc định là 4.

#### 1.3.3.2. Kiểu dữ liệu đặc biệt utf8mb4

[Support full Unicode in MySQL databases](https://mathiasbynens.be/notes/mysql-utf8mb4)

 *  Utf8mb4 là kiểu dữ liệu đặc biệt ánh xạ tới từ UTF-8, do đó hỗ trợ đầy đủ Unicode, bao gồm cả các biểu tượng astral.
 *  Đặc điểm
    * Hỗ trợ BMP và các kí tự bổ sung
    * Yêu cầu tối đa 4 byte cho mỗi ký tự nhiều byte

* utf8mb4 tương phản với bộ ký tự utf8mb3, chỉ hỗ trợ các ký tự BMP và sử dụng tối đa ba byte cho mỗi ký tự:
    * Đối với một ký tự BMP, utf8mb4 và utf8mb3 có các đặc tính lưu trữ giống nhau: cùng một giá trị mã, cùng một mã hóa, cùng độ dài. 
    * Đối với một ký tự bổ sung, utf8mb4 yêu cầu bốn byte để lưu trữ nó, trong khi utf8mb3 không thể lưu trữ ký tự đó.

 *  Chuyển đổi `utf8` sang `utf8mb4` trong MySQL
    * Tạo bản sao lưu
    * Nâng cấp MySQL Server phiên bản 5.5.3+
    * Sửa đổi databases, tables, columns

    ```Shell
        # For each database:
        ALTER DATABASE database_name CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
        # For each table:
        ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        # For each column:
        ALTER TABLE table_name CHANGE column_name column_name VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        # (Don’t blindly copy-paste this! The exact statement depends on the column type, maximum length, and other properties. The above line is just an example for a `VARCHAR` column.)
    ```

    * Kiểm tra độ dài tối đa của các cột và các khóa chỉ mục: khi chuyển đổi từ utf8 sang utf8mb4, số byte tối đa trong các cột hoặc các khóa không thay đổi, chỉ thay đổi số lượng kí tự do độ dài tối da của mỗi kí tự bây giờ là 4 byte thay vì 3 byte như cũ
    * Sửa đổi bộ kí tự connection, client và server

    ```Shell
        mysql> SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';
        +--------------------------+--------------------+
        | Variable_name            | Value              |
        +--------------------------+--------------------+
        | character_set_client     | utf8mb4            |
        | character_set_connection | utf8mb4            |
        | character_set_database   | utf8mb4            |
        | character_set_filesystem | binary             |
        | character_set_results    | utf8mb4            |
        | character_set_server     | utf8mb4            |
        | character_set_system     | utf8               |
        | collation_connection     | utf8mb4_unicode_ci |
        | collation_database       | utf8mb4_unicode_ci |
        | collation_server         | utf8mb4_unicode_ci |
        +--------------------------+--------------------+
        10 rows in set (0.00 sec)
    ```

    * Sửa chữa và tối ưu hóa các bảng

    ``` Shell
        # For each table
        REPAIR TABLE table_name;
        OPTIMIZE TABLE table_name;
    ```


### 1.3.4. Transaction

#### 1.3.4.1. Transaction

##### 1.3.4.1.1. Transaction là gì?

Có thể hiểu Transaction là một tiến trình xử lý có xác định điểm đầu và điểm cuối, được chia nhỏ thành các operation (phép thực thi) , tiến trình được thực thi một cách tuần tự và độc lập các operation đó theo nguyên tắc hoặc tất cả đều thành công hoặc một operation thất bại thì toàn bộ tiến trình thất bại. Nếu việc thực thi một operation nào đó bị fail đồng nghĩa với việc dữ liệu phải rollback về trạng thái ban đầu.

Có thể lấy ví dụ về 1 Transaction đơn giản nhất là tiến trình cài đặt phần mềm hoặc gỡ bỏ phần mềm. Việc cài đặt được chia thành các bước, thực hiện tuần tự từ đầu đến cuối, nếu toàn bộ các bước thực thi thành công đồng nghĩa với việc tiến trình cài đặt hoặc gỡ bỏ phần mềm thành công và ngược lại, một phép thất bại thì tiến trình phải rollback lại tức sẽ không có bất kỳ thay đổi nào trên máy tính.

##### 1.3.4.1.2. Kiểu của transaction

Các kiểu transaction khác nhau được phân biệt bằng việc chia các operation như thế nào. Có hai mô hình transaction như sau:

- **Flat Transaction – Transaction ngang hàng** Việc chia các operation là ngang hàng nhau. Thực thi các operation là tuần tự từ trái sang phải hoặc từ trên xuống dưới.

- **Nested Transaction – Transaction lồng nhau** Việc thực thi các operation dựa theo nguyên tắc từ trong ra ngoài. Như vậy khi nhìn vào hình vẽ chúng ta thấy các operation ở dạng này có vẻ phụ thuộc vào nhau nhưng khi thực thi thì là độc lập theo nguyên tắc operation trong thực thi xong thì mới đến operation ngoài.

##### 1.3.4.1.3. Các thuộc tính của Transaction

Mô hình ACID được gắn chặt với cơ sở dữ liệu quan hệ (Relation DB). Tuy nhiên, xét về transaction nói chung, chúng ta cũng có thể áp dụng các thuộc tính này vào.

- **Atomicity – tính đơn vị:** Một transaction xác định ranh giới của nó rất rõ ràng, tức xác định điểm bắt đầu và kết thúc của tiến trình. Như vậy có thể coi nó như một đơn vị thực thi và đơn vị thực thi này thực hiện theo nguyên tắc “all or nothing”. Nghĩa là nếu một thành phần nào đó trong transaction thực thi hỏng (fail) thì đồng nghĩa với việc không có gì xảy ra tức không có gì thay đổi về mặt dữ liệu.

- **Consistency – nhất quán:** Dữ liệu nhất quán với transaction ở thời điểm bắt đầu và kết thúc. Nhất quán ở transaction là strong consistency. Để tìm hiểu kỹ hơn về tính nhất quán, xin đọc lại bài viết NoSQL.

- **Isolation – độc lập:** Nếu hai transaction thực thi cùng lúc thì nguyên tắc thực thi là thực thi độc lập. Nghĩa là một transaction không thể “nhìn thấy” một transaction khác. “Không nhìn thấy” ở đây là không tác động lẫn nhau, chủ yếu trên dữ liệu.

- **Durability – bền vững:** Dữ liệu của transaction sau khi thực thi xong được cố định, chính thức và bền vững. Nghĩa là những thay đổi đã được cố định, không có chuyện có thể chuyển lại trạng thái dữ liệu lúc trước khi thực hiện transaction.

##### 1.3.4.1.4. Rủi ro khi thực thi transaction

Có ba loại rủi ro chính khiến việc thực thi một transaction có thể bị fail.

- **Việc thực thi operation bị hỏng:** rõ ràng việc này sẽ dẫn tới transaction bị hỏng. Điều này đã được quy định rõ trong định nghĩa về transaction.

- **Vấn đề về phần cứng và mạng:** việc phần cứng hoặc mạng có vấn đề trong lúc đang thực thi transaction sẽ dẫn đến tiến trình xử lý thất bại.

- **Các vấn đề với dữ liệu dùng chung:** Đây là vấn đề khó nhất. Rõ ràng data là một tài nguyên dùng chung, do đó sẽ có những nguy cơ mà transaction gặp phải khi xử lý dữ liệu dùng chung này. Ta sẽ xem xét kỹ hơn dưới đây. Như chúng ta đã biết, phần mềm viết ra là để xử lý dữ liệu, 2 operations (phép) căn bản của phần mềm với dữ liệu là đọc và ghi (read và write) trong đó phép write lại được chia nhỏ thành 3 operations nhỏ hơn là insert (thêm mới), update (sửa), delete (xóa). Dữ liệu là một tài nguyên dùng chung, nếu như có nhiều tiến trình xử lý đồng thời thực hiện các phép trên dữ liệu sẽ xảy ra những rủi ro: write-write, write-read,... việc dữ liệu ghi cùng lúc dẫn tới hỏng dữ liệu hoặc dữ liệu đọc ra không đồng nhất với dữ liệu mới ghi vào,... sẽ đề cập kỹ hơn trong phần tiếp theo dưới đây.

##### 1.3.4.1.5. Xử lý transaction

Các lệnh sau đây được sử dụng để xử lý transaction.

- **COMMIT** – để lưu các thay đổi.
- **ROLLBACK** – để khôi phục lại các thay đổi.
- **SAVEPOINT** – tạo ra các điểm trong transaction để ROLLBACK.
- **SET TRANSACTION** – thiết lập các thuộc tính cho transaction.

Các lệnh điều khiển transaction chỉ được sử dụng với các lệnh thao tác dữ liệu **DML** như – INSERT, UPDATE và DELETE.

Chúng không thể được sử dụng trong lệnh CREATE TABLE hoặc DROP TABLE vì các hoạt động này được tự động được commit trong cơ sở dữ liệu.

###### 1.3.4.1.5.1. Lệnh COMMIT

Lệnh COMMIT được sử dụng để lưu các thay đổi gọi bởi một transaction với cơ sở dữ liệu.

Lệnh COMMIT lưu tất cả các transaction vào cơ sở dữ liệu kể từ khi lệnh COMMIT hoặc ROLLBACK cuối cùng.

Cú pháp của lệnh COMMIT như sau.

```sql
COMMIT;
```

**Ví dụ**

Giả sử bảng CUSTOMERS có các bản ghi sau đây:

```sql
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  1 | Ha Anh   |  32 | Da Nang   |  2000.00 |
|  2 | Van Ha   |  25 | Ha Noi    |  1500.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  4 | Thu Minh |  25 | Ha Noi    |  6500.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------
```

Sau đây là một ví dụ có thể xóa các bản ghi từ bảng có age = 25 và sau đó COMMIT thay đổi trong cơ sở dữ liệu.

```sql
DELETE FROM CUSTOMERS
   WHERE AGE = 25;
COMMIT;
```

Vì vậy, hai hàng từ bảng sẽ bị xóa và câu lệnh SELECT sẽ cho kết quả sau.

```sql
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  1 | Ha Anh   |  32 | Da Nang   |  2000.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------+
```

###### 1.3.4.1.5.2. Lệnh ROLLBACK

Lệnh ROLLBACK được sử dụng để hoàn tác các transaction chưa được lưu vào cơ sở dữ liệu. Lệnh này chỉ có thể được sử dụng để hoàn tác các transaction kể từ khi lệnh COMMIT hoặc ROLLBACK cuối cùng được phát hành.

Cú pháp lệnh ROLLBACK như sau:

```sql
ROLLBACK;
```

**Ví dụ**

Giả sử bảng CUSTOMERS có các bản ghi sau đây:

```sql
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  1 | Ha Anh   |  32 | Da Nang   |  2000.00 |
|  2 | Van Ha   |  25 | Ha Noi    |  1500.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  4 | Thu Minh |  25 | Ha Noi    |  6500.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------+
```

Sau đây là một ví dụ, có thể xóa các bản ghi từ bảng có age = 25 và sau đó XÓA các thay đổi trong cơ sở dữ liệu.

```sql
DELETE FROM CUSTOMERS
   WHERE AGE = 25;
ROLLBACK;
```

Vì vậy, hoạt động xóa sẽ không ảnh hưởng đến bảng và câu lệnh SELECT sẽ cho kết quả sau.

```sql
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  1 | Ha Anh   |  32 | Da Nang   |  2000.00 |
|  2 | Van Ha   |  25 | Ha Noi    |  1500.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  4 | Thu Minh |  25 | Ha Noi    |  6500.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------+
```

###### 1.3.4.1.5.3. Lệnh SAVEPOINT

SAVEPOINT là một điểm trong một transaction khi bạn có thể cuộn transaction trở lại một điểm nhất định mà không quay trở lại toàn bộ transaction.

Cú pháp của lệnh SAVEPOINT như thể hiện dưới đây.

```sql
SAVEPOINT SAVEPOINT_NAME;
```

Lệnh này chỉ phục vụ trong việc tạo ra SAVEPOINT trong số tất cả các câu lệnh transaction. Lệnh ROLLBACK được sử dụng để hoàn tác một nhóm các transaction.

Cú pháp để cuộn lại một SAVEPOINT như thể hiện dưới đây.

```sql
ROLLBACK TO SAVEPOINT_NAME;
```

Sau đây là ví dụ bạn định xóa ba bản ghi khác nhau từ bảng CUSTOMERS. Bạn muốn tạo một SAVEPOINT trước mỗi lần xoá, để bạn có thể XÓA trở lại SAVEPOINT bất kỳ lúc nào để trả lại dữ liệu thích hợp cho trạng thái ban đầu.

**Ví dụ**

Giả sử bảng CUSTOMERS có các bản ghi sau.

```sql
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  1 | Ha Anh   |  32 | Da Nang   |  2000.00 |
|  2 | Van Ha   |  25 | Ha Noi    |  1500.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  4 | Thu Minh |  25 | Ha Noi    |  6500.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------+
```

Khối mã sau đây có chứa hàng loạt các hoạt động.

```sql
SQL> SAVEPOINT SP1;
Savepoint created.
SQL> DELETE FROM CUSTOMERS WHERE ID=1;
1 row deleted.
SQL> SAVEPOINT SP2;
Savepoint created.
SQL> DELETE FROM CUSTOMERS WHERE ID=2;
1 row deleted.
SQL> SAVEPOINT SP3;
Savepoint created.
SQL> DELETE FROM CUSTOMERS WHERE ID=3;
1 row deleted.
```

Bây giờ, ba lần xóa đã xảy ra, giả sử rằng bạn đã thay đổi quyết định và quyết định khôi phục lại SAVEPOINT mà bạn đã định nghĩa là SP2. Bởi vì SP2 được tạo ra sau khi xóa đầu tiên, hai lần xóa cuối cùng được khôi phục lại:

```sql
ROLLBACK TO SP2;
Rollback complete.
```

Lưu ý rằng chỉ có lần xoá đầu tiên xảy ra kể từ khi bạn khôi phục lại SP2.

```sql
SELECT * FROM CUSTOMERS;
+----+----------+-----+-----------+----------+
| ID | NAME     | AGE | ADDRESS   | SALARY   |
+----+----------+-----+-----------+----------+
|  2 | Van Ha   |  25 | Ha Noi    |  1500.00 |
|  3 | Vu Bang  |  23 | Vinh      |  2000.00 |
|  4 | Thu Minh |  25 | Ha Noi    |  6500.00 |
|  5 | Hai An   |  27 | Ha Noi    |  8500.00 |
|  6 | Hoang    |  22 | Ha Noi    |  4500.00 |
|  7 | Binh     |  24 | Ha Noi    | 10000.00 |
+----+----------+-----+-----------+----------+
6 rows selected.
```

Lệnh **SAVEPOINT RELEASE**

Lệnh SAVEPOINT RELEASE được sử dụng để loại bỏ một SAVEPOINT mà bạn đã tạo ra.

Cú pháp của lệnh SAVEPOINT RELEASE như sau.

```sql
RELEASE SAVEPOINT SAVEPOINT_NAME;
```

Khi SAVEPOINT bị xóa, bạn không thể sử dụng lệnh ROLLBACK để hoàn tác các transaction được thực hiện kể từ lần SAVEPOINT cuối cùng.

###### 1.3.4.1.5.4. Lệnh SET TRANSACTION

Lệnh SET TRANSACTION có thể được sử dụng để bắt đầu một transaction cơ sở dữ liệu. Lệnh này được sử dụng để chỉ định các đặc tính cho transaction sau. Ví dụ, bạn có thể chỉ định một transaction chỉ được đọc hoặc đọc viết.

Cú pháp cho lệnh SET TRANSACTION như sau.

```sql
SET TRANSACTION [ READ WRITE | READ ONLY ];
```

#### 1.3.4.2. Distributed transaction

[Distributed transaction](https://kipalog.com/posts/Mot-so-giai-phap-de-xu-ly-distributed-transaction-trong-he-thong-phan-tan)

Một điều ta cần lưu tâm nữa là giao dịch không phải chỉ là ở Database, cần phải hiểu giao dịch là từ khi bắt đầu tới khi kết thúc nghĩa nó phải bao gồm cả client và tất cả các node tham gia vào quá trình xử lý đó. Vì khi hệ thống lớn thì việc cập nhật sửa đổi dữ liệu nó nằm rải ra trên rất nhiều node từ client tới server.

**Ví dụ**: Khi update kho hàng, xác nhận dữ liệu đơn hàng. Hàng có thể đã không update thành công (database) nhưng đơn hàng thì vẫn cứ đổi trạng thái (ghi log ở client).

Vậy có các giải pháp xử lý nào. Có hai nhóm giai pháp để giải quyết vấn đề này:

- Giải pháp giải quyết triệt để, đảm bảo tất cả các tính chất của một transaction

- Giải pháp giải quyết không triệt để nhưng vẫn đảm bảo nghiệp vụ chạy đúng trong phần lớn các trường hợp.

##### 1.3.4.2.1. Two Phase Commit

Two phase commit là giải pháp duy nhất đảm bảo các tính chất ACID của distributed transaction. Như tên gọi, quá trình thực thi giao dịch sẽ chia làm 2 giai đoạn:

- Giai đoạn một, Request Commit Phase: giai đoạn này từ client sẽ gửi lệnh ghi tới các resources. Đồng thời ghi client sẽ ghi log Undo và Redo.

- Giai đoạn hai, Commit Phase: sau khi nhận được từ response ghi thành công từ tất cả các resources, thì từ client gửi lệnh Commit tới tất cả resources.

- Nếu có bất cứ request nào thực thi bị lỗi thì sẽ tiến hành gửi lệnh undo tới tất cả các resources.

Qua đây, ta thấy có 2 điểm chú ý:

- Các resources phải hỗ trợ cơ chế lock trong quá trình chờ lệnh commit từ client

- Client phải có khả năng phối hợp quá trình xử lý ở các resources khác nhau. Nó còn gọi là các cordinator. 

Với phương pháp này, tất cả các tính chất ACID của giao dịch được đảm bảo. Nhưng nó sẽ đòi hỏi các resources phải bị lock trong quá trình xử lý. Điều này sẽ có tác động tới quá trình thiết kế hệ thống khi bạn phải cân bằng giữa ba tính chất CAP của hệ phân tán.

##### 1.3.4.2.2. Các giải pháp đảm bảo Eventually Consistency

Nếu đã tìm hiểu về nguyên lý CAP, thì ta sẽ thấy là chỉ đạt được 2 trên 3 tính chất trên. Do đó khi đảm bảo khả năng Consistency thì 1 trong 2 tính chất Availability (khả năng hoạt động của hệ thống khi một trong các node bị ngừng hoạt động) và Partion Tolerance (khả năng hoạt động của hệ thống khi đường mạng giữa các node bị đứt) khó đảm bảo. Do vậy để có hệ thống hoạt động ổn định cao, và hiệu năng lớn thì người ta thường hi sinh tính chất consistency. Như vậy khi thiết kế để giải quyết distributed transaction thì sẽ phải thiết kế sao cho việc không đảm bảo consistency không ảnh hưởng tới tính chính xác của nghiệp vụ. Điều đó có nghĩa là **sẽ có khoảng thời gian trạng thái giữa các node trong hệ thống không nhất quán**, hay tính chất của hệ thống là eventually consistency.

###### 1.3.4.2.2.1. Phương pháp lưu log kết quả giao dịch theo transaction id

Đây là phương pháp cơ bản được sử dụng rộng rãi. Theo đó khi thực hiện một giao dịch, client sẽ gửi đi một transactionid kèm theo. Server sẽ lưu log giao dịch, kết quả thực thi theo transactionid đó. Nếu quá trình trả lại kết quả bị lỗi, client thực hiện lại giao dịch vời cùng transactionid, thì server sẽ trả lại kết quả tương ứng với transactionid đã lưu log đó. Khi cần rollback thì cũng dựa trên transactionid và log để thực hiện các xử lý tương ứng.

Nhưng với cách thiết kế này thì cần lưu tâm 2 điểm:

- Resources thực sự không bị lock, nên trong quá trình chờ kết quả trả về thì có thể resouces đã bị sửa đổi rồi. Do đó khi thiết kế cần lưu tâm, quản lý chặt chẽ các nghiệp vụ có giao dịch liên quan tới resouces tương ứng. Nếu tồn tại các giao dịch có độ tranh chấp cao, đòi hỏi tính chính xác lớn thì cách thiết kế này không đảm bảo. Trong trường hợp đó buộc phải cài đặt Two Phase Commit.

- Việc rollback không đơn giản, nó phụ thuộc vào tính chất nghiệp vụ. Vì nhiều khi trong quá trình client bắt đầu rollback thì thực sự dữ liệu đã bị thay đổi bởi nghiệp vụ khác rồi. Do đó việc rollback lại có thể làm sai hoàn toàn nghiệp vụ, rất khó để truy vết lại. Vì vậy cần hết sức cẩn thận khi thực hiện rollback. Ưu điểm lớn nhất của phương pháp này chính là nó đảm bảo tính chất AP của hệ thống.

###### 1.3.4.2.2.2. Sử dụng cặp queue Request và Response.

Phương pháp lưu log trên đảm bảo việc eventually consistency, nhưng nó chưa thật sự perfect lắm trong trường hợp xử lý các sự cố: đường mạng bị đứt, rồi client server lúc sống lúc chết. 

Ví dụ khi client gửi một request tới server xử lý, client gửi xong thì đường truyền bị đứt. Lúc này client nên làm gỉ? Gửi lại để nhận kết quả, hay gửi lệnh rollback cho server? Client không rõ là server có nhận được hay không, đã xử lý hay chưa xử lý, đã xử lý đúng hay sai?

Trong trường hợp đòi hỏi phải có tính chặt chẽ cao hơn thì có thể thiết kế hệ thống để giải quyết distributed transaction bằng 2 queue là:

- Queue Request: dùng để lưu các request gửi đi

- Queue Response: dùng để lưu các kết quả xử lý xong. Khi client cần thực hiện một request nào đó thì gửi một request vào queue request, Server sẽ nhận request từ queue request và xử lý, sau đó gửi kết quả vào queue response, Client sẽ lắng nghe queue response để nhận kết quả tương ứng. Bằng cách làm như vậy thì cả client và server không cần tồn tại tại cùng một thời điểm. Client gửi xong, client có thể chết, Server nhận xử lý xong và trả kết quả rồi chết... Kết quả quá trình xử lý vẫn được đảm bảo do lưu trữ trong queue. 

Ngoài các vấn đề của việc thiết kế eventually consistency thì có 2 điểm cần lưu ý khi thiết kế dạng này là:

- Do queue response có chứa rất nhiều kết quả của các giao dịch khác nhau được server trả về, nên client phải có cách lọc lấy chỉ response tương ứng với request gửi đi. Như RabbitMQ thì phải tạo queue tạm tương ứng với request gửi đi, khi server nhận được request sẽ nhận được tên queue mà mình sẽ trả lại kết quả. Với một số loại message queue khác Windows Service Bus thì nó có hỗ trợ fillter message theo sessionid. Khi đó chỉ cần filter response kết quả tương ứng với transactionid gửi đi là được.

- Do các message queue chứa các request và response nên nó phải có độ ổn định cao, bằng không nếu nó có vấn đề dẫn tới mất dữ liệu request và response thì sẽ rất nguy hiểm. Không thể biết là có giao dịch nào đã xử lý, giao dịch nào chưa, kết quả các giao dịch ra sao... Việc phụ hồi hệ thống trong trường hợp sự cố sẽ rất đau đầu. 

>Trên đây là một số giải pháp để giải quyết vấn đề distributed transaction. Không có giải pháp nào là tuyệt đối, cần phải hiểu bản chất của transaction, tính chất của các nghiệp vụ mà có sự lựa chọn cho phù hợp.

### 1.3.5. Isolation

**Bài toán**: Giả sử khi chúng ta đang tiến hành song song và đồng thời 2 transaction cùng cập nhật giá trị vào 1 bản ghi trong CSDL. Ở đây sẽ xảy ra **concurency** giữa các transaction và xảy ra các vấn đề :

- Transaction trước hay sau sẽ được tiến hành hay cả 2 cùng được tiến hành một lúc.

- Kết quả cuối cùng là kết quả của transaction nào trước hay sau? Ở đây xảy ra concurency giữa các transaction, chúng ta cùng tìm hiểu các mức level của Isolation để giải quyết vấn đề trên.

#### 1.3.5.1. Read Uncommitted

Một transaction lấy dữ liệu từ một transaction khác ngay cả khi transaction đó chưa được commit. Xét ví dụ cụ thể như sau:

Tạo bảng test:

```sql
CREATE DATABASE test;
```

Tạo mới bản ghi:

```sql
INSERT INTO `users` (`id`, `name`, `point`) VALUES ('1', 'BaLongStupid', '1');
```

Tiến hành tạo một transaction update point. Query 1:

```sql
START TRANSACTION;
    UPDATE `users` SET `point`= 100;
    SELECT SLEEP(30);
ROLLBACK;
```

Tiến hành Query 2:

```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
	SELECT * FROM `users`;
COMMIT;
```
Giả sử sau khi tiến hành câu Query 1 ta tiến hành chạy câu Query 2 thì kết quả trả về sẽ là 'point' = 100. Nhưng ngay sau khi câu Query 1 chạy xong và bị rollback thì kết quả trả về thực tế sẽ là là 'point' = 1. Như vậy transaction thứ 2 lấy kết quả chưa được commit của transaction thứ 1 => Hiện tượng trên gọi còn được gọi là Dirty Read. Ưu điểm ở đây là các transaction sẽ chạy liên tục và transaction sau ghi đè lên Transaction trước (**Dirty Write**). Đây là mức Isolation thấp nhất và nó cũng tương đương với câu lệnh:

```sql
SELECT * FROM users WITH (nolock)
```

#### 1.3.5.2. Read Committed

Đây là level default của một transaction nếu như chúng ta không config gì thêm. Tại level này thì Transaction sẽ không thể đọc dữ liệu từ từ một Transaction đang trong quá trình cập nhật hay sửa đổi mà phải đợi transacction đó hoàn tất. Như vậy thì chúng ta có thể tránh được Dirty Read và Dirty Write nhưng các Transaction sẽ phải chờ nhau => Perfoman hệ thống thấp. Ta thực hiện câu Query 1 như sau:

```sql
START TRANSACTION;
    UPDATE `users` SET `point`= 100 WHERE 'id' > 0;
    SELECT SLEEP(30);
COMMIT;
    SELECT * FROM `users` WHERE `id` = 2;
```

và ngay sau đó thực hiện câu Query 2:

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
    INSERT INTO `users` (`id`, `name`, `point`) VALUES ('2', 'DaoAnhDungStupid', '2');
COMMIT;
```

Khi ta tiến hành thực thi câu Query 2 thì kết quả trả về sẽ bản ghi 'id' = 2 sẽ có point = 2. Mặc dù câu query q1 đã update tất cả bản ghi có id > 0 và updated point = 100 nhưng bản ghi với id = 2 được cập nhật sau khi bảng users được cập nhật và trước khi transaction (q1) kết thúc => Bản ghi này được gọi là **Phantom Row** (Bản ghi ma).

#### 1.3.5.3. Repeatable read

Giống như mức độ của Read Committed, tại mức độ này thì transaction còn không thể đọc / ghi đè dữ liệu từ một transaction đang tiến hành cập nhật trên bản ghi đó. Query 1:

```sql
START TRANSACTION;
    SELECT SLEEP(30);
    SELECT * FROM `users` WHERE `id` = 2;
COMMIT;
```

Query 2:

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    SELECT * FROM `users` WHERE `id` = 2;
COMMIT;
```

Khi thực thi 2 câu query trên thì câu Query 2 phải đợi câu Query 1 commit hoàn tất mới có thể thực thi. Ở level này khi chúng ta sẽ được bảo vệ khi đọc dữ liệu select các bản ghi trong cùng một transaction. Giả sử ở câu Query 2 ta thay thế lệnh select thành lệnh **Update / Delete** thì dữ liệu tại 2 câu query sẽ khác nhau và chúng ta cũng không thể tránh được các **Phantom Row**.

#### 1.3.5.4. Serializable

Level cao nhất của Isolation, khi transaction tiến hành thực thi nó sẽ khóa các bản ghi liên quan và sẽ unlock cho tới khi rollback hoặc commit dữ liệu. Query 1:

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;
    SELECT * FROM `users`;
    SELECT SLEEP(30);
    SELECT * FROM `users`;
COMMIT;
```
Query 2:

```sql
INSERT INTO `users` (`id`, `name`, `point`) VALUES ('3', 'Dat09', '3');
```

Khi tiến hành 2 câu query trên thì bản ghi trả về giữa 2 lần select ở câu Query 1 là giống như nhau, và câu Query thứ 2 sẽ pending cho tới khi Query 1 kết thúc.

#### 1.3.5.5. SnapShot

Tương tự với level Serializable, nhưng cách thức hoạt động nó lại khác so với Serializable. Khi một transaction select các bản ghi thì nó sẽ không lock các bản ghi này lại, mà tạo một bản sao trên bản ghi hoặc các bản ghi đó. Khi ta tiến hành **UPDATE/DELETE** ta tiến hành trên bản sao dữ liệu đó và không gây ảnh hưởng tới dữ liệu ban đầu. Ưu điểm của snapshot là giảm độ trễ giữa các transaction nhưng bù lại cần tốn thêm tài nguyên lưu trữ các bản sao.

#### 1.3.5.6. Tóm tắt Isolation Level

| Transaction isolation level | Dirty reads | Nonrepeatable reads | Phantoms |
|:----------------------------|:-----------:|:-------------------:|:--------:|
| Read uncommitted            |      X      |          X          |    X     |
| Read committed              |      -      |          X          |    X     |
| Repeatable read             |      -      |          -          |    X     |
| Serializable                |      -      |          -          |    -     |

### 1.3.6. Connector

#### 1.3.6.1. JDBC Driver for MySQL (Connector/J)

[MySQL Connector/J Installation Instructions](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-installing.html)

#### 1.3.6.2. Python Driver for MySQL (Connector/Python)

[MySQL Connector/Python Installation Instructions](https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html)

`pip3 install mysql-connector-python`

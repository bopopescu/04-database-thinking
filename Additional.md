# 1. Optimistic Locking vs Pessimistic Locking

|Optimistic Locking|Pessimistic Locking|
|:---|:---|
|Locks are not used|Use exclusive and shared locks|
|Assume the majority of database operations do not conflict|Assume the conflicts most likely will happen|
|Conflicts are possible but are resolved before commit|Transactions wait for each other|
|Process each transaction in three phases: read, validation and write|Locl, process and unlock|
|High concurrency - scale well|Low concurrency - does not scale|
|Less restriction, may repeat process|More restriction, no repeat process|

**Locking steps:**

*Optimistic Locking*

- Read data
- Process transaction
- Issue update
- Look for conflict
- IF no conflict occured THEN commit transaction
- ELSE rollback and repeat transaction

*Pessimistic Locking*

- Lock required resources
- Read data
- Process transaction
- Issue commit
- Release locks

# 2. Design key for Redis Chat App

> Id = UUID

## 2.1. Save account and check online/offline

**User:UserId** (Hashes)
- username: string (Indexed)
- password: string
- email: string
- online: bool

## 2.2. Add friend and friend list

**Notification:UserId1:UserId2** (Hashes with Key=Composite Key)
- status: int (sended, isAccept, isCancel)
- datetime: string

> Check UserId1 request add friend UserId2

**FriendList:UserId** (Sets)
[friendId1, friendId2,...]

## 2.3. Group Chat

**Group:GroupId** (Hashes)
- title: string
- creatorId: string
- numberMember: int
- createdAt: datetime

**GroupMember:GroupId** (Sets)
[memberId1, memberId2,...]

## 2.4. Couple Chat

**Couple:UserId1:UserId2** (Hashes with Key=Composite Key)
- createdAt

> Check have couple chat [(userId1 and userId2) or (userId2 and userId1)]

## 2.5. Message of Chat History and Message Status (Seen)

**Message:ConversationId:SenderId:MessageId** (Hashes)
- content: string
- createdAt: string

**MessageStatus:ConversationId:ReceiverId** (Hashes)
- isSeen: bool

> Note: ConversationId = GroupId OR ConversationId = CompositeKey(UserId1:UserId2)


